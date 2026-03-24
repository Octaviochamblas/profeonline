from apps.content.models import Resource


def get_published_resources(subject_slug=None, topic_slug=None, level_slug=None):
    queryset = Resource.objects.filter(is_published=True).select_related("subject", "topic").prefetch_related("levels")

    if subject_slug:
        queryset = queryset.filter(subject__slug=subject_slug)

    if topic_slug:
        queryset = queryset.filter(topic__slug=topic_slug)

    if level_slug:
        queryset = queryset.filter(levels__slug=level_slug)

    return queryset.distinct()