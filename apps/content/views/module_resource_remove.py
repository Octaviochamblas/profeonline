from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.content.models import ModuleResource


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
@require_POST
def module_resource_remove(request, module_id):
    resource_id = request.POST.get("resource_id")

    if not resource_id:
        return JsonResponse({"ok": False, "error": "Falta resource_id"}, status=400)

    deleted, _ = ModuleResource.objects.filter(
        module_id=module_id,
        resource_id=resource_id,
    ).delete()

    return JsonResponse(
        {
            "ok": True,
            "deleted": deleted > 0,
        }
    )