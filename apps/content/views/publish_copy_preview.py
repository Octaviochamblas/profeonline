from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from apps.content.models import Subject, Topic
from apps.content.services.resource_copy import build_resource_copy
from apps.content.views.permissions import is_admin

@user_passes_test(is_admin)
def publish_copy_preview(request):
    title = request.GET.get("title", "").strip()
    subject_id = request.GET.get("subject_id")
    topic_id = request.GET.get("topic_id")

    if not title or not subject_id or not topic_id:
        return HttpResponseBadRequest("Faltan parametros requeridos: title, subject_id, topic_id")

    try:
        subject = Subject.objects.get(id=subject_id)
        topic = Topic.objects.get(id=topic_id)
    except (Subject.DoesNotExist, Topic.DoesNotExist, ValueError):
        return HttpResponseBadRequest("Asignatura o tema no encontrado")

    video = {"title": title, "video_url": ""}
    description, content = build_resource_copy(video, subject, topic)

    return JsonResponse({
        "title": title,
        "description": description,
        "content_md": content
    })
