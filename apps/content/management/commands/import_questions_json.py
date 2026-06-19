import json
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.content.models import Resource
from apps.content.services.ai_generation_service import _save_questions


class Command(BaseCommand):
    help = "Importa preguntas a un recurso desde un archivo JSON estructurado."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Ruta al archivo JSON.")
        parser.add_argument("--resource", required=True, help="Slug del recurso.")
        parser.add_argument(
            "--level",
            type=int,
            required=True,
            choices=[1, 2, 3],
            help="Nivel de las preguntas.",
        )
        parser.add_argument(
            "--mode",
            default="ambas",
            choices=["preparacion", "evaluacion", "ambas"],
            help="Modo.",
        )
        parser.add_argument(
            "--status",
            default="publicada",
            choices=["borrador", "publicada"],
            help="Estado.",
        )

    def _configure_windows_utf8(self):
        if not sys.platform.startswith("win"):
            return
        for stream in (sys.stdout, sys.stderr):
            reconfigure = getattr(stream, "reconfigure", None)
            if reconfigure is None:
                continue
            try:
                reconfigure(encoding="utf-8")
            except (OSError, ValueError):
                continue

    def handle(self, *args, **options):
        self._configure_windows_utf8()
        path = Path(options["file"])
        resource_slug = options["resource"]
        level = options["level"]
        mode = options["mode"]
        status = options["status"]

        if not path.is_file():
            raise CommandError(f"No existe el archivo JSON: {path}")

        try:
            resource = Resource.objects.get(slug=resource_slug)
        except Resource.DoesNotExist as exc:
            raise CommandError(
                f"El recurso con slug '{resource_slug}' no existe."
            ) from exc

        try:
            with path.open("r", encoding="utf-8") as fh:
                questions_data = json.load(fh)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise CommandError(f"Error parseando el JSON: {exc}") from exc

        if not isinstance(questions_data, (list, dict)):
            raise CommandError("El JSON debe contener una lista de preguntas.")

        self.stdout.write(f"Importando preguntas para '{resource.title}'...")
        try:
            with transaction.atomic():
                created = _save_questions(
                    resource,
                    level,
                    mode,
                    questions_data,
                    status,
                )
        except (TypeError, ValueError) as exc:
            raise CommandError(f"Error al guardar preguntas: {exc}") from exc

        if not created:
            raise CommandError("El JSON no contenía preguntas válidas para importar.")

        self.stdout.write(
            self.style.SUCCESS(f"¡Éxito! Se importaron {len(created)} preguntas.")
        )
