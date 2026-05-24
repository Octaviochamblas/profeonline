import json
import os
import secrets
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from apps.content.models import Resource, Subject, Level

@csrf_exempt
@require_POST
def create_resource_from_video(request):
    # Verify Token
    expected_token = os.environ.get("API_SECRET_TOKEN")
    if not expected_token or expected_token == "default_secret_token_change_me":
        return JsonResponse({"ok": False, "error": "Token de seguridad no configurado en el servidor"}, status=500)
    
    # Check token only in headers
    token = request.headers.get("X-Api-Token") or request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]
        
    if not token or not secrets.compare_digest(token, expected_token):
        return JsonResponse({"ok": False, "error": "No autorizado"}, status=401)
        
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "JSON inválido"}, status=400)
        
    title = data.get("title")
    video_url = data.get("video_url")
    description = data.get("description", "")
    content = data.get("content", "")
    subject_slug = data.get("subject_slug")
    level_slugs = data.get("level_slugs", [])
    is_published = data.get("is_published", False)

    
    if not title or not video_url:
        return JsonResponse({"ok": False, "error": "Faltan parámetros requeridos: title y video_url"}, status=400)
        
    # Find subject by slug if provided
    subject = None
    if subject_slug:
        subject = Subject.objects.filter(slug=subject_slug, is_active=True).first()
        if not subject:
            # Fallback to search by name or case-insensitive slug
            subject = Subject.objects.filter(slug__iexact=subject_slug).first()
            
    # Get or create the Resource
    resource, created = Resource.objects.get_or_create(
        video_url=video_url,
        defaults={
            "title": title,
            "description": description,
            "content": content,
            "subject": subject,
            "is_published": is_published,
        }
    )
    
    if not created:
        # Update existing resource if needed
        resource.title = title
        if description:
            resource.description = description
        if content:
            resource.content = content
        if subject:
            resource.subject = subject
        resource.is_published = is_published
        resource.save()
        
    # Associate levels if provided
    if level_slugs:
        levels = Level.objects.filter(slug__in=level_slugs, is_active=True)
        if levels.exists():
            resource.levels.set(levels)
            
    resource_path = reverse("content:resource_detail", kwargs={"slug": resource.slug})
    absolute_url = request.build_absolute_uri(resource_path)
    
    return JsonResponse({
        "ok": True,
        "created": created,
        "resource_id": resource.id,
        "slug": resource.slug,
        "url": absolute_url
    }, status=201 if created else 200)
