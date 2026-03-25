from apps.content.models import Resource


def get_published_resources(subject_id=None, topic_id=None, level_id=None):
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