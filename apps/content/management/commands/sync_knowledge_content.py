"""Sincroniza `docs/conocimiento/` con la BD, pero solo si cambió.

Reemplaza la cadena
`import_knowledge_tree && load_node_content && load_exercise_bank && publish_knowledge_nodes`
del Pre-Deploy / Start Command de Railway. Hashea el contenido del repo y lo
compara con el último hash sincronizado (`ContentSyncState`): si es igual, sale
en ~1 s; si cambió, corre los 4 loaders y guarda el nuevo hash.

Con `--force` corre siempre (útil si se tocó la BD a mano).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

CONTENT_ROOT = "docs/conocimiento"
STATE_KEY = "knowledge"
LOADERS = (
    "import_knowledge_tree",
    "load_node_content",
    "load_exercise_bank",
    "publish_knowledge_nodes",
)
_SUFFIXES = {".yaml", ".yml", ".jsonl"}


def content_hash() -> str:
    root = Path(settings.BASE_DIR) / CONTENT_ROOT
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.suffix in _SUFFIXES and p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


class Command(BaseCommand):
    help = "Corre los loaders de docs/conocimiento/ solo si el contenido cambió desde el ultimo deploy."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Correr los loaders sin chequear el hash.",
        )

    def handle(self, *args, **options):
        from apps.content.models import ContentSyncState

        current = content_hash()
        state, _ = ContentSyncState.objects.get_or_create(key=STATE_KEY)

        if not options["force"] and state.content_hash == current:
            self.stdout.write(
                f"docs/conocimiento/ sin cambios (hash {current[:12]}) — loaders omitidos."
            )
            return

        for name in LOADERS:
            self.stdout.write(f"-> {name}")
            call_command(name)

        state.content_hash = current
        state.save(update_fields=["content_hash", "synced_at"])
        self.stdout.write(self.style.SUCCESS(f"Sincronizado. hash={current[:12]}"))
