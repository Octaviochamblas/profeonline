"""Vistas HTMX para el sistema de evaluación gamificada."""

import json

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from apps.content.models import Question, QuestionErrorReport, Resource, Topic
from apps.content.services.evaluation_service import (
    QUESTIONS_PER_LEVEL,
    get_attempts_info,
    get_questions_for_quiz,
    get_resource_mastery,
    get_topic_exam_info,
    get_topic_exam_questions,
    recover_attempt,
    submit_quiz,
    submit_topic_exam,
)

QUIZ_LEVELS = [
    (1, "Definición"),
    (2, "Ejercicios simples"),
    (3, "Problemas de aplicación"),
]


def _quiz_section_context(user, resource):
    """Contexto compartido para refrescar la sección de quiz por HTMX."""
    has_questions = {}
    for lvl in (1, 2, 3):
        has_questions[lvl] = Question.objects.filter(
            resource=resource,
            level=lvl,
            status="publicada",
        ).exists()
    return {
        "resource": resource,
        "mastery": get_resource_mastery(user, resource),
        "has_questions": has_questions,
        "quiz_available": any(has_questions.values()),
        "levels": QUIZ_LEVELS,
    }


@login_required
def quiz_start(request, slug, level, mode):
    """GET — Renderiza el formulario de quiz con preguntas aleatorias."""
    resource = get_object_or_404(Resource, slug=slug, is_published=True)
    level = int(level)

    if level not in (1, 2, 3) or mode not in ("preparacion", "evaluacion"):
        return HttpResponseBadRequest("Nivel o modo inválido.")

    # Verificar bloqueo para evaluación
    if mode == "evaluacion":
        info = get_attempts_info(request.user, resource, level)
        if info["passed"]:
            return TemplateResponse(
                request,
                "includes/quiz_section.html",
                _quiz_section_context(request.user, resource),
            )
        if info["max_reached"] and not info["can_recover"]:
            return TemplateResponse(
                request,
                "includes/quiz_blocked.html",
                {"resource": resource, "level": level, "info": info},
            )

    questions = get_questions_for_quiz(resource, level, mode)
    if not questions:
        return TemplateResponse(
            request,
            "includes/quiz_empty.html",
            {"resource": resource, "level": level, "mode": mode},
        )

    # Guardar IDs en session para validar en submit
    session_key = f"quiz_{resource.pk}_{level}_{mode}"
    request.session[session_key] = [q.pk for q in questions]

    total = QUESTIONS_PER_LEVEL.get(level, 5)
    level_labels = {1: "Definición", 2: "Ejercicios simples", 3: "Problemas de aplicación"}

    return TemplateResponse(
        request,
        "includes/quiz_form.html",
        {
            "resource": resource,
            "questions": questions,
            "level": level,
            "level_label": level_labels.get(level, ""),
            "mode": mode,
            "total": total,
        },
    )


@login_required
@require_POST
def quiz_submit(request, slug, level, mode):
    """POST (HTMX) — Valida respuestas y retorna resultados con feedback."""
    resource = get_object_or_404(Resource, slug=slug, is_published=True)
    level = int(level)

    if level not in (1, 2, 3) or mode not in ("preparacion", "evaluacion"):
        return HttpResponseBadRequest("Nivel o modo inválido.")

    # Recuperar preguntas de la session
    session_key = f"quiz_{resource.pk}_{level}_{mode}"
    question_ids = request.session.get(session_key, [])

    if not question_ids:
        return HttpResponseBadRequest("No hay quiz activo para enviar.")

    # Construir dict de respuestas {question_id: choice_id}
    answers_dict = {}
    for q_id in question_ids:
        choice_id = request.POST.get(f"question_{q_id}")
        if choice_id:
            answers_dict[int(q_id)] = int(choice_id)
        else:
            answers_dict[int(q_id)] = None

    try:
        attempt = submit_quiz(request.user, resource, level, mode, answers_dict)
    except ValueError as e:
        return TemplateResponse(
            request,
            "includes/quiz_error.html",
            {"resource": resource, "error": str(e)},
        )

    # Limpiar session
    request.session.pop(session_key, None)

    # Cargar las respuestas con preguntas y choices para feedback.
    # Se conserva el mismo orden (aleatorio) en que se presentaron las preguntas
    # en el reproductor; `question_ids` viene de la sesión.
    answers = list(
        attempt.answers.select_related("question", "selected_choice")
    )
    order_index = {q_id: pos for pos, q_id in enumerate(question_ids)}
    answers.sort(key=lambda a: order_index.get(a.question_id, len(order_index)))

    # Para cada respuesta, incluir la choice correcta
    results = []
    for answer in answers:
        correct_choice = answer.question.choices.filter(is_correct=True).first()
        results.append({
            "question": answer.question,
            "selected": answer.selected_choice,
            "correct_choice": correct_choice,
            "is_correct": answer.is_correct,
            "explanation": answer.question.explanation,
        })

    mastery = get_resource_mastery(request.user, resource)
    info = get_attempts_info(request.user, resource, level)

    level_labels = {1: "Definición", 2: "Ejercicios simples", 3: "Problemas de aplicación"}

    return TemplateResponse(
        request,
        "includes/quiz_results.html",
        {
            "resource": resource,
            "attempt": attempt,
            "results": results,
            "level": level,
            "level_label": level_labels.get(level, ""),
            "mode": mode,
            "mastery": mastery,
            "info": info,
        },
    )


@login_required
def quiz_status(request, slug):
    """GET (HTMX) — Retorna el panel de estado de niveles 1/2/3."""
    resource = get_object_or_404(Resource, slug=slug, is_published=True)
    mastery = get_resource_mastery(request.user, resource)

    return TemplateResponse(
        request,
        "includes/quiz_section.html",
        _quiz_section_context(request.user, resource) | {"mastery": mastery},
    )


@login_required
@require_POST
def quiz_recover(request, slug, level):
    """POST (HTMX) — Intenta recuperar un intento de evaluación."""
    resource = get_object_or_404(Resource, slug=slug, is_published=True)
    level = int(level)

    recovered = recover_attempt(request.user, resource, level)
    info = get_attempts_info(request.user, resource, level)
    mastery = get_resource_mastery(request.user, resource)

    return TemplateResponse(
        request,
        "includes/quiz_recover_result.html",
        {
            "resource": resource,
            "level": level,
            "recovered": recovered,
            "info": info,
            "mastery": mastery,
        },
    )


@login_required
@require_POST
def report_error(request, question_id):
    """POST (HTMX) — Crea un reporte de error en una pregunta."""
    question = get_object_or_404(Question, pk=question_id)
    reason = request.POST.get("reason", "")
    comment = request.POST.get("comment", "")

    valid_reasons = [r[0] for r in QuestionErrorReport.REASON_CHOICES]
    if reason not in valid_reasons:
        return HttpResponseBadRequest("Motivo inválido.")

    report = QuestionErrorReport.objects.create(
        user=request.user,
        question=question,
        reason=reason,
        comment=comment,
    )

    # Enviar email de notificación
    try:
        send_mail(
            subject=f"[ProfeOnline] Reporte de error — {question.resource.title}",
            message=(
                f"Pregunta: {question.text}\n\n"
                f"Motivo: {report.get_reason_display()}\n"
                f"Comentario: {comment or '(sin comentario)'}\n"
                f"Reportado por: {request.user.username}\n"
                f"Recurso: {question.resource.title}\n"
            ),
            from_email=None,  # usa DEFAULT_FROM_EMAIL
            recipient_list=["contacto@profeonline.cl"],
            fail_silently=True,
        )
    except Exception:
        pass  # No bloquear la UX por un fallo de email

    return TemplateResponse(
        request,
        "includes/report_confirmation.html",
        {"question": question},
    )


# ---------------------------------------------------------------------------
# Evaluación final por tema (Fase 7)
# ---------------------------------------------------------------------------


def _get_active_topic(slug):
    return get_object_or_404(Topic, slug=slug, is_active=True)


@login_required
def topic_exam_start(request, slug):
    """GET (HTMX) — Renderiza el formulario de la evaluación final del tema."""
    topic = _get_active_topic(slug)

    questions = get_topic_exam_questions(topic)
    if not questions:
        return TemplateResponse(
            request,
            "includes/topic_exam_empty.html",
            {"topic": topic},
        )

    request.session[f"topic_exam_{topic.pk}"] = [q.pk for q in questions]

    return TemplateResponse(
        request,
        "includes/topic_exam_form.html",
        {"topic": topic, "questions": questions},
    )


@login_required
@require_POST
def topic_exam_submit(request, slug):
    """POST (HTMX) — Califica la evaluación final del tema y muestra resultados."""
    topic = _get_active_topic(slug)

    session_key = f"topic_exam_{topic.pk}"
    question_ids = request.session.get(session_key, [])
    if not question_ids:
        return HttpResponseBadRequest("No hay evaluación activa para enviar.")

    answers_dict = {}
    for q_id in question_ids:
        choice_id = request.POST.get(f"question_{q_id}")
        answers_dict[int(q_id)] = int(choice_id) if choice_id else None

    attempt, results = submit_topic_exam(request.user, topic, answers_dict)
    request.session.pop(session_key, None)

    info = get_topic_exam_info(request.user, topic)

    return TemplateResponse(
        request,
        "includes/topic_exam_results.html",
        {
            "topic": topic,
            "attempt": attempt,
            "results": results,
            "info": info,
        },
    )
