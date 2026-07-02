"""Carga contenido pedagógico (NodeContent + NodeMedia) desde YAML.

Formato esperado: docs/conocimiento/contenido/*.yaml
Idempotente: segunda ejecución actualiza sin duplicar.
"""

from pathlib import Path

import yaml
from django.core.management.base import BaseCommand

from apps.content.models import KnowledgeNode, NodeContent, NodeMedia


class Command(BaseCommand):
    help = "Importa NodeContent y NodeMedia desde docs/conocimiento/contenido/*.yaml"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="docs/conocimiento/contenido",
            help="Directorio raíz con los YAML de contenido (default: docs/conocimiento/contenido)",
        )
        parser.add_argument(
            "--file",
            default=None,
            help="Importar un único archivo YAML",
        )
        parser.add_argument(
            "--force-manual",
            action="store_true",
            help="Reemplazar también contenidos protegidos por una edición manual.",
        )

    def handle(self, *args, **options):
        if options["file"]:
            files = [Path(options["file"])]
        else:
            dirpath = Path(options["dir"])
            files = sorted(dirpath.glob("*.yaml")) + sorted(dirpath.glob("*.yml"))

        created = updated = not_found = protected = 0

        for path in files:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data:
                continue

            semantic_id = data.get("semantic_id")
            if not semantic_id:
                self.stderr.write(f"Sin semantic_id: {path.name} — omitido")
                continue

            try:
                node = KnowledgeNode.objects.get(semantic_id=semantic_id)
            except KnowledgeNode.DoesNotExist:
                self.stderr.write(
                    f"semantic_id no encontrado en DB: {semantic_id} ({path.name})"
                )
                not_found += 1
                continue

            defaults = {
                "objetivo": data.get("objetivo", ""),
                "introduccion": data.get("introduccion", ""),
                "resumen": data.get("resumen", ""),
                "explicacion": data.get("explicacion", ""),
                "procedimiento": data.get("procedimiento") or [],
                "ejemplos": data.get("ejemplos") or [],
                "errores_frecuentes": data.get("errores_frecuentes") or [],
                "estado": data.get("estado", NodeContent.ESTADO_BORRADOR),
                "fuente": data.get("fuente", ""),
                "manual_override": False,
                "manual_edited_at": None,
                "manual_edited_by": None,
            }

            current = NodeContent.objects.filter(node=node).first()
            if current and current.manual_override and not options["force_manual"]:
                protected += 1
            else:
                _, is_new = NodeContent.objects.update_or_create(
                    node=node, defaults=defaults
                )
                if is_new:
                    created += 1
                else:
                    updated += 1

            # Sincronizar media: reemplaza completo si la clave está presente.
            if "media" in data and data["media"] is not None:
                NodeMedia.objects.filter(node=node).delete()
                for m in data["media"]:
                    NodeMedia.objects.create(
                        node=node,
                        kind=m.get("kind", NodeMedia.KIND_VIDEO_YOUTUBE),
                        video_kind=m.get("video_kind", ""),
                        url=m.get("url", ""),
                        order=m.get("order", 0),
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Creados: {created}, Actualizados: {updated}, "
                f"protegidos omitidos: {protected}, "
                f"semantic_id no encontrado: {not_found}"
            )
        )
