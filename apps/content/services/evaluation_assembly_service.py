"""Selection rules for structured level evaluations and final tests."""

import random
from collections import defaultdict

from apps.content.models import EvaluationSessionQuestion, Question, ResourceExerciseItem

LEVEL_DISTRIBUTION_KEYS = {"conceptual": 1, "mecanico": 2, "aplicacion": 3}


def _base_pool(topic, scope):
    if not topic.is_active or not topic.structured_bank_enabled:
        raise ValueError("El tema no tiene habilitado el banco estructurado.")
    return (
        Question.objects.filter(
            resource__topic=topic,
            resource__is_published=True,
            exercise_item__topic=topic,
            exercise_item__status="aprobado",
            status="publicada",
            scope=scope,
            estimated_minutes__gt=0,
            points__gt=0,
        )
        .select_related("resource", "exercise_item")
        .prefetch_related("choices")
    )


def _used_question_ids(user, topic, kind, level=None):
    filters = {
        "session__user": user,
        "session__topic": topic,
        "session__kind": kind,
    }
    if level is not None:
        filters["session__level"] = level
    return set(
        EvaluationSessionQuestion.objects.filter(**filters).values_list(
            "question_id", flat=True
        )
    )


def _choose_without_repetition(candidates, count, used_ids, rng):
    candidates = list(candidates)
    unseen = [q for q in candidates if q.id not in used_ids]
    source = unseen if len(unseen) >= count else candidates
    rng.shuffle(source)
    return source[:count]


def assemble_level_evaluation(*, user, topic, resource, level, seed=None):
    """Select each approved item's configured quota for one resource and level."""
    if resource.topic_id != topic.id or not resource.is_published:
        raise ValueError("El recurso no pertenece al tema o no está publicado.")
    links = list(
        ResourceExerciseItem.objects.filter(
            resource=resource,
            exercise_item__topic=topic,
            exercise_item__status="aprobado",
            exercise_item__level=level,
        ).select_related("exercise_item")
    )
    if not links:
        raise ValueError("El recurso no tiene ítems aprobados para este nivel.")
    pool = _base_pool(topic, "evaluacion_nivel").filter(
        resource=resource, level=level
    )
    by_item = defaultdict(list)
    for question in pool:
        by_item[question.exercise_item_id].append(question)
    used = _used_question_ids(user, topic, "evaluacion_nivel", level)
    rng = random.Random(seed)
    selected = []
    for link in links:
        quota = link.evaluation_quota or link.exercise_item.detected_exercise_count
        if quota <= 0:
            continue
        candidates = by_item[link.exercise_item_id]
        if len(candidates) < quota:
            raise ValueError(
                f"Pool insuficiente para el ítem {link.exercise_item_id}: "
                f"{len(candidates)}/{quota}."
            )
        selected.extend(_choose_without_repetition(candidates, quota, used, rng))
    if not selected:
        raise ValueError("No hay preguntas configuradas para esta evaluación.")
    rng.shuffle(selected)
    return selected


def _largest_remainder(total, distribution):
    raw = {
        level: total * distribution.get(key, 0) / 100
        for key, level in LEVEL_DISTRIBUTION_KEYS.items()
    }
    result = {level: int(value) for level, value in raw.items()}
    remaining = total - sum(result.values())
    order = sorted(raw, key=lambda level: (raw[level] - result[level], -level), reverse=True)
    for level in order[:remaining]:
        result[level] += 1
    return result


def assemble_final_evaluation(*, user, topic, config, seed=None):
    """Assemble the reserved final pool by point distribution and duration bound."""
    pool = list(_base_pool(topic, "prueba_final"))
    if not pool:
        raise ValueError("No hay preguntas publicadas para la prueba final.")
    desired_points = sum(
        link.evaluation_quota or link.exercise_item.detected_exercise_count
        for link in ResourceExerciseItem.objects.filter(
            resource__topic=topic,
            resource__is_published=True,
            exercise_item__status="aprobado",
        ).select_related("exercise_item")
    )
    if desired_points <= 0:
        desired_points = sum(q.points for q in pool)
    targets = _largest_remainder(desired_points, config.final_distribution)
    used = _used_question_ids(user, topic, "prueba_final")
    rng = random.Random(seed)
    unseen = [q for q in pool if q.id not in used]
    source = unseen if sum(q.points for q in unseen) >= desired_points else pool
    rng.shuffle(source)

    selected = []
    points_by_level = defaultdict(int)
    remaining = list(source)
    for level in (1, 2, 3):
        for question in list(remaining):
            if question.level != level or points_by_level[level] >= targets[level]:
                continue
            if points_by_level[level] + question.points <= targets[level]:
                selected.append(question)
                points_by_level[level] += question.points
                remaining.remove(question)
    # A sparse level may be completed by another level; the gate in Fase 7 reports this drift.
    current_points = sum(q.points for q in selected)
    for question in remaining:
        if current_points >= desired_points:
            break
        if current_points + question.points <= desired_points:
            selected.append(question)
            current_points += question.points
    if current_points != desired_points:
        raise ValueError("El pool final no permite completar el puntaje requerido.")

    duration = sum(q.estimated_minutes for q in selected)
    tolerance = config.final_minutes * config.duration_tolerance_pct / 100
    if not config.final_minutes - tolerance <= duration <= config.final_minutes + tolerance:
        raise ValueError(
            f"La duración estimada ({duration} min) queda fuera del rango permitido."
        )
    rng.shuffle(selected)
    return selected
