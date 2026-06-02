import os
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Muestra información de diagnóstico del entorno actual sin exponer credenciales sensibles."

    def handle(self, *args, **options):
        self.stdout.write("=== Diagnóstico del Entorno ===")
        self.stdout.write(f"DEBUG: {settings.DEBUG}")

        # Sentry
        sentry_env = os.environ.get("SENTRY_ENVIRONMENT", "no definido (default: production en production.py)")
        self.stdout.write(f"SENTRY_ENVIRONMENT: {sentry_env}")

        # Base de datos
        db_config = settings.DATABASES["default"]
        db_engine = db_config["ENGINE"]
        db_name = db_config["NAME"]
        db_host = db_config.get("HOST", "localhost/empty (default)")
        self.stdout.write(f"DB Engine: {db_engine}")
        self.stdout.write(f"DB Host: {db_host}")
        self.stdout.write(f"DB Name: {db_name}")

        # Cache
        cache_config = settings.CACHES.get("default", {})
        cache_backend = cache_config.get("BACKEND", "LocMemCache (default)")
        self.stdout.write(f"Cache Backend: {cache_backend}")

        # URLs y Hosts
        self.stdout.write(f"Canonical Base URL: {getattr(settings, 'CANONICAL_BASE_URL', 'no definida')}")
        self.stdout.write(f"Allowed Hosts: {settings.ALLOWED_HOSTS}")
        self.stdout.write(f"CSRF Trusted Origins: {getattr(settings, 'CSRF_TRUSTED_ORIGINS', 'no definido')}")

        # Comprobar si parece producción o staging
        if settings.DEBUG:
            self.stdout.write(self.style.SUCCESS("Entorno detectado: DESARROLLO (DEBUG=True)"))
        else:
            is_remote_db = db_host not in ["", "localhost", "127.0.0.1", "db"]
            # Indicios de staging
            host_str = "".join(settings.ALLOWED_HOSTS)
            if sentry_env == "staging" or "staging" in db_host or "staging" in host_str:
                self.stdout.write(self.style.WARNING("Entorno detectado: STAGING (DEBUG=False, indicios de staging)"))
            elif is_remote_db:
                self.stdout.write(self.style.NOTICE("Entorno detectado: PRODUCCIÓN (DEBUG=False, DB remota)"))
            else:
                self.stdout.write(self.style.NOTICE("Entorno detectado: PRODUCCIÓN LOCAL/CONTENEDOR (DEBUG=False, DB local)"))
