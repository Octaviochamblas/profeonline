"""Transactional lifecycle and grading for structured evaluations."""

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import Max
from django.utils import timezone

from apps.content.models import (
    EvaluationSession,
    EvaluationSessionAnswer,
    EvaluationSessionQuestion,
)
from apps.content.services.answer_grading_service import grade_answer
from apps.content.services.evaluation_assembly_service import (
    assemble_final_evaluation,
    assemble_level_evaluation,
)


def _config_for(topic):
    config, _ = topic.__class__._meta.apps.get_model(
        "content", "TopicBankConfig"
    ).objects.get_or_create(topic=topic)
    return config


def _expire_stale_session(session, now):
    config = _config_for(session.topic)
    deadline = session.expires_at + timedelta(
        seconds=config.network_tolerance_seconds
    )
    if session.status == "en_curso" and now > deadline:
        finalize_session(session=session, answers={}, now=now)


def create_evaluation_session(
    *, user, topic, kind, resource=None, level=0, now=None, seed=None
):
    """Create one server-timed attempt, safely consuming its attempt number."""
    if kind not in {"evaluacion_nivel", "prueba_final"}:
        raise ValueError("Tipo de evaluación no válido.")
    if not topic.is_active or not topic.structured_bank_enabled:
        raise ValueError("El tema no tiene habilitado el banco estructurado.")
    if kind == "evaluacion_nivel":
        if resource is None or level not in {1, 2, 3}:
            raise ValueError("La evaluación de nivel requiere recurso y nivel.")
    else:
        resource = None
        level = 0
    now = now or timezone.now()

    for retry in range(2):
        try:
            with transaction.atomic():
                topic.__class__.objects.select_for_update().get(pk=topic.pk)
                config = _config_for(topic)
                active = (
                    EvaluationSession.objects.select_for_update()
                    .filter(
                        user=user,
                        topic=topic,
                        kind=kind,
                        level=level,
                        status="en_curso",
                    )
                    .order_by("-started_at")
                    .first()
                )
                if active:
                    _expire_stale_session(active, now)
                    active.refresh_from_db()
                    if active.status == "en_curso":
                        return active
                maximum = (
                    config.level_eval_attempts
                    if kind == "evaluacion_nivel"
                    else config.final_attempts
                )
                last = (
                    EvaluationSession.objects.filter(
                        user=user, topic=topic, kind=kind, level=level
                    ).aggregate(value=Max("attempt_number"))["value"]
                    or 0
                )
                if last >= maximum:
                    raise ValueError("No quedan intentos disponibles.")
                questions = (
                    assemble_level_evaluation(
                        user=user,
                        topic=topic,
                        resource=resource,
                        level=level,
                        seed=seed,
                    )
                    if kind == "evaluacion_nivel"
                    else assemble_final_evaluation(
                        user=user, topic=topic, config=config, seed=seed
                    )
                )
                minutes = (
                    config.level_eval_minutes
                    if kind == "evaluacion_nivel"
                    else config.final_minutes
                )
                session = EvaluationSession.objects.create(
                    user=user,
                    topic=topic,
                    resource=resource,
                    kind=kind,
                    level=level,
                    attempt_number=last + 1,
                    started_at=now,
                    expires_at=now + timedelta(minutes=minutes),
                )
                EvaluationSessionQuestion.objects.bulk_create(
                    [
                        EvaluationSessionQuestion(
                            session=session, question=question, order=index
                        )
                        for index, question in enumerate(questions, start=1)
                    ]
                )
                return session
        except IntegrityError:
            if retry:
                raise
    raise RuntimeError("No fue posible crear la sesión.")


def finalize_session(*, session, answers, now=None):
    """Grade every assigned question once; safe to call repeatedly."""
    now = now or timezone.now()
    with transaction.atomic():
        session = (
            EvaluationSession.objects.select_for_update()
            .select_related("topic")
            .get(pk=session.pk)
        )
        if session.status != "en_curso":
            return session
        config = _config_for(session.topic)
        expired = now > session.expires_at + timedelta(
            seconds=config.network_tolerance_seconds
        )
        assigned = list(
            session.session_questions.select_related("question")
            .prefetch_related("question__choices")
            .order_by("order")
        )
        assigned_ids = {entry.question_id for entry in assigned}
        if set(answers) - assigned_ids:
            raise ValueError("Se enviaron respuestas ajenas a la sesión.")
        for entry in assigned:
            question = entry.question
            raw = answers.get(question.id, "")
            selected_choice = None
            text_answer = ""
            if not expired and question.question_type == "alternativa" and raw:
                try:
                    choice_id = int(raw)
                except (TypeError, ValueError) as exc:
                    raise ValueError("Alternativa no válida.") from exc
                selected_choice = next(
                    (choice for choice in question.choices.all() if choice.id == choice_id),
                    None,
                )
                if selected_choice is None:
                    raise ValueError("La alternativa no pertenece a la pregunta.")
                correct = selected_choice.is_correct
            elif not expired and question.question_type in {"numerica", "algebraica"}:
                text_answer = str(raw)
                correct = grade_answer(question, text_answer)["correct"]
            else:
                correct = False
            EvaluationSessionAnswer.objects.update_or_create(
                session=session,
                question=question,
                defaults={
                    "selected_choice": selected_choice,
                    "text_answer": text_answer,
                    "is_correct": correct,
                    "points_awarded": question.points if correct else 0,
                },
            )
        session.status = "vencida" if expired else "enviada"
        session.save(update_fields=["status"])
        return session
