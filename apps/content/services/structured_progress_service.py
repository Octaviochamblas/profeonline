"""Academic domain for the structured bank, isolated from legacy QuizAttempt."""

from django.db.models import Prefetch

from apps.content.models import (
    EvaluationSession,
    EvaluationSessionAnswer,
    ResourceExerciseItem,
)


def _score(session):
    if not session:
        return 0
    answers = getattr(session, "_domain_answers", None)
    if answers is None:
        answers = list(session.answers.select_related("question"))
    earned = sum(answer.points_awarded for answer in answers)
    possible = sum(answer.question.points for answer in answers)
    return round(earned * 100 / possible) if possible else 0


def get_structured_topic_domain(user, topic):
    if not topic.structured_bank_enabled:
        return None
    required_pairs = set(
        ResourceExerciseItem.objects.filter(
            resource__topic=topic,
            resource__is_published=True,
            exercise_item__status="aprobado",
        )
        .exclude(evaluation_quota=0, exercise_item__detected_exercise_count=0)
        .values_list("resource_id", "exercise_item__level")
    )
    sessions = list(
        EvaluationSession.objects.filter(
            user=user,
            topic=topic,
            kind__in=["evaluacion_nivel", "prueba_final"],
            status__in=["enviada", "vencida"],
        )
        .prefetch_related(
            Prefetch(
                "answers",
                queryset=EvaluationSessionAnswer.objects.select_related("question"),
                to_attr="_domain_answers",
            )
        )
        .order_by("kind", "resource_id", "level", "-attempt_number")
    )
    latest_by_pair = {}
    latest_final = None
    for session in sessions:
        if session.kind == "evaluacion_nivel":
            latest_by_pair.setdefault((session.resource_id, session.level), session)
        elif latest_final is None:
            latest_final = session

    scores_by_level = {1: [], 2: [], 3: []}
    by_resource = {}
    for resource_id, level in required_pairs:
        score = _score(latest_by_pair.get((resource_id, level)))
        scores_by_level[level].append(score)
        by_resource.setdefault(resource_id, {})[level] = score
    per_level = {
        level: round(sum(scores) / len(scores)) if scores else 0
        for level, scores in scores_by_level.items()
    }
    required_levels = [level for level, scores in scores_by_level.items() if scores]
    levels_average = (
        round(sum(per_level[level] for level in required_levels) / len(required_levels))
        if required_levels
        else 0
    )
    final_score = _score(latest_final)
    weighted = round(levels_average * 0.6 + final_score * 0.4)
    return {
        "resource_scores": by_resource,
        "level_scores": per_level,
        "levels_average": levels_average,
        "final_score": final_score,
        "weighted_score": weighted,
        "dominated": weighted >= 80 and final_score >= 80,
    }
