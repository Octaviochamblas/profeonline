"""Selectores de lectura para el sistema de evaluación gamificada."""

from collections import defaultdict

from django.db.models import Max, Q
from apps.content.models import QuizAttempt, ResourceView, Resource, Question


def get_question_availability_map(resource_ids):
    """Disponibilidad de práctica/evaluación por recurso y nivel. Una query.

    Las preguntas ``ambas`` habilitan los dos modos. Retorna:
    ``{resource_id: {level: {"practice": bool, "evaluation": bool}}}``.
    """
    resource_ids = list(resource_ids)
    if not resource_ids:
        return {}

    rows = (
        Question.objects.filter(resource_id__in=resource_ids, status="publicada")
        .values("resource_id", "level", "mode")
        .distinct()
    )
    availability = defaultdict(
        lambda: defaultdict(lambda: {"practice": False, "evaluation": False})
    )
    for row in rows:
        level = row["level"]
        if level not in (1, 2, 3):
            continue
        slot = availability[row["resource_id"]][level]
        if row["mode"] in ("preparacion", "ambas"):
            slot["practice"] = True
        if row["mode"] in ("evaluacion", "ambas"):
            slot["evaluation"] = True

    return {
        rid: {
            level: dict(modes)
            for level, modes in sorted(availability.get(rid, {}).items())
        }
        for rid in resource_ids
    }


def get_available_levels_map(resource_ids):
    """Niveles (1-3) con preguntas publicadas por recurso. Una sola query.

    Returns: dict {resource_id: [niveles ordenados]}.
    """
    availability = get_question_availability_map(resource_ids)
    return {rid: list(levels) for rid, levels in availability.items()}


def get_recent_attempts_by_resource(user, resource_ids, limit=3):
    """Últimos `limit` intentos por (recurso, nivel, modo) más el flag histórico
    de aprobación. Sin N+1: una sola query.

    Returns:
        dict {resource_id: {(level, mode): {"recent": [pct...], "passed": bool,
        "count": int}}}; `recent` ordenado del más reciente al más antiguo.
    """
    resource_ids = list(resource_ids)
    if not getattr(user, "is_authenticated", False) or not resource_ids:
        return {}

    attempts = (
        QuizAttempt.objects.filter(user=user, resource_id__in=resource_ids)
        .order_by("resource_id", "level", "mode", "-created_at", "-id")
        .values("resource_id", "level", "mode", "score", "total", "passed")
    )

    grouped = defaultdict(lambda: defaultdict(
        lambda: {"recent": [], "passed": False, "count": 0}
    ))
    for attempt in attempts:
        slot = grouped[attempt["resource_id"]][(attempt["level"], attempt["mode"])]
        slot["count"] += 1
        if attempt["passed"]:
            slot["passed"] = True
        if len(slot["recent"]) < limit:
            total = attempt["total"] or 0
            pct = round(attempt["score"] / total * 100) if total else 0
            slot["recent"].append(pct)

    # Convertir a dict normal (evita defaultdict en plantillas/tests).
    return {rid: dict(levels) for rid, levels in grouped.items()}


def get_resource_progress_map(user, resource_ids):
    """Genera un mapa de progreso por recurso para un usuario.

    Args:
        user: usuario autenticado.
        resource_ids: iterable de IDs de recursos.

    Returns:
        dict {resource_id: {"viewed": bool, "max_level": int, "stars": int}}
    """
    if not user.is_authenticated or not resource_ids:
        return {}

    resource_ids = list(resource_ids)

    # Recursos vistos
    viewed_ids = set(
        ResourceView.objects.filter(
            user=user,
            resource_id__in=resource_ids,
        ).values_list("resource_id", flat=True)
    )

    # Máximo nivel aprobado por recurso
    passed_data = (
        QuizAttempt.objects.filter(
            user=user,
            resource_id__in=resource_ids,
            mode="evaluacion",
            passed=True,
        )
        .values("resource_id")
        .annotate(max_level=Max("level"))
    )
    passed_map = {row["resource_id"]: row["max_level"] for row in passed_data}

    result = {}
    for rid in resource_ids:
        max_level = passed_map.get(rid, 0)
        result[rid] = {
            "viewed": rid in viewed_ids,
            "max_level": max_level,
            "stars": max_level,
        }
    return result


def get_topic_evaluation_summary(user, topic):
    """Resumen de progreso de evaluación para un tema.

    Returns:
        dict con recursos_total, vistos, aprobados, estrellas_total.
    """
    if not user.is_authenticated:
        return {
            "total": 0,
            "viewed": 0,
            "approved": 0,
            "stars": 0,
        }

    resources = topic.resources.filter(is_published=True)
    resource_ids = list(resources.values_list("id", flat=True))

    if not resource_ids:
        return {
            "total": 0,
            "viewed": 0,
            "approved": 0,
            "stars": 0,
        }

    progress_map = get_resource_progress_map(user, resource_ids)

    viewed = sum(1 for p in progress_map.values() if p["viewed"])
    approved = sum(1 for p in progress_map.values() if p["max_level"] > 0)
    stars = sum(p["stars"] for p in progress_map.values())

    return {
        "total": len(resource_ids),
        "viewed": viewed,
        "approved": approved,
        "stars": stars,
    }


def get_topics_progress_map(user, topic_ids):
    """Genera un mapa de progreso en lote para múltiples temas de un usuario.

    Previene consultas N+1 al procesar todos los temas en una sola query por modelo.

    Args:
        user: usuario autenticado o anónimo.
        topic_ids: iterable de IDs de temas.

    El porcentaje ya **no** depende de "Comprendido" (`ResourceCompletion`):
    se calcula como el **progreso ponderado** (práctica 30% / evaluación 70%)
    promediado sobre los recursos trabajados del tema. `worked` indica cuántos
    recursos tienen algún intento (cobertura).

    Returns:
        dict {topic_id: {total, viewed, approved, stars, worked,
        weighted_progress, percentage}}
    """
    topic_ids = list(topic_ids)
    if not topic_ids:
        return {}

    # Recursos publicados para estos temas
    resources = Resource.objects.filter(
        topic_id__in=topic_ids, is_published=True
    ).values("id", "topic_id")

    topic_resources = defaultdict(list)
    all_resource_ids = []
    for r in resources:
        topic_resources[r["topic_id"]].append(r["id"])
        all_resource_ids.append(r["id"])

    empty = lambda tid: {
        "total": len(topic_resources.get(tid, [])),
        "viewed": 0,
        "approved": 0,
        "stars": 0,
        "worked": 0,
        "weighted_progress": 0,
        "percentage": 0,
    }

    if not getattr(user, "is_authenticated", False) or not all_resource_ids:
        return {tid: empty(tid) for tid in topic_ids}

    # Progreso ponderado por recurso (sin N+1). Import diferido para evitar ciclo.
    from apps.content.services.progress_service import get_resources_progress

    progress_by_resource = get_resources_progress(user, all_resource_ids)

    # Recursos vistos
    viewed_ids = set(
        ResourceView.objects.filter(
            user=user,
            resource_id__in=all_resource_ids,
        ).values_list("resource_id", flat=True)
    )

    # Máximo nivel de evaluación aprobado por recurso
    passed_data = (
        QuizAttempt.objects.filter(
            user=user,
            resource_id__in=all_resource_ids,
            mode="evaluacion",
            passed=True,
        )
        .values("resource_id")
        .annotate(max_level=Max("level"))
    )
    passed_map = {row["resource_id"]: row["max_level"] for row in passed_data}

    result = {}
    for tid in topic_ids:
        rids = topic_resources.get(tid, [])
        if not rids:
            result[tid] = empty(tid)
            continue

        viewed = sum(1 for rid in rids if rid in viewed_ids)
        approved = sum(1 for rid in rids if passed_map.get(rid, 0) > 0)
        stars = sum(passed_map.get(rid, 0) for rid in rids)

        worked_values = [
            progress_by_resource[rid]["weighted_progress"]
            for rid in rids
            if progress_by_resource.get(rid, {}).get("worked_levels")
        ]
        weighted = round(sum(worked_values) / len(worked_values)) if worked_values else 0

        result[tid] = {
            "total": len(rids),
            "viewed": viewed,
            "approved": approved,
            "stars": stars,
            "worked": len(worked_values),
            "weighted_progress": weighted,
            "percentage": weighted,
        }

    return result
