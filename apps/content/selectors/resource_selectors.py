from apps.content.models import Resource


def get_published_resources():
    return Resource.objects.filter(is_published=True)