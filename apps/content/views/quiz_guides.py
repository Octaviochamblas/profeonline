"""Gestión de guías de referencia (QuizGuide) — página solo-admin.

Permite subir un documento (PDF/Word/texto) o pegar texto, guardarlo como guía
reutilizable y vincularlo a asignaturas, temas o recursos. Esas guías son las
que el "modo documento" usa para copiar el formato de las preguntas.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.content.models import QuizGuide, Resource, Subject, Topic
from apps.content.services import drive_service
from apps.content.services.guide_service import extract_guide_text, normalize_text
from apps.content.views.permissions import is_admin


def _set_guide_links(guide, request):
    """Vincula la guía a las asignaturas/temas/recursos elegidos en el form."""
    sub_ids = request.POST.getlist("subjects")
    top_ids = request.POST.getlist("topics")
    res_ids = request.POST.getlist("resources")
    if sub_ids:
        guide.subjects.set(Subject.objects.filter(id__in=sub_ids))
    if top_ids:
        guide.topics.set(Topic.objects.filter(id__in=top_ids))
    if res_ids:
        guide.resources.set(Resource.objects.filter(id__in=res_ids))


@user_passes_test(is_admin)
def quiz_guides(request):
    if request.method == "POST":
        title = (request.POST.get("title") or "").strip()
        description = (request.POST.get("description") or "").strip()
        pasted = (request.POST.get("text") or "").strip()
        upload = request.FILES.get("file")

        if not title:
            messages.error(request, "El título de la guía es obligatorio.")
            return redirect("content:quiz_guides")

        source_filename = ""
        raw = ""
        if upload:
            source_filename = upload.name
            raw = extract_guide_text(upload.read(), filename=upload.name)
        elif pasted:
            raw = pasted

        text = normalize_text(raw)
        if not text:
            messages.error(
                request,
                "No se pudo extraer texto. Subí un archivo con texto seleccionable "
                "(PDF/Word/txt) o pegá el contenido en el cuadro de texto.",
            )
            return redirect("content:quiz_guides")

        guide = QuizGuide.objects.create(
            title=title,
            description=description,
            source_filename=source_filename,
            content_text=text,
        )

        _set_guide_links(guide, request)

        messages.success(
            request, f"Guía '{guide.title}' guardada ({len(text)} caracteres)."
        )
        return redirect("content:quiz_guides")

    guides = QuizGuide.objects.prefetch_related(
        "subjects", "topics", "resources"
    ).order_by("title")
    context = {
        "guides": guides,
        "subjects": Subject.objects.filter(is_active=True).order_by("name"),
        "topics": Topic.objects.filter(is_active=True).select_related("subject").order_by("name"),
        "resources": Resource.objects.filter(is_published=True).order_by("title"),
    }
    context.update(_drive_context(request))
    return render(request, "pages/quiz_guides.html", context)


def _drive_context(request):
    """Estado de Drive y, si corresponde, el contenido de la carpeta actual.

    Se navega por subcarpetas con ``?drive_folder=<id>`` (la biblioteca suele
    estar anidada). Si hay carpeta por defecto configurada, se lista al entrar.
    """
    default_folder = getattr(settings, "GUIDES_DRIVE_FOLDER_ID", "")
    folder = (request.GET.get("drive_folder") or "").strip() or default_folder
    ctx = {
        "drive_configured": drive_service.is_configured(),
        "drive_default_folder": default_folder,
        "drive_folder": folder,
        "drive_folder_name": None,
        "drive_folders": None,
        "drive_files": None,
        "drive_error": None,
    }
    if folder and ctx["drive_configured"]:
        try:
            listing = drive_service.list_folder(folder)
            ctx["drive_folder_name"] = listing["name"]
            ctx["drive_folders"] = listing["folders"]
            ctx["drive_files"] = listing["files"]
        except Exception as exc:  # noqa: BLE001 - mostrar el error, no romper la página
            ctx["drive_error"] = str(exc)
    return ctx


@user_passes_test(is_admin)
@require_POST
def import_drive_guides(request):
    """Importa los archivos de Drive seleccionados como guías (`QuizGuide`)."""
    file_ids = request.POST.getlist("drive_files")
    if not file_ids:
        messages.error(request, "No seleccionaste ningún archivo de Drive.")
        return redirect("content:quiz_guides")

    imported = 0
    skipped = []
    for file_id in file_ids:
        try:
            data = drive_service.fetch_file(file_id)
        except Exception as exc:  # noqa: BLE001 - un archivo no debe tumbar la importación
            skipped.append(f"{file_id} ({exc})")
            continue

        text = normalize_text(data.get("text", ""))
        name = data.get("name", file_id)
        if not text:
            skipped.append(f"{name} (sin texto extraíble)")
            continue

        guide = QuizGuide.objects.create(
            title=name,
            source_filename=name,
            content_text=text,
        )
        _set_guide_links(guide, request)
        imported += 1

    if imported:
        messages.success(request, f"{imported} guía(s) importada(s) desde Drive.")
    if skipped:
        messages.error(request, "No se importaron: " + "; ".join(skipped))
    return redirect("content:quiz_guides")


@user_passes_test(is_admin)
@require_POST
def delete_quiz_guide(request, guide_id):
    guide = get_object_or_404(QuizGuide, id=guide_id)
    titulo = guide.title
    guide.delete()
    messages.success(request, f"Guía '{titulo}' eliminada.")
    return redirect("content:quiz_guides")
