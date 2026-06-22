import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from django.db.models import Q

from apps.content.views.permissions import is_admin
from apps.content.models import Resource
from apps.content.models.topic import Topic
from apps.content.models.quiz_guide import QuizGuide
from apps.content.models.exercise_item import ExerciseItem, ResourceExerciseItem
from apps.content.models.question import Question
from apps.content.services.item_extraction_service import propose_items_from_guide

logger = logging.getLogger(__name__)

VALID_LEVELS = [lvl for lvl, _ in Question.LEVEL_CHOICES]
VALID_DIFFICULTIES = [diff for diff, _ in Question.DIFFICULTY_CHOICES]


# --- Helpers de aislamiento (flag por tema) y contexto ---------------------

def _get_enabled_topic(topic_id):
    """Tema activo con el banco estandarizado habilitado, o 404.

    Aísla toda la Fase 1 tras ``Topic.structured_bank_enabled``: un tema con el
    flag apagado no puede crear ni listar ítems.
    """
    return get_object_or_404(
        Topic, id=topic_id, is_active=True, structured_bank_enabled=True
    )


def _get_enabled_item(item_id):
    """Ítem cuyo tema está activo y con el flag habilitado, o 404."""
    return get_object_or_404(
        ExerciseItem,
        id=item_id,
        topic__is_active=True,
        topic__structured_bank_enabled=True,
    )


def _items_list_context(topic, **extra):
    """Contexto del listado de ítems sin N+1.

    Prefetch de ``resource_links__resource`` + recursos del tema cargados una sola
    vez; cada ítem recibe ``unlinked_resources_list`` ya calculado en memoria.
    """
    topic_resources = list(topic.resources.order_by("title"))
    items = list(
        ExerciseItem.objects.filter(topic=topic)
        .exclude(status="archivado")
        .prefetch_related("resource_links__resource")
    )
    for item in items:
        item.unlinked_resources_list = item.get_unlinked_resources(topic_resources)
    ctx = {
        "items": items,
        "topic": topic,
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    ctx.update(extra)
    return ctx


def _item_row_context(item, **extra):
    """Contexto para renderizar una sola fila de ítem (paths de mutación puntual)."""
    item.unlinked_resources_list = item.get_unlinked_resources()
    ctx = {
        "item": item,
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    ctx.update(extra)
    return ctx


# --- Vistas ----------------------------------------------------------------

@user_passes_test(is_admin)
def item_extraction(request):
    """Panel de ítems de aprendizaje (GET) y sus parciales HTMX.

    Solo opera sobre temas activos con el banco estandarizado habilitado.
    """
    action = request.GET.get("action")

    if action == "load_guides":
        topic_id = request.GET.get("topic_id")
        if not topic_id:
            return HttpResponse('<option value="">-- Primero selecciona un tema --</option>')
        topic = _get_enabled_topic(topic_id)
        # Guías asociadas al tema o a su asignatura (privadas, activas).
        guides = QuizGuide.objects.filter(
            Q(topics=topic) | Q(subjects=topic.subject),
            is_active=True,
        ).distinct().order_by("title")
        return render(request, "partials/_guide_options.html", {"guides": guides})

    if action == "list_items":
        topic_id = request.GET.get("topic_id")
        if not topic_id:
            return HttpResponse("")
        topic = _get_enabled_topic(topic_id)
        return render(request, "partials/_items_list.html", _items_list_context(topic))

    # Carga inicial completa: solo temas con el flag habilitado.
    topics = Topic.objects.filter(
        is_active=True, structured_bank_enabled=True
    ).order_by("subject__name", "name")
    ctx = {
        "topics": topics,
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    return render(request, "pages/item_extraction.html", ctx)


@user_passes_test(is_admin)
@require_POST
def propose_items(request):
    """Invoca la extracción de ítems por IA (POST), valida, normaliza y persiste."""
    topic_id = request.POST.get("topic_id")
    guide_id = request.POST.get("guide_id")

    if not topic_id or not guide_id:
        return HttpResponse(
            '<div class="alert alert--danger mb-3">Debes seleccionar un tema y una guía.</div>',
            status=400,
        )

    topic = _get_enabled_topic(topic_id)

    # La guía debe estar activa y asociada al tema o a su asignatura (no se envía
    # contenido privado de una guía ajena a la IA).
    guide = QuizGuide.objects.filter(
        Q(topics=topic) | Q(subjects=topic.subject),
        id=guide_id,
        is_active=True,
    ).distinct().first()
    if guide is None:
        return HttpResponse(
            '<div class="alert alert--danger mb-3">La guía no está disponible para este tema.</div>',
            status=404,
        )

    try:
        # Disparo único (a cuentagotas), sin reintentos automáticos masivos.
        proposed_list = propose_items_from_guide(guide, topic)
    except Exception as e:
        # El servicio ya sanea la llave; aquí no exponemos detalle del proveedor.
        logger.error("Error en propose_items: %s", e)
        return HttpResponse(
            '<div class="alert alert--danger mb-3">No se pudieron generar los ítems. '
            'Revisa la configuración de IA e inténtalo de nuevo.</div>',
            status=500,
        )

    allowed_resource_ids = set(topic.resources.values_list("id", flat=True))

    created_items = []
    with transaction.atomic():
        for item_data in proposed_list:
            title = (item_data.get("title") or "").strip()
            objective = (item_data.get("objective") or "").strip()
            if not title or not objective:
                continue

            level = item_data.get("level")
            if level not in VALID_LEVELS:
                level = 1

            difficulty = item_data.get("difficulty") or ""
            if difficulty not in VALID_DIFFICULTIES:
                difficulty = "intermedia"

            try:
                detected = int(item_data.get("detected_exercise_count") or 0)
            except (ValueError, TypeError):
                detected = 0
            if detected < 0:
                detected = 0

            item = ExerciseItem.objects.create(
                topic=topic,
                title=title,
                level=level,
                difficulty=difficulty,
                objective=objective,
                recommendation=(item_data.get("recommendation") or "").strip(),
                common_errors=(item_data.get("common_errors") or "").strip(),
                detected_exercise_count=detected,
                status="propuesto",
                learning_guide=None,  # nulo en Fase 1
            )

            # Recursos sugeridos: solo IDs válidos del tema y sin duplicados
            # (un ID repetido violaría unique_item_resource y abortaría todo).
            seen = set()
            for r_id in item_data.get("suggested_resource_ids") or []:
                try:
                    r_id_int = int(r_id)
                except (ValueError, TypeError):
                    continue
                if r_id_int in allowed_resource_ids and r_id_int not in seen:
                    seen.add(r_id_int)
                    ResourceExerciseItem.objects.create(
                        exercise_item=item,
                        resource_id=r_id_int,
                        practice_quota=0,
                        evaluation_quota=0,
                        order=0,
                    )

            created_items.append(item)

    ctx = _items_list_context(
        topic,
        success_msg=f"Se propusieron e ingresaron con éxito {len(created_items)} ítems de aprendizaje.",
    )
    return render(request, "partials/_items_list.html", ctx)


@user_passes_test(is_admin)
@require_http_methods(["GET", "POST"])
def edit_item_inline(request, item_id):
    """Ver el formulario o guardar los cambios editados de un ítem en línea (GET/POST)."""
    item = _get_enabled_item(item_id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        objective = request.POST.get("objective", "").strip()

        # Validación server-side de choices (no confiar solo en el <select>).
        try:
            level = int(request.POST.get("level", item.level))
        except (ValueError, TypeError):
            level = None
        difficulty = request.POST.get("difficulty", "")

        error = None
        if not title or not objective:
            error = "El título y el objetivo no pueden estar vacíos."
        elif level not in VALID_LEVELS:
            error = "Nivel no válido."
        elif difficulty not in VALID_DIFFICULTIES:
            error = "Dificultad no válida."

        if error:
            ctx = {
                "item": item,
                "LEVEL_CHOICES": Question.LEVEL_CHOICES,
                "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
                "error": error,
            }
            return render(request, "partials/_item_edit_row.html", ctx, status=400)

        try:
            detected = int(request.POST.get("detected_exercise_count", item.detected_exercise_count))
        except (ValueError, TypeError):
            detected = item.detected_exercise_count
        if detected < 0:
            detected = 0

        with transaction.atomic():
            item.title = title
            item.objective = objective
            item.level = level
            item.difficulty = difficulty
            item.recommendation = request.POST.get("recommendation", "").strip()
            item.common_errors = request.POST.get("common_errors", "").strip()
            item.detected_exercise_count = detected
            item.save()

        return render(request, "partials/_item_row.html", _item_row_context(item))

    # GET: cancelar vuelve a modo lectura; si no, abre el formulario de edición.
    if request.GET.get("cancel") == "true":
        return render(request, "partials/_item_row.html", _item_row_context(item))

    ctx = {
        "item": item,
        "LEVEL_CHOICES": Question.LEVEL_CHOICES,
        "DIFFICULTY_CHOICES": Question.DIFFICULTY_CHOICES,
    }
    return render(request, "partials/_item_edit_row.html", ctx)


@user_passes_test(is_admin)
@require_POST
def set_item_status(request, item_id):
    """Cambia el estado de un ítem a 'aprobado', 'archivado' o 'propuesto' (POST)."""
    item = _get_enabled_item(item_id)
    status = request.POST.get("status")

    if status not in ["aprobado", "archivado", "propuesto"]:
        return HttpResponse("Estado no válido", status=400)

    with transaction.atomic():
        item.status = status
        item.save()

    if status == "archivado":
        return HttpResponse("")  # desaparece del DOM

    return render(request, "partials/_item_row.html", _item_row_context(item))


@user_passes_test(is_admin)
@require_POST
def merge_items(request):
    """Fusiona ítems del MISMO tema (habilitado) en uno nuevo y archiva los orígenes."""
    item_ids_raw = request.POST.getlist("item_ids")
    if not item_ids_raw or len(item_ids_raw) < 2:
        return HttpResponse(
            '<div class="alert alert--danger mb-3">Debes seleccionar al menos 2 ítems para fusionar.</div>',
            status=400,
        )

    try:
        item_ids = [int(id_str) for id_str in item_ids_raw]
    except (ValueError, TypeError):
        return HttpResponse("IDs no válidos", status=400)

    items_to_merge = list(
        ExerciseItem.objects.filter(id__in=item_ids)
        .select_related("topic")
        .prefetch_related("resource_links")
    )
    if len(items_to_merge) < 2:
        return HttpResponse("No se encontraron suficientes ítems para fusionar", status=404)

    # No permitir mezclar ítems de temas distintos (corrompería asociaciones).
    topic_ids = {itm.topic_id for itm in items_to_merge}
    if len(topic_ids) != 1:
        return HttpResponse(
            '<div class="alert alert--danger mb-3">No se pueden fusionar ítems de temas distintos.</div>',
            status=400,
        )

    topic = items_to_merge[0].topic
    if not (topic.is_active and topic.structured_bank_enabled):
        return HttpResponse(
            '<div class="alert alert--danger mb-3">El tema no tiene el banco estandarizado habilitado.</div>',
            status=400,
        )

    merged_title = f"Fusión de {len(items_to_merge)} ítems: " + ", ".join(itm.title for itm in items_to_merge)
    if len(merged_title) > 200:
        merged_title = merged_title[:197] + "..."

    merged_level = max(itm.level for itm in items_to_merge)
    merged_difficulty = items_to_merge[0].difficulty
    merged_detected = sum(itm.detected_exercise_count for itm in items_to_merge)
    merged_objective = "\n---\n".join(f"De '{itm.title}': {itm.objective}" for itm in items_to_merge)
    merged_recommendation = "\n---\n".join(
        f"De '{itm.title}': {itm.recommendation}" for itm in items_to_merge if itm.recommendation
    )
    merged_errors = "\n---\n".join(
        f"De '{itm.title}': {itm.common_errors}" for itm in items_to_merge if itm.common_errors
    )

    with transaction.atomic():
        new_item = ExerciseItem.objects.create(
            topic=topic,
            title=merged_title,
            level=merged_level,
            difficulty=merged_difficulty,
            objective=merged_objective,
            recommendation=merged_recommendation,
            common_errors=merged_errors,
            detected_exercise_count=merged_detected,
            status="propuesto",
        )

        # Reasignar recursos sin duplicar (respeta unique_item_resource).
        merged_resources = set()
        for itm in items_to_merge:
            for link in itm.resource_links.all():
                merged_resources.add(link.resource_id)
        for res_id in merged_resources:
            ResourceExerciseItem.objects.create(
                exercise_item=new_item,
                resource_id=res_id,
                practice_quota=0,
                evaluation_quota=0,
                order=0,
            )

        ExerciseItem.objects.filter(id__in=item_ids).update(status="archivado")

    ctx = _items_list_context(
        topic,
        success_msg=f"Se fusionaron con éxito los ítems en el nuevo ítem ID {new_item.id}.",
    )
    return render(request, "partials/_items_list.html", ctx)


@user_passes_test(is_admin)
@require_POST
def link_item_resource(request, item_id):
    """Vincula un recurso del tema a un ítem de aprendizaje (POST)."""
    item = _get_enabled_item(item_id)
    resource_id = request.POST.get("resource_id")
    if not resource_id:
        return HttpResponse("Falta resource_id", status=400)

    try:
        res_id_int = int(resource_id)
    except (ValueError, TypeError):
        return HttpResponse("ID de recurso no válido", status=400)

    if not Resource.objects.filter(id=res_id_int, topic=item.topic).exists():
        return HttpResponse("El recurso no pertenece al tema del ítem", status=400)

    with transaction.atomic():
        ResourceExerciseItem.objects.get_or_create(
            exercise_item=item,
            resource_id=res_id_int,
            defaults={"practice_quota": 0, "evaluation_quota": 0, "order": 0},
        )

    return render(request, "partials/_item_row.html", _item_row_context(item))


@user_passes_test(is_admin)
@require_POST
def unlink_item_resource(request, item_id):
    """Desvincula un recurso de un ítem de aprendizaje (POST)."""
    item = _get_enabled_item(item_id)
    resource_id = request.POST.get("resource_id")
    if not resource_id:
        return HttpResponse("Falta resource_id", status=400)

    try:
        res_id_int = int(resource_id)
    except (ValueError, TypeError):
        return HttpResponse("ID de recurso no válido", status=400)

    with transaction.atomic():
        ResourceExerciseItem.objects.filter(
            exercise_item=item, resource_id=res_id_int
        ).delete()

    return render(request, "partials/_item_row.html", _item_row_context(item))
