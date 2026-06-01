"""Comando de management para generar preguntas con IA para un recurso."""

from django.core.management.base import BaseCommand, CommandError
from apps.content.models import Resource
from apps.content.services.ai_generation_service import generate_questions_for_resource


class Command(BaseCommand):
    help = "Genera preguntas en estado borrador para un recurso utilizando la IA (Gemini/OpenAI)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--resource",
            required=True,
            help="Slug del recurso para el cual generar preguntas.",
        )
        parser.add_argument(
            "--level",
            type=int,
            required=True,
            choices=[1, 2, 3],
            help="Nivel de las preguntas (1, 2 o 3).",
        )
        parser.add_argument(
            "--count",
            type=int,
            default=3,
            help="Cantidad de preguntas a generar (por defecto 3).",
        )
        parser.add_argument(
            "--mode",
            choices=["preparacion", "evaluacion", "ambas"],
            default="ambas",
            help="Modo de las preguntas (por defecto 'ambas').",
        )
        parser.add_argument(
            "--api-key",
            default=None,
            help="Opcional. API Key de Gemini o OpenAI a utilizar.",
        )

    def handle(self, *args, **options):
        resource_slug = options["resource"]
        level = options["level"]
        count = options["count"]
        mode = options["mode"]
        api_key = options["api_key"]

        try:
            resource = Resource.objects.get(slug=resource_slug)
        except Resource.DoesNotExist:
            raise CommandError(f"El recurso con slug '{resource_slug}' no existe.")

        self.stdout.write(
            f"Iniciando generación de {count} preguntas de Nivel {level} (Modo: '{mode}') para el recurso '{resource.title}'..."
        )

        try:
            questions = generate_questions_for_resource(
                resource=resource,
                level=level,
                mode=mode,
                count=count,
                api_key=api_key,
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"¡Éxito! Se han generado y guardado {len(questions)} preguntas en estado 'borrador'."
                )
            )
            for idx, q in enumerate(questions, start=1):
                self.stdout.write(f"  {idx}. [ID {q.pk}] {q.text[:80]}...")
                for choice in q.choices.all():
                    mark = "[V]" if choice.is_correct else "[X]"
                    self.stdout.write(f"     - {mark} {choice.text[:60]}")

        except Exception as e:
            raise CommandError(f"Error durante la generación de preguntas: {str(e)}")
