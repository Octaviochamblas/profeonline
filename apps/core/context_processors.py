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


def csp_nonce(request):
    return {"csp_nonce": getattr(request, "csp_nonce", "")}


def google_login(request):
    enabled = bool(
        getattr(settings, "GOOGLE_CLIENT_ID", "")
        and getattr(settings, "GOOGLE_CLIENT_SECRET", "")
    )
    return {"GOOGLE_LOGIN_ENABLED": enabled}
