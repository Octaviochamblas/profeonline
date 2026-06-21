from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import Resource
from apps.content.services.title_cleanup_service import (
    TITLE_CLEANUP_VERSION,
    clean_resource_title,
)


class Command(BaseCommand):
    help = (
        "Previsualiza o aplica la limpieza editorial de títulos de recursos "
        "sin modificar sus slugs."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Aplica los cambios. Sin esta opción el comando es dry-run.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        apply_changes = options["apply"]
        changed = 0
        resources = Resource.objects.select_related("subject", "topic").order_by("pk")

        for resource in resources.iterator():
            cleaned = clean_resource_title(
                resource.title,
                subject_name=resource.subject.name if resource.subject else "",
                topic_name=resource.topic.name if resource.topic else "",
                topic_slug=resource.topic.slug if resource.topic else "",
            )
            if cleaned == resource.title:
                continue

            changed += 1
            line = f"[{resource.slug}] {resource.title} -> {cleaned}"
            encoding = getattr(self.stdout._out, "encoding", None) or "utf-8"
            self.stdout.write(
                line.encode(encoding, errors="replace").decode(encoding)
            )
            if apply_changes:
                original_slug = resource.slug
                resource.title = cleaned
                resource.save(update_fields=["title"])
                if resource.slug != original_slug:
                    raise RuntimeError("La limpieza no puede modificar slugs.")

        mode = "aplicados" if apply_changes else "detectados (dry-run)"
        self.stdout.write(
            self.style.SUCCESS(
                f"Limpieza v{TITLE_CLEANUP_VERSION}: {changed} cambios {mode}."
            )
        )
