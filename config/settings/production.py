import os
import dj_database_url

from django.core.exceptions import ImproperlyConfigured

from .base import *


def get_env(name):
    value = os.environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value


def get_env_list(name, required=False):
    value = os.environ.get(name, "")
    values = [item.strip() for item in value.split(",") if item.strip()]

    if required and not values:
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")

    return values


def get_env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default

    return value.lower() in {"1", "true", "yes", "on"}


DEBUG = False

SECRET_KEY = get_env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = get_env_list("DJANGO_ALLOWED_HOSTS", required=True)
CSRF_TRUSTED_ORIGINS = get_env_list("DJANGO_CSRF_TRUSTED_ORIGINS")

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = get_env_bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SECURE_HSTS_SECONDS = int(os.environ.get("DJANGO_SECURE_HSTS_SECONDS", "31536000"))
SECURE_HSTS_INCLUDE_SUBDOMAINS = get_env_bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=False,
)
SECURE_HSTS_PRELOAD = get_env_bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)

if get_env_bool("DJANGO_USE_X_FORWARDED_PROTO", default=False):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Referrer Policy
SECURE_REFERRER_POLICY = "same-origin"

# Canonical base URL for SEO
CANONICAL_BASE_URL = os.environ.get("CANONICAL_BASE_URL", "https://www.profeonline.cl")


# Database Configuration
# DATABASE_URL es obligatorio en producción: el fallback silencioso a SQLite
# en hosts efímeros (Railway/nixpacks) provoca pérdida de datos en cada deploy.
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL es obligatorio en producción. "
        "Sin él la app caería en una base SQLite efímera que se pierde en cada deploy."
    )

DATABASES = {
    "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}
# Supabase generally requires SSL. We check if the provider is postgresql to apply SSL.
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Email Configuration
# Si EMAIL_HOST está definido se usa SMTP real (necesario para reset de
# contraseña y verificación de email). Si no, se mantiene el backend de
# consola heredado de base.py para no romper el arranque, pero los correos
# NO se entregan.
EMAIL_HOST = os.environ.get("EMAIL_HOST")
if EMAIL_HOST:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = get_env_bool("EMAIL_USE_TLS", default=True)
    EMAIL_USE_SSL = get_env_bool("EMAIL_USE_SSL", default=False)
    DEFAULT_FROM_EMAIL = os.environ.get(
        "DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "no-reply@profeonline.cl"
    )
    SERVER_EMAIL = DEFAULT_FROM_EMAIL


# Logging
# Con DEBUG=False, Django no imprime los tracebacks por defecto (los enruta a
# 'mail_admins'). Enviamos errores y registros a stdout para que queden
# visibles en los logs del proveedor (Railway).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}


# Redis Cache Configuration (For shared cache, rate limiting, and performance PEND-009)
REDIS_URL = os.environ.get("REDIS_URL")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }
