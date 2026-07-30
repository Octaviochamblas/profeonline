import hashlib
import json
import logging
import os
import re
import secrets

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from apps.content.models import (
    Choice,
    EvaluationSessionAnswer,
    Level,
    NodeAssessmentAnswer,
    PublicationItem,
    Question,
    QuestionErrorReport,
    QuizAttemptAnswer,
    Resource,
    Subject,
    Topic,
)
from apps.core.ratelimit import get_client_ip, is_rate_limited, increment_rate_limit
from apps.content.services.publication_pipeline_service import (
    PipelineError,
    apply_content_package,
    apply_editorial_package,
    apply_question_package,
    finalize_publication,
    validate_editorial_content,
    validate_editorial_package,
)
from apps.content.services.editorial_asset_service import upload_concept_image, upload_infographic
from apps.content.services.editorial_guide_service import (
    insert_concept_image_after_explanations,
    insert_infographic_before_closing,
    validate_closing,
    validate_guide_structure,
)

logger = logging.getLogger(__name__)


def _rate_limit_config():
    return (
        getattr(settings, "VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS", 10),
        getattr(settings, "VIDEO_WEBHOOK_RATE_LIMIT_WINDOW", 300),
    )


def _is_rate_limited(request):
    max_attempts, _window = _rate_limit_config()
    return is_rate_limited(request, "video_webhook_failures", max_attempts)


def _record_failed_attempt(request, reason):
    max_attempts, window = _rate_limit_config()
    attempts = increment_rate_limit(request, "video_webhook_failures", max_attempts, window)

    logger.warning(
        "Rejected video webhook request",
        extra={
            "client": get_client_ip(request),
            "reason": reason,
            "attempts": attempts,
            "max_attempts": max_attempts,
        },
    )


def _reject(request, message, status, reason):
    _record_failed_attempt(request, reason)
    return JsonResponse({"ok": False, "error": message}, status=status)


def _has_valid_api_token(request):
    expected_token = os.environ.get("API_SECRET_TOKEN")
    if not expected_token or expected_token == "default_secret_token_change_me":
        return False
    token = request.headers.get("X-Api-Token") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
    return bool(token and secrets.compare_digest(token, expected_token))


@csrf_exempt
@require_POST
@transaction.atomic
def create_resource_from_video(request):
    if _is_rate_limited(request):
        logger.warning(
            "Rate limited video webhook request",
            extra={"client": get_client_ip(request)},
        )
        return JsonResponse({"ok": False, "error": "Demasiados intentos"}, status=429)

    expected_token = os.environ.get("API_SECRET_TOKEN")
    if not expected_token or expected_token == "default_secret_token_change_me":
        return _reject(
            request,
            "Token de seguridad no configurado en el servidor",
            500,
            "missing_or_default_token",
        )

    token = request.headers.get("X-Api-Token") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]

    if not token or not secrets.compare_digest(token, expected_token):
        return _reject(request, "No autorizado", 401, "invalid_token")

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return _reject(request, "JSON invalido", 400, "invalid_json")

    title = data.get("title")
    video_url = data.get("video_url")
    description = data.get("description", "")
    content = data.get("content", "")
    transcript = data.get("transcript", "")
    subject_slug = data.get("subject_slug")
    topic_slug = data.get("topic_slug")
    level_slugs = data.get("level_slugs", [])
    batch_id = str(data.get("batch_id", "")).strip()
    source_filename = str(data.get("source_filename", "")).strip()
    taxonomy = data.get("taxonomy") if isinstance(data.get("taxonomy"), dict) else {}
    instructions = str(data.get("instructions", "")).strip()
    target_counts = data.get("target_counts") if isinstance(data.get("target_counts"), dict) else {}
    youtube_privacy = str(data.get("youtube_privacy", "unlisted")).strip() or "unlisted"
    is_published_provided = "is_published" in data
    is_published = data.get("is_published", False)
    if batch_id:
        # El pipeline siempre ingresa en borrador. La publicación ocurre solo al
        # completar guía, metadatos y auditoría de preguntas. Si el recurso ya
        # existía y estaba publicado, conserva su versión vigente hasta el cierre.
        is_published = False
        is_published_provided = False
    order_provided = "order" in data
    resource_order = 0

    if not title or not video_url:
        return JsonResponse(
            {"ok": False, "error": "Faltan parametros requeridos: title y video_url"},
            status=400,
        )
    if batch_id and not source_filename:
        return JsonResponse(
            {"ok": False, "error": "source_filename es obligatorio cuando se envía batch_id"},
            status=400,
        )

    if order_provided:
        try:
            resource_order = int(data.get("order") or 0)
        except (TypeError, ValueError):
            return JsonResponse(
                {"ok": False, "error": "El orden del recurso debe ser un numero entero"},
                status=400,
            )

    from apps.content.views.resource_detail import get_youtube_id
    youtube_id = get_youtube_id(video_url)
    if not youtube_id:
        return JsonResponse(
            {"ok": False, "error": "La URL del video debe ser un enlace valido de YouTube"},
            status=400,
        )


    subject = None
    if subject_slug:
        subject = Subject.objects.filter(slug=subject_slug, is_active=True).first()
        if not subject:
            subject = Subject.objects.filter(slug__iexact=subject_slug).first()
        if not subject:
            return JsonResponse(
                {"ok": False, "error": "La asignatura indicada no existe"},
                status=400,
            )

    topic = None
    if topic_slug:
        topic_queryset = Topic.objects.filter(slug=topic_slug, is_active=True)
        if subject:
            topic_queryset = topic_queryset.filter(subject=subject)
        topic = topic_queryset.first()
        if not topic:
            return JsonResponse(
                {
                    "ok": False,
                    "error": "El tema indicado no existe o no pertenece a la asignatura indicada",
                },
                status=400,
            )
        if not subject:
            subject = topic.subject

    # Deduplica por ID de YouTube (no por URL literal): así youtu.be/X,
    # youtube.com/watch?v=X y /embed/X se reconocen como el mismo video y no
    # se crean recursos duplicados. El filtro icontains acota y get_youtube_id
    # confirma la coincidencia exacta del ID.
    resource = next(
        (
            candidate
            for candidate in Resource.objects.filter(video_url__icontains=youtube_id)
            if get_youtube_id(candidate.video_url) == youtube_id
        ),
        None,
    )
    created = resource is None

    if created:
        resource = Resource(
            title=title,
            video_url=video_url,
            description=description,
            content=content,
            transcript=transcript,
            subject=subject,
            topic=topic,
            is_published=is_published,
            order=resource_order,
        )
        resource.save()
    else:
        if not batch_id:
            resource.title = title
            if description:
                resource.description = description
            if content:
                resource.content = content
        # El transcript suele llegar en una llamada posterior (los subtitulos de
        # YouTube tardan en estar listos). Solo se actualiza si viene con contenido.
        if transcript:
            resource.transcript = transcript
        if subject and not batch_id:
            resource.subject = subject
        if topic and not batch_id:
            resource.topic = topic
        # Solo cambia el estado de publicación si se envía explícitamente,
        # para no despublicar recursos al re-procesar una subida.
        if is_published_provided:
            resource.is_published = is_published
        if order_provided:
            resource.order = resource_order
        resource.save()

    if level_slugs:
        levels = Level.objects.filter(slug__in=level_slugs, is_active=True)
        if levels.exists():
            resource.levels.set(levels)

    publication_item = None
    if batch_id:
        publication_item, _ = PublicationItem.objects.update_or_create(
            batch_id=batch_id,
            source_filename=source_filename,
            defaults={
                "youtube_video_id": youtube_id,
                "youtube_url": video_url,
                "youtube_privacy": youtube_privacy,
                "resource": resource,
                "taxonomy": taxonomy or {
                    "subject_slug": subject_slug or "",
                    "topic_slug": topic_slug or "",
                },
                "instructions": instructions,
                "target_counts": target_counts,
            },
        )
        if transcript and publication_item.state in {
            PublicationItem.STATE_TRANSCRIPT_PENDING,
            PublicationItem.STATE_FAILED,
        }:
            publication_item.state = PublicationItem.STATE_UPLOADED
            publication_item.last_error = ""
            publication_item.save(update_fields=["state", "last_error", "updated_at"])

    resource_path = reverse("content:resource_detail", kwargs={"slug": resource.slug})
    absolute_url = request.build_absolute_uri(resource_path)

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "resource_id": resource.id,
            "slug": resource.slug,
            "url": absolute_url,
            "publication_item_id": publication_item.id if publication_item else None,
            "publication_state": publication_item.state if publication_item else None,
        },
        status=201 if created else 200,
    )


@require_GET
def publication_item_status(request, item_id):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    item = PublicationItem.objects.select_related("resource", "canonical_guide").filter(id=item_id).first()
    if item is None:
        return JsonResponse({"ok": False, "error": "Ítem no encontrado"}, status=404)
    return JsonResponse({
        "ok": True,
        "id": item.id,
        "state": item.state,
        "last_error": item.last_error,
        "youtube_privacy": item.youtube_privacy,
        "infographic_ready": bool(item.resource and item.resource.infographic_key),
        "metadata": item.metadata if item.state in {
            PublicationItem.STATE_METADATA_READY,
            PublicationItem.STATE_QUESTIONS_READY,
            PublicationItem.STATE_PUBLISHED,
        } else {},
    })


@csrf_exempt
@require_POST
@transaction.atomic
def publication_item_editorial_package(request, item_id):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    item = PublicationItem.objects.filter(id=item_id).first()
    if item is None:
        return JsonResponse({"ok": False, "error": "Ítem no encontrado"}, status=404)
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)
    stage = data.get("stage")
    try:
        if stage == "content":
            item = apply_content_package(item, data)
        elif stage == "questions":
            item = apply_question_package(item, data)
        elif stage in (None, "full"):
            item = apply_editorial_package(item, data)
        else:
            raise PipelineError("Etapa editorial inválida.")
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    return JsonResponse(
        {
            "ok": True,
            "state": item.state,
            "resource_id": item.resource_id,
            "question_count": item.questions.count(),
        }
    )


def _store_infographic_for_resource(resource, uploaded_file, alt_text):
    try:
        upload_infographic(resource, uploaded_file, alt_text)
        item = (
            PublicationItem.objects.select_for_update()
            .filter(resource=resource)
            .order_by("-updated_at")
            .first()
        )
        if item and item.canonical_guide_id:
            guide = item.canonical_guide
            guide.content_text = insert_infographic_before_closing(guide.content_text, resource)
            guide.save(update_fields=["content_text", "updated_at"])
            resource.content = guide.content_text
            resource.save(update_fields=["content"])
        else:
            resource.content = insert_infographic_before_closing(resource.content, resource)
            resource.save(update_fields=["content"])
    except (ValueError, ValidationError, ImproperlyConfigured) as exc:
        raise PipelineError(str(exc)) from exc


def _store_concept_image_for_resource(resource, uploaded_file, alt_text):
    try:
        upload_concept_image(resource, uploaded_file, alt_text)
        item = (
            PublicationItem.objects.select_for_update()
            .filter(resource=resource)
            .order_by("-updated_at")
            .first()
        )
        if item and item.canonical_guide_id:
            guide = item.canonical_guide
            guide.content_text = insert_concept_image_after_explanations(
                guide.content_text,
                resource,
            )
            guide.save(update_fields=["content_text", "updated_at"])
            resource.content = guide.content_text
            resource.save(update_fields=["content"])
        else:
            resource.content = insert_concept_image_after_explanations(
                resource.content,
                resource,
            )
            resource.save(update_fields=["content"])
    except (ValueError, ValidationError, ImproperlyConfigured) as exc:
        raise PipelineError(str(exc)) from exc


@csrf_exempt
@require_POST
@transaction.atomic
def upload_publication_infographic(request, item_id):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    item = PublicationItem.objects.select_for_update().select_related("resource").filter(id=item_id).first()
    if item is None or item.resource is None:
        return JsonResponse({"ok": False, "error": "Ítem o recurso no encontrado"}, status=404)
    image = request.FILES.get("image")
    if image is None:
        return JsonResponse({"ok": False, "error": "Falta el archivo de infografía"}, status=400)
    try:
        _store_infographic_for_resource(item.resource, image, request.POST.get("alt_text", ""))
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    return JsonResponse({"ok": True, "resource_id": item.resource_id, "infographic_ready": True})


@csrf_exempt
@require_POST
@transaction.atomic
def upload_resource_infographic(request, resource_id=None, slug=None):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    lookup = {"id": resource_id} if resource_id is not None else {"slug": slug}
    resource = Resource.objects.select_for_update().filter(**lookup).first()
    if resource is None:
        return JsonResponse({"ok": False, "error": "Recurso no encontrado"}, status=404)
    image = request.FILES.get("image")
    if image is None:
        return JsonResponse({"ok": False, "error": "Falta el archivo de infografía"}, status=400)
    try:
        _store_infographic_for_resource(resource, image, request.POST.get("alt_text", ""))
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    return JsonResponse({"ok": True, "resource_id": resource.id, "infographic_ready": True})


@csrf_exempt
@require_POST
@transaction.atomic
def upload_publication_concept_image(request, item_id):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    item = PublicationItem.objects.select_for_update().select_related("resource").filter(id=item_id).first()
    if item is None or item.resource is None:
        return JsonResponse({"ok": False, "error": "Ítem o recurso no encontrado"}, status=404)
    image = request.FILES.get("image")
    if image is None:
        return JsonResponse({"ok": False, "error": "Falta la imagen conceptual"}, status=400)
    try:
        _store_concept_image_for_resource(item.resource, image, request.POST.get("alt_text", ""))
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    return JsonResponse({"ok": True, "resource_id": item.resource_id, "concept_image_ready": True})


@csrf_exempt
@require_POST
@transaction.atomic
def upload_resource_concept_image(request, resource_id=None, slug=None):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    lookup = {"id": resource_id} if resource_id is not None else {"slug": slug}
    resource = Resource.objects.select_for_update().filter(**lookup).first()
    if resource is None:
        return JsonResponse({"ok": False, "error": "Recurso no encontrado"}, status=404)
    image = request.FILES.get("image")
    if image is None:
        return JsonResponse({"ok": False, "error": "Falta la imagen conceptual"}, status=400)
    try:
        _store_concept_image_for_resource(resource, image, request.POST.get("alt_text", ""))
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    return JsonResponse({"ok": True, "resource_id": resource.id, "concept_image_ready": True})


def _direct_resource_history(resource):
    counts = {
        "QuizAttemptAnswer": QuizAttemptAnswer.objects.filter(
            question__resource=resource
        ).count(),
        "QuestionErrorReport": QuestionErrorReport.objects.filter(
            question__resource=resource
        ).count(),
        "EvaluationSessionAnswer": EvaluationSessionAnswer.objects.filter(
            question__resource=resource
        ).count(),
        "NodeAssessmentAnswer": 0,
    }
    if resource.related_node_id:
        counts["NodeAssessmentAnswer"] = NodeAssessmentAnswer.objects.filter(
            question__node_id=resource.related_node_id
        ).count()
    return counts


@csrf_exempt
@require_POST
@transaction.atomic
def refresh_direct_resource_editorial(request, slug):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    resource = Resource.objects.select_for_update().filter(slug=slug).first()
    if resource is None:
        return JsonResponse({"ok": False, "error": "Recurso no encontrado"}, status=404)
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON invalido"}, status=400)

    metadata = dict(payload.get("metadata") or {})
    description = str(metadata.get("resource_description") or resource.description or resource.title)
    metadata.setdefault("resource_title", resource.title)
    metadata.setdefault("youtube_title", resource.title)
    metadata.setdefault("resource_description", description)
    metadata.setdefault("youtube_description", description)
    metadata.setdefault("introduction", description)
    metadata.setdefault("guide_title", f"Guia: {resource.title}")
    metadata.setdefault("pedagogical_document", description)
    payload["metadata"] = metadata
    replace_questions = payload.get("replace_questions", True) is not False
    try:
        package = (
            validate_editorial_package(payload)
            if replace_questions
            else validate_editorial_content(payload)
        )
        validate_guide_structure(package["guide"]["content"])
        validate_closing(package["guide"]["content"])
    except (PipelineError, ValueError) as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)

    history = _direct_resource_history(resource)
    blocked = {name: count for name, count in history.items() if count}
    if replace_questions and blocked:
        return JsonResponse(
            {
                "ok": False,
                "error": "El recurso tiene historial y no permite reemplazar preguntas.",
                "history": blocked,
            },
            status=409,
        )

    content = package["guide"]["content"]
    if resource.concept_image_key:
        content = insert_concept_image_after_explanations(content, resource)
    if resource.infographic_key:
        content = insert_infographic_before_closing(content, resource)

    if payload.get("dry_run") is True:
        return JsonResponse(
            {
                "ok": True,
                "dry_run": True,
                "resource_id": resource.id,
                "questions": "would_replace" if replace_questions else "preserved",
                "reading_checkpoints": len(package["guide"].get("checkpoints", resource.reading_checkpoints)),
                "concept_image": bool(resource.concept_image_key),
                "infographic": bool(resource.infographic_key),
                "history": history,
            }
        )

    publication_item = (
        PublicationItem.objects.select_for_update()
        .filter(resource=resource)
        .order_by("-updated_at")
        .first()
    )
    if publication_item and publication_item.canonical_guide_id:
        guide = publication_item.canonical_guide
        guide.title = package["metadata"]["guide_title"][:200]
        guide.description = package["metadata"]["resource_description"][:300]
        guide.content_text = content
        guide.canonical_resource = resource
        guide.save(
            update_fields=[
                "title",
                "description",
                "content_text",
                "canonical_resource",
                "updated_at",
            ]
        )
        publication_item.metadata = {
            **(publication_item.metadata or {}),
            **package["metadata"],
        }
        publication_item.save(update_fields=["metadata", "updated_at"])

    created_questions = []
    if replace_questions:
        Question.objects.filter(resource=resource).delete()
        created_questions = Question.objects.bulk_create(
            [
                Question(
                    resource=resource,
                    level=item["level"],
                    mode="ambas",
                    text=item["text"],
                    explanation=item["explanation"],
                    status="publicada",
                    order=order,
                    generation_key=hashlib.sha256(
                        f"{resource.slug}:{item['level']}:{item['text']}".encode("utf-8")
                    ).hexdigest(),
                    audit_data={
                        "accepted": True,
                        "source": "direct_resource_editorial_api",
                        "cognitive_type": item["cognitive_type"],
                    },
                )
                for order, item in enumerate(package["questions"], start=1)
            ]
        )
        Choice.objects.bulk_create(
            [
                Choice(
                    question=question,
                    text=choice["text"],
                    is_correct=choice["is_correct"],
                    order=choice_order,
                )
                for question, item in zip(
                    created_questions,
                    package["questions"],
                    strict=True,
                )
                for choice_order, choice in enumerate(item["choices"], start=1)
            ]
        )
    resource.title = package["metadata"]["resource_title"]
    resource.content = content
    resource.description = package["metadata"]["resource_description"]
    update_fields = ["title", "content", "description"]
    if "checkpoints" in package["guide"]:
        resource.reading_checkpoints = package["guide"]["checkpoints"]
        update_fields.append("reading_checkpoints")
    resource.save(update_fields=update_fields)
    return JsonResponse(
        {
            "ok": True,
            "resource_id": resource.id,
            "questions": len(created_questions) if replace_questions else "preserved",
            "reading_checkpoints": len(resource.reading_checkpoints),
            "history": history,
        }
    )


_MATH_SPAN = re.compile(r"\$(?!\$)([^$\n]+)\$(?!\$)")
_BARE_KATEX = re.compile(r"(?<!\\)\b(leq|geq|ldots|neq|square|circ|mathrm)\b")
_PROSE_IN_MATH = re.compile(r"\b(y|o|otra|saldo|cuenta|tiene)\b", re.IGNORECASE)


def _repair_editorial_text(value):
    def repair_span(match):
        body = _BARE_KATEX.sub(lambda item: "\\" + item.group(1), match.group(1))
        if any(character.isspace() for character in body) and _PROSE_IN_MATH.search(body):
            return body
        return f"${body}$"

    return _MATH_SPAN.sub(repair_span, value or "")


@csrf_exempt
@require_POST
@transaction.atomic
def repair_direct_resource_editorial_text(request, slug):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    resource = Resource.objects.select_for_update().filter(slug=slug).first()
    if resource is None:
        return JsonResponse({"ok": False, "error": "Recurso no encontrado"}, status=404)

    changed = {"content": 0, "questions": 0, "choices": 0}
    repaired_content = _repair_editorial_text(resource.content)
    if repaired_content != resource.content:
        resource.content = repaired_content
        resource.save(update_fields=["content"])
        changed["content"] = 1

    for question in Question.objects.filter(resource=resource).prefetch_related("choices"):
        repaired_text = _repair_editorial_text(question.text)
        repaired_explanation = _repair_editorial_text(question.explanation)
        update_fields = []
        if repaired_text != question.text:
            question.text = repaired_text
            update_fields.append("text")
        if repaired_explanation != question.explanation:
            question.explanation = repaired_explanation
            update_fields.append("explanation")
        if update_fields:
            question.save(update_fields=update_fields)
            changed["questions"] += 1
        for choice in question.choices.all():
            repaired_choice = _repair_editorial_text(choice.text)
            if repaired_choice != choice.text:
                choice.text = repaired_choice
                choice.save(update_fields=["text"])
                changed["choices"] += 1

    return JsonResponse({"ok": True, "resource_id": resource.id, "changed": changed})


@csrf_exempt
@require_POST
@transaction.atomic
def confirm_publication_item(request, item_id):
    if not _has_valid_api_token(request):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
    item = PublicationItem.objects.select_for_update().filter(id=item_id).first()
    if item is None:
        return JsonResponse({"ok": False, "error": "Ítem no encontrado"}, status=404)
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)
    if data.get("youtube_privacy") != "public":
        return JsonResponse(
            {"ok": False, "error": "Se requiere confirmación explícita de YouTube público"},
            status=400,
        )
    item.youtube_privacy = "public"
    try:
        finalize_publication(item)
    except PipelineError as exc:
        return JsonResponse({"ok": False, "error": str(exc)}, status=409)
    item.save(update_fields=["youtube_privacy", "updated_at"])
    return JsonResponse({"ok": True, "state": item.state, "resource_id": item.resource_id})
