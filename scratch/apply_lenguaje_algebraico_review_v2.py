"""Aplica el paquete v2 aprobado de Lenguaje Algebraico.

Archiva el banco vigente para preservar intentos/reportes y publica exactamente
90 preguntas nuevas por recurso. Dry-run por defecto; la escritura requiere una
frase explícita de confirmación.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
PACKAGE_PATH = (
    BASE_DIR / "scratch" / "review_lenguaje_algebraico_v2" / "package.json"
)
CONFIRMATION = "PUBLICAR_LENGUAJE_ALGEBRAICO_V2"
TOPIC_SLUG = "lenguaje-algebraico"
MODES = ("preparacion", "evaluacion", "ambas")

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.conf import settings
from django.db import transaction
from django.db.models import Count, Q

from apps.content.models import Choice, Question, Resource, ResourceQuizConfig


def load_package():
    payload = json.loads(PACKAGE_PATH.read_text(encoding="utf-8"))
    if payload.get("schema") != "profeonline.question-review/v2":
        raise RuntimeError("Esquema de paquete no soportado.")
    if payload.get("topic") != TOPIC_SLUG:
        raise RuntimeError("El paquete pertenece a otro tema.")
    if payload.get("question_count") != 1530:
        raise RuntimeError("El paquete no contiene 1.530 preguntas.")
    return payload


def validate_package(payload, resources):
    errors = []
    if set(payload["resources"]) != set(resources):
        errors.append("El inventario del paquete no coincide con producción.")
    seen_global = set()
    for slug, resource in resources.items():
        item = payload["resources"].get(slug)
        if not item:
            continue
        transcript_hash = hashlib.sha256(
            resource.transcript.encode("utf-8")
        ).hexdigest()
        if item.get("transcript_sha256") != transcript_hash:
            errors.append(f"{slug}: cambió la transcripción.")
        questions = item.get("questions") or []
        if len(questions) != 90:
            errors.append(f"{slug}: total={len(questions)}.")
        for level in (1, 2, 3):
            for mode in MODES:
                count = sum(
                    question.get("level") == level
                    and question.get("mode") == mode
                    for question in questions
                )
                if count != 10:
                    errors.append(f"{slug}: N{level}/{mode}={count}.")
        local_texts = set()
        for index, question in enumerate(questions, 1):
            text = " ".join(str(question.get("text", "")).lower().split())
            explanation = str(question.get("explanation", "")).strip()
            choices = question.get("choices") or []
            correct = sum(bool(choice.get("is_correct")) for choice in choices)
            choice_texts = [
                " ".join(str(choice.get("text", "")).lower().split())
                for choice in choices
            ]
            if not text or not explanation:
                errors.append(f"{slug}: P{index} incompleta.")
            if text in local_texts:
                errors.append(f"{slug}: P{index} duplicada dentro del recurso.")
            local_texts.add(text)
            if len(choices) != 4 or correct != 1:
                errors.append(f"{slug}: P{index} alternativas inválidas.")
            if len(choice_texts) != len(set(choice_texts)):
                errors.append(f"{slug}: P{index} distractores repetidos.")
            global_key = (slug, text)
            if global_key in seen_global:
                errors.append(f"{slug}: P{index} repetida globalmente.")
            seen_global.add(global_key)
    if errors:
        raise RuntimeError("\n".join(errors[:30]))


def write_backup(resources):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = BASE_DIR / "backups" / f"lenguaje_algebraico_before_v2_{timestamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    questions = (
        Question.objects.filter(resource__in=resources.values())
        .select_related("resource")
        .prefetch_related("choices")
        .order_by("resource_id", "id")
    )
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "topic": TOPIC_SLUG,
        "questions": [
            {
                "id": question.id,
                "resource_id": question.resource_id,
                "resource_slug": question.resource.slug,
                "level": question.level,
                "mode": question.mode,
                "status": question.status,
                "text": question.text,
                "explanation": question.explanation,
                "order": question.order,
                "audit_data": question.audit_data,
                "choices": [
                    {
                        "text": choice.text,
                        "is_correct": choice.is_correct,
                        "order": choice.order,
                    }
                    for choice in question.choices.all()
                ],
            }
            for question in questions
        ],
    }
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return path


def apply_package(payload, resources):
    backup = write_backup(resources)
    with transaction.atomic():
        locked_resources = {
            resource.slug: resource
            for resource in Resource.objects.select_for_update().filter(
                id__in=[resource.id for resource in resources.values()]
            )
        }
        current = Question.objects.select_for_update().filter(
            resource_id__in=[resource.id for resource in resources.values()],
            status="publicada",
        )
        archived_count = current.update(status="archivada")

        question_objects = []
        choice_payloads = []
        for slug, package_item in payload["resources"].items():
            resource = locked_resources[slug]
            transcript_hash = package_item["transcript_sha256"]
            level_orders = {1: 0, 2: 0, 3: 0}
            for item in package_item["questions"]:
                level = item["level"]
                level_orders[level] += 1
                audit_data = {
                    "editorial_source": "codex_transcript",
                    "transcript_sha256": transcript_hash,
                    "topic": TOPIC_SLUG,
                    "generator": "lenguaje_algebraico_v2",
                    "cognitive_type": item.get("cognitive_type", "aplicacion"),
                    "reviewed_before_publication": True,
                    "published_at": datetime.now(timezone.utc).isoformat(),
                }
                if item.get("_reference_id"):
                    audit_data["source_reference_question_id"] = item["_reference_id"]
                question = Question(
                    resource=resource,
                    level=level,
                    mode=item["mode"],
                    text=item["text"],
                    explanation=item["explanation"],
                    status="publicada",
                    order=level_orders[level],
                    audit_data=audit_data,
                )
                question_objects.append(question)
                choice_payloads.append((question, item["choices"]))

        Question.objects.bulk_create(question_objects, batch_size=500)
        Choice.objects.bulk_create(
            [
                Choice(
                    question=question,
                    text=choice["text"],
                    is_correct=choice["is_correct"],
                    order=index,
                )
                for question, choices in choice_payloads
                for index, choice in enumerate(choices, 1)
            ],
            batch_size=1000,
        )

        matrix = {
            (row["resource_id"], row["level"], row["mode"]): row["count"]
            for row in (
                Question.objects.filter(
                    resource_id__in=[
                        resource.id for resource in locked_resources.values()
                    ],
                    status="publicada",
                )
                .values("resource_id", "level", "mode")
                .annotate(count=Count("id"))
            )
        }
        for resource in locked_resources.values():
            for level in (1, 2, 3):
                for mode in MODES:
                    if matrix.get((resource.id, level, mode)) != 10:
                        raise RuntimeError(
                            f"{resource.slug}: matriz inválida N{level}/{mode}"
                        )
            ResourceQuizConfig.objects.update_or_create(
                resource=resource,
                defaults={
                    "counts": {
                        str(level): {
                            "practice": {"pool": 20, "shown": 5},
                            "eval": {
                                "pool": 20,
                                "shown": 5 if level < 3 else 3,
                            },
                        }
                        for level in (1, 2, 3)
                    }
                },
            )

        active = Question.objects.filter(
            resource_id__in=[resource.id for resource in locked_resources.values()],
            status="publicada",
        )
        if active.count() != 1530:
            raise RuntimeError("El total publicado final no es 1.530.")
        invalid_choices = (
            active.annotate(
                choice_count=Count("choices"),
                correct_count=Count(
                    "choices",
                    filter=Q(choices__is_correct=True),
                ),
            )
            .exclude(choice_count=4, correct_count=1)
            .count()
        )
        if invalid_choices:
            raise RuntimeError(
                f"Hay {invalid_choices} preguntas con alternativas inválidas."
            )
    return backup, archived_count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    payload = load_package()
    resources = {
        resource.slug: resource
        for resource in Resource.objects.filter(
            topic__slug=TOPIC_SLUG
        ).order_by("order", "id")
    }
    validate_package(payload, resources)
    current = Question.objects.filter(resource__in=resources.values())
    active = current.filter(status="publicada")
    active_v2 = active.filter(
        audit_data__generator="lenguaje_algebraico_v2"
    ).count()
    print(
        "VALIDATION_OK "
        f"resources={len(resources)} package_questions={payload['question_count']} "
        f"current={current.count()} "
        f"answered={current.filter(attempt_answers__isnull=False).distinct().count()} "
        f"reported={current.filter(error_reports__isnull=False).distinct().count()}"
    )
    if active.count() == 1530 and active_v2 == 1530:
        print("ALREADY_APPLIED published=1530 generator=lenguaje_algebraico_v2")
        return
    if not args.apply:
        print("DRY_RUN_OK")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la escritura con DEBUG=True.")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")
    backup, archived = apply_package(payload, resources)
    print(f"APPLY_OK archived={archived} published=1530 backup={backup}")


if __name__ == "__main__":
    main()
