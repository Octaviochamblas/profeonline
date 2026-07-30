"""Migra infografías e imágenes conceptuales legadas (PNG/JPEG) al estándar WebP
ya usado por las subidas nuevas (``editorial_asset_service``), sin regenerar
contenido con IA ni alterar el diseño visual.

Reutiliza exactamente la misma optimización de Pillow y las mismas funciones de
subida/sincronización que usa la subida manual (``upload_infographic``,
``upload_concept_image``, ``insert_infographic_before_closing``,
``insert_concept_image_after_explanations``); este comando solo decide *qué*
recursos migrar y *cuándo* respaldar/confirmar/verificar.

Uso:
    python manage.py migrate_editorial_images_to_webp --dry-run
    python manage.py migrate_editorial_images_to_webp --apply
    python manage.py migrate_editorial_images_to_webp --apply --resource-ids 12,45
    python manage.py migrate_editorial_images_to_webp --apply --limit 20
    python manage.py migrate_editorial_images_to_webp --verify
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from PIL import Image

from apps.content.models import PublicationItem, Resource
from apps.content.services.editorial_asset_service import (
    CONCEPT_WEBP_QUALITY,
    INFOGRAPHIC_WEBP_QUALITY,
    MAX_WEB_IMAGE_SIZE,
    _optimized_image_payload,
    get_concept_image_object,
    get_infographic_object,
    upload_concept_image,
    upload_infographic,
)
from apps.content.services.editorial_guide_service import (
    insert_concept_image_after_explanations,
    insert_infographic_before_closing,
)

LEGACY_EXTENSIONS = (".png", ".jpg", ".jpeg")
BACKUP_DIR = Path("resource_refresh_backups")

# kind -> (key_field, alt_text_field, get_object, upload_fn, quality, insert_fn, bucket_prefix)
ASSET_KINDS = {
    "infographic": dict(
        key_field="infographic_key",
        alt_field="infographic_alt_text",
        get_object=get_infographic_object,
        upload=upload_infographic,
        quality=INFOGRAPHIC_WEBP_QUALITY,
        insert=insert_infographic_before_closing,
        prefix="editorial-infographics",
    ),
    "concept_image": dict(
        key_field="concept_image_key",
        alt_field="concept_image_alt_text",
        get_object=get_concept_image_object,
        upload=upload_concept_image,
        quality=CONCEPT_WEBP_QUALITY,
        insert=insert_concept_image_after_explanations,
        prefix="editorial-concept-images",
    ),
}


def _is_legacy(key: str) -> bool:
    return bool(key) and key.lower().endswith(LEGACY_EXTENSIONS)


def _candidate_kinds(resource: Resource) -> list[str]:
    return [
        kind
        for kind, spec in ASSET_KINDS.items()
        if _is_legacy(getattr(resource, spec["key_field"]))
    ]


def _predicted_key(resource_id: int, kind: str, payload: bytes) -> str:
    digest = hashlib.sha256(payload).hexdigest()
    return f"{ASSET_KINDS[kind]['prefix']}/{resource_id}/{digest[:24]}.webp"


def _question_fingerprint(resource: Resource) -> str:
    rows = [
        (
            q.id, q.level, q.mode, q.status, q.text, q.explanation,
            tuple((c.id, c.text, c.is_correct) for c in q.choices.order_by("id")),
        )
        for q in resource.questions.order_by("id").prefetch_related("choices")
    ]
    return hashlib.sha256(repr(rows).encode()).hexdigest()


def _metadata_fingerprint(resource: Resource) -> str:
    values = (
        resource.title,
        resource.description,
        resource.subject_id,
        resource.topic_id,
        tuple(sorted(resource.levels.values_list("id", flat=True))),
        resource.video_url,
        resource.order,
        resource.is_published,
    )
    return hashlib.sha256(repr(values).encode()).hexdigest()


def _canonical_guide_item(resource: Resource, *, for_update: bool = False):
    qs = PublicationItem.objects.filter(resource=resource).exclude(canonical_guide__isnull=True)
    if for_update:
        qs = qs.select_for_update()
    return qs.order_by("-updated_at").first()


def _current_text(resource: Resource) -> str:
    item = _canonical_guide_item(resource)
    return item.canonical_guide.content_text if item else resource.content


def _would_block(resource: Resource, kinds: list[str]) -> str | None:
    """Simula (sin guardar) la inserción editorial para detectar bloqueos
    estructurales antes de aplicar, ej. guía sin las secciones requeridas."""
    text = _current_text(resource)
    for kind in kinds:
        try:
            text = ASSET_KINDS[kind]["insert"](text, resource)
        except ValueError as exc:
            return str(exc)
    return None


def _download_legacy_source(resource: Resource, kind: str):
    """Lee el objeto legado actual desde el bucket (nunca desde HTML)."""
    spec = ASSET_KINDS[kind]
    obj = spec["get_object"](resource)
    if obj is None:
        return None
    body = obj["Body"].read()
    with Image.open(BytesIO(body)) as opened:
        original_format = opened.format
        original_size = opened.size
    return {
        "bytes": body,
        "content_type": obj.get("ContentType", ""),
        "format": original_format,
        "size": original_size,
        "key": getattr(resource, ASSET_KINDS[kind]["key_field"]),
    }


def _inspect(resource: Resource, kind: str) -> dict | None:
    """Calcula en memoria la conversión a WebP, sin escribir nada (dry-run)."""
    source = _download_legacy_source(resource, kind)
    if source is None:
        return None
    upload_name = source["key"].rsplit("/", 1)[-1]
    uploaded_file = SimpleUploadedFile(
        upload_name, source["bytes"], content_type=source["content_type"]
    )
    payload, content_type, extension = _optimized_image_payload(
        uploaded_file, quality=ASSET_KINDS[kind]["quality"]
    )
    with Image.open(BytesIO(payload)) as optimized:
        new_size = optimized.size
    original_bytes = len(source["bytes"])
    new_bytes = len(payload)
    reduction_pct = (
        round(100 * (1 - new_bytes / original_bytes), 1) if original_bytes else 0.0
    )
    return {
        "resource_id": resource.id,
        "slug": resource.slug,
        "kind": kind,
        "old_key": source["key"],
        "predicted_new_key": _predicted_key(resource.id, kind, payload),
        "original_format": source["format"],
        "original_size": source["size"],
        "original_bytes": original_bytes,
        "new_size": new_size,
        "new_bytes": new_bytes,
        "reduction_pct": reduction_pct,
    }


def _apply_one_resource(resource: Resource, kinds: list[str]) -> dict:
    """Migra un recurso completo (ambas imágenes candidatas) en su propia
    transacción: si algo falla, se revierte solo este recurso."""
    backup = {
        "resource_id": resource.id,
        "slug": resource.slug,
        "title": resource.title,
        "old_keys": {},
        "new_keys": {},
        "content_before": resource.content,
        "canonical_guide_content_before": None,
        "canonical_guide_id": None,
        "inspected": {},
        "questions_fingerprint_before": _question_fingerprint(resource),
        "metadata_fingerprint_before": _metadata_fingerprint(resource),
    }
    inspected = {}
    for kind in kinds:
        info = _inspect(resource, kind)
        if info is None:
            continue
        inspected[kind] = info
        backup["old_keys"][kind] = info["old_key"]
        backup["new_keys"][kind] = info["predicted_new_key"]
    backup["inspected"] = inspected
    if not inspected:
        return {"resource_id": resource.id, "status": "omitted", "reason": "sin objeto legado legible"}

    processed = []
    with transaction.atomic():
        resource = Resource.objects.select_for_update().get(pk=resource.pk)
        # Revalida bajo el lock: otro proceso pudo haber migrado este mismo
        # recurso mientras esperábamos el lock (ej. una corrida previa que
        # quedó huérfana). Reprocesar una clave ya-webp la recomprimiría
        # (pérdida generacional) sin necesidad; se omite si ya no es legada.
        still_legacy = set(_candidate_kinds(resource))
        item = _canonical_guide_item(resource, for_update=True)
        guide = item.canonical_guide if item else None
        backup["canonical_guide_id"] = guide.id if guide else None
        backup["canonical_guide_content_before"] = guide.content_text if guide else None
        current_text = guide.content_text if guide else resource.content

        for kind, info in inspected.items():
            if kind not in still_legacy:
                continue
            spec = ASSET_KINDS[kind]
            source = _download_legacy_source(resource, kind)
            uploaded_file = SimpleUploadedFile(
                info["old_key"].rsplit("/", 1)[-1],
                source["bytes"],
                content_type=source["content_type"],
            )
            existing_alt = getattr(resource, spec["alt_field"])
            spec["upload"](resource, uploaded_file, existing_alt)
            current_text = spec["insert"](current_text, resource)
            processed.append(kind)

        if not processed:
            return {"resource_id": resource.id, "status": "omitted", "reason": "ya migrado por otra corrida"}

        if guide is not None:
            guide.content_text = current_text
            guide.save(update_fields=["content_text", "updated_at"])
            resource.content = current_text
            resource.save(update_fields=["content"])
        else:
            resource.content = current_text
            resource.save(update_fields=["content"])

        for kind in processed:
            backup["new_keys"][kind] = getattr(resource, ASSET_KINDS[kind]["key_field"])

    return {"resource_id": resource.id, "status": "migrated", "kinds": processed, "backup": backup}


_RUN_STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _write_backup_line(entry: dict) -> Path:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    path = BACKUP_DIR / f"migrate_editorial_images_to_webp_{_RUN_STAMP}.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")
    return path


class Command(BaseCommand):
    help = (
        "Migra infografías e imágenes conceptuales legadas (PNG/JPEG) de recursos "
        "publicados al estándar WebP, reutilizando el pipeline de optimización "
        "existente. Modo dry-run por defecto salvo --apply."
    )

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Solo reporta, no escribe (por defecto).")
        parser.add_argument("--apply", action="store_true", help="Aplica la migración.")
        parser.add_argument("--verify", action="store_true", help="Verifica en producción una migración ya aplicada.")
        parser.add_argument("--resource-ids", default="", help="Lista separada por comas de IDs a procesar.")
        parser.add_argument("--limit", type=int, default=None, help="Máximo de recursos a procesar.")

    def _candidate_queryset(self, options):
        qs = Resource.objects.filter(is_published=True).order_by("pk")
        ids = [i.strip() for i in options["resource_ids"].split(",") if i.strip()]
        if ids:
            qs = qs.filter(pk__in=ids)
        candidates = [r for r in qs if _candidate_kinds(r)]
        if options["limit"] is not None:
            candidates = candidates[: options["limit"]]
        return candidates

    def handle(self, *args, **options):
        modes = [m for m in ("dry_run", "apply", "verify") if options[m]]
        if len(modes) > 1:
            raise CommandError("Usa un solo modo: --dry-run, --apply o --verify.")
        if options["verify"]:
            return self._verify()
        apply_changes = bool(options["apply"])

        resources = self._candidate_queryset(options)
        if not resources:
            self.stdout.write(self.style.SUCCESS("0 candidatos: nada por migrar (ya en WebP o sin imágenes legadas)."))
            return

        migrated, omitted, blocked, failed = 0, 0, 0, 0
        for resource in resources:
            kinds = _candidate_kinds(resource)
            if apply_changes:
                try:
                    result = _apply_one_resource(resource, kinds)
                except Exception as exc:  # noqa: BLE001 - se registra y se sigue con el resto
                    failed += 1
                    self.stdout.write(self.style.ERROR(f"[{resource.id}] FALLÓ: {exc}"))
                    continue
                if result["status"] == "omitted":
                    omitted += 1
                    self.stdout.write(f"[{resource.id}] omitido: {result['reason']}")
                    continue
                _write_backup_line(result["backup"])
                migrated += 1
                self.stdout.write(self.style.SUCCESS(f"[{resource.id}] migrado: {result['kinds']}"))
            else:
                block_reason = _would_block(resource, kinds)
                for kind in kinds:
                    info = _inspect(resource, kind)
                    if info is None:
                        omitted += 1
                        self.stdout.write(f"[{resource.id}] omitido ({kind}): objeto legado no disponible")
                        continue
                    self.stdout.write(
                        f"[{resource.id}] {resource.slug} {kind}: "
                        f"{info['original_format']} {info['original_size']} {info['original_bytes']}B -> "
                        f"WEBP {info['new_size']} {info['new_bytes']}B "
                        f"(-{info['reduction_pct']}%)"
                    )
                    if block_reason:
                        blocked += 1
                        self.stdout.write(self.style.WARNING(f"[{resource.id}] BLOQUEADO ({kind}): {block_reason}"))
                    else:
                        migrated += 1

        label = "aplicados" if apply_changes else "candidatos (dry-run)"
        self.stdout.write(
            self.style.SUCCESS(f"{migrated} {label}, {omitted} omitidos, {blocked} bloqueados, {failed} fallidos.")
        )

    def _verify(self):
        if not BACKUP_DIR.exists():
            raise CommandError(f"No existe {BACKUP_DIR}/, no hay nada que verificar.")
        entries = []
        for path in sorted(BACKUP_DIR.glob("*.jsonl")):
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    entries.append(json.loads(line))
        if not entries:
            raise CommandError("No hay entradas de respaldo para verificar.")

        sample = entries[:10] if len(entries) > 10 else entries
        ok, drift = 0, 0
        for entry in sample:
            resource = Resource.objects.filter(pk=entry["resource_id"]).first()
            if resource is None:
                self.stdout.write(self.style.ERROR(f"[{entry['resource_id']}] ya no existe"))
                drift += 1
                continue
            problems = []
            for kind, new_key in entry["new_keys"].items():
                if not new_key.endswith(".webp"):
                    problems.append(f"{kind}: clave no termina en .webp")
                    continue
                current_key = getattr(resource, ASSET_KINDS[kind]["key_field"])
                if current_key != new_key:
                    problems.append(f"{kind}: clave actual difiere del respaldo")
                obj = ASSET_KINDS[kind]["get_object"](resource)
                if obj is None:
                    problems.append(f"{kind}: objeto no encontrado en el bucket")
                    continue
                body = obj["Body"].read()
                if not body:
                    problems.append(f"{kind}: archivo vacío")
                if obj.get("ContentType") != "image/webp":
                    problems.append(f"{kind}: Content-Type != image/webp")
                with Image.open(BytesIO(body)) as image:
                    if image.width > MAX_WEB_IMAGE_SIZE[0] or image.height > MAX_WEB_IMAGE_SIZE[1]:
                        problems.append(f"{kind}: excede dimensiones máximas")
                original_bytes = entry["inspected"].get(kind, {}).get("original_bytes")
                if original_bytes and len(body) >= original_bytes:
                    problems.append(f"{kind}: no hubo reducción de peso")
                markdown_fragment = "?asset=infographic" if kind == "infographic" else "?asset=concept"
                if markdown_fragment not in resource.content:
                    problems.append(f"{kind}: no está insertada en Resource.content")

            if _question_fingerprint(resource) != entry["questions_fingerprint_before"]:
                problems.append("preguntas/alternativas cambiaron")
            if _metadata_fingerprint(resource) != entry["metadata_fingerprint_before"]:
                problems.append("metadatos del recurso cambiaron")

            if problems:
                drift += 1
                self.stdout.write(self.style.ERROR(f"[{entry['resource_id']}] {'; '.join(problems)}"))
            else:
                ok += 1
                self.stdout.write(self.style.SUCCESS(f"[{entry['resource_id']}] OK"))

        self.stdout.write(
            self.style.SUCCESS(f"Verificación: {ok}/{len(sample)} sin problemas, {drift} con drift.")
        )
