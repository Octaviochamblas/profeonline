"""Selectores de lectura para el sistema de evaluación gamificada."""

from django.db.models import Max, Q
from apps.content.models import QuizAttempt, ResourceView, Resource, ResourceCompletion


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

    Returns:
        dict {topic_id: {total, viewed, approved, stars, completed, percentage}}
    """
    topic_ids = list(topic_ids)
    if not topic_ids:
        return {}

    # Recursos publicados para estos temas
    resources = Resource.objects.filter(topic_id__in=topic_ids, is_published=True)

    from collections import defaultdict
    topic_resources = defaultdict(list)
    all_resource_ids = []
    for r in resources:
        topic_resources[r.topic_id].append(r.id)
        all_resource_ids.append(r.id)

    # Si el usuario no está autenticado o no hay recursos, retornar mapa vacío/cero
    if not user.is_authenticated or not all_resource_ids:
        return {
            tid: {
                "total": len(topic_resources.get(tid, [])),
                "viewed": 0,
                "approved": 0,
                "stars": 0,
                "completed": 0,
                "percentage": 0,
            }
            for tid in topic_ids
        }

    # Recursos vistos
    viewed_ids = set(
        ResourceView.objects.filter(
            user=user,
            resource_id__in=all_resource_ids,
        ).values_list("resource_id", flat=True)
    )

    # Recursos marcados como comprendidos
    completed_ids = set(
        ResourceCompletion.objects.filter(
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
            result[tid] = {
                "total": 0,
                "viewed": 0,
                "approved": 0,
                "stars": 0,
                "completed": 0,
                "percentage": 0,
            }
            continue

        viewed = sum(1 for rid in rids if rid in viewed_ids)
        completed = sum(1 for rid in rids if rid in completed_ids)
        approved = sum(1 for rid in rids if passed_map.get(rid, 0) > 0)
        stars = sum(passed_map.get(rid, 0) for rid in rids)

        percentage = round((completed / len(rids)) * 100)

        result[tid] = {
            "total": len(rids),
            "viewed": viewed,
            "approved": approved,
            "stars": stars,
            "completed": completed,
            "percentage": percentage,
        }

    return result
