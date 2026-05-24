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


# Database Configuration (PostgreSQL/SQLite hybrid)
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
    # Supabase generally requires SSL. We check if the provider is postgresql to apply SSL.
    if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
        DATABASES["default"]["OPTIONS"] = {"sslmode": "require"}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

