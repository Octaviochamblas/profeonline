"""Selectores de lectura para el sistema de evaluación gamificada."""

from django.db.models import Max, Q

from apps.content.models import QuizAttempt, ResourceView


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
