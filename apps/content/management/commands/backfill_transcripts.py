"""Baja transcripciones de YouTube y las guarda en los recursos (FASE 2).

Pensado para correr **desde el PC** (IP residencial), conectado a la base de
producción por su URL pública. Va de a poco (con pausas) para no gatillar el
bloqueo por IP de YouTube, y guarda el texto en `Resource.transcript`. Luego la
generación de preguntas usa ese transcript guardado sin volver a tocar YouTube.

Uso (desde el PC, contra producción):
    $env:DJANGO_SECRET_KEY = "cli-dummy"
    $env:DJANGO_ALLOWED_HOSTS = "localhost"
    $env:DATABASE_URL = "postgresql://...@zephyr.proxy.rlwy.net:PUERTO/railway"
    .venv\\Scripts\\python.exe manage.py backfill_transcripts --limit 5 --delay 8 ^
        --settings=config.settings.production

Empezá con --limit chico (3-5) la primera vez para confirmar que la IP no está
bloqueada; si ves varios fallos seguidos, el comando se detiene solo (probable
bloqueo) y conviene reintentar más tarde.
"""

import time

from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.content.models import Resource
from apps.content.services.transcript_service import fetch_transcript


class Command(BaseCommand):
    help = (
        "Baja transcripciones de YouTube (IP residencial) y las guarda en "
        "Resource.transcript, de a poco para no ser bloqueado."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit", type=int, default=20,
            help="Máximo de videos a procesar en esta corrida (def. 20).",
        )
        parser.add_argument(
            "--delay", type=float, default=8.0,
            help="Pausa en segundos entre cada video (def. 8). No bajar de ~5.",
        )
        parser.add_argument(
            "--resource", default=None,
            help="Slug de un recurso puntual. Por defecto, todos los que falten.",
        )
        parser.add_argument(
            "--overwrite", action="store_true",
            help="Rebajar el transcript aunque el recurso ya tenga uno guardado.",
        )
        parser.add_argument(
            "--max-fails", type=int, default=3,
            help="Fallos seguidos antes de abortar (probable bloqueo de IP). Def. 3.",
        )

    def handle(self, *args, **options):
        limit = max(1, options["limit"])
        delay = max(0.0, options["delay"])
        max_fails = max(1, options["max_fails"])

        qs = (
            Resource.objects.filter(is_published=True)
            .exclude(video_url__isnull=True)
            .exclude(video_url="")
        )
        if options["resource"]:
            qs = qs.filter(slug=options["resource"])
        if not options["overwrite"]:
            qs = qs.filter(Q(transcript__isnull=True) | Q(transcript=""))
        qs = qs.order_by("id")[:limit]

        total = qs.count()
        if total == 0:
            self.stdout.write(self.style.SUCCESS(
                "No hay recursos pendientes de transcript. Nada que hacer."
            ))
            return

        self.stdout.write(self.style.MIGRATE_HEADING(
            f"Backfill de transcripts: {total} recurso(s) a procesar."
        ))

        backfilled = 0
        failed = 0
        consecutive_fails = 0

        for index, resource in enumerate(qs, start=1):
            texto = fetch_transcript(resource.video_url)
            if texto:
                resource.transcript = texto
                resource.save(update_fields=["transcript"])
                backfilled += 1
                consecutive_fails = 0
                self.stdout.write(self.style.SUCCESS(
                    f"  [ok] ({index}/{total}) '{resource.title}': {len(texto)} caracteres."
                ))
            else:
                failed += 1
                consecutive_fails += 1
                self.stdout.write(self.style.WARNING(
                    f"  [--] ({index}/{total}) '{resource.title}': sin transcript "
                    f"(no disponible o IP bloqueada)."
                ))
                if consecutive_fails >= max_fails:
                    self.stdout.write(self.style.ERROR(
                        f"\nAbortado: {consecutive_fails} fallos seguidos. "
                        f"Probable bloqueo de IP de YouTube. Reintentá más tarde "
                        f"(y dejá un --delay más alto)."
                    ))
                    break

            # Pausa entre videos (no después del último).
            if index < total and delay:
                time.sleep(delay)

        self.stdout.write(self.style.MIGRATE_HEADING("\nResumen"))
        self.stdout.write(self.style.SUCCESS(f"  Transcripts guardados: {backfilled}"))
        if failed:
            self.stdout.write(f"  Sin transcript:        {failed}")
        self.stdout.write(
            "  Ahora podés generar preguntas: usarán el transcript guardado "
            "sin tocar YouTube."
        )
