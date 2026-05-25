from django.conf import settings


def canonical_settings(request):
    host = request.get_host()
    if settings.DEBUG or "testserver" in host:
        base_url = f"{request.scheme}://{host}"
    else:
        base_url = getattr(settings, "CANONICAL_BASE_URL", "https://www.profeonline.cl")

    return {
        "CANONICAL_BASE_URL": base_url
    }
