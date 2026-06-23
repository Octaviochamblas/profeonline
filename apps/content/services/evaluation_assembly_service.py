"""Selection rules for structured level evaluations and final tests."""

import logging
import random
from collections import defaultdict
from decimal import Decimal, InvalidOperation

from apps.content.models import EvaluationSessionQuestion, Question, ResourceExerciseItem

logger = logging.getLogger(__name__)

LEVEL_DISTRIBUTION_KEYS = {"conceptual": 1, "mecanico": 2, "aplicacion": 3}
MAX_ASSEMBLY_STATES = 50_000


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
            mode="evaluacion",
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
    unseen = [question for question in candidates if question.id not in used_ids]
    source = unseen if len(unseen) >= count else candidates
    rng.shuffle(source)
    return source[:count]


def _effective_quota(link):
    return link.evaluation_quota or link.exercise_item.detected_exercise_count


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
        quota = _effective_quota(link)
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


def _normalize_distribution(distribution):
    if not isinstance(distribution, dict):
        raise ValueError("La distribución final debe ser un objeto JSON.")
    normalized = {}
    try:
        for key in LEVEL_DISTRIBUTION_KEYS:
            value = Decimal(str(distribution[key]))
            if value < 0:
                raise ValueError
            normalized[key] = value
    except (KeyError, InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("La distribución final contiene valores no válidos.") from exc
    if sum(normalized.values()) != Decimal("100"):
        raise ValueError("La distribución final debe sumar 100%.")
    return normalized


def _largest_remainder(total, distribution):
    normalized = _normalize_distribution(distribution)
    raw = {
        level: Decimal(total) * normalized[key] / Decimal("100")
        for key, level in LEVEL_DISTRIBUTION_KEYS.items()
    }
    result = {level: int(value) for level, value in raw.items()}
    remaining = total - sum(result.values())
    order = sorted(
        raw,
        key=lambda level: (raw[level] - result[level], -level),
        reverse=True,
    )
    for level in order[:remaining]:
        result[level] += 1
    return result


def _selection_options(
    candidates, quota, used_ids, max_minutes, rng, *, force_reset=False
):
    """Return all useful (points, minutes) choices for exactly one link quota."""
    candidates = list(candidates)
    unseen = [question for question in candidates if question.id not in used_ids]
    source = (
        candidates
        if force_reset
        else (unseen if len(unseen) >= quota else candidates)
    )
    if len(source) < quota:
        return {}
    rng.shuffle(source)
    states = {(0, 0, 0): ()}
    for question in source:
        additions = {}
        for (count, points, minutes), selected in list(states.items()):
            next_minutes = minutes + question.estimated_minutes
            if count >= quota or next_minutes > max_minutes:
                continue
            key = (count + 1, points + question.points, next_minutes)
            additions.setdefault(key, selected + (question,))
        states.update(additions)
        if len(states) > MAX_ASSEMBLY_STATES:
            raise ValueError("La configuración del pool final es demasiado compleja.")
    return {
        (points, minutes): selected
        for (count, points, minutes), selected in states.items()
        if count == quota
    }


def assemble_final_evaluation(*, user, topic, config, seed=None):
    """Respect link quotas, point distribution, duration and no-repeat rules."""
    _normalize_distribution(config.final_distribution)
    if config.final_minutes <= 0 or config.duration_tolerance_pct > 100:
        raise ValueError("La duración o tolerancia de la prueba final no es válida.")
    links = [
        link
        for link in ResourceExerciseItem.objects.filter(
            resource__topic=topic,
            resource__is_published=True,
            exercise_item__status="aprobado",
        ).select_related("exercise_item", "resource")
        if _effective_quota(link) > 0
    ]
    if not links:
        raise ValueError("No hay cuotas configuradas para la prueba final.")

    pool_by_link = defaultdict(list)
    for question in _base_pool(topic, "prueba_final"):
        if question.level != question.exercise_item.level:
            continue
        pool_by_link[(question.exercise_item_id, question.resource_id)].append(question)

    used = _used_question_ids(user, topic, "prueba_final")
    rng = random.Random(seed)
    max_minutes = config.final_minutes * (
        100 + config.duration_tolerance_pct
    ) / 100
    min_minutes = config.final_minutes * (
        100 - config.duration_tolerance_pct
    ) / 100
    def build_duration_candidates(force_reset=False):
        group_options = []
        for link in links:
            quota = _effective_quota(link)
            candidates = pool_by_link[(link.exercise_item_id, link.resource_id)]
            if len(candidates) < quota:
                raise ValueError(
                    f"Pool final insuficiente para el ítem "
                    f"{link.exercise_item_id} y recurso {link.resource_id}: "
                    f"{len(candidates)}/{quota}."
                )
            options = _selection_options(
                candidates,
                quota,
                used,
                max_minutes,
                rng,
                force_reset=force_reset,
            )
            if not options:
                return []
            group_options.append((link.exercise_item.level, options))

        # State = (points N1, points N2, points N3, minutes) -> questions.
        states = {(0, 0, 0, 0): ()}
        for level, options in group_options:
            next_states = {}
            for (p1, p2, p3, minutes), selected in states.items():
                for (points, option_minutes), questions in options.items():
                    duration = minutes + option_minutes
                    if duration > max_minutes:
                        continue
                    point_totals = [p1, p2, p3]
                    point_totals[level - 1] += points
                    key = (*point_totals, duration)
                    next_states.setdefault(key, selected + questions)
            if not next_states:
                return []
            if len(next_states) > MAX_ASSEMBLY_STATES:
                raise ValueError("La configuración del pool final es demasiado compleja.")
            states = next_states
        return [
            (state, selected)
            for state, selected in states.items()
            if min_minutes <= state[3] <= max_minutes
        ]

    duration_candidates = build_duration_candidates()
    if not duration_candidates:
        duration_candidates = build_duration_candidates(force_reset=True)
    if not duration_candidates:
        raise ValueError("Ninguna combinación respeta la duración de la prueba final.")

    exact = []
    for state, selected in duration_candidates:
        actual = {1: state[0], 2: state[1], 3: state[2]}
        target = _largest_remainder(sum(actual.values()), config.final_distribution)
        if actual == target:
            exact.append((state, selected))

    if exact:
        _, selected = rng.choice(exact)
    else:
        def deviation(candidate):
            state, _ = candidate
            actual = {1: state[0], 2: state[1], 3: state[2]}
            target = _largest_remainder(
                sum(actual.values()), config.final_distribution
            )
            return sum(abs(actual[level] - target[level]) for level in (1, 2, 3))

        best_state, selected = min(duration_candidates, key=deviation)
        actual = {1: best_state[0], 2: best_state[1], 3: best_state[2]}
        target = _largest_remainder(sum(actual.values()), config.final_distribution)
        logger.warning(
            "Desvío de distribución en prueba final topic=%s actual=%s objetivo=%s",
            topic.id,
            actual,
            target,
        )

    result = list(selected)
    rng.shuffle(result)
    return result
