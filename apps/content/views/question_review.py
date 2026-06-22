from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.db.models import Count, Prefetch, Q

from apps.content.views.permissions import is_admin
from apps.content.models import Resource, Question, Choice, ResourceQuizConfig
from apps.content.models.topic import Topic
from apps.content.models.exercise_item import ExerciseItem, ResourceExerciseItem
from apps.content.models.learning_guide import LearningGuide
from apps.content.services.evaluation_service import get_quiz_config

# Modos que se muestran como secciones plegables dentro de cada nivel.
# "ambas" (legacy) solo aparece si tiene preguntas.
MODE_GROUPS = [
    ("preparacion", "Práctica"),
    ("evaluacion", "Evaluación"),
    ("ambas", "Ambas"),
]

ITEM_LOW_ACCURACY = 30
ITEM_HIGH_ACCURACY = 95


def _visible_question_publication_error(question):
    """Return a validation message when a visible-bank question is not publishable."""
    if not question.text.strip() or not question.explanation.strip():
        return "Completa el enunciado y la explicación antes de publicar."
    if question.difficulty not in dict(Question.DIFFICULTY_CHOICES):
        return "Selecciona una dificultad válida antes de publicar."
    if not question.hint.strip():
        return "Completa la pista antes de publicar."
    choices = list(question.choices.all())
    if len(choices) != 4:
        return "Cada pregunta debe tener exactamente cuatro alternativas."
    correct = [choice for choice in choices if choice.is_correct]
    if len(correct) != 1:
        return "Cada pregunta debe tener exactamente una alternativa correcta."
    if len({choice.text.strip() for choice in choices}) != 4 or any(
        not choice.text.strip() for choice in choices
    ):
        return "Las alternativas deben ser únicas y no estar vacías."
    if question.canonical_answer != correct[0].text:
        return "La respuesta canónica no coincide con la alternativa correcta."
    return None


def _questions_with_analysis(resource=None, question_ids=None):
    """Carga preguntas + distribución de alternativas en dos consultas fijas."""
    choice_qs = Choice.objects.annotate(
        selection_count=Count("attempt_answers"),
    ).order_by("order", "id")
    questions = Question.objects.annotate(
        answer_count=Count("attempt_answers", distinct=True),
        correct_answer_count=Count(
            "attempt_answers",
            filter=Q(attempt_answers__is_correct=True),
            distinct=True,
        ),
    ).prefetch_related(Prefetch("choices", queryset=choice_qs))
    if resource is not None:
        questions = questions.filter(resource=resource)
    if question_ids is not None:
        questions = questions.filter(id__in=question_ids)
    questions = list(questions.order_by("level", "order", "id"))

    for question in questions:
        question.accuracy_percentage = (
            round(question.correct_answer_count / question.answer_count * 100)
            if question.answer_count
            else None
        )
        choices = list(question.choices.all())
        correct_picks = sum(
            choice.selection_count for choice in choices if choice.is_correct
        )
        max_distractor = max(
            (choice.selection_count for choice in choices if not choice.is_correct),
            default=0,
        )
        question.analysis_flags = []
        if question.answer_count:
            if question.accuracy_percentage < ITEM_LOW_ACCURACY:
                question.analysis_flags.append("Acierto muy bajo: revisar enunciado o clave.")
            elif question.accuracy_percentage >= ITEM_HIGH_ACCURACY:
                question.analysis_flags.append("Acierto muy alto: puede ser demasiado fácil.")
            if max_distractor > correct_picks:
                question.analysis_flags.append(
                    "Un distractor fue elegido más veces que la alternativa correcta."
                )
        for choice in choices:
            choice.selection_percentage = (
                round(choice.selection_count / question.answer_count * 100)
                if question.answer_count
                else 0
            )
            choice.is_dominant_distractor = bool(
                not choice.is_correct
                and choice.selection_count == max_distractor
                and max_distractor > correct_picks
            )
    return questions


def _question_with_analysis(question_id):
    return _questions_with_analysis(question_ids=[question_id])[0]


def _edit_choices_ctx(question):
    return {"LEVEL_CHOICES": Question.LEVEL_CHOICES,
            "MODE_CHOICES": Question.MODE_CHOICES,
            "STATUS_CHOICES": Question.STATUS_CHOICES}


def _build_levels_data(resource):
    """Agrupa las preguntas del recurso en Nivel → Modo → preguntas (con choices)."""
    all_questions = _questions_with_analysis(resource=resource)
    levels_data = []
    for lvl, lvl_name in Question.LEVEL_CHOICES:
        lvl_questions = [q for q in all_questions if q.level == lvl]
        modes = []
        for mkey, mlabel in MODE_GROUPS:
            mqs = [q for q in lvl_questions if q.mode == mkey]
            if mkey == "ambas" and not mqs:
                continue
            modes.append({"key": mkey, "label": mlabel, "questions": mqs, "count": len(mqs)})
        levels_data.append(
            {"num": lvl, "name": lvl_name, "count": len(lvl_questions), "modes": modes}
        )
    return levels_data


@user_passes_test(is_admin)
def question_review(request, slug):
    """Vista principal: acordeón Nivel → Modo → preguntas → alternativas."""
    resource = get_object_or_404(Resource, slug=slug)

    scope = request.GET.get("scope", "")
    if scope == "banco_visible":
        exercise_item_id = request.GET.get("exercise_item_id")
        if not exercise_item_id:
            return HttpResponse("Falta el ítem de aprendizaje", status=400)

        topic = resource.topic
        if not topic.structured_bank_enabled or not topic.is_active:
            return HttpResponse("Tema no habilitado", status=400)

        exercise_item = get_object_or_404(ExerciseItem, id=exercise_item_id)
        if exercise_item.topic != topic or exercise_item.status != "aprobado":
            return HttpResponse("Ítem inválido o no aprobado", status=400)

        try:
            ResourceExerciseItem.objects.get(exercise_item=exercise_item, resource=resource)
        except ResourceExerciseItem.DoesNotExist:
            return HttpResponse("Vínculo no existe para este recurso e ítem", status=400)

        guide = get_object_or_404(LearningGuide, topic=topic, status="publicada", visibility="publica")

        # Cargar las preguntas del banco visible
        questions = Question.objects.filter(
            resource=resource,
            exercise_item=exercise_item,
            scope="banco_visible",
            learning_guide=guide
        ).prefetch_related("choices").order_by("difficulty", "order", "id")

        context = {
            "resource": resource,
            "exercise_item": exercise_item,
            "learning_guide": guide,
            "scope": scope,
            "questions": questions,
            "LEVEL_CHOICES": Question.LEVEL_CHOICES,
            "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
            "STATUS_CHOICES": Question.STATUS_CHOICES,
        }
        return render(request, "pages/question_review.html", context)

    config = get_quiz_config(resource)
    config_db = getattr(resource, "quiz_config", None)

    topic_edu_level = resource.get_education_level()
    context = {
        "resource": resource,
        "config": config,
        "config_db": config_db,
        "levels_data": _build_levels_data(resource),
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "RECOVERY_CHOICES": ResourceQuizConfig.RECOVERY_CHOICES,
        "EDUCATION_LEVEL_CHOICES": Topic.EDUCATION_LEVEL_CHOICES,
        "topic_edu_level": topic_edu_level,
        "topic_edu_label": dict(Topic.EDUCATION_LEVEL_CHOICES).get(topic_edu_level, ""),
    }
    return render(request, "pages/question_review.html", context)


@user_passes_test(is_admin)
@require_POST
def save_resource_quiz_config(request, resource_id):
    """Guarda la configuración de quiz de un recurso."""
    resource = get_object_or_404(Resource, id=resource_id)
    config, created = ResourceQuizConfig.objects.get_or_create(resource=resource)

    try:
        # El "pool" (meta del banco) ya no se edita desde el formulario: se conserva
        # el valor existente del recurso (o el default). Desde la UI solo se ajusta
        # la "muestra" (cuántas preguntas ve el alumno) y los parámetros de evaluación.
        existing_counts = config.counts or {}
        default_pool = {"practice": 15, "eval": 10}
        counts = {}
        for lvl in ["1", "2", "3"]:
            lvl_existing = existing_counts.get(lvl, {})
            counts[lvl] = {
                "practice": {
                    "pool": int(
                        lvl_existing.get("practice", {}).get("pool", default_pool["practice"])
                    ),
                    "shown": int(request.POST.get(f"practice_shown_{lvl}", 5)),
                },
                "eval": {
                    "pool": int(
                        lvl_existing.get("eval", {}).get("pool", default_pool["eval"])
                    ),
                    "shown": int(request.POST.get(f"eval_shown_{lvl}", 3)),
                },
            }

        config.counts = counts
        config.max_attempts = int(request.POST.get("max_attempts", 3))
        # El umbral se ingresa de 0 a 100; tolerante a coma decimal.
        threshold_pct = float(str(request.POST.get("pass_threshold", "100")).replace(",", "."))
        config.pass_threshold = threshold_pct / 100.0
        config.recovery_rule = request.POST.get("recovery_rule", "practice_5_5")
        config.allow_retake_passed = request.POST.get("allow_retake_passed") in ["true", "on", "checked"]
        config.autopublish = request.POST.get("autopublish") in ["true", "on", "checked"]

        config.clean()
        config.save()

        if request.headers.get("HX-Request"):
            response = HttpResponse(
                '<div class="alert alert--success" role="alert" id="config-alert">'
                "Configuración guardada correctamente."
                '<button type="button" class="alert-close" aria-label="Cerrar">&times;</button>'
                "</div>"
            )
            response["HX-Trigger"] = "configUpdated"
            return response

        return redirect("content:question_review", slug=resource.slug)

    except Exception as e:
        error_msg = str(e)
        if request.headers.get("HX-Request"):
            return HttpResponse(
                f'<div class="alert alert--danger" role="alert" id="config-alert">'
                f"Error al guardar la configuración: {error_msg}"
                '<button type="button" class="alert-close" aria-label="Cerrar">&times;</button>'
                "</div>",
                status=400,
            )
        return HttpResponse(f"Error: {error_msg}", status=400)


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_question_inline(request, question_id):
    """GET: formulario de edición (o lectura si cancel). POST: guarda y devuelve el ítem."""
    question = get_object_or_404(Question, id=question_id)

    if request.method == "POST":
        question.text = request.POST.get("text", "").strip()
        question.explanation = request.POST.get("explanation", "").strip()
        try:
            question.level = int(request.POST.get("level", 1))
            question.order = int(request.POST.get("order", 0))
        except ValueError:
            pass
        if question.scope == "banco_visible":
            difficulty = request.POST.get("difficulty", "").strip()
            if difficulty not in dict(Question.DIFFICULTY_CHOICES):
                return HttpResponse("Dificultad inválida.", status=400)
            question.level = question.exercise_item.level
            question.mode = "preparacion"
            question.status = "borrador"
            question.difficulty = difficulty
            question.hint = request.POST.get("hint", "").strip()
        else:
            question.mode = request.POST.get("mode", "ambas")
            question.status = request.POST.get("status", "borrador")
        question.save()

        if request.headers.get("HX-Request"):
            # Devuelve el <details> completo (abierto) para refrescar resumen + cuerpo.
            question = _question_with_analysis(question.id)
            return render(request, "partials/question_item.html", {"question": question, "open": True})
        return redirect("content:question_review", slug=question.resource.slug)

    # GET
    if request.GET.get("cancel"):
        question = _question_with_analysis(question.id)
        return render(request, "partials/question_detail.html", {"question": question})
    return render(request, "partials/question_edit_form.html", {"question": question, **_edit_choices_ctx(question)})


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_choice_inline(request, choice_id):
    """GET: form de edición (o lectura si cancel). POST: guarda y devuelve la alternativa."""
    choice = get_object_or_404(Choice, id=choice_id)
    question = choice.question

    if request.method == "POST":
        choice.text = request.POST.get("text", "").strip()
        is_correct = request.POST.get("is_correct") in ["true", "on", "checked"]

        with transaction.atomic():
            if is_correct:
                question.choices.all().update(is_correct=False)
            choice.is_correct = is_correct
            choice.save()
            if question.scope == "banco_visible":
                correct_choice = question.choices.filter(is_correct=True).first()
                question.canonical_answer = correct_choice.text if correct_choice else ""
                question.status = "borrador"
                question.save(update_fields=["canonical_answer", "status", "updated_at"])

        correct_count = question.choices.filter(is_correct=True).count()
        warning = None
        if correct_count == 0:
            warning = "Sin alternativa correcta."
        elif correct_count > 1:
            warning = f"{correct_count} alternativas marcadas como correctas."

        if request.headers.get("HX-Request"):
            return render(request, "partials/choice_item.html", {"choice": choice, "warning": warning})
        return redirect("content:question_review", slug=question.resource.slug)

    # GET
    if request.GET.get("cancel"):
        return render(request, "partials/choice_item.html", {"choice": choice})
    return render(request, "partials/choice_edit_form.html", {"choice": choice})


@user_passes_test(is_admin)
@require_POST
def add_question_inline(request, resource_id):
    """Crea una pregunta en el nivel/modo indicados y devuelve el ítem (abierto)."""
    resource = get_object_or_404(Resource, id=resource_id)
    try:
        level = int(request.POST.get("level", 1))
    except (ValueError, TypeError):
        level = 1
    mode = request.POST.get("mode", "ambas")
    if mode not in dict(Question.MODE_CHOICES):
        mode = "ambas"

    last_order = Question.objects.filter(resource=resource, level=level).count()
    question = Question.objects.create(
        resource=resource,
        level=level,
        mode=mode,
        text="Nueva pregunta (editar aquí)",
        explanation="",
        status="borrador",
        order=last_order + 1,
    )
    Choice.objects.create(question=question, text="Alternativa A (correcta)", is_correct=True, order=1)
    Choice.objects.create(question=question, text="Alternativa B", is_correct=False, order=2)
    Choice.objects.create(question=question, text="Alternativa C", is_correct=False, order=3)
    Choice.objects.create(question=question, text="Alternativa D", is_correct=False, order=4)

    if request.headers.get("HX-Request"):
        question = _question_with_analysis(question.id)
        return render(request, "partials/question_item.html", {"question": question, "open": True})
    return redirect("content:question_review", slug=resource.slug)


@user_passes_test(is_admin)
@require_POST
def add_choice_inline(request, question_id):
    """Crea una alternativa y devuelve su formulario de edición (para completarla)."""
    question = get_object_or_404(Question, id=question_id)
    if question.scope == "banco_visible":
        question.status = "archivada"
        question.save(update_fields=["status", "updated_at"])
        return HttpResponse("")
    last_order = question.choices.count()
    choice = Choice.objects.create(
        question=question, text="Nueva alternativa", is_correct=False, order=last_order + 1
    )
    if question.scope == "banco_visible" and question.status != "borrador":
        question.status = "borrador"
        question.save(update_fields=["status", "updated_at"])
    if request.headers.get("HX-Request"):
        return render(request, "partials/choice_edit_form.html", {"choice": choice})
    return redirect("content:question_review", slug=question.resource.slug)


@user_passes_test(is_admin)
@require_POST
def delete_question(request, question_id):
    """Elimina la pregunta. Retorna vacío para que HTMX remueva el ítem."""
    question = get_object_or_404(Question, id=question_id)
    if question.scope == "banco_visible":
        question.status = "archivada"
        question.save(update_fields=["status", "updated_at"])
        return HttpResponse("")
    if question.attempt_answers.exists() or question.error_reports.exists():
        question.status = "archivada"
        question.save(update_fields=["status", "updated_at"])
        return HttpResponse(
            "La pregunta tiene historial de alumnos y fue archivada, no eliminada.",
            status=409,
        )
    question.delete()
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def delete_choice(request, choice_id):
    """Elimina la alternativa. Retorna vacío para que HTMX la remueva."""
    choice = get_object_or_404(Choice, id=choice_id)
    if choice.attempt_answers.exists():
        return HttpResponse(
            "La alternativa tiene respuestas históricas y no puede eliminarse.",
            status=409,
        )
    question = choice.question
    choice.delete()
    if question.scope == "banco_visible":
        correct_choice = question.choices.filter(is_correct=True).first()
        question.canonical_answer = correct_choice.text if correct_choice else ""
        question.status = "borrador"
        question.save(
            update_fields=["canonical_answer", "status", "updated_at"]
        )
    return HttpResponse("")


@user_passes_test(is_admin)
@require_POST
def bulk_action_questions(request, resource_id):
    """Acción en lote sobre preguntas seleccionadas. Devuelve HTML HTMX o redirige."""
    resource = get_object_or_404(Resource, id=resource_id)
    action = request.POST.get("action")
    question_ids = request.POST.getlist("selected_questions")
    level = request.POST.get("level")
    mode_key = request.POST.get("mode")
    scope = request.POST.get("scope", "")

    if scope == "banco_visible":
        exercise_item_id = request.POST.get("exercise_item_id")
        learning_guide_id = request.POST.get("learning_guide_id")
        if not exercise_item_id or not learning_guide_id:
            return HttpResponse("Faltan parámetros de banco visible", status=400)

        # Validar permisos y existencia
        topic = resource.topic
        if not topic.structured_bank_enabled or not topic.is_active:
            return HttpResponse("Tema no habilitado", status=400)

        exercise_item = get_object_or_404(ExerciseItem, id=exercise_item_id)
        if exercise_item.topic != topic or exercise_item.status != "aprobado":
            return HttpResponse("Ítem inválido o no aprobado", status=400)

        try:
            ResourceExerciseItem.objects.get(exercise_item=exercise_item, resource=resource)
        except ResourceExerciseItem.DoesNotExist:
            return HttpResponse("Vínculo no existe para este recurso e ítem", status=400)

        guide = get_object_or_404(LearningGuide, id=learning_guide_id, topic=topic, status="publicada", visibility="publica")

        # Validar que todos los IDs pertenecen a este recurso, guía, ítem y scope esperado antes de mutar
        if question_ids:
            actual_count = Question.objects.filter(
                id__in=question_ids,
                resource=resource,
                exercise_item=exercise_item,
                learning_guide=guide,
                scope="banco_visible"
            ).count()
            if actual_count != len(question_ids):
                return HttpResponse("Uno o más IDs de pregunta no pertenecen al recurso, guía, ítem o scope esperados.", status=400)

            qs_target = Question.objects.filter(
                id__in=question_ids,
                resource=resource,
                exercise_item=exercise_item,
                learning_guide=guide,
                scope="banco_visible",
            ).prefetch_related("choices")
            if action == "publicar":
                for question in qs_target:
                    error = _visible_question_publication_error(question)
                    if error:
                        return HttpResponse(
                            f"Pregunta {question.id}: {error}",
                            status=400,
                        )
                Question.objects.filter(
                    id__in=[question.id for question in qs_target]
                ).update(status="publicada")
            elif action == "borrador":
                qs_target.update(status="borrador")
            elif action == "archivar":
                qs_target.update(status="archivada")
            elif action == "eliminar":
                qs_target.update(status="archivada")
            else:
                return HttpResponse("Acción inválida.", status=400)

        # Retornar la lista actualizada de preguntas para este ítem
        if request.headers.get("HX-Request"):
            questions = Question.objects.filter(
                resource=resource,
                exercise_item=exercise_item,
                scope="banco_visible",
                learning_guide=guide
            ).prefetch_related("choices").order_by("difficulty", "order", "id")
            parts = [
                render_to_string("partials/question_item.html", {"question": q}, request=request)
                for q in questions
            ]
            if not parts:
                parts = ['<p class="acc-empty">Sin preguntas en esta sección todavía.</p>']
            return HttpResponse("".join(parts))

        return redirect(f"{reverse('content:question_review', args=[resource.slug])}?scope=banco_visible&exercise_item_id={exercise_item.id}")

    if question_ids:
        qs_target = Question.objects.filter(resource=resource, id__in=question_ids)
        if action == "publicar":
            qs_target.update(status="publicada")
        elif action == "borrador":
            qs_target.update(status="borrador")
        elif action == "archivar":
            qs_target.update(status="archivada")
        elif action == "eliminar":
            protected = qs_target.filter(
                Q(attempt_answers__isnull=False) | Q(error_reports__isnull=False)
            ).distinct()
            protected.update(status="archivada")
            qs_target.exclude(id__in=protected.values("id")).delete()

    if request.headers.get("HX-Request") and level and mode_key:
        qs = [
            question
            for question in _questions_with_analysis(resource=resource)
            if question.level == int(level) and question.mode == mode_key
        ]
        parts = [
            render_to_string("partials/question_item.html", {"question": q}, request=request)
            for q in qs
        ]
        if not parts:
            parts = ['<p class="acc-empty">Sin preguntas en esta sección todavía.</p>']
        return HttpResponse("".join(parts))

    return redirect("content:question_review", slug=resource.slug)


@user_passes_test(is_admin)
@require_POST
def generate_questions_inline(request, resource_id):
    """Genera una tanda de preguntas para una sección (nivel + modo) del recurso.

    `source`:
      - "video": usa el transcript guardado (lo que se explica en el video).
      - "document": copia el formato de una guía vinculada, SIN usar el video.

    Devuelve los <details> de las preguntas nuevas para que HTMX las anexe.
    """
    from django.utils.html import escape

    from apps.content.services.ai_generation_service import generate_questions_for_resource
    from apps.content.services.guide_service import build_reference_block

    resource = get_object_or_404(Resource, id=resource_id)
    try:
        level = int(request.POST.get("level", 1))
    except (ValueError, TypeError):
        level = 1
    mode = request.POST.get("mode", "preparacion")
    if mode not in dict(Question.MODE_CHOICES):
        mode = "preparacion"
    source = request.POST.get("source", "video")
    custom_instructions = (request.POST.get("description", "") or "").strip() or None
    try:
        count = int(request.POST.get("count", 5))
    except (ValueError, TypeError):
        count = 5
    count = max(1, min(count, 5))  # tope para no chocar el timeout de gunicorn

    def _msg(text):
        return HttpResponse(f'<p class="acc-empty">{text}</p>')

    # Modo documento: necesita una guía vinculada de donde copiar el formato.
    if source == "document" and not build_reference_block(resource):
        return _msg(
            "No hay guía vinculada a este recurso, tema o asignatura. "
            "Cargá una en la página de Guías y vinculala."
        )

    config = getattr(resource, "quiz_config", None)
    status = "publicada" if (config and config.autopublish) else "borrador"
    edu_level = resource.get_education_level() or "media"

    try:
        created = generate_questions_for_resource(
            resource=resource,
            level=level,
            mode=mode,
            count=count,
            status=status,
            education_level=edu_level,
            custom_instructions=custom_instructions,
            use_transcript=(source == "video"),
            use_guides=True,
        )
    except Exception as exc:  # noqa: BLE001 - se reporta al usuario, no se cae
        return _msg(f"Error al generar: {escape(str(exc))}")

    if not created:
        if source == "video":
            return _msg("No se generaron preguntas. ¿El recurso tiene transcript guardado?")
        return _msg("No se generaron preguntas.")

    created_questions = _questions_with_analysis(
        question_ids=[question.id for question in created]
    )
    html = "".join(
        render_to_string("partials/question_item.html", {"question": q}, request=request)
        for q in created_questions
    )
    return HttpResponse(html)
