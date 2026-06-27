"""Importa el banco de ejercicios (NodeExercise) desde JSONL.

Formato: una línea JSON por ejercicio (salida del pipeline NotebookLM → Claude,
handoff §12). Idempotente por `stable_id`: reejecutar actualiza sin duplicar.

Regla de seguridad (handoff §13): el importador NUNCA publica. Un ejercicio entra
como `review_required` si trae `legal_review`/`rewrite_required`, le falta
`correct_answer`, o ya viene marcado para revisión; `published` entrante baja a
`ready` (la publicación se aprueba a mano).
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.content.models import ItemGroup, KnowledgeNode, NodeExercise
from apps.content.models.node_bank import STANDARD_ITEM_GROUPS

_STANDARD_BY_CODE = {g["code"]: g for g in STANDARD_ITEM_GROUPS}
_STANDARD_ORDER = {g["code"]: i for i, g in enumerate(STANDARD_ITEM_GROUPS, start=1)}


def _valid(value, choices, default):
    valid = {key for key, _ in choices}
    return value if value in valid else default


def _resolve_item_group(node, code):
    """Devuelve el ItemGroup (node, code), creándolo desde plantilla si falta."""
    spec = _STANDARD_BY_CODE.get(code)
    if spec:
        defaults = {
            "title": spec["title"],
            "purpose": spec["purpose"],
            "level": spec["level"],
            "order": _STANDARD_ORDER[code],
        }
    else:
        defaults = {
            "title": code.replace("_", " ").capitalize(),
            "level": ItemGroup.LEVEL_RESOLVER,
            "order": 99,
        }
    group, _ = ItemGroup.objects.get_or_create(node=node, code=code, defaults=defaults)
    return group


def _resolve_status(raw):
    """(status, flagged_for_review). El importador nunca devuelve 'published'."""
    incoming = _valid(
        raw.get("status") or NodeExercise.STATUS_DRAFT,
        NodeExercise.STATUS_CHOICES,
        NodeExercise.STATUS_DRAFT,
    )
    if incoming == NodeExercise.STATUS_PUBLISHED:
        incoming = NodeExercise.STATUS_READY

    has_answer = bool(str(raw.get("correct_answer") or "").strip())
    needs_review = (
        bool(raw.get("legal_review"))
        or bool(raw.get("rewrite_required"))
        or not has_answer
        or incoming == NodeExercise.STATUS_REVIEW_REQUIRED
    )
    if needs_review:
        return NodeExercise.STATUS_REVIEW_REQUIRED, True
    return incoming, False


class Command(BaseCommand):
    help = "Importa NodeExercise desde JSONL (pipeline NotebookLM → Claude)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dir",
            default="docs/conocimiento/ejercicios",
            help="Directorio con los .jsonl (default: docs/conocimiento/ejercicios)",
        )
        parser.add_argument("--file", default=None, help="Importar un único .jsonl")

    def handle(self, *args, **options):
        if options["file"]:
            files = [Path(options["file"])]
        else:
            files = sorted(Path(options["dir"]).glob("*.jsonl"))

        created = updated = not_found = invalid = flagged = 0

        for path in files:
            with open(path, encoding="utf-8") as f:
                for lineno, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        raw = json.loads(line)
                    except json.JSONDecodeError as exc:
                        self.stderr.write(f"{path.name}:{lineno} JSON inválido: {exc}")
                        invalid += 1
                        continue

                    semantic_id = (raw.get("semantic_id") or "").strip()
                    group_code = (raw.get("item_group") or "").strip()
                    prompt = (raw.get("prompt") or "").strip()
                    if not semantic_id or not group_code or not prompt:
                        self.stderr.write(
                            f"{path.name}:{lineno} faltan campos obligatorios "
                            "(semantic_id / item_group / prompt) — omitido"
                        )
                        invalid += 1
                        continue

                    try:
                        node = KnowledgeNode.objects.get(semantic_id=semantic_id)
                    except KnowledgeNode.DoesNotExist:
                        self.stderr.write(
                            f"{path.name}:{lineno} semantic_id no encontrado: {semantic_id}"
                        )
                        not_found += 1
                        continue

                    group = _resolve_item_group(node, group_code)
                    status, was_flagged = _resolve_status(raw)

                    defaults = {
                        "node": node,
                        "item_group": group,
                        "kind": _valid(
                            raw.get("kind"), NodeExercise.KIND_CHOICES, NodeExercise.KIND_ITEM
                        ),
                        "format": _valid(
                            raw.get("format"),
                            NodeExercise.FORMAT_CHOICES,
                            NodeExercise.FORMAT_MULTIPLE_CHOICE,
                        ),
                        "difficulty": _valid(
                            raw.get("difficulty"),
                            NodeExercise.DIFFICULTY_CHOICES,
                            NodeExercise.DIFFICULTY_BASICA,
                        ),
                        "competencia": _valid(
                            raw.get("competencia"), NodeExercise.COMPETENCIA_CHOICES, ""
                        ),
                        "prompt": prompt,
                        "choices": raw.get("choices") or [],
                        "correct_answer": raw.get("correct_answer") or "",
                        "solution_steps": raw.get("solution_steps") or "",
                        "explanation": raw.get("explanation") or "",
                        "conceptual_checks": raw.get("conceptual_checks") or [],
                        "prerequisites": raw.get("prerequisites") or [],
                        "pattern": raw.get("pattern") or {},
                        "paes_style": bool(raw.get("paes_style")),
                        "source_title": raw.get("source_title") or "",
                        "source_location": raw.get("source_location") or "",
                        "source_reference": raw.get("source_reference") or "",
                        "source_kind": _valid(
                            raw.get("source_kind"),
                            NodeExercise.SOURCE_KIND_CHOICES,
                            NodeExercise.SOURCE_NOTEBOOKLM,
                        ),
                        "status": status,
                        "legal_review": bool(raw.get("legal_review")),
                        "rewrite_required": bool(raw.get("rewrite_required")),
                        "duplicate_candidate": bool(raw.get("duplicate_candidate")),
                        "notes": raw.get("notes") or "",
                        "order": raw.get("order") or 0,
                    }

                    stable_id = (raw.get("stable_id") or "").strip()
                    existing = (
                        NodeExercise.objects.filter(stable_id=stable_id).first()
                        if stable_id
                        else None
                    )
                    # La publicación es una decisión MANUAL: un reimport refresca el
                    # contenido pero nunca degrada un ejercicio ya publicado.
                    if existing and existing.status == NodeExercise.STATUS_PUBLISHED:
                        defaults["status"] = NodeExercise.STATUS_PUBLISHED
                        was_flagged = False

                    if was_flagged:
                        flagged += 1

                    if stable_id:
                        _, is_new = NodeExercise.objects.update_or_create(
                            stable_id=stable_id, defaults=defaults
                        )
                    else:
                        NodeExercise.objects.create(**defaults)
                        is_new = True

                    if is_new:
                        created += 1
                    else:
                        updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Creados: {created}, Actualizados: {updated}, "
                f"semantic_id no encontrado: {not_found}, inválidos: {invalid}, "
                f"marcados para revisión: {flagged}"
            )
        )
