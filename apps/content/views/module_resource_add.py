from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.content.models import Module, ModuleResource, Resource



def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
@require_POST
def module_resource_add(request, module_id):
    resource_id = request.POST.get("resource_id")

    if not resource_id:
        return JsonResponse({"ok": False, "error": "Falta resource_id"}, status=400)

    try:
        module = Module.objects.get(pk=module_id)
        resource = Resource.objects.get(pk=resource_id)
    except (Module.DoesNotExist, Resource.DoesNotExist):
        return JsonResponse({"ok": False, "error": "Módulo o recurso no encontrado"}, status=404)

    existing = ModuleResource.objects.filter(module=module).order_by("-order").first()
    next_order = existing.order + 1 if existing else 1

    module_resource, created = ModuleResource.objects.get_or_create(
        module=module,
        resource=resource,
        defaults={
            "order": next_order,
            "is_required": True,
        },
    )

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "module_resource_id": module_resource.id,
            "order": module_resource.order,
        }
    )