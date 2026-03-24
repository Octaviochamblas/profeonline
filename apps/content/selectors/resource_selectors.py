from apps.content.models import Resource


def get_published_resources(subject_slug=None):
    queryset = Resource.objects.filter(is_published=True).select_related("subject")

    if subject_slug:
        queryset = queryset.filter(subject__slug=subject_slug)

    return queryset