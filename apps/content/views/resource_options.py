from django.http import JsonResponse
from apps.content.models import Resource
from apps.content.selectors import get_module_resource_options


def resource_options(request):
    subject_id = request.GET.get("subject_id")
    topic_id = request.GET.get("topic_id")
    level_id = request.GET.get("level_id")
    selected_ids = request.GET.getlist("selected_ids")

    resources = get_module_resource_options(
        subject_id=subject_id or None,
        topic_id=topic_id or None,
        level_id=level_id or None,
        limit=30,
    )

    selected_resources = Resource.objects.filter(id__in=selected_ids).select_related(
        "subject",
        "topic",
    ).prefetch_related("levels")

    combined = []
    seen_ids = set()

    for resource in list(selected_resources) + list(resources):
        if resource.id not in seen_ids:
            combined.append(resource)
            seen_ids.add(resource.id)

    data = []
    for resource in combined:
        data.append(
            {
                "id": resource.id,
                "title": resource.title,
                "subject": resource.subject.name if resource.subject else "",
                "topic": resource.topic.name if resource.topic else "",
                "levels": [level.name for level in resource.levels.all()],
                "checked": str(resource.id) in selected_ids,
            }
        )

    return JsonResponse({"resources": data})