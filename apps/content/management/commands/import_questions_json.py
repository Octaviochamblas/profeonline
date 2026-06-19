import json
import os
import sys
from django.core.management.base import BaseCommand, CommandError
from apps.content.models import Resource
from apps.content.services.ai_generation_service import _save_questions

# Asegurar codificación UTF-8 en consola para evitar UnicodeEncodeError en Windows
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

class Command(BaseCommand):
    help = "Importa preguntas a un recurso desde un archivo JSON estructurado."

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Ruta al archivo JSON.")
        parser.add_argument("--resource", required=True, help="Slug del recurso.")
        parser.add_argument("--level", type=int, required=True, choices=[1, 2, 3], help="Nivel de las preguntas.")
        parser.add_argument("--mode", default="ambas", choices=["preparacion", "evaluacion", "ambas"], help="Modo.")
        parser.add_argument("--status", default="publicada", choices=["borrador", "publicada"], help="Estado.")

    def handle(self, *args, **options):
        path = options["file"]
        resource_slug = options["resource"]
        level = options["level"]
        mode = options["mode"]
        status = options["status"]

        if not os.path.exists(path):
            raise CommandError(f"No existe el archivo JSON: {path}")

        try:
            resource = Resource.objects.get(slug=resource_slug)
        except Resource.DoesNotExist:
            raise CommandError(f"El recurso con slug '{resource_slug}' no existe.")

        try:
            with open(path, "r", encoding="utf-8") as fh:
                questions_data = json.load(fh)
        except Exception as e:
            raise CommandError(f"Error parseando el JSON: {e}")

        self.stdout.write(f"Importando preguntas para '{resource.title}'...")
        try:
            created = _save_questions(resource, level, mode, questions_data, status)
            self.stdout.write(self.style.SUCCESS(f"¡Éxito! Se importaron {len(created)} preguntas."))
        except Exception as e:
            raise CommandError(f"Error al guardar preguntas: {e}")
