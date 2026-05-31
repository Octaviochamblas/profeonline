"""Lógica de negocio para el sistema de evaluación gamificada."""

from django.db.models import Max, Q

from apps.content.models import (
    Choice,
    Question,
    QuizAttempt,
    QuizAttemptAnswer,
)

# Preguntas por nivel: N1 y N2 = 5, N3 = 3
QUESTIONS_PER_LEVEL = {1: 5, 2: 5, 3: 3}

# Intentos máximos de evaluación por nivel
MAX_EVAL_ATTEMPTS = 3

# Porcentaje mínimo de preparación para recuperar un intento
PRACTICE_RECOVERY_THRESHOLD = 0.8  # 80%


def get_questions_for_quiz(resource, level, mode, count=None):
    """Selecciona preguntas aleatorias publicadas para un quiz.

    Retorna una lista de Question con choices prefetched.
    """
    if count is None:
        count = QUESTIONS_PER_LEVEL.get(level, 5)

    qs = Question.objects.filter(
        resource=resource,
        level=level,
        status="publicada",
    ).filter(
        Q(mode=mode) | Q(mode="ambas"),
    ).prefetch_related("choices")

    return list(qs.order_by("?")[:count])


def get_next_attempt_number(user, resource, level, mode):
    """Retorna el siguiente número de intento para un usuario/recurso/nivel/modo."""
    result = QuizAttempt.objects.filter(
        user=user,
        resource=resource,
        level=level,
        mode=mode,
    ).aggregate(max_num=Max("attempt_number"))
    return (result["max_num"] or 0) + 1


def get_attempts_info(user, resource, level):
    """Retorna información sobre intentos de evaluación de un nivel.

    Returns:
        dict con claves: used, remaining, max_reached, passed,
        best_score, can_recover.
    """
    eval_attempts = QuizAttempt.objects.filter(
        user=user,
        resource=resource,
        level=level,
        mode="evaluacion",
    )
    used = eval_attempts.count()
    passed = eval_attempts.filter(passed=True).exists()
    best = eval_attempts.order_by("-score").first()
    best_score = best.score if best else 0
    total = QUESTIONS_PER_LEVEL.get(level, 5)

    return {
        "used": used,
        "remaining": max(0, MAX_EVAL_ATTEMPTS - used),
        "max_reached": used >= MAX_EVAL_ATTEMPTS,
        "passed": passed,
        "best_score": best_score,
        "total": total,
        "can_recover": not passed and used >= MAX_EVAL_ATTEMPTS and _can_recover(
            user, resource, level
        ),
    }


def _can_recover(user, resource, level):
    """Verifica si la última preparación del nivel alcanza ≥80%."""
    last_practice = (
        QuizAttempt.objects.filter(
            user=user,
            resource=resource,
            level=level,
            mode="preparacion",
        )
        .order_by("-created_at")
        .first()
    )
    if not last_practice or last_practice.total == 0:
        return False
    return (last_practice.score / last_practice.total) >= PRACTICE_RECOVERY_THRESHOLD


def recover_attempt(user, resource, level):
    """Recupera 1 intento de evaluación eliminando el último fallido.

    Solo funciona si _can_recover() es True.
    Retorna True si se recuperó, False si no se pudo.
    """
    if not _can_recover(user, resource, level):
        return False

    # Eliminar el último intento fallido para liberar espacio
    last_failed = (
        QuizAttempt.objects.filter(
            user=user,
            resource=resource,
            level=level,
            mode="evaluacion",
            passed=False,
        )
        .order_by("-created_at")
        .first()
    )
    if last_failed:
        last_failed.delete()
        return True
    return False


def submit_quiz(user, resource, level, mode, answers_dict):
    """Envía respuestas de un quiz y crea el intento.

    Args:
        answers_dict: dict {question_id: choice_id}

    Returns:
        QuizAttempt con answers ya creadas.

    Raises:
        ValueError: si se exceden los intentos o el quiz está bloqueado.
    """
    total = QUESTIONS_PER_LEVEL.get(level, 5)

    if mode == "evaluacion":
        info = get_attempts_info(user, resource, level)
        if info["passed"]:
            raise ValueError("Ya aprobaste este nivel.")
        if info["max_reached"] and not info["can_recover"]:
            raise ValueError(
                "Has alcanzado el máximo de intentos. "
                "Practica para recuperar un intento."
            )
        # Si puede recuperar, hacerlo automáticamente antes del nuevo intento
        if info["max_reached"] and info["can_recover"]:
            recover_attempt(user, resource, level)

    question_ids = list(answers_dict.keys())
    questions = {
        question.pk: question
        for question in Question.objects.filter(
            pk__in=question_ids,
            resource=resource,
            level=level,
        ).prefetch_related("choices")
    }
    valid_choice_ids = {
        choice.pk
        for question in questions.values()
        for choice in question.choices.all()
    }

    attempt_number = get_next_attempt_number(user, resource, level, mode)
    score = 0
    answer_objects = []

    for question_id, choice_id in answers_dict.items():
        question = questions.get(question_id)
        if not question:
            continue

        if choice_id is None:
            is_correct = False
            choice = None
        elif choice_id not in valid_choice_ids:
            is_correct = False
            choice = None
        else:
            try:
                choice = question.choices.get(pk=choice_id)
                is_correct = choice.is_correct
            except Choice.DoesNotExist:
                is_correct = False
                choice = None

        if is_correct:
            score += 1

        answer_objects.append(
            QuizAttemptAnswer(
                question_id=question_id,
                selected_choice=choice,
                is_correct=is_correct,
            )
        )

    # Para aprobar: todas correctas (5/5 en N1/N2, 3/3 en N3)
    passed = score == total if mode == "evaluacion" else False

    attempt = QuizAttempt.objects.create(
        user=user,
        resource=resource,
        level=level,
        mode=mode,
        score=score,
        total=total,
        passed=passed,
        attempt_number=attempt_number,
    )

    for answer in answer_objects:
        answer.attempt = attempt
    QuizAttemptAnswer.objects.bulk_create(answer_objects)

    return attempt


def get_resource_mastery(user, resource):
    """Retorna el dominio de un usuario sobre un recurso.

    Returns:
        dict con claves: max_level_passed (0-3), stars, levels_info.
    """
    levels_info = {}
    max_level_passed = 0

    for level in (1, 2, 3):
        info = get_attempts_info(user, resource, level)
        levels_info[level] = info
        if info["passed"]:
            max_level_passed = level

    return {
        "max_level_passed": max_level_passed,
        "stars": max_level_passed,  # 1 star per level passed
        "levels_info": levels_info,
    }
