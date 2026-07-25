from django.core.management.base import BaseCommand

from apps.content.models import Resource
from apps.content.services.node_matching_service import generate_suggestion


class Command(BaseCommand):
    help = (
        "Genera sugerencias de nodo de conocimiento (KnowledgeNode) para recursos "
        "(videos) publicados que aun no tienen ninguna ResourceNodeSuggestion."
    )

    def handle(self, *args, **options):
        resources = Resource.objects.filter(
            is_published=True,
            node_suggestion__isnull=True,
        )

        created = 0
        skipped = 0
        for resource in resources:
            try:
                generate_suggestion(resource)
                created += 1
            except Exception as exc:
                skipped += 1
                self.stderr.write(f"Error en recurso {resource.pk} ({resource.title}): {exc}")

        self.stdout.write(
            self.style.SUCCESS(f"Sugerencias generadas: {created}. Con error: {skipped}.")
        )
