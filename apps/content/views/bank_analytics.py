from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import render

from apps.content.models import (
    Area,
    QuizAttempt,
    QuizGuide,
    Resource,
    Subject,
    Topic,
    TopicEvaluationAttempt,
)
from apps.content.services.evaluation_service import get_quiz_config
from apps.content.views.permissions import is_admin


User = get_user_model()

CELL_DEFINITIONS = (
    (1, "practice", "Práctica"),
    (1, "eval", "Evaluación"),
    (2, "practice", "Práctica"),
    (2, "eval", "Evaluación"),
    (3, "practice", "Práctica"),
    (3, "eval", "Evaluación"),
)


def _question_count_annotations():
    annotations = {
        "published_total": Count(
            "questions",
            filter=Q(questions__status="publicada"),
            distinct=True,
        ),
        "draft_total": Count(
            "questions",
            filter=Q(questions__status="borrador"),
            distinct=True,
        ),
    }
    for level, mode_key, _label in CELL_DEFINITIONS:
        mode = "preparacion" if mode_key == "practice" else "evaluacion"
        annotations[f"published_l{level}_{mode_key}"] = Count(
            "questions",
            filter=Q(
                questions__status="publicada",
                questions__level=level,
            )
            & (Q(questions__mode=mode) | Q(questions__mode="ambas")),
            distinct=True,
        )
    return annotations


def _coverage_queryset():
    active_guides = QuizGuide.objects.filter(is_active=True)
    return (
        Resource.objects.select_related(
            "subject__area",
            "topic__subject__area",
            "quiz_config",
        )
        .annotate(
            **_question_count_annotations(),
            has_direct_guide=Exists(
                active_guides.filter(resources=OuterRef("pk"))
            ),
            has_topic_guide=Exists(
                active_guides.filter(topics=OuterRef("topic_id"))
            ),
            has_subject_guide=Exists(
                active_guides.filter(subjects=OuterRef("subject_id"))
            ),
            has_topic_subject_guide=Exists(
                active_guides.filter(subjects=OuterRef("topic__subject_id"))
            ),
        )
        .order_by(
            "subject__area__order",
            "subject__area__name",
            "subject__name",
            "topic__name",
            "title",
        )
    )


def _build_coverage_rows():
    rows = []
    for resource in _coverage_queryset():
        subject = resource.subject or getattr(resource.topic, "subject", None)
        area = getattr(subject, "area", None)
        config = get_quiz_config(resource)
        cells = []
        cells_by_level = {1: {}, 2: {}, 3: {}}
        total_missing = 0

        for level, mode_key, mode_label in CELL_DEFINITIONS:
            settings = config.counts[str(level)][mode_key]
            available = getattr(resource, f"published_l{level}_{mode_key}")
            pool = settings["pool"]
            shown = settings["shown"]
            missing = max(pool - available, 0)
            total_missing += missing
            if available == 0:
                state = "empty"
            elif missing:
                state = "partial"
            else:
                state = "complete"
            cell = {
                "level": level,
                "mode_key": mode_key,
                "mode_label": mode_label,
                "available": available,
                "pool": pool,
                "shown": shown,
                "missing": missing,
                "state": state,
            }
            cells.append(cell)
            cells_by_level[level][mode_key] = cell

        if resource.published_total == 0:
            overall_state = "empty"
        elif total_missing:
            overall_state = "partial"
        else:
            overall_state = "complete"

        rows.append(
            {
                "resource": resource,
                "area": area,
                "subject": subject,
                "topic": resource.topic,
                "cells": cells,
                "levels": [
                    {
                        "level": level,
                        "practice": cells_by_level[level]["practice"],
                        "eval": cells_by_level[level]["eval"],
                    }
                    for level in (1, 2, 3)
                ],
                "published_total": resource.published_total,
                "draft_total": resource.draft_total,
                "total_missing": total_missing,
                "overall_state": overall_state,
                "has_video": bool(resource.video_url),
                "has_transcript": bool(resource.transcript.strip()),
                "has_guide": (
                    resource.has_direct_guide
                    or resource.has_topic_guide
                    or resource.has_subject_guide
                    or resource.has_topic_subject_guide
                ),
            }
        )
    return rows


@user_passes_test(is_admin)
def bank_coverage(request):
    rows = _build_coverage_rows()
    context = {
        "rows": rows,
        "areas": Area.objects.filter(
            Q(subjects__resources__isnull=False)
            | Q(subjects__topics__resources__isnull=False)
        ).distinct(),
        "subjects": Subject.objects.filter(
            Q(resources__isnull=False) | Q(topics__resources__isnull=False)
        )
        .select_related("area")
        .distinct(),
        "topics": Topic.objects.filter(resources__isnull=False)
        .select_related("subject")
        .distinct(),
        "totals": {
            "resources": len(rows),
            "empty": sum(row["overall_state"] == "empty" for row in rows),
            "published": sum(row["published_total"] for row in rows),
            "missing": sum(row["total_missing"] for row in rows),
        },
    }
    return render(request, "pages/bank_coverage.html", context)


def _attempt_rows(filters):
    quiz_attempts = QuizAttempt.objects.select_related(
        "user",
        "resource__subject__area",
        "resource__topic",
    )
    if filters["area"]:
        quiz_attempts = quiz_attempts.filter(
            Q(resource__subject__area_id=filters["area"])
            | Q(resource__topic__subject__area_id=filters["area"])
        )
    if filters["subject"]:
        quiz_attempts = quiz_attempts.filter(
            Q(resource__subject_id=filters["subject"])
            | Q(resource__topic__subject_id=filters["subject"])
        )
    if filters["topic"]:
        quiz_attempts = quiz_attempts.filter(resource__topic_id=filters["topic"])
    if filters["user"]:
        quiz_attempts = quiz_attempts.filter(user_id=filters["user"])

    topic_attempts = TopicEvaluationAttempt.objects.select_related(
        "user",
        "topic__subject__area",
    )
    if filters["area"]:
        topic_attempts = topic_attempts.filter(topic__subject__area_id=filters["area"])
    if filters["subject"]:
        topic_attempts = topic_attempts.filter(topic__subject_id=filters["subject"])
    if filters["topic"]:
        topic_attempts = topic_attempts.filter(topic_id=filters["topic"])
    if filters["user"]:
        topic_attempts = topic_attempts.filter(user_id=filters["user"])

    rows = []
    for attempt in quiz_attempts:
        percentage = round(attempt.score / attempt.total * 100) if attempt.total else 0
        subject = attempt.resource.subject or getattr(
            attempt.resource.topic,
            "subject",
            None,
        )
        rows.append(
            {
                "kind": "Recurso",
                "user": attempt.user,
                "area": getattr(subject, "area", None),
                "subject": subject,
                "topic": attempt.resource.topic,
                "target": attempt.resource.title,
                "target_key": f"resource-{attempt.resource_id}",
                "level": f"N{attempt.level}",
                "mode": attempt.get_mode_display(),
                "score": attempt.score,
                "total": attempt.total,
                "percentage": percentage,
                "passed": attempt.passed,
                "attempt_number": attempt.attempt_number,
                "created_at": attempt.created_at,
            }
        )
    for attempt in topic_attempts:
        rows.append(
            {
                "kind": "Tema",
                "user": attempt.user,
                "area": attempt.topic.subject.area,
                "subject": attempt.topic.subject,
                "topic": attempt.topic,
                "target": attempt.topic.name,
                "target_key": f"topic-{attempt.topic_id}",
                "level": "Final",
                "mode": "Evaluación",
                "score": attempt.score,
                "total": attempt.total,
                "percentage": attempt.percentage,
                "passed": attempt.passed,
                "attempt_number": attempt.attempt_number,
                "created_at": attempt.created_at,
            }
        )
    return sorted(rows, key=lambda row: row["created_at"], reverse=True)


def _aggregate_results(rows, key_name):
    groups = defaultdict(
        lambda: {
            "attempts": 0,
            "passed": 0,
            "percentage_sum": 0,
            "users": set(),
        }
    )
    for row in rows:
        if key_name == "student":
            key = row["user"].pk
            label = row["user"].get_full_name() or row["user"].get_username()
        else:
            key = row["target_key"]
            label = f'{row["kind"]}: {row["target"]}'
        group = groups[key]
        group["label"] = label
        group["attempts"] += 1
        group["passed"] += int(row["passed"])
        group["percentage_sum"] += row["percentage"]
        group["users"].add(row["user"].pk)

    results = []
    for group in groups.values():
        attempts = group["attempts"]
        results.append(
            {
                "label": group["label"],
                "attempts": attempts,
                "students": len(group["users"]),
                "average": round(group["percentage_sum"] / attempts, 1),
                "pass_rate": round(group["passed"] / attempts * 100, 1),
            }
        )
    return sorted(results, key=lambda item: (-item["attempts"], item["label"].lower()))


@user_passes_test(is_admin)
def bank_results(request):
    filters = {
        "area": request.GET.get("area", ""),
        "subject": request.GET.get("subject", ""),
        "topic": request.GET.get("topic", ""),
        "user": request.GET.get("user", ""),
    }
    group_by = request.GET.get("group_by", "student")
    if group_by not in {"student", "resource"}:
        group_by = "student"

    rows = _attempt_rows(filters)
    users_with_attempts = User.objects.filter(
        Q(quiz_attempts__isnull=False) | Q(topic_eval_attempts__isnull=False)
    ).distinct()
    context = {
        "rows": rows,
        "summary": _aggregate_results(rows, group_by),
        "group_by": group_by,
        "filters": filters,
        "areas": Area.objects.all(),
        "subjects": Subject.objects.select_related("area").all(),
        "topics": Topic.objects.select_related("subject").all(),
        "users_with_attempts": users_with_attempts,
    }
    return render(request, "pages/bank_results.html", context)
