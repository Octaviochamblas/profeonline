import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify
from apps.content.views.permissions import is_admin
from apps.content.models import Area, Level, Subject, Topic, Module
from apps.content.services.youtube_utils import extract_playlist_id

PALETTES = [
    ("azul-profeonline", "Azul ProfeOnline"),
    ("teal-profeonline", "Teal ProfeOnline"),
    ("gris-cool", "Gris Cool"),
]

PRIVACY_OPTIONS = [
    ("public", "Publico"),
    ("unlisted", "Oculto (Unlisted)"),
    ("private", "Privado"),
]

def get_publish_studio_context(request):
    areas = Area.objects.filter(is_active=True).order_by("order")
    levels = Level.objects.filter(is_active=True).order_by("order")
    return {
        "areas": areas,
        "levels": levels,
        "palettes": PALETTES,
        "privacy_options": PRIVACY_OPTIONS,
    }

@user_passes_test(is_admin)
def publish_studio(request):
    if request.method == "POST":
        errors = {}

        # 1. File info
        file_name = request.POST.get("file_name", "").strip()
        if not file_name:
            errors["file_name"] = "El nombre del archivo es obligatorio."
        watch_folder = request.POST.get("watch_folder", "default").strip()

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

        level_ids = request.POST.getlist("level_ids") or request.POST.getlist("level_ids[]")
        clean_level_ids = []
        for lid in level_ids:
            if lid:
                try:
                    clean_level_ids.append(int(lid))
                except ValueError:
                    errors["level_ids"] = "Nivel seleccionado invalido."

        level_slugs = []
        if not errors.get("level_ids"):
            if not clean_level_ids:
                errors["level_ids"] = "Debe seleccionar al menos un nivel."
            else:
                levels = Level.objects.filter(id__in=clean_level_ids, is_active=True)
                if len(levels) != len(set(clean_level_ids)):
                    errors["level_ids"] = "Uno o mas niveles seleccionados son invalidos o estan inactivos."
                else:
                    level_slugs = list(levels.values_list("slug", flat=True))

        # 3. YouTube/Playlist
        privacy = request.POST.get("privacy", "public").strip()
        skip_playlist = request.POST.get("skip_playlist") == "true" or request.POST.get("skip_playlist") == "on"
        playlist_id_raw = request.POST.get("playlist_id", "").strip()
        playlist_title = request.POST.get("playlist_title", "").strip()

        playlist_id = ""
        if not skip_playlist:
            if playlist_id_raw:
                playlist_id = extract_playlist_id(playlist_id_raw)
                if not playlist_id:
                    errors["playlist_id"] = "El ID o URL de la lista de reproduccion no es valido."
            else:
                errors["playlist_id"] = "Debe ingresar una playlist valida o marcar 'Subir sin playlist'."

        # 4. Thumbnail & copy
        palette = request.POST.get("palette", "azul-profeonline").strip()
        main_text = request.POST.get("main_text", "").strip()
        if not main_text:
            errors["main_text"] = "El texto principal de la miniatura es obligatorio."
        class_label = request.POST.get("class_label", "").strip()
        ai_panel_instructions = request.POST.get("ai_panel_instructions", "").strip()

        title = request.POST.get("title", "").strip()
        if not title:
            errors["title"] = "El titulo del recurso es obligatorio."
        description = request.POST.get("description", "").strip()
        content_md = request.POST.get("content_md", "").strip()
        ai_instructions = request.POST.get("ai_instructions", "").strip()

        is_published = request.POST.get("is_published") == "true" or request.POST.get("is_published") == "on"

        if errors:
            context = get_publish_studio_context(request)
            context["errors"] = errors
            # Preserving submitted values in context
            context["form_data"] = request.POST
            context["selected_levels"] = [int(lid) for lid in level_ids if str(lid).isdigit()]
            return render(request, "pages/publish_studio.html", context)


        # Build output JSON
        job_data = {
            "schema": "profeonline.upload-job/v1",
            "file": {
                "watch_folder": watch_folder,
                "file_name": file_name
            },
            "youtube": {
                "privacy": privacy,
                "playlist_id": "" if skip_playlist else playlist_id,
                "playlist_title": playlist_title,
                "skip_playlist": skip_playlist
            },
            "taxonomy": {
                "area_slug": area_slug,
                "subject_slug": subject_slug,
                "topic_slug": topic_slug,
                "module_slug": module_slug,
                "level_slugs": level_slugs
            },
            "thumbnail": {
                "class_label": class_label,
                "main_text": main_text,
                "palette": palette,
                "ai_panel_instructions": ai_panel_instructions
            },
            "copy": {
                "title": title,
                "description": description,
                "content_md": content_md
            },
            "ai_instructions": ai_instructions,
            "publish": {
                "is_published": is_published
            }
        }

        # Return json file as attachment
        response = HttpResponse(
            json.dumps(job_data, indent=2, ensure_ascii=False),
            content_type="application/json; charset=utf-8"
        )
        response['Content-Disposition'] = f'attachment; filename="upload-job-{slugify(title) or "video"}.json"'
        return response

    # GET
    context = get_publish_studio_context(request)
    return render(request, "pages/publish_studio.html", context)
