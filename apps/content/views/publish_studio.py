import json
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify
from apps.content.views.permissions import is_admin
from apps.content.models import Area, Subject, Topic, Module
from apps.content.services.youtube_utils import extract_playlist_id

def get_publish_studio_context(request):
    areas = Area.objects.filter(is_active=True).order_by("order")
    return {
        "areas": areas,
    }

@user_passes_test(is_admin)
def publish_studio(request):
    if request.method == "POST":
        errors = {}

        # 1. File names list (hidden JSON field)
        file_names_raw = request.POST.get("file_names", "[]")
        try:
            files = json.loads(file_names_raw)
            if not isinstance(files, list) or not all(isinstance(f, str) for f in files):
                return HttpResponse("El parametro file_names debe ser una lista de nombres de archivos (strings).", status=400)
        except (json.JSONDecodeError, TypeError, ValueError):
            return HttpResponse("El parametro file_names tiene un formato JSON invalido.", status=400)

        if not files:
            errors["file_names"] = "Debe seleccionar al menos un archivo."

        watch_folder = request.POST.get("watch_folder", "default").strip() or "default"

        # 2. Taxonomy slugs mapping
        area = None
        area_slug = None
        area_id = request.POST.get("area_id")
        if area_id:
            try:
                area = Area.objects.get(id=area_id)
                if not area.is_active:
                    errors["area_id"] = "El area seleccionada esta inactiva."
                else:
                    area_slug = area.slug
            except (Area.DoesNotExist, ValueError):
                errors["area_id"] = "Area seleccionada invalida."
        else:
            errors["area_id"] = "El area es obligatoria."

        subject = None
        subject_slug = None
        subject_id = request.POST.get("subject_id")
        if subject_id:
            try:
                subject = Subject.objects.get(id=subject_id)
                if not subject.is_active:
                    errors["subject_id"] = "La asignatura seleccionada esta inactiva."
                elif area and subject.area != area:
                    errors["subject_id"] = "La asignatura no pertenece al area seleccionada."
                else:
                    subject_slug = subject.slug
            except (Subject.DoesNotExist, ValueError):
                errors["subject_id"] = "Asignatura seleccionada invalida."
        else:
            errors["subject_id"] = "La asignatura es obligatoria."

        topic = None
        topic_slug = None
        topic_id = request.POST.get("topic_id")
        if topic_id:
            try:
                topic = Topic.objects.get(id=topic_id)
                if not topic.is_active:
                    errors["topic_id"] = "El tema seleccionado esta inactivo."
                elif subject and topic.subject != subject:
                    errors["topic_id"] = "El tema no pertenece a la asignatura seleccionada."
                else:
                    topic_slug = topic.slug
            except (Topic.DoesNotExist, ValueError):
                errors["topic_id"] = "Tema seleccionado invalido."
        else:
            errors["topic_id"] = "El tema es obligatorio."

        module_slug = None
        module_id = request.POST.get("module_id")
        if module_id:
            try:
                module = Module.objects.get(id=module_id)
                if not module.is_published:
                    errors["module_id"] = "El modulo seleccionado no esta publicado."
                elif subject and module.subject != subject:
                    errors["module_id"] = "El modulo no pertenece a la asignatura seleccionada."
                elif topic and module.topic is not None and module.topic != topic:
                    errors["module_id"] = "El modulo no pertenece al tema seleccionado."
                else:
                    module_slug = module.slug
            except (Module.DoesNotExist, ValueError):
                errors["module_id"] = "Modulo seleccionado invalido."

        # 3. YouTube/Playlist
        playlist_id_raw = request.POST.get("playlist_id", "").strip()
        playlist_title = request.POST.get("playlist_title", "").strip()

        playlist_id = ""
        if playlist_id_raw:
            playlist_id = extract_playlist_id(playlist_id_raw)
            if not playlist_id:
                errors["playlist_id"] = "El ID o URL de la lista de reproduccion no es valido."

        # 4. Instructions
        instructions = request.POST.get("instructions", "").strip()

        if errors:
            context = get_publish_studio_context(request)
            context["errors"] = errors
            # Preserving submitted values in context
            context["form_data"] = request.POST
            context["file_list"] = files
            return render(request, "pages/publish_studio.html", context)

        # Build output batch JSON
        batch_data = {
            "schema": "profeonline.upload-batch/v1",
            "watch_folder": watch_folder,
            "files": files,
            "taxonomy": {
                "area_slug": area_slug,
                "subject_slug": subject_slug,
                "topic_slug": topic_slug,
                "module_slug": module_slug
            },
            "youtube": {
                "playlist_id": playlist_id,
                "playlist_title": playlist_title
            },
            "instructions": instructions
        }

        # Return json file as attachment
        response = HttpResponse(
            json.dumps(batch_data, indent=2, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
        topic_suffix = slugify(topic.name) if topic else "batch"
        response['Content-Disposition'] = f'attachment; filename="upload-batch-{topic_suffix}.json"'
        return response

    # GET
    context = get_publish_studio_context(request)
    return render(request, "pages/publish_studio.html", context)
