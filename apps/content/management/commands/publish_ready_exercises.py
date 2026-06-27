"""Publica todos los ejercicios en estado 'ready' y activa sus ItemGroups.

Uso típico: después de importar un lote de ejercicios revisados y querer
verlos en el browser sin pasar por el admin uno por uno.

  python manage.py publish_ready_exercises
  python manage.py publish_ready_exercises --semantic-id MAT.NUM.ENTEROS_CONJUNTO.ORDEN_LOGICA
  python manage.py publish_ready_exercises --dry-run
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.content.models import ItemGroup, NodeExercise


class Command(BaseCommand):
    help = "Publica ejercicios 'ready' y activa sus ItemGroups."

    def add_arguments(self, parser):
        parser.add_argument(
            "--semantic-id",
            default=None,
            help="Limitar a un semantic_id específico (opcional).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Mostrar qué se publicaría sin hacer cambios.",
        )

    def handle(self, *args, **options):
        qs = NodeExercise.objects.filter(status=NodeExercise.STATUS_READY)
        if options["semantic_id"]:
            qs = qs.filter(item_group__node__semantic_id=options["semantic_id"])

        count = qs.count()
        if count == 0:
            self.stdout.write("No hay ejercicios en estado 'ready'.")
            return

        self.stdout.write(f"Ejercicios 'ready' encontrados: {count}")
        if options["dry_run"]:
            for ex in qs.select_related("item_group__node")[:20]:
                self.stdout.write(
                    f"  [{ex.item_group.node.semantic_id}] {ex.stable_id or ex.id} "
                    f"— {ex.item_group.code}"
                )
            if count > 20:
                self.stdout.write(f"  ... y {count - 20} más.")
            self.stdout.write("(dry-run: sin cambios)")
            return

        with transaction.atomic():
            published = qs.update(status=NodeExercise.STATUS_PUBLISHED)
            # Activar los ItemGroups que tienen al menos un ejercicio publicado.
            groups = ItemGroup.objects.filter(
                exercises__status=NodeExercise.STATUS_PUBLISHED
            ).distinct()
            activated = groups.update(is_published=True)

        self.stdout.write(
            self.style.SUCCESS(
                f"Publicados: {published} ejercicios, {activated} ItemGroups activados."
            )
        )
