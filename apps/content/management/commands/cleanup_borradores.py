"""
Elimina preguntas con status='borrador' que son residuos de loops de generación antiguos.

Criterio seguro:
  - status = 'borrador'
  - Y (sin publication_item  OR  publication_item.state en 'published'/'failed')

Las preguntas ligadas a un PublicationItem activo (uploaded, transcript_pending,
context_ready, metadata_ready, questions_ready) quedan intactas para no romper
pipelines en vuelo.

Uso:
  python manage.py cleanup_borradores             # dry-run (muestra qué borraría)
  python manage.py cleanup_borradores --confirmar # borra de verdad
"""

from django.core.management.base import BaseCommand
from django.db.models import Q

from apps.content.models.publication_pipeline import PublicationItem
from apps.content.models.question import Question


ESTADOS_INACTIVOS = {
    PublicationItem.STATE_PUBLISHED,
    PublicationItem.STATE_FAILED,
}

ESTADOS_ACTIVOS = {
    PublicationItem.STATE_UPLOADED,
    PublicationItem.STATE_TRANSCRIPT_PENDING,
    PublicationItem.STATE_CONTEXT_READY,
    PublicationItem.STATE_METADATA_READY,
    PublicationItem.STATE_QUESTIONS_READY,
}


class Command(BaseCommand):
    help = "Elimina borradores residuales de loops de generación antiguos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirmar",
            action="store_true",
            help="Ejecutar el borrado real (sin este flag es dry-run)",
        )

    def handle(self, *args, **options):
        confirmar = options["confirmar"]

        qs = Question.objects.filter(status="borrador").filter(
            Q(publication_item__isnull=True)
            | Q(publication_item__state__in=ESTADOS_INACTIVOS)
        )

        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("No hay borradores residuales. Nada que hacer."))
            return

        # Desglose por recurso
        self.stdout.write(f"\n{'DRY-RUN' if not confirmar else 'BORRADO REAL'}: {total} pregunta(s) borrador residual(es)\n")
        self.stdout.write(f"{'Recurso':<60} {'Sin item':>8} {'Item inactivo':>13}")
        self.stdout.write("-" * 85)

        from django.db.models import Count
        breakdown = (
            qs.values("resource__slug", "publication_item__state")
            .annotate(n=Count("id"))
            .order_by("resource__slug")
        )
        for row in breakdown:
            slug = row["resource__slug"] or "(sin recurso)"
            estado = row["publication_item__state"] or "NULL"
            n = row["n"]
            self.stdout.write(f"{slug:<60} {estado:>13}   {n:>4}")

        self.stdout.write("-" * 85)

        if not confirmar:
            self.stdout.write(
                self.style.WARNING(
                    f"\nDRY-RUN: se borrarían {total} preguntas. "
                    "Agrega --confirmar para borrar de verdad."
                )
            )
            return

        deleted_count, _ = qs.delete()
        self.stdout.write(
            self.style.SUCCESS(f"\nEliminadas {deleted_count} preguntas borrador residuales.")
        )
