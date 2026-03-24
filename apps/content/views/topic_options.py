from django.http import JsonResponse
from apps.content.models import Topic


def topic_options_by_subject(request):
    subject_id = request.GET.get("subject_id")

    if not subject_id:
        return JsonResponse({"topics": []})

    topics = Topic.objects.filter(
        subject_id=subject_id,
        is_active=True,
    ).order_by("name")

    data = [
        {"id": topic.id, "name": topic.name}
        for topic in topics
    ]

    return JsonResponse({"topics": data})