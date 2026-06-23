import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.html import escape

from apps.content.views.permissions import is_admin
from apps.content.models.topic import Topic
from apps.content.models.quiz_guide import QuizGuide
from apps.content.models.learning_guide import LearningGuide
from apps.content.models.question import Question
from apps.content.services.learning_guide_service import (
    generate_guide_draft,
    validate_guide_schema,
)
from apps.content.services.originality_service import (
    check_originality,
    calculate_audit_hash,
)


def _authorized_private_guides(topic):
    return QuizGuide.objects.filter(
        Q(topics=topic) | Q(subjects=topic.subject) | Q(resources__topic=topic),
        is_active=True,
    ).distinct()


def _sources_are_authorized(topic, private_guides):
    source_ids = {guide.id for guide in private_guides}
    if not source_ids:
        return False
    authorized_ids = set(
        _authorized_private_guides(topic)
        .filter(id__in=source_ids)
        .values_list("id", flat=True)
    )
    return authorized_ids == source_ids


def _details_context(topic, guide=None, **extra):
    context = {
        "topic": topic,
        "guide": guide,
        "approved_items": topic.exercise_items.filter(
            status="aprobado"
        ).order_by("level", "order"),
        "private_guides": _authorized_private_guides(topic).order_by("title"),
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    context.update(extra)
    return context


@user_passes_test(is_admin)
def learning_guide_review(request):
    """Vista principal para la gestión, generación e inspección de guías ProfeOnline."""
    topic_id = request.GET.get("topic_id")
    action = request.GET.get("action")

    # Carga dinámica de fuentes y guías de un tema por HTMX
    if action == "load_topic_details":
        if not topic_id:
            return HttpResponse("")

        # Prefetch para evitar consultas N+1
        topic = get_object_or_404(
            Topic.objects.select_related("subject").prefetch_related("resources"),
            id=topic_id
        )

        if not topic.structured_bank_editable:
            return HttpResponse(
                '<div class="alert alert--danger">El tema seleccionado no tiene activado el banco estructurado.</div>',
                status=400
            )

        # Cargar la guía del tema (si existe) pre-cargando relaciones
        guides = LearningGuide.objects.filter(topic=topic).prefetch_related(
            "resources", "private_sources"
        )
        guide = (
            guides.filter(status="borrador").order_by("-updated_at", "-id").first()
            or guides.filter(status="publicada").order_by("-updated_at", "-id").first()
        )

        # Guías privadas autorizadas del tema
        ctx = _details_context(topic, guide)
        return render(request, "partials/_guide_details_panel.html", ctx)

    # Carga inicial del panel (incluye temas en preparación / staging).
    topics = Topic.objects.filter(
        Q(structured_bank_enabled=True) | Q(structured_bank_staging=True),
        is_active=True,
    ).order_by("subject__name", "name")
    ctx = {
        "topics": topics,
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    return render(request, "pages/learning_guide_review.html", ctx)


@user_passes_test(is_admin)
@require_POST
def generate_guide_draft_view(request):
    """Invoca la generación del borrador de la guía ProfeOnline usando la IA (POST)."""
    topic_id = request.POST.get("topic_id")
    private_guide_ids = request.POST.getlist("private_guide_ids")

    if not topic_id:
        return HttpResponse("Falta topic_id", status=400)

    topic = get_object_or_404(Topic, id=topic_id)
    if not topic.structured_bank_editable:
        return HttpResponse("Tema no habilitado para banco estructurado", status=400)

    approved_items = topic.exercise_items.filter(status="aprobado")
    if not approved_items.exists():
        return HttpResponse("El tema no tiene ítems de aprendizaje aprobados", status=400)

    # Validar y autorizar fuentes privadas server-side
    try:
        requested_ids = {int(guide_id) for guide_id in private_guide_ids}
    except (TypeError, ValueError):
        return HttpResponse("IDs de fuentes privadas no válidos", status=400)
    allowed_guides = _authorized_private_guides(topic).filter(id__in=requested_ids)
    if not requested_ids or allowed_guides.count() != len(requested_ids):
        return HttpResponse("Debes seleccionar al menos una guía privada autorizada y activa", status=400)

    try:
        # Generar borrador de la guía con IA (a cuentagotas)
        draft_content = generate_guide_draft(topic, allowed_guides)
    except Exception:
        return HttpResponse(
            '<div class="alert alert--danger mb-3">No fue posible generar el borrador con IA.</div>',
            status=500
        )

    with transaction.atomic():
        Topic.objects.select_for_update().get(id=topic.id)
        # Obtener o crear LearningGuide borrador
        # Si ya existe una publicada, creamos un nuevo borrador. Si hay un borrador previo, lo actualizamos.
        guide = LearningGuide.objects.filter(
            topic=topic, status="borrador"
        ).order_by("-updated_at", "-id").first()
        if not guide:
            # Crear nueva guía borrador
            guide = LearningGuide.objects.create(
                topic=topic,
                title=f"Guía de {topic.name}",
                status="borrador",
                visibility="interna",
                structured_content=draft_content
            )
        else:
            guide.structured_content = draft_content
            guide.save()

        # Sincronizar fuentes privadas utilizadas
        guide.private_sources.set(allowed_guides)

        # Limpiar datos de originalidad anteriores ante la nueva generación
        guide.originality_report = {}
        guide.originality_checked_at = None
        guide.originality_content_hash = ""
        guide.save()

    # Devolver el panel del borrador
    ctx = _details_context(
        topic,
        guide,
        success_msg="Borrador de guía generado de manera exitosa.",
    )
    return render(request, "partials/_guide_details_panel.html", ctx)


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_guide_draft_view(request, guide_id):
    """Permite ver el formulario o guardar los cambios editados manualmente de una guía (GET/POST)."""
    guide = get_object_or_404(LearningGuide, id=guide_id)
    topic = guide.topic

    if guide.status != "borrador":
        return HttpResponse("Solo se pueden editar guías en estado borrador.", status=400)

    if not topic.structured_bank_editable:
        return HttpResponse("Tema no habilitado para banco estructurado", status=400)

    if request.method == "POST":
        content_json_str = request.POST.get("structured_content_json", "").strip()
        try:
            new_content = json.loads(content_json_str)
            # Validar esquema del nuevo contenido
            approved_items = topic.exercise_items.filter(status="aprobado")
            validate_guide_schema(new_content, approved_items)
        except json.JSONDecodeError:
            ctx = {
                "guide": guide,
                "error": "El contenido no es un JSON válido.",
                "draft_json": content_json_str
            }
            response = render(request, "partials/_guide_edit_form.html", ctx)
            response["HX-Retarget"] = "#guide-content-box"
            return response
        except ValueError as ve:
            ctx = {
                "guide": guide,
                "error": f"Error de validación de esquema: {str(ve)}",
                "draft_json": content_json_str
            }
            response = render(request, "partials/_guide_edit_form.html", ctx)
            response["HX-Retarget"] = "#guide-content-box"
            return response

        with transaction.atomic():
            guide = LearningGuide.objects.select_for_update().get(id=guide.id)
            # Invalidación de validaciones si el contenido cambió
            if new_content != guide.structured_content:
                guide.originality_report = {}
                guide.originality_checked_at = None
                guide.originality_content_hash = ""

            guide.structured_content = new_content
            guide.save()

        ctx = _details_context(topic, guide)
        return render(request, "partials/_guide_details_panel.html", ctx)

    if request.GET.get("cancel") == "true":
        return render(
            request,
            "partials/_guide_content_box.html",
            {"guide": guide},
        )

    # GET: Formulario de edición inline
    draft_json = json.dumps(guide.structured_content, indent=2, ensure_ascii=False)
    ctx = {
        "guide": guide,
        "draft_json": draft_json
    }
    return render(request, "partials/_guide_edit_form.html", ctx)


@user_passes_test(is_admin)
@require_POST
def validate_originality_view(request, guide_id):
    """Ejecuta el motor de originalidad y guarda atómicamente la evidencia y hash (POST)."""
    with transaction.atomic():
        guide = get_object_or_404(
            LearningGuide.objects.select_for_update().select_related("topic"),
            id=guide_id,
        )
        topic = Topic.objects.select_for_update().get(id=guide.topic_id)
        if not topic.structured_bank_editable:
            return HttpResponse("Tema no habilitado para banco estructurado", status=400)
        if guide.status != "borrador":
            return HttpResponse("Solo se pueden validar guías en estado borrador.", status=400)

        source_ids = list(guide.private_sources.values_list("id", flat=True))
        private_guides = list(
            QuizGuide.objects.select_for_update().filter(id__in=source_ids).order_by("id")
        )
        if not _sources_are_authorized(topic, private_guides):
            return HttpResponse(
                "Las fuentes privadas están vacías, inactivas o ya no pertenecen al tema.",
                status=400,
            )

        try:
            result = check_originality(guide.structured_content, private_guides)
        except ValueError as ve:
            return HttpResponse(
                f'<div class="alert alert--danger mb-3">Error de validación operativa: {escape(str(ve))}</div>',
                status=400
            )

        guide.originality_report = result
        guide.originality_checked_at = timezone.now()
        # Generar hash de auditoría extendido con huellas de fuentes privadas
        guide.originality_content_hash = calculate_audit_hash(guide.structured_content, private_guides)
        guide.save()

    ctx = {
        "guide": guide,
        "result": result
    }
    return render(request, "partials/_originality_report_panel.html", ctx)


@user_passes_test(is_admin)
@require_POST
def publish_learning_guide_view(request, guide_id):
    """Publica formalmente la guía de forma segura tras revalidar en caliente en una transacción."""
    guide = get_object_or_404(LearningGuide, id=guide_id)
    topic = guide.topic

    if not topic.structured_bank_editable:
        return HttpResponse("Tema no habilitado para banco estructurado", status=400)

    # Iniciar transacción y bloquear Topic y guías en orden estable
    with transaction.atomic():
        # Bloquear Topic
        Topic.objects.select_for_update().get(id=topic.id)
        # Bloquear todas las guías existentes de ese tema en orden estable de id
        list(LearningGuide.objects.filter(topic=topic).select_for_update().order_by("id"))

        # Volver a cargar la guía con bloqueo
        guide = LearningGuide.objects.select_for_update().get(id=guide_id)
        if guide.status != "borrador":
            return HttpResponse("Solo se pueden publicar guías en estado borrador.", status=400)

        # 1. Obtener fuentes privadas persistidas
        source_ids = list(guide.private_sources.values_list("id", flat=True))
        private_guides = list(
            QuizGuide.objects.select_for_update().filter(id__in=source_ids).order_by("id")
        )
        if not _sources_are_authorized(topic, private_guides):
            return HttpResponse(
                "Las fuentes privadas están vacías, inactivas o ya no pertenecen al tema.",
                status=400,
            )

        # 2. Revalidar hash en caliente
        current_hash = calculate_audit_hash(guide.structured_content, private_guides)
        if current_hash != guide.originality_content_hash:
            return HttpResponse(
                '<div class="alert alert--danger mb-3">La guía o sus fuentes han cambiado desde la última validación. Por favor, realiza la validación de originalidad antes de publicar.</div>',
                status=400
            )

        try:
            originality_result = check_originality(guide.structured_content, private_guides)
        except ValueError as error:
            return HttpResponse(
                f'<div class="alert alert--danger mb-3">Fallo en la revalidación en caliente: {escape(str(error))}</div>',
                status=400
            )

        guide.originality_report = originality_result
        guide.originality_checked_at = timezone.now()
        guide.originality_content_hash = current_hash
        if not originality_result["passed"]:
            guide.save(
                update_fields=[
                    "originality_report",
                    "originality_checked_at",
                    "originality_content_hash",
                    "updated_at",
                ]
            )
            return HttpResponse(
                '<div class="alert alert--danger mb-3">La validación en caliente de originalidad falló. Corrige las coincidencias antes de publicar.</div>',
                status=400
            )

        # 3. Validar esquema final
        approved_items = topic.exercise_items.filter(status="aprobado")
        try:
            validate_guide_schema(guide.structured_content, approved_items)
        except ValueError as ve:
            return HttpResponse(
                f'<div class="alert alert--danger mb-3">El borrador no cumple con el esquema: {escape(str(ve))}</div>',
                status=400
            )

        # 4. Despublicar las guías anteriores del mismo tema (política de única guía pública activa)
        LearningGuide.objects.filter(topic=topic, status="publicada").exclude(id=guide.id).update(
            status="archivada",
            visibility="interna"
        )

        # 5. Enlazar únicamente los items aprobados incluidos en el JSON
        # Limpiar enlaces previos (si los hubiera)
        topic.exercise_items.filter(learning_guide=guide).update(learning_guide=None)

        json_item_ids = []
        for itm_data in guide.structured_content.get("items", []):
            try:
                json_item_ids.append(int(itm_data.get("item_id")))
            except (ValueError, TypeError):
                continue

        topic.exercise_items.filter(id__in=json_item_ids, status="aprobado").update(learning_guide=guide)

        # 6. Cambiar estado a publicada y visibilidad a publica
        guide.status = "publicada"
        guide.visibility = "publica"
        guide.save()

    # Recargar el panel completo de detalles
    ctx = _details_context(
        topic,
        guide,
        success_msg="La guía ha sido validada y publicada formalmente con éxito.",
    )
    return render(request, "partials/_guide_details_panel.html", ctx)
