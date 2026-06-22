from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from apps.content.models import EvaluationSession, Resource, Topic
from apps.content.services.evaluation_session_service import (
    create_evaluation_session,
    finalize_session,
)
from apps.content.services.structured_progress_service import (
    get_structured_topic_domain,
)


def _answers_from_post(request, question_ids):
    answers = {}
    allowed = set(question_ids)
    for key, values in request.POST.lists():
        if not key.startswith("question_"):
            continue
        if len(values) != 1:
            raise ValueError("Respuesta duplicada.")
        try:
            question_id = int(key.removeprefix("question_"))
        except ValueError as exc:
            raise ValueError("Respuesta manipulada.") from exc
        if question_id not in allowed:
            raise ValueError("La pregunta no pertenece a esta sesión.")
        answers[question_id] = values[0]
    return answers


@login_required
@require_POST
def start_structured_evaluation(request, topic_id):
    topic = get_object_or_404(
        Topic, pk=topic_id, is_active=True, structured_bank_enabled=True
    )
    kind = request.POST.get("kind")
    resource = None
    level = 0
    if kind == "evaluacion_nivel":
        resource = get_object_or_404(
            Resource,
            pk=request.POST.get("resource_id"),
            topic=topic,
            is_published=True,
        )
        try:
            level = int(request.POST.get("level"))
        except (TypeError, ValueError):
            return HttpResponse("Nivel no válido.", status=400)
    try:
        session = create_evaluation_session(
            user=request.user,
            topic=topic,
            resource=resource,
            kind=kind,
            level=level,
        )
    except ValueError as exc:
        return HttpResponse(str(exc), status=400)
    entries = list(
        session.session_questions.select_related("question")
        .prefetch_related("question__choices")
        .order_by("order")
    )
    return render(
        request,
        "partials/_structured_evaluation_player.html",
        {"session": session, "entries": entries, "topic": topic},
    )


@login_required
@require_POST
def submit_structured_evaluation(request, session_id):
    session = get_object_or_404(
        EvaluationSession.objects.select_related("topic"),
        pk=session_id,
        user=request.user,
        topic__structured_bank_enabled=True,
    )
    question_ids = list(
        session.session_questions.values_list("question_id", flat=True)
    )
    try:
        answers = _answers_from_post(request, question_ids)
        session = finalize_session(session=session, answers=answers)
    except ValueError as exc:
        return HttpResponse(str(exc), status=400)
    answers = list(
        session.answers.select_related("question", "selected_choice")
        .prefetch_related("question__choices")
        .order_by("question__level", "question__order", "question_id")
    )
    possible = sum(answer.question.points for answer in answers)
    earned = sum(answer.points_awarded for answer in answers)
    percentage = round(earned * 100 / possible) if possible else 0
    return render(
        request,
        "partials/_structured_evaluation_player.html",
        {
            "session": session,
            "results": answers,
            "earned": earned,
            "possible": possible,
            "percentage": percentage,
            "topic": session.topic,
            "domain": get_structured_topic_domain(request.user, session.topic),
        },
    )
