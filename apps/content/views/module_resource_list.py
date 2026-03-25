from django.http import JsonResponse
from apps.content.models import ModuleResource


def module_resource_list(request, module_id):
    items = ModuleResource.objects.filter(
        module_id=module_id
    ).select_related(
        "resource",
        "resource__subject",
        "resource__topic",
    ).prefetch_related(
        "resource__levels",
    ).order_by("order", "id")

    data = []
    for item in items:
        data.append(
            {
                "id": item.resource.id,
                "module_resource_id": item.id,
                "title": item.resource.title,
                "subject": item.resource.subject.name if item.resource.subject else "",
                "topic": item.resource.topic.name if item.resource.topic else "",
                "levels": [level.name for level in item.resource.levels.all()],
                "order": item.order,
                "is_required": item.is_required,
            }
        )

    return JsonResponse({"resources": data})