import json
import logging
import os
import secrets

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from apps.content.models import Level, Resource, Subject, Topic
from apps.core.ratelimit import get_client_ip, is_rate_limited, increment_rate_limit

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


@csrf_exempt
@require_POST
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
    subject_slug = data.get("subject_slug")
    topic_slug = data.get("topic_slug")
    level_slugs = data.get("level_slugs", [])
    is_published_provided = "is_published" in data
    is_published = data.get("is_published", False)

    if not title or not video_url:
        return JsonResponse(
            {"ok": False, "error": "Faltan parametros requeridos: title y video_url"},
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
            subject=subject,
            topic=topic,
            is_published=is_published,
        )
        resource.save()
    else:
        resource.title = title
        if description:
            resource.description = description
        if content:
            resource.content = content
        if subject:
            resource.subject = subject
        if topic:
            resource.topic = topic
        # Solo cambia el estado de publicación si se envía explícitamente,
        # para no despublicar recursos al re-procesar una subida.
        if is_published_provided:
            resource.is_published = is_published
        resource.save()

    if level_slugs:
        levels = Level.objects.filter(slug__in=level_slugs, is_active=True)
        if levels.exists():
            resource.levels.set(levels)

    resource_path = reverse("content:resource_detail", kwargs={"slug": resource.slug})
    absolute_url = request.build_absolute_uri(resource_path)

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "resource_id": resource.id,
            "slug": resource.slug,
            "url": absolute_url,
        },
        status=201 if created else 200,
    )
