"""Sincroniza transcripciones locales con los recursos publicados de producción.

Modo predeterminado: dry-run. La escritura exige --apply y confirmación.
Antes de modificar Resource.transcript crea un respaldo JSON completo.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_UPLOADER_DIR = BASE_DIR.parent.parent / "profeonline-uploader"
UPLOADER_DIR = Path(
    os.environ.get("PROFEONLINE_UPLOADER_DIR", DEFAULT_UPLOADER_DIR)
).expanduser().resolve()
TRANSCRIPTS_PATH = (
    UPLOADER_DIR / "editorial-packages" / "all-resource-transcripts.json"
)
CONFIRMATION = "SINCRONIZAR_TRANSCRIPCIONES_RECURSOS"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.conf import settings
from django.db import transaction

from apps.content.models import Resource


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    payload = read_json(TRANSCRIPTS_PATH)
    items = payload["items"]
    resources = list(Resource.objects.filter(is_published=True).order_by("id"))
    plan = []
    failures = []
    for resource in resources:
        current = (resource.transcript or "").strip()
        item = items.get(resource.slug)
        if len(current.split()) >= 80:
            plan.append((resource, current, "conservar"))
            continue
        if not item or item.get("status") != "ready":
            failures.append(resource.slug)
            continue
        text = (item.get("text") or "").strip()
        if len(text.split()) < 80:
            failures.append(resource.slug)
            continue
        plan.append((resource, text, "actualizar"))

    print(f"RECURSOS={len(resources)}")
    print(f"CONSERVAR={sum(action == 'conservar' for _, _, action in plan)}")
    print(f"ACTUALIZAR={sum(action == 'actualizar' for _, _, action in plan)}")
    print(f"FALTANTES={len(failures)}")
    if failures:
        raise RuntimeError(f"Hay recursos sin transcripción suficiente: {failures}")
    if not args.apply:
        print("DRY_RUN_OK")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la operación con DEBUG=True")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BASE_DIR / "backups" / f"resources_before_transcript_sync_{timestamp}.json"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database_name": settings.DATABASES["default"].get("NAME"),
        "resources": [
            {
                "id": resource.id,
                "slug": resource.slug,
                "title": resource.title,
                "video_url": resource.video_url,
                "transcript": resource.transcript,
            }
            for resource in resources
        ],
    }
    backup_path.write_text(
        json.dumps(backup, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with transaction.atomic():
        locked = {
            resource.id: resource
            for resource in Resource.objects.select_for_update().filter(
                id__in=[resource.id for resource in resources]
            )
        }
        for resource, text, action in plan:
            if action != "actualizar":
                continue
            target = locked[resource.id]
            target.transcript = text
            target.save(update_fields=["transcript"])

    missing_after = list(
        Resource.objects.filter(is_published=True)
        .filter(transcript="")
        .values_list("slug", flat=True)
    )
    insufficient_after = [
        resource.slug
        for resource in Resource.objects.filter(is_published=True).only(
            "slug", "transcript"
        )
        if len((resource.transcript or "").split()) < 80
    ]
    if missing_after or insufficient_after:
        raise RuntimeError(
            f"Verificación fallida: vacías={missing_after}, insuficientes={insufficient_after}"
        )
    print(f"BACKUP={backup_path}")
    print("SYNC_OK")


if __name__ == "__main__":
    main()
