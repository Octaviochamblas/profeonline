"""Depura el banco existente de racionales y agrega el banco diversificado.

Por seguridad:
- el modo por defecto es dry-run;
- las repetidas se archivan, no se borran físicamente;
- se genera un respaldo JSON antes de cualquier escritura;
- toda la mutación ocurre dentro de una única transacción.
"""

import argparse
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.conf import settings
from django.db import transaction

from apps.content.models import Question, Resource
from apps.content.services.ai_generation_service import _save_questions
from scratch.generate_racionales_questions import (
    GENERATORS,
    NOMBRES,
    OBJETOS,
    audit_questions,
    build_all_questions,
)


CONFIRMATION = "ARCHIVAR_REPETIDAS_Y_POBLAR_RACIONALES"
MODE_BY_POSITION = ("preparacion", "evaluacion", "ambas")


def normalize_template(text):
    """Reduce un enunciado a su molde pedagógico, ignorando datos superficiales."""
    normalized = unicodedata.normalize("NFKC", text).lower()
    normalized = re.sub(r"\((?:caso|variación)\s+\d+\)", "", normalized)
    for name in sorted(set(NOMBRES), key=len, reverse=True):
        normalized = re.sub(rf"\b{re.escape(name.lower())}\b", "<nombre>", normalized)
    for obj in sorted(set(OBJETOS), key=len, reverse=True):
        normalized = normalized.replace(obj.lower(), "<objeto>")
        if obj.endswith("s"):
            normalized = normalized.replace(obj[:-1].lower(), "<objeto>")
    normalized = re.sub(r"\d+(?:[.,]\d+)?", "<n>", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip(" .")


def serialize_questions(queryset):
    payload = []
    for question in queryset.prefetch_related("choices").order_by("resource_id", "level", "order", "id"):
        payload.append(
            {
                "id": question.id,
                "resource_id": question.resource_id,
                "resource_slug": question.resource.slug,
                "level": question.level,
                "mode": question.mode,
                "text": question.text,
                "explanation": question.explanation,
                "status": question.status,
                "order": question.order,
                "created_at": question.created_at.isoformat(),
                "updated_at": question.updated_at.isoformat(),
                "choices": [
                    {
                        "id": choice.id,
                        "text": choice.text,
                        "is_correct": choice.is_correct,
                        "order": choice.order,
                    }
                    for choice in question.choices.all()
                ],
            }
        )
    return payload


def write_backup(resources):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = BASE_DIR / "backups" / f"racionales_questions_before_{timestamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    queryset = Question.objects.filter(resource__in=resources).select_related("resource")
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database_name": settings.DATABASES["default"].get("NAME"),
        "resources": list(resources.values_list("slug", flat=True)),
        "questions": serialize_questions(queryset),
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path, len(payload["questions"])


def build_plan(resources):
    generated = build_all_questions()
    plan = {}
    for resource in resources:
        existing = list(
            resource.questions.filter(status="publicada")
            .prefetch_related("choices")
            .order_by("level", "order", "id")
        )
        groups = defaultdict(list)
        for question in existing:
            groups[(question.level, normalize_template(question.text))].append(question)

        keep_ids = {questions[0].id for questions in groups.values()}
        archive_ids = [question.id for question in existing if question.id not in keep_ids]
        new_questions = generated[resource.slug]
        audit_questions(resource.slug, new_questions)
        existing_texts = set(resource.questions.values_list("text", flat=True))
        new_questions = [question for question in new_questions if question["text"] not in existing_texts]
        plan[resource.slug] = {
            "resource": resource,
            "published_before": len(existing),
            "kept_old": len(keep_ids),
            "archive_ids": archive_ids,
            "new_questions": new_questions,
        }
    return plan


def print_plan(plan):
    print("RECURSO\tPUBLICADAS_ANTES\tCONSERVAR\tARCHIVAR\tAGREGAR\tPUBLICADAS_DESPUES")
    for slug, item in plan.items():
        after = item["kept_old"] + len(item["new_questions"])
        print(
            f"{slug}\t{item['published_before']}\t{item['kept_old']}\t"
            f"{len(item['archive_ids'])}\t{len(item['new_questions'])}\t{after}"
        )
    print(
        "TOTAL\t"
        f"{sum(item['published_before'] for item in plan.values())}\t"
        f"{sum(item['kept_old'] for item in plan.values())}\t"
        f"{sum(len(item['archive_ids']) for item in plan.values())}\t"
        f"{sum(len(item['new_questions']) for item in plan.values())}\t"
        f"{sum(item['kept_old'] + len(item['new_questions']) for item in plan.values())}"
    )


def apply_plan(plan):
    with transaction.atomic():
        for item in plan.values():
            resource = item["resource"]
            Question.objects.filter(id__in=item["archive_ids"]).update(status="archivada")
            for level in (1, 2, 3):
                level_questions = item["new_questions"][(level - 1) * 30:level * 30]
                for mode_index, mode in enumerate(MODE_BY_POSITION):
                    batch = level_questions[mode_index * 10:(mode_index + 1) * 10]
                    _save_questions(
                        resource=resource,
                        level=level,
                        mode=mode,
                        questions_data=batch,
                        status="publicada",
                    )


def verify(plan):
    failures = []
    for slug, item in plan.items():
        resource = item["resource"]
        published = resource.questions.filter(status="publicada")
        expected = item["kept_old"] + len(item["new_questions"])
        if published.count() != expected:
            failures.append(f"{slug}: publicadas={published.count()}, esperado={expected}")
        for level in (1, 2, 3):
            for mode in MODE_BY_POSITION:
                generated_count = published.filter(
                    level=level,
                    mode=mode,
                    text__in=[
                        question["text"]
                        for question in item["new_questions"][(level - 1) * 30:level * 30]
                    ],
                ).count()
                if generated_count != 10:
                    failures.append(
                        f"{slug}: N{level}/{mode} contiene {generated_count} nuevas, esperado=10"
                    )
    if failures:
        raise RuntimeError("Verificación fallida: " + "; ".join(failures))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    resources = Resource.objects.filter(slug__in=GENERATORS).order_by("slug")
    if resources.count() != len(GENERATORS):
        found = set(resources.values_list("slug", flat=True))
        missing = sorted(set(GENERATORS) - found)
        raise RuntimeError(f"Faltan recursos esperados: {missing}")

    plan = build_plan(resources)
    print_plan(plan)
    if not args.apply:
        print("\nDRY-RUN: no se modificó la base de datos.")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la operación con DEBUG=True.")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Confirmación inválida; use --confirm {CONFIRMATION}")

    backup_path, backup_count = write_backup(resources)
    print(f"\nBACKUP_OK\t{backup_path}\t{backup_count} preguntas")
    apply_plan(plan)
    verify(plan)
    print("\nAPPLY_OK: repetidas archivadas y banco diversificado poblado.")


if __name__ == "__main__":
    main()
