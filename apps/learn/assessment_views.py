from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST

from apps.content.models import KnowledgeNode
from apps.content.services.node_assessment_service import (
    get_questions_for_assessment,
    get_attempts_info,
    submit_assessment,
    get_node_mastery,
    QUESTIONS_PER_LEVEL,
)


def _node_assessment_context(user, node):
    """Contexto compartido para refrescar la sección de evaluación de nodo."""
    mastery = get_node_mastery(user, node)
    return {
        "node": node,
        "mastery": mastery,
    }


@login_required
def node_assessment_start(request, recurso_slug, level, **kwargs):
    """GET — Renderiza el formulario de evaluación de nodo con preguntas aleatorias."""
    node = get_object_or_404(KnowledgeNode, slug=recurso_slug, is_published=True, node_type=KnowledgeNode.NODE_RECURSO)
    try:
        level = int(level)
    except ValueError:
        return HttpResponseBadRequest("Nivel inválido.")

    if level not in (1, 2, 3):
        return HttpResponseBadRequest("Nivel inválido.")

    info = get_attempts_info(request.user, node, level)
    if info["passed"]:
        # Ya aprobado, redirecciona a mostrar el estado actual
        return TemplateResponse(
            request,
            "learn/includes/assessment_section.html",
            _node_assessment_context(request.user, node),
        )
    if info["max_reached"]:
        return TemplateResponse(
            request,
            "learn/includes/assessment_blocked.html",
            {"node": node, "level": level, "info": info},
        )

    questions = get_questions_for_assessment(node, level)
    if not questions:
        return TemplateResponse(
            request,
            "learn/includes/assessment_empty.html",
            {"node": node, "level": level},
        )

    session_key = f"node_assessment_{node.pk}_{level}"
    request.session[session_key] = [q.pk for q in questions]

    level_labels = {1: "Definición", 2: "Ejercicios simples", 3: "Problemas de aplicación"}

    return TemplateResponse(
        request,
        "learn/includes/assessment_form.html",
        {
            "node": node,
            "questions": questions,
            "level": level,
            "level_label": level_labels.get(level, ""),
            "total": len(questions),
        },
    )


@login_required
@require_POST
def node_assessment_submit(request, recurso_slug, level, **kwargs):
    """POST — Califica el intento de evaluación de nodo y retorna la pauta de resultados."""
    node = get_object_or_404(KnowledgeNode, slug=recurso_slug, is_published=True, node_type=KnowledgeNode.NODE_RECURSO)
    try:
        level = int(level)
    except ValueError:
        return HttpResponseBadRequest("Nivel inválido.")

    if level not in (1, 2, 3):
        return HttpResponseBadRequest("Nivel inválido.")

    session_key = f"node_assessment_{node.pk}_{level}"
    question_ids = request.session.get(session_key, [])

    if not question_ids:
        return HttpResponseBadRequest("No hay evaluación activa para enviar.")

    answers_dict = {}
    for q_id in question_ids:
        choice_id = request.POST.get(f"question_{q_id}")
        answers_dict[int(q_id)] = int(choice_id) if choice_id else None

    try:
        attempt = submit_assessment(request.user, node, level, answers_dict)
    except ValueError as e:
        return TemplateResponse(
            request,
            "learn/includes/assessment_error.html",
            {"node": node, "error": str(e)},
        )

    # Limpiar session
    request.session.pop(session_key, None)

    # Ordenar y calificar las respuestas para el feedback
    answers = list(attempt.answers.select_related("question", "selected_choice"))
    order_index = {q_id: pos for pos, q_id in enumerate(question_ids)}
    answers.sort(key=lambda a: order_index.get(a.question_id, len(order_index)))

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

    mastery = get_node_mastery(request.user, node)
    info = get_attempts_info(request.user, node, level)
    level_labels = {1: "Definición", 2: "Ejercicios simples", 3: "Problemas de aplicación"}

    return TemplateResponse(
        request,
        "learn/includes/assessment_results.html",
        {
            "node": node,
            "attempt": attempt,
            "results": results,
            "level": level,
            "level_label": level_labels.get(level, ""),
            "mastery": mastery,
            "info": info,
        },
    )


@login_required
def node_assessment_status(request, recurso_slug, **kwargs):
    """GET — Retorna el panel de estado actualizado de la evaluación de nodo."""
    node = get_object_or_404(KnowledgeNode, slug=recurso_slug, is_published=True, node_type=KnowledgeNode.NODE_RECURSO)
    return TemplateResponse(
        request,
        "learn/includes/assessment_section.html",
        _node_assessment_context(request.user, node),
    )
