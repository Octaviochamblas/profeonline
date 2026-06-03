import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """
    Resuelve la IP real del cliente leyendo X-Forwarded-For (primer valor)
    con un fallback a REMOTE_ADDR.
    """
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip() or "unknown"
    return request.META.get("REMOTE_ADDR", "unknown") or "unknown"

def is_rate_limited(request, key_prefix, max_attempts):
    """
    Verifica si la IP del cliente ya superó el número máximo de intentos configurado.
    """
    ip = get_client_ip(request)
    key = f"{key_prefix}:{ip}"
    return cache.get(key, 0) >= max_attempts

def increment_rate_limit(request, key_prefix, max_attempts, window):
    """
    Incrementa el contador de la caché para la IP del cliente y retorna el total actual.
    """
    ip = get_client_ip(request)
    key = f"{key_prefix}:{ip}"

    if cache.add(key, 1, timeout=window):
        attempts = 1
    else:
        try:
            attempts = cache.incr(key)
        except ValueError:
            cache.set(key, 1, timeout=window)
            attempts = 1

    return attempts
