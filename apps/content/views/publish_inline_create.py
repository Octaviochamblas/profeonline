from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from apps.content.views.permissions import is_admin
from apps.content.forms.content_forms import AreaForm, SubjectForm, TopicForm, LevelForm
from apps.content.forms.module_forms import ModuleForm
from apps.content.models import Area, Subject, Topic, Level, Module

@user_passes_test(is_admin)
@require_POST
def publish_inline_create(request, entity_type):
    post_data = request.POST.copy()
    if "order" not in post_data or not post_data["order"]:
        post_data["order"] = "0"
    if "is_active" not in post_data:
        post_data["is_active"] = "true"
    if "is_published" not in post_data:
        post_data["is_published"] = "true"
    # Topic.resource_ordering_method es obligatorio en TopicForm (modelo default="level");
    # el modal inline no lo pide, así que inyectamos el default del modelo.
    if "resource_ordering_method" not in post_data or not post_data["resource_ordering_method"]:
        post_data["resource_ordering_method"] = "level"

    if entity_type == "area":
        form = AreaForm(post_data)
    elif entity_type == "subject":
        form = SubjectForm(post_data)
    elif entity_type == "topic":
        form = TopicForm(post_data)
    elif entity_type == "level":
        form = LevelForm(post_data)
    elif entity_type == "module":
        if "subject" not in post_data and "subject_id" in post_data:
            post_data["subject"] = post_data["subject_id"]
        form = ModuleForm(post_data)
    else:
        return HttpResponseBadRequest("Tipo de entidad no soportado")

    # Special validation checks before standard form validation if needed
    if entity_type == "subject":
        area_id = request.POST.get("area_id")
        if not area_id:
            return JsonResponse({
                "ok": False,
                "errors": {"area_id": ["El area es obligatoria para crear una asignatura."]}
            }, status=400)
        try:
            area = Area.objects.get(id=area_id)
        except (Area.DoesNotExist, ValueError):
            return JsonResponse({
                "ok": False,
                "errors": {"area_id": ["Area seleccionada no existe."]}
            }, status=400)

    if form.is_valid():
        obj = form.save(commit=False)

        if entity_type == "subject":
            obj.area = area

        obj.save()
        form.save_m2m()  # In case there are ManyToMany relations, e.g., levels in Subject/Topic

        if entity_type == "module":
            topic_id = request.POST.get("topic_id")
            if topic_id:
                try:
                    obj.topic = Topic.objects.get(id=topic_id)
                    obj.save()
                except (Topic.DoesNotExist, ValueError):
                    pass
            level_ids = request.POST.getlist("level_ids") or request.POST.getlist("level_ids[]")
            if level_ids:
                obj.levels.set(level_ids)

        label = getattr(obj, "name", None) or getattr(obj, "title", None)
        return JsonResponse({
            "ok": True,
            "id": obj.id,
            "name": label,
            "slug": obj.slug
        })
    else:
        errors = {k: [v["message"] for v in list_errs] for k, list_errs in form.errors.get_json_data().items()}
        return JsonResponse({
            "ok": False,
            "errors": errors
        }, status=400)
