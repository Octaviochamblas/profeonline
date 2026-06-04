from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.text import slugify
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from django.urls import reverse
from apps.content.models import Resource
from apps.content.views.permissions import is_admin

@user_passes_test(is_admin)
def publish_duplicates(request):
    title = request.GET.get("title", "").strip()
    topic_id = request.GET.get("topic_id")

    if not title or not topic_id:
        return HttpResponseBadRequest("Faltan parametros requeridos: title, topic_id")

    slug = slugify(title)

    try:
        duplicates = Resource.objects.filter(
            topic_id=topic_id
        ).filter(
            Q(slug=slug) |
            Q(title__iexact=title) |
            Q(title__icontains=title)
        ).distinct()
    except ValueError:
        return HttpResponseBadRequest("Tema invalido")

    data = []
    for r in duplicates:
        data.append({
            "title": r.title,
            "url": reverse("content:resource_detail", args=[r.slug])
        })

    return JsonResponse(data, safe=False)
