from django.conf import settings
from django.core.checks import Warning, register

@register()
def cache_backend_check(app_configs, **kwargs):
    if settings.DEBUG:
        return []
    from django.core.cache import caches
    from django.core.cache.backends.locmem import LocMemCache
    if isinstance(caches["default"], LocMemCache):
        return [Warning(
            "Producción sin cache compartida (LocMemCache): el rate-limit del webhook es por-worker.",
            hint="Definir REDIS_URL en el entorno para usar RedisCache.",
            id="core.W001",
        )]
    return []
