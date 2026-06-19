from django.core.management.base import BaseCommand, CommandError

from apps.content.models import PublicationItem
from apps.content.services.publication_pipeline_service import (
    PipelineError,
    process_publication_item,
)


class Command(BaseCommand):
    help = "Avanza ítems del pipeline educativo hasta questions_ready."

    def add_arguments(self, parser):
        parser.add_argument("--item", type=int, default=0)
        parser.add_argument("--batch", default="")
        parser.add_argument("--limit", type=int, default=1)

    def handle(self, *args, **options):
        qs = PublicationItem.objects.exclude(
            state__in=[
                PublicationItem.STATE_QUESTIONS_READY,
                PublicationItem.STATE_PUBLISHED,
            ]
        ).select_related("resource", "resource__topic", "canonical_guide")
        if options["item"]:
            qs = qs.filter(id=options["item"])
        if options["batch"]:
            qs = qs.filter(batch_id=options["batch"])
        qs = qs.order_by("created_at", "id")
        if options["limit"] > 0:
            qs = qs[: options["limit"]]
        items = list(qs)
        if not items:
            raise CommandError("No hay ítems pendientes que coincidan con el filtro.")

        for item in items:
            self.stdout.write(f"[{item.id}] {item.source_filename}: {item.state}")
            try:
                process_publication_item(item)
            except Exception as exc:  # noqa: BLE001 - un ítem fallido no corta el lote
                item.resume_state = item.state
                item.state = PublicationItem.STATE_FAILED
                item.last_error = str(exc)
                item.attempts += 1
                item.save(
                    update_fields=[
                        "resume_state",
                        "state",
                        "last_error",
                        "attempts",
                        "updated_at",
                    ]
                )
                self.stdout.write(self.style.ERROR(f"  [x] {exc}"))
                continue
            item.refresh_from_db()
            if item.state == PublicationItem.STATE_TRANSCRIPT_PENDING:
                self.stdout.write(self.style.WARNING(f"  [espera] {item.last_error}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"  [ok] {item.state}"))
