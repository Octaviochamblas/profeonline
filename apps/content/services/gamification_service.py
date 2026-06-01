"""Servicios de gamificacion: XP, skills, rangos y rachas."""

from datetime import timedelta

from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.utils import timezone

from apps.content.models import XPEvent, UserSkill, UserStreak

PRACTICE_XP = 5
PRACTICE_HIGH_SCORE_XP = 15
PRACTICE_REPEAT_XP = 2
PRACTICE_REPEAT_HIGH_SCORE_XP = 5
PRACTICE_FULL_XP_LIMIT = 3
RESOURCE_LEVEL_PASS_XP = {1: 25, 2: 40, 3: 60}
TOPIC_EXAM_PASS_XP = 100
SKILL_UNLOCK_XP = 50
DAILY_STREAK_XP = 10

RANKS = [
    {"name": "Explorador", "min_xp": 0, "min_skills": 0},
    {"name": "Aprendiz", "min_xp": 150, "min_skills": 1},
    {"name": "Practico", "min_xp": 400, "min_skills": 2},
    {"name": "Avanzado", "min_xp": 900, "min_skills": 4},
    {"name": "Experto", "min_xp": 1600, "min_skills": 7},
]


def _update_streak(user):
    today = timezone.localdate()
    streak, _ = UserStreak.objects.get_or_create(user=user)

    if streak.last_activity_date == today:
        return streak, False

    continued = streak.last_activity_date == today - timedelta(days=1)
    streak.current_count = streak.current_count + 1 if continued else 1
    streak.longest_count = max(streak.longest_count, streak.current_count)
    streak.last_activity_date = today
    streak.save(update_fields=["current_count", "longest_count", "last_activity_date", "updated_at"])
    return streak, continued


def award_xp(
    *,
    user,
    amount,
    event_type,
    event_key,
    resource=None,
    topic=None,
    quiz_attempt=None,
    topic_attempt=None,
    metadata=None,
    update_streak=True,
):
    """Crea un evento XP idempotente y actualiza racha si corresponde."""
    if amount <= 0:
        return None, False

    try:
        with transaction.atomic():
            event = XPEvent.objects.create(
                user=user,
                amount=amount,
                event_type=event_type,
                event_key=event_key,
                resource=resource,
                topic=topic,
                quiz_attempt=quiz_attempt,
                topic_attempt=topic_attempt,
                metadata=metadata or {},
            )
    except IntegrityError:
        return XPEvent.objects.filter(event_key=event_key).first(), False

    if update_streak:
        streak, continued = _update_streak(user)
        if continued:
            award_xp(
                user=user,
                amount=DAILY_STREAK_XP,
                event_type="streak_bonus",
                event_key=f"streak:{user.pk}:{streak.last_activity_date.isoformat()}",
                metadata={"streak_days": streak.current_count},
                update_streak=False,
            )

    return event, True


def award_quiz_attempt_xp(attempt):
    """Otorga XP por practica o aprobacion de nivel de recurso."""
    if attempt.mode == "preparacion":
        same_section_attempts = attempt.__class__.objects.filter(
            user=attempt.user,
            resource=attempt.resource,
            level=attempt.level,
            mode="preparacion",
            created_at__lte=attempt.created_at,
        ).count()
        high_score = attempt.total > 0 and (attempt.score / attempt.total) >= 0.8
        if same_section_attempts > PRACTICE_FULL_XP_LIMIT:
            amount = PRACTICE_REPEAT_HIGH_SCORE_XP if high_score else PRACTICE_REPEAT_XP
        else:
            amount = PRACTICE_HIGH_SCORE_XP if high_score else PRACTICE_XP

        return award_xp(
            user=attempt.user,
            amount=amount,
            event_type="practice",
            event_key=f"quiz-practice:{attempt.pk}",
            resource=attempt.resource,
            quiz_attempt=attempt,
            metadata={
                "level": attempt.level,
                "score": attempt.score,
                "total": attempt.total,
                "high_score": high_score,
                "same_section_attempts": same_section_attempts,
            },
        )

    if attempt.mode == "evaluacion" and attempt.passed:
        return award_xp(
            user=attempt.user,
            amount=RESOURCE_LEVEL_PASS_XP.get(attempt.level, 0),
            event_type="resource_level_pass",
            event_key=f"quiz-pass:{attempt.user_id}:{attempt.resource_id}:{attempt.level}",
            resource=attempt.resource,
            quiz_attempt=attempt,
            metadata={"level": attempt.level},
        )

    return None, False


def award_topic_exam_xp_and_skill(attempt):
    """Otorga XP y skill al aprobar por primera vez la evaluacion final de tema."""
    if not attempt.passed:
        return {"xp_created": False, "skill_created": False}

    _, xp_created = award_xp(
        user=attempt.user,
        amount=TOPIC_EXAM_PASS_XP,
        event_type="topic_exam_pass",
        event_key=f"topic-pass:{attempt.user_id}:{attempt.topic_id}",
        topic=attempt.topic,
        topic_attempt=attempt,
        metadata={"percentage": attempt.percentage},
    )

    skill_created = False
    skill, created = UserSkill.objects.get_or_create(
        user=attempt.user,
        topic=attempt.topic,
        defaults={
            "name": f"Dominio en {attempt.topic.name}",
            "unlocked_by_attempt": attempt,
        },
    )
    if created:
        skill_created = True
        award_xp(
            user=attempt.user,
            amount=SKILL_UNLOCK_XP,
            event_type="skill_unlock",
            event_key=f"skill-unlock:{attempt.user_id}:{attempt.topic_id}",
            topic=attempt.topic,
            topic_attempt=attempt,
            metadata={"skill_id": skill.pk},
        )

    return {"xp_created": xp_created, "skill_created": skill_created}


def get_user_xp_total(user):
    return XPEvent.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or 0


def get_user_rank(total_xp, skill_count):
    rank = RANKS[0]
    for candidate in RANKS:
        if total_xp >= candidate["min_xp"] and skill_count >= candidate["min_skills"]:
            rank = candidate
    return rank


def get_gamification_summary(user):
    total_xp = get_user_xp_total(user)
    skills = UserSkill.objects.filter(user=user).select_related("topic", "topic__subject")
    skill_count = skills.count()
    streak, _ = UserStreak.objects.get_or_create(user=user)
    rank = get_user_rank(total_xp, skill_count)

    return {
        "total_xp": total_xp,
        "rank": rank,
        "skill_count": skill_count,
        "skills": skills[:6],
        "streak": streak,
    }
