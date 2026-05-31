from django.db.models import Q
from apps.content.models import Resource, ResourceCompletion, ResourceView


def get_resume_resource(user):
    """Devuelve (resource, completed) del último recurso publicado que el
    usuario abrió, o (None, False) si no hay ninguno."""
    if not getattr(user, "is_authenticated", False):
        return None, False

    view = (
        ResourceView.objects.filter(user=user, resource__is_published=True)
        .select_related("resource", "resource__subject", "resource__topic")
        .order_by("-viewed_at")
        .first()
    )
    if not view:
        return None, False

    resource = view.resource
    completed = ResourceCompletion.objects.filter(
        user=user, resource=resource
    ).exists()
    return resource, completed


def get_published_resources(subject_id=None, topic_id=None, level_id=None, q=None):
    queryset = Resource.objects.filter(is_published=True).select_related(
        "subject",
        "topic",
    ).prefetch_related(
        "levels",
    )

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if topic_id:
        queryset = queryset.filter(topic_id=topic_id)

    if level_id:
        queryset = queryset.filter(levels__id=level_id)

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return queryset.distinct()


def get_module_resource_options(
    subject_id=None,
    topic_id=None,
    level_id=None,
    limit=30,
):
    queryset = Resource.objects.filter(is_published=True).select_related(
        "subject",
        "topic",
    ).prefetch_related(
        "levels",
    )

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if topic_id:
        queryset = queryset.filter(topic_id=topic_id)

    if level_id:
        queryset = queryset.filter(levels__id=level_id)

    return queryset.distinct().order_by("title")[:limit]
