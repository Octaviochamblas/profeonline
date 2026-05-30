from urllib.parse import urlparse

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Sincroniza el dominio del framework Sites con CANONICAL_BASE_URL. "
        "Es necesario para que los enlaces de los correos (p. ej. el reset de "
        "contraseña) apunten al dominio real y no a 'example.com'."
    )

    def handle(self, *args, **options):
        base_url = getattr(settings, "CANONICAL_BASE_URL", "") or ""
        host = urlparse(base_url).netloc or "www.profeonline.cl"
        site_id = getattr(settings, "SITE_ID", 1)

        site, created = Site.objects.update_or_create(
            pk=site_id,
            defaults={"domain": host, "name": "ProfeOnline"},
        )

        verb = "creado" if created else "actualizado"
        self.stdout.write(
            self.style.SUCCESS(f"Site '{site.name}' {verb} con dominio '{site.domain}'.")
        )
