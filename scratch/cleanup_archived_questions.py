"""Borra preguntas archivadas sin historial y audita el banco activo.

El modo predeterminado es dry-run. La escritura exige ``--apply`` y una frase
de confirmación. Antes del borrado se crea un respaldo JSON completo.
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

from apps.content.models import Choice, Question


CONFIRMATION = "BORRAR_PREGUNTAS_ARCHIVADAS"
EXPECTED_ARCHIVED = 1351
EXPECTED_ACTIVE = 2476


def normalized_text(text):
    return re.sub(
        r"\s+",
        " ",
        unicodedata.normalize("NFKC", text).strip().lower(),
    )


def structural_template(text):
    text = normalized_text(text)
    text = re.sub(r"\((?:caso|variación)\s+\d+\)", "", text)
    text = re.sub(r"\d+(?:[.,]\d+)?", "<n>", text)
    return re.sub(r"\s+", " ", text).strip()


def serialize_questions(queryset):
    payload = []
    for question in queryset.select_related(
        "resource",
        "resource__topic",
        "resource__subject",
    ).prefetch_related("choices").order_by("resource_id", "level", "order", "id"):
        payload.append(
            {
                "id": question.id,
                "resource_id": question.resource_id,
                "resource_slug": question.resource.slug,
                "topic_slug": question.resource.topic.slug if question.resource.topic else None,
                "subject_slug": question.resource.subject.slug if question.resource.subject else None,
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


def dependency_counts(queryset):
    return {
        "questions_with_answers": queryset.filter(
            attempt_answers__isnull=False
        ).distinct().count(),
        "answer_rows": sum(
            question.attempt_answers.count()
            for question in queryset.prefetch_related("attempt_answers")
        ),
        "questions_with_reports": queryset.filter(
            error_reports__isnull=False
        ).distinct().count(),
        "report_rows": sum(
            question.error_reports.count()
            for question in queryset.prefetch_related("error_reports")
        ),
    }


def active_counts_by_resource():
    counts = defaultdict(int)
    for resource_id in Question.objects.exclude(status="archivada").values_list(
        "resource_id", flat=True
    ):
        counts[resource_id] += 1
    return dict(counts)


def build_audit():
    active = list(
        Question.objects.exclude(status="archivada")
        .select_related("resource", "resource__topic", "resource__subject")
        .order_by("resource_id", "level", "mode", "order", "id")
    )
    exact_groups = defaultdict(list)
    structural_groups = defaultdict(list)
    for question in active:
        base_key = (question.resource_id, question.level)
        exact_groups[base_key + (normalized_text(question.text),)].append(question)
        structural_groups[base_key + (structural_template(question.text),)].append(question)

    exact_duplicates = [group for group in exact_groups.values() if len(group) > 1]
    candidates = [group for group in structural_groups.values() if len(group) > 1]
    candidates.sort(key=lambda group: (-len(group), group[0].resource.slug, group[0].level))

    groups = []
    for index, questions in enumerate(candidates, 1):
        first = questions[0]
        groups.append(
            {
                "group": index,
                "resource": {
                    "id": first.resource_id,
                    "slug": first.resource.slug,
                    "title": first.resource.title,
                },
                "topic": {
                    "slug": first.resource.topic.slug if first.resource.topic else None,
                    "name": first.resource.topic.name if first.resource.topic else None,
                },
                "subject": {
                    "slug": first.resource.subject.slug if first.resource.subject else None,
                    "name": first.resource.subject.name if first.resource.subject else None,
                },
                "level": first.level,
                "modes": sorted({question.mode for question in questions}),
                "template": structural_template(first.text),
                "count": len(questions),
                "recommendation": (
                    "Revisar manualmente; la similitud estructural no demuestra duplicidad "
                    "pedagógica y no se recomienda borrado automático."
                ),
                "questions": [
                    {
                        "id": question.id,
                        "mode": question.mode,
                        "status": question.status,
                        "text": question.text,
                    }
                    for question in questions
                ],
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "active_questions": len(active),
        "exact_duplicate_groups": len(exact_duplicates),
        "exact_duplicate_excess": sum(len(group) - 1 for group in exact_duplicates),
        "structural_candidate_groups": len(groups),
        "structural_candidate_questions": sum(group["count"] for group in groups),
        "structural_candidate_excess": sum(group["count"] - 1 for group in groups),
        "groups": groups,
    }


def markdown_report(audit):
    lines = [
        "# Auditoría global del banco de preguntas — 2026-06-19",
        "",
        "## Resumen",
        "",
        f"- Preguntas activas auditadas: **{audit['active_questions']}**.",
        f"- Grupos duplicados textualmente: **{audit['exact_duplicate_groups']}**.",
        f"- Grupos estructuralmente similares: **{audit['structural_candidate_groups']}**.",
        f"- Preguntas incluidas en esos grupos: **{audit['structural_candidate_questions']}**.",
        f"- Exceso estructural teórico: **{audit['structural_candidate_excess']}**.",
        "",
        "> La similitud estructural solo identifica candidatos de revisión. Cambiar números puede ser",
        "> una práctica válida; este informe no autoriza eliminación automática.",
        "",
        "## Grupos candidatos",
        "",
    ]
    for group in audit["groups"]:
        lines.extend(
            [
                f"### Grupo {group['group']} — {group['resource']['title']}",
                "",
                f"- Recurso: `{group['resource']['slug']}`",
                f"- Tema: `{group['topic']['slug']}`",
                f"- Nivel: **{group['level']}** · Modos: {', '.join(group['modes'])}",
                f"- Cantidad: **{group['count']}**",
                f"- Molde: `{group['template']}`",
                f"- Recomendación: {group['recommendation']}",
                "",
            ]
        )
        for question in group["questions"]:
            lines.append(
                f"- `#{question['id']}` · `{question['mode']}` — {question['text']}"
            )
        lines.append("")
    return "\n".join(lines)


def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    archived = Question.objects.filter(status="archivada")
    archived_count = archived.count()
    active_count = Question.objects.exclude(status="archivada").count()
    dependencies = dependency_counts(archived)
    audit = build_audit()

    print(f"ARCHIVED={archived_count}")
    print(f"ACTIVE={active_count}")
    print(f"DEPENDENCIES={dependencies}")
    print(
        "AUDIT="
        f"exact:{audit['exact_duplicate_groups']} "
        f"structural:{audit['structural_candidate_groups']} "
        f"questions:{audit['structural_candidate_questions']}"
    )

    if archived_count != EXPECTED_ARCHIVED or active_count != EXPECTED_ACTIVE:
        raise RuntimeError(
            f"Conteos inesperados: archivadas={archived_count}, activas={active_count}"
        )
    if any(dependencies.values()):
        raise RuntimeError(f"Hay dependencias asociadas a preguntas archivadas: {dependencies}")
    if not args.apply:
        print("DRY_RUN_OK: no se modificó la base ni se escribieron artefactos.")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la operación con DEBUG=True.")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BASE_DIR / "backups" / f"archived_questions_before_delete_{timestamp}.json"
    backup = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database_name": settings.DATABASES["default"].get("NAME"),
        "question_count": archived_count,
        "dependencies": dependencies,
        "questions": serialize_questions(archived),
    }
    write_json(backup_path, backup)
    if len(json.loads(backup_path.read_text(encoding="utf-8"))["questions"]) != archived_count:
        raise RuntimeError("El respaldo no contiene todas las preguntas archivadas.")

    before_by_resource = active_counts_by_resource()
    with transaction.atomic():
        locked = Question.objects.select_for_update().filter(status="archivada")
        if locked.count() != archived_count:
            raise RuntimeError("Cambió el conjunto de preguntas archivadas durante la operación.")
        locked_dependencies = dependency_counts(locked)
        if any(locked_dependencies.values()):
            raise RuntimeError(f"Aparecieron dependencias durante la operación: {locked_dependencies}")
        deleted_summary = locked.delete()

    after_by_resource = active_counts_by_resource()
    if Question.objects.filter(status="archivada").exists():
        raise RuntimeError("Persisten preguntas archivadas después del borrado.")
    if Question.objects.exclude(status="archivada").count() != EXPECTED_ACTIVE:
        raise RuntimeError("Cambió el conteo de preguntas activas.")
    if before_by_resource != after_by_resource:
        raise RuntimeError("Cambió el conteo activo de uno o más recursos.")
    if Choice.objects.filter(question__isnull=True).exists():
        raise RuntimeError("Se detectaron alternativas huérfanas.")

    report_base = BASE_DIR / "docs" / "auditorias" / "2026-06-19-auditoria-global-preguntas"
    write_json(report_base.with_suffix(".json"), audit)
    report_base.with_suffix(".md").write_text(markdown_report(audit), encoding="utf-8")

    print(f"BACKUP={backup_path}")
    print(f"DELETED={deleted_summary}")
    print(f"REPORT_MD={report_base.with_suffix('.md')}")
    print(f"REPORT_JSON={report_base.with_suffix('.json')}")
    print("APPLY_OK")


if __name__ == "__main__":
    main()
