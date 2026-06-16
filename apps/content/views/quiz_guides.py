"""Gestión de guías de referencia (QuizGuide) — página solo-admin.

Permite subir un documento (PDF/Word/texto) o pegar texto, guardarlo como guía
reutilizable y vincularlo a asignaturas, temas o recursos. Esas guías son las
que el "modo documento" usa para copiar el formato de las preguntas.
"""

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.content.models import QuizGuide, Resource, Subject, Topic
from apps.content.services.guide_service import extract_guide_text, normalize_text
from apps.content.views.permissions import is_admin


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

        sub_ids = request.POST.getlist("subjects")
        top_ids = request.POST.getlist("topics")
        res_ids = request.POST.getlist("resources")
        if sub_ids:
            guide.subjects.set(Subject.objects.filter(id__in=sub_ids))
        if top_ids:
            guide.topics.set(Topic.objects.filter(id__in=top_ids))
        if res_ids:
            guide.resources.set(Resource.objects.filter(id__in=res_ids))

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
    return render(request, "pages/quiz_guides.html", context)


@user_passes_test(is_admin)
@require_POST
def delete_quiz_guide(request, guide_id):
    guide = get_object_or_404(QuizGuide, id=guide_id)
    titulo = guide.title
    guide.delete()
    messages.success(request, f"Guía '{titulo}' eliminada.")
    return redirect("content:quiz_guides")
