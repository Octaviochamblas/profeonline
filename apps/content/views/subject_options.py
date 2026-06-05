from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test
from apps.content.models import Subject, Module
from apps.content.views.permissions import is_admin

@user_passes_test(is_admin)
def subject_options(request):
    area_id = request.GET.get("area_id")
    if not area_id:
        return JsonResponse({"subjects": []})

    subjects = Subject.objects.filter(
        area_id=area_id,
        is_active=True
    ).order_by("name")

    data = [
        {"id": s.id, "name": s.name}
        for s in subjects
    ]
    return JsonResponse({"subjects": data})

@user_passes_test(is_admin)
def module_options(request):
    subject_id = request.GET.get("subject_id")
    if not subject_id:
        return JsonResponse({"modules": []})

    modules = Module.objects.filter(
        subject_id=subject_id,
        is_published=True
    ).order_by("order", "title")

    data = [
        {"id": m.id, "title": m.title}
        for m in modules
    ]
    return JsonResponse({"modules": data})
