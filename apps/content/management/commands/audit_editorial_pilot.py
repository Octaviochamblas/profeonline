"""Read-only editorial audit and pilot selection for one subject at a time."""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from apps.content.models import (
    EvaluationSessionAnswer,
    NodeAssessmentAnswer,
    PublicationItem,
    Question,
    QuestionErrorReport,
    QuizAttemptAnswer,
    Resource,
)
from apps.content.services.editorial_guide_service import (
    REQUIRED_GUIDE_SECTIONS,
    has_current_infographic,
)
from apps.content.services.publication_pipeline_service import transcript_is_sufficient


CLASS_REFERENCE = re.compile(
    r"\b(según (?:la )?clase|esta clase|la clase\s*\d|clase\s*\d|al cerrar la clase|en esta lección|según el video|en el video|modo (?:preparación|evaluación))\b",
    re.IGNORECASE,
)
COSMETIC_PREFIX = re.compile(
    r"^(?:antes de una práctica guiada|en una evaluación donde debes justificar tu elección|al transferir lo aprendido a un ejercicio nuevo)\s*[:.-]*\s*",
    re.IGNORECASE,
)
RAW_MATH = re.compile(r"\b(?:Phi_[A-Za-z]|Delta\s*[A-Za-z]|lambda_[A-Za-z0-9]|sqrt\(|int(?:_|\s)|tanh\(|eps0|V_final|W_[A-Za-z])")


def normalize_question(value: str) -> str:
    return re.sub(r"\W+", " ", COSMETIC_PREFIX.sub("", value.lower())).strip()


def history_counts(resource: Resource) -> dict[str, int]:
    values = {
        "QuizAttemptAnswer": QuizAttemptAnswer.objects.filter(question__resource=resource).count(),
        "QuestionErrorReport": QuestionErrorReport.objects.filter(question__resource=resource).count(),
        "EvaluationSessionAnswer": EvaluationSessionAnswer.objects.filter(question__resource=resource).count(),
        "NodeAssessmentAnswer": 0,
    }
    if resource.related_node_id:
        values["NodeAssessmentAnswer"] = NodeAssessmentAnswer.objects.filter(
            question__node_id=resource.related_node_id
        ).count()
    return values


class Command(BaseCommand):
    help = "Audita una asignatura y propone un único recurso piloto, sin escribir datos."

    def add_arguments(self, parser):
        parser.add_argument("--subject", required=True, help="Slug de la asignatura a revisar.")
        parser.add_argument("--json", action="store_true", help="Emite el informe completo en JSON.")

    def handle(self, *args, **options):
        resources = list(
            Resource.objects.filter(subject__slug=options["subject"], is_published=True)
            .select_related("subject", "topic")
            .order_by("order", "id")
        )
        if not resources:
            raise CommandError("No hay recursos publicados para esa asignatura.")
        ids = [resource.id for resource in resources]
        items = {
            item.resource_id: item
            for item in PublicationItem.objects.select_related("canonical_guide").filter(resource_id__in=ids)
        }
        questions_by_resource = defaultdict(list)
        for question in Question.objects.filter(resource_id__in=ids).prefetch_related("choices").order_by("resource_id", "order", "id"):
            questions_by_resource[question.resource_id].append(question)

        entries = []
        for resource in resources:
            item = items.get(resource.id)
            guide = item.canonical_guide.content_text if item and item.canonical_guide_id else resource.content
            guide = guide or ""
            headings = re.findall(r"^##\s+(.+?)\s*$", guide, flags=re.MULTILINE)
            questions = questions_by_resource[resource.id]
            distribution = defaultdict(Counter)
            normalized = Counter()
            class_references = 0
            raw_math = 0
            for question in questions:
                distribution[str(question.level)][question.mode] += 1
                normalized[normalize_question(question.text)] += 1
                fields = [question.text, question.explanation] + [choice.text for choice in question.choices.all()]
                joined = "\n".join(fields)
                class_references += int(bool(CLASS_REFERENCE.search(joined)))
                raw_math += int(bool(RAW_MATH.search(joined)))
            history = history_counts(resource)
            blocked = {key: value for key, value in history.items() if value}
            target = {"1": {"ambas": 10}, "2": {"ambas": 10}, "3": {"ambas": 10}}
            actual_distribution = {key: dict(value) for key, value in distribution.items()}
            breaches = {
                "missing_transcript": not transcript_is_sufficient(resource.transcript),
                "guide_structure": headings != list(REQUIRED_GUIDE_SECTIONS),
                "infographic": not has_current_infographic(guide, resource),
                "question_scheme": actual_distribution != target,
                "class_references": class_references,
                "duplicates": sum(count - 1 for count in normalized.values() if count > 1),
                "raw_math": raw_math,
            }
            score = (
                5 * int(breaches["guide_structure"])
                + 3 * int(breaches["infographic"])
                + 3 * int(breaches["question_scheme"])
                + 2 * (class_references > 0)
                + 2 * (breaches["duplicates"] > 0)
                + 2 * (raw_math > 0)
            )
            entries.append(
                {
                    "id": resource.id,
                    "slug": resource.slug,
                    "title": resource.title,
                    "topic": resource.topic.slug if resource.topic else None,
                    "mechanism": "publication_item" if item else "direct_resource",
                    "transcript_ready": not breaches["missing_transcript"],
                    "questions_blocked_by_history": blocked,
                    "question_distribution": actual_distribution,
                    "breaches": breaches,
                    "pilot_score": score,
                }
            )

        eligible = [entry for entry in entries if entry["transcript_ready"] and not entry["questions_blocked_by_history"]]
        eligible.sort(key=lambda entry: (-entry["pilot_score"], entry["id"]))
        report = {
            "read_only": True,
            "subject": options["subject"],
            "resources": entries,
            "recommended_pilot": eligible[0] if eligible else None,
            "blocked_or_missing_transcript": len(entries) - len(eligible),
        }
        if options["json"]:
            self.stdout.write(json.dumps(report, ensure_ascii=False, indent=2))
            return
        pilot = report["recommended_pilot"]
        self.stdout.write(f"Asignatura: {report['subject']} | recursos: {len(entries)}")
        if pilot:
            self.stdout.write(
                f"Piloto recomendado: #{pilot['id']} {pilot['title']} (puntaje de brechas {pilot['pilot_score']})."
            )
        else:
            self.stdout.write(self.style.WARNING("No hay piloto elegible: faltan transcripciones o hay historial en todos los recursos."))
