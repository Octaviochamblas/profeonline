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

from apps.content.models import Level, Resource, Subject

logger = logging.getLogger(__name__)


def _client_identifier(request):
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip() or "unknown"
    return request.META.get("REMOTE_ADDR", "unknown") or "unknown"


def _rate_limit_config():
    return (
        getattr(settings, "VIDEO_WEBHOOK_RATE_LIMIT_ATTEMPTS", 10),
        getattr(settings, "VIDEO_WEBHOOK_RATE_LIMIT_WINDOW", 300),
    )


def _rate_limit_key(request):
    return f"video_webhook_failures:{_client_identifier(request)}"


def _is_rate_limited(request):
    max_attempts, _window = _rate_limit_config()
    return cache.get(_rate_limit_key(request), 0) >= max_attempts


def _record_failed_attempt(request, reason):
    max_attempts, window = _rate_limit_config()
    key = _rate_limit_key(request)

    if cache.add(key, 1, timeout=window):
        attempts = 1
    else:
        try:
            attempts = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=window)
            attempts = 1

    logger.warning(
        "Rejected video webhook request",
        extra={
            "client": _client_identifier(request),
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
            extra={"client": _client_identifier(request)},
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
    level_slugs = data.get("level_slugs", [])
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

    resource, created = Resource.objects.get_or_create(
        video_url=video_url,
        defaults={
            "title": title,
            "description": description,
            "content": content,
            "subject": subject,
            "is_published": is_published,
        },
    )

    if not created:
        resource.title = title
        if description:
            resource.description = description
        if content:
            resource.content = content
        if subject:
            resource.subject = subject
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
