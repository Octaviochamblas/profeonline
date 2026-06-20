from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import render

from apps.content.models import (
    Area,
    QuizAttemptAnswer,
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

LOW_SAMPLE_ANSWERS = 10


def _clean_id(value):
    """Normaliza un id de filtro (GET) a string numérico o "".

    Evita un 500 si llega un parámetro inválido (p. ej. ``?area=abc``): el id se
    usa luego en ``.filter(..._id=value)`` y un valor no entero reventaría la query.
    Devolver "" hace que el filtro se ignore (lo cubre el guard ``if filters[...]``).
    Se mantiene como string para no romper la comparación en los <select> del template.
    """
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return ""


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

        audit = resource.editorial_audit or {}
        transcript_audit = audit.get("transcript") or {}
        web_audit = audit.get("web") or {}
        youtube_audit = audit.get("youtube") or {}
        has_transcript = (
            bool(transcript_audit.get("available"))
            or len((resource.transcript or "").split()) >= 50
        )
        editorial_checks = {
            "transcript": has_transcript
            and bool(transcript_audit.get("audited", has_transcript)),
            "web_title": bool(web_audit.get("title_audited")),
            "web_description": bool(web_audit.get("description_audited")),
            "youtube_title": bool(youtube_audit.get("title_audited")),
            "youtube_description": bool(
                youtube_audit.get("description_audited")
            ),
        }
        editorial_complete = all(editorial_checks.values())

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
                "has_transcript": has_transcript,
                "editorial_checks": editorial_checks,
                "editorial_complete": editorial_complete,
                "editorial_pending": sum(
                    not value for value in editorial_checks.values()
                ),
                "editorial_audited_at": audit.get("audited_at"),
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
            "editorial_complete": sum(
                row["editorial_complete"] for row in rows
            ),
            "editorial_pending": sum(
                not row["editorial_complete"] for row in rows
            ),
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


def _accuracy(correct, answers):
    return round(correct / answers * 100, 1) if answers else 0.0


def _effectiveness_base(filters):
    queryset = QuizAttemptAnswer.objects.all()
    if filters["area"]:
        queryset = queryset.filter(
            Q(question__resource__subject__area_id=filters["area"])
            | Q(question__resource__topic__subject__area_id=filters["area"])
        )
    if filters["subject"]:
        queryset = queryset.filter(
            Q(question__resource__subject_id=filters["subject"])
            | Q(question__resource__topic__subject_id=filters["subject"])
        )
    if filters["topic"]:
        queryset = queryset.filter(question__resource__topic_id=filters["topic"])
    if filters["resource"]:
        queryset = queryset.filter(question__resource_id=filters["resource"])
    return queryset


def _effectiveness_annotations(user_ids):
    selected = Q()
    selected_correct = Q(is_correct=True)
    if user_ids:
        selected &= Q(attempt__user_id__in=user_ids)
        selected_correct &= Q(attempt__user_id__in=user_ids)
    return {
        "answers": Count("id", filter=selected, distinct=True),
        "correct": Count("id", filter=selected_correct, distinct=True),
        "students": Count(
            "attempt__user_id",
            filter=selected,
            distinct=True,
        ),
        "global_answers": Count("id", distinct=True),
        "global_correct": Count(
            "id",
            filter=Q(is_correct=True),
            distinct=True,
        ),
    }


def _format_effectiveness_rows(rows, label_builder):
    formatted = []
    for row in rows:
        answers = row["answers"]
        if not answers:
            continue
        accuracy = _accuracy(row["correct"], answers)
        global_accuracy = _accuracy(row["global_correct"], row["global_answers"])
        formatted.append(
            {
                **row,
                "label": label_builder(row),
                "accuracy": accuracy,
                "global_accuracy": global_accuracy,
                "delta": round(accuracy - global_accuracy, 1),
                "low_sample": answers < LOW_SAMPLE_ANSWERS,
            }
        )
    return sorted(formatted, key=lambda item: (item["accuracy"], -item["answers"]))


def _build_effectiveness_context(filters, user_ids):
    base = _effectiveness_base(filters)
    annotations = _effectiveness_annotations(user_ids)

    totals = base.aggregate(**annotations)
    totals["accuracy"] = _accuracy(totals["correct"], totals["answers"])
    totals["global_accuracy"] = _accuracy(
        totals["global_correct"],
        totals["global_answers"],
    )
    totals["delta"] = round(totals["accuracy"] - totals["global_accuracy"], 1)

    topic_rows = (
        base.values(
            "question__resource__topic_id",
            "question__resource__topic__name",
            "question__resource__topic__subject__name",
        )
        .annotate(**annotations)
    )
    topics = _format_effectiveness_rows(
        topic_rows,
        lambda row: row["question__resource__topic__name"] or "Sin tema",
    )

    resource_rows = (
        base.values(
            "question__resource_id",
            "question__resource__slug",
            "question__resource__title",
            "question__resource__topic__name",
        )
        .annotate(**annotations)
    )
    resources = _format_effectiveness_rows(
        resource_rows,
        lambda row: row["question__resource__title"],
    )

    question_rows = (
        base.values(
            "question_id",
            "question__text",
            "question__level",
            "question__mode",
            "question__resource__slug",
            "question__resource__title",
            "question__resource__topic__name",
        )
        .annotate(**annotations)
    )
    questions = _format_effectiveness_rows(
        question_rows,
        lambda row: row["question__text"],
    )
    mode_labels = {
        "preparacion": "Práctica",
        "evaluacion": "Evaluación",
        "ambas": "Ambas",
    }
    for question in questions:
        question["mode_label"] = mode_labels.get(
            question["question__mode"],
            question["question__mode"],
        )

    return {
        "totals": totals,
        "topic_stats": topics,
        "resource_stats": resources,
        "question_stats": questions,
    }


@user_passes_test(is_admin)
def bank_results(request):
    filters = {
        "area": _clean_id(request.GET.get("area", "")),
        "subject": _clean_id(request.GET.get("subject", "")),
        "topic": _clean_id(request.GET.get("topic", "")),
        "user": _clean_id(request.GET.get("user", "")),
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


@user_passes_test(is_admin)
def bank_effectiveness(request):
    user_ids = []
    for raw_id in request.GET.getlist("users"):
        try:
            user_ids.append(int(raw_id))
        except (TypeError, ValueError):
            continue
    user_ids = list(dict.fromkeys(user_ids))
    filters = {
        "area": _clean_id(request.GET.get("area", "")),
        "subject": _clean_id(request.GET.get("subject", "")),
        "topic": _clean_id(request.GET.get("topic", "")),
        "resource": _clean_id(request.GET.get("resource", "")),
    }
    effectiveness = _build_effectiveness_context(filters, user_ids)
    users_with_answers = (
        User.objects.filter(quiz_attempts__answers__isnull=False)
        .distinct()
        .order_by("last_name", "first_name", "username")
    )
    selected_users = list(users_with_answers.filter(id__in=user_ids))
    context = {
        **effectiveness,
        "filters": filters,
        "selected_user_ids": user_ids,
        "selected_users": selected_users,
        "users_with_answers": users_with_answers,
        "areas": Area.objects.all(),
        "subjects": Subject.objects.select_related("area").all(),
        "topics": Topic.objects.select_related("subject").all(),
        "resources": Resource.objects.select_related("subject", "topic").all(),
        "low_sample_answers": LOW_SAMPLE_ANSWERS,
    }
    return render(request, "pages/bank_effectiveness.html", context)
