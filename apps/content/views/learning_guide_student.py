import random
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.content.models import ExerciseItem, Question, Resource, ResourceExerciseItem, Topic
from apps.content.models.learning_guide import LearningGuide
from apps.content.services.answer_grading_service import grade_answer
from apps.content.services.visible_bank_service import select_visible_practice_questions

VISIBLE_BANK_INITIAL_LIMIT = 200

@login_required
def learning_guide_detail(request, slug):
    """Muestra el detalle público de la guía para los alumnos."""
    guide = get_object_or_404(
        LearningGuide.objects.select_related("topic", "topic__subject"),
        slug=slug,
        status="publicada",
        visibility="publica",
        topic__is_active=True,
        topic__structured_bank_enabled=True,
    )

    topic = guide.topic

    # Query única base para el banco visible (no N+1)
    question_queryset = (
        Question.objects.filter(
            status="publicada",
            scope="banco_visible",
            resource__is_published=True,
            resource__topic=topic,
            exercise_item__topic=topic,
            exercise_item__status="aprobado",
            learning_guide=guide,
            learning_guide__status="publicada",
            learning_guide__visibility="publica",
        )
        .select_related("resource", "exercise_item", "learning_guide")
        .prefetch_related("choices")
        .order_by("exercise_item__order", "difficulty", "order", "id")
    )
    questions = list(question_queryset[: VISIBLE_BANK_INITIAL_LIMIT + 1])
    bank_truncated = len(questions) > VISIBLE_BANK_INITIAL_LIMIT
    questions = questions[:VISIBLE_BANK_INITIAL_LIMIT]

    # Agrupar en memoria por ítem y separar en normales y desafíos
    grouped_by_item = defaultdict(lambda: {"item": None, "normal": [], "desafio": []})
    for q in questions:
        item_id = q.exercise_item_id
        if not grouped_by_item[item_id]["item"]:
            grouped_by_item[item_id]["item"] = q.exercise_item
        if q.difficulty == "desafio":
            grouped_by_item[item_id]["desafio"].append(q)
        else:
            grouped_by_item[item_id]["normal"].append(q)

    # Ordenar por el orden curricular del ítem
    sorted_items = sorted(
        grouped_by_item.values(),
        key=lambda x: (x["item"].order, x["item"].id)
    )

    context = {
        "guide": guide,
        "topic": topic,
        "sorted_items": sorted_items,
        "total_questions": len(questions),
        "bank_truncated": bank_truncated,
    }
    return render(request, "pages/learning_guide_detail.html", context)


@login_required
@require_POST
def start_visible_practice(request, topic_id):
    """Inicia una práctica no académica, seleccionando las preguntas y guardando el estado en sesión."""
    topic = get_object_or_404(
        Topic,
        id=topic_id,
        is_active=True,
        structured_bank_enabled=True
    )

    item_id = request.POST.get("item_id")
    resource_id = request.POST.get("resource_id")

    try:
        count = int(request.POST.get("count", 10))
    except (ValueError, TypeError):
        count = 10

    # Validaciones defensivas de tema/recurso cruzados si se proveen
    if item_id:
        try:
            item_id = int(item_id)
            exercise_item = get_object_or_404(ExerciseItem, id=item_id, topic=topic, status="aprobado")
        except (ValueError, TypeError):
            return HttpResponse("Filtro de ítem no válido", status=400)
    else:
        exercise_item = None

    if resource_id:
        try:
            resource_id = int(resource_id)
            resource = get_object_or_404(Resource, id=resource_id, topic=topic, is_published=True)
        except (ValueError, TypeError):
            return HttpResponse("Filtro de recurso no válido", status=400)
    else:
        resource = None

    if exercise_item and resource and not ResourceExerciseItem.objects.filter(
        exercise_item=exercise_item,
        resource=resource,
    ).exists():
        return HttpResponse("El recurso no está vinculado al ítem solicitado.", status=400)

    # Seleccionar preguntas del banco visible
    questions = select_visible_practice_questions(
        topic=topic,
        item_id=item_id,
        resource_id=resource_id,
        count=count,
        seed=random.randint(1, 100000)
    )

    if not questions:
        return render(request, "partials/_practice_quiz_player.html", {"empty": True, "topic": topic})

    # Guardar en sesión reemplazando cualquier práctica previa del mismo tema
    session_key = f"visible_practice_{request.user.id}_{topic.id}"
    question_ids = [q.id for q in questions]

    request.session[session_key] = {
        "question_ids": question_ids,
        "filters": {
            "item_id": item_id,
            "resource_id": resource_id,
            "count": count,
        },
        "order": question_ids,
    }
    request.session.modified = True

    context = {
        "topic": topic,
        "questions": questions,
        "exercise_item": exercise_item,
        "resource_filter": resource,
        "total_questions": len(questions),
    }
    return render(request, "partials/_practice_quiz_player.html", context)


@login_required
@require_POST
def submit_visible_practice(request, topic_id):
    """Califica al vuelo una práctica no académica sin afectar el progreso ni registrar intentos académicos."""
    topic = get_object_or_404(
        Topic,
        id=topic_id,
        is_active=True,
        structured_bank_enabled=True
    )

    session_key = f"visible_practice_{request.user.id}_{topic.id}"
    session_data = request.session.get(session_key)

    if not session_data:
        return HttpResponse("No tienes una sesión de práctica activa para este tema.", status=400)

    question_ids = session_data.get("question_ids", [])
    if not question_ids:
        return HttpResponse("La sesión de práctica está vacía.", status=400)

    # 1. Validar llaves ajenas y parámetros duplicados antes de corregir.
    raw_answers = {}
    for key, values in request.POST.lists():
        if key.startswith("question_"):
            if len(values) != 1:
                return HttpResponse("Respuesta duplicada o manipulada.", status=400)
            try:
                q_id = int(key.removeprefix("question_"))
            except ValueError:
                return HttpResponse("Estructura de envío manipulada.", status=400)
            if q_id not in question_ids:
                return HttpResponse("La pregunta no pertenece a esta práctica.", status=400)
            if q_id in raw_answers:
                return HttpResponse("Respuesta duplicada o manipulada.", status=400)
            raw_answers[q_id] = values[0]

    # 2. Cargar preguntas respetando el orden original guardado en sesión
    questions_map = {
        q.id: q
        for q in Question.objects.filter(
            id__in=question_ids,
            status="publicada",
            scope="banco_visible",
            resource__topic=topic,
            resource__is_published=True,
            exercise_item__topic=topic,
            exercise_item__status="aprobado",
            learning_guide__topic=topic,
            learning_guide__status="publicada",
            learning_guide__visibility="publica",
        )
        .prefetch_related("choices")
        .select_related("exercise_item")
    }
    if len(questions_map) != len(set(question_ids)):
        return HttpResponse(
            "La práctica cambió desde que fue iniciada. Iníciala nuevamente.",
            status=400,
        )

    results = []
    score = 0
    recommendations = {}  # Recomendaciones efímeras por ítem de menor rendimiento

    for q_id in question_ids:
        q = questions_map.get(q_id)
        if not q:
            continue

        selected_choice = None
        correct_choice = None
        text_answer = ""
        normalized_answer = ""
        raw_answer = raw_answers.get(q_id, "")

        if q.question_type == "alternativa":
            choices = list(q.choices.all())
            correct_choice = next(
                (choice for choice in choices if choice.is_correct),
                None,
            )
            if raw_answer:
                try:
                    selected_choice_id = int(raw_answer)
                except (TypeError, ValueError):
                    return HttpResponse(
                        "Estructura de alternativas manipulada.",
                        status=400,
                    )
                selected_choice = next(
                    (
                        choice
                        for choice in choices
                        if choice.id == selected_choice_id
                    ),
                    None,
                )
                if selected_choice is None:
                    return HttpResponse(
                        "La alternativa seleccionada no corresponde a la pregunta.",
                        status=400,
                    )
            is_correct = bool(selected_choice and selected_choice.is_correct)
            grading_reason = (
                "correct"
                if is_correct
                else ("incorrect" if selected_choice else "empty")
            )
        elif q.question_type in {"numerica", "algebraica"}:
            text_answer = raw_answer
            grading = grade_answer(q, raw_answer)
            is_correct = grading["correct"]
            grading_reason = grading["reason"]
            normalized_answer = grading["normalized"]
        else:
            return HttpResponse(
                "La práctica contiene un tipo de pregunta no soportado.",
                status=400,
            )

        if is_correct:
            score += 1
        else:
            # Registrar recomendación de estudio para este ítem
            item = q.exercise_item
            if item:
                recommendations[item.id] = {
                    "title": item.title,
                    "objective": item.objective,
                }

        results.append(
            {
                "question": q,
                "selected_choice": selected_choice,
                "correct_choice": correct_choice,
                "text_answer": text_answer,
                "normalized_answer": normalized_answer,
                "grading_reason": grading_reason,
                "is_correct": is_correct,
            }
        )

    total = len(question_ids)
    percentage = round((score / total) * 100) if total > 0 else 0

    # 3. Limpiar sesión al finalizar exitosamente
    if session_key in request.session:
        del request.session[session_key]
        request.session.modified = True

    context = {
        "topic": topic,
        "results": results,
        "score": score,
        "total": total,
        "percentage": percentage,
        "recommendations": list(recommendations.values()),
    }
    return render(request, "partials/_practice_quiz_player.html", context)
