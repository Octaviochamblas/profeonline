from django.db.models import Max
from apps.content.models import (
    NodeAssessmentQuestion,
    NodeAssessmentChoice,
    NodeAssessmentAttempt,
    NodeAssessmentAnswer,
)

MAX_EVAL_ATTEMPTS = 3
PASS_THRESHOLD = 0.8
QUESTIONS_PER_LEVEL = 7


def get_questions_for_assessment(node, level):
    """Selecciona hasta 7 preguntas aleatorias publicadas para la evaluación formal.

    Retorna una lista de NodeAssessmentQuestion con choices prefetched.
    """
    qs = NodeAssessmentQuestion.objects.filter(
        node=node,
        level=level,
        status=NodeAssessmentQuestion.STATUS_PUBLICADA,
    ).prefetch_related("choices")

    return list(qs.order_by("?")[:QUESTIONS_PER_LEVEL])


def get_next_attempt_number(user, node, level):
    """Retorna el siguiente número de intento para un usuario/nodo/nivel."""
    result = NodeAssessmentAttempt.objects.filter(
        user=user,
        node=node,
        level=level,
    ).aggregate(max_num=Max("attempt_number"))
    return (result["max_num"] or 0) + 1


def get_attempts_info(user, node, level):
    """Retorna información sobre intentos de evaluación de un nivel del nodo."""
    attempts = NodeAssessmentAttempt.objects.filter(
        user=user,
        node=node,
        level=level,
    )
    used = attempts.count()
    passed = attempts.filter(passed=True).exists()
    best = attempts.order_by("-score").first()
    best_score = best.score if best else 0

    return {
        "used": used,
        "remaining": max(0, MAX_EVAL_ATTEMPTS - used),
        "max_reached": used >= MAX_EVAL_ATTEMPTS,
        "passed": passed,
        "best_score": best_score,
        "total": QUESTIONS_PER_LEVEL,
    }


def submit_assessment(user, node, level, answers_dict):
    """Envía respuestas de evaluación formal para un nodo de conocimiento y crea el intento.

    Args:
        answers_dict: dict {question_id: choice_id|None}

    Returns:
        NodeAssessmentAttempt creado.

    Raises:
        ValueError: si se exceden los intentos o ya aprobó.
    """
    info = get_attempts_info(user, node, level)
    if info["passed"]:
        raise ValueError("Ya aprobaste este nivel.")
    if info["max_reached"]:
        raise ValueError("Has alcanzado el máximo de intentos (3/3) para este nivel.")

    question_ids = list(answers_dict.keys())
    questions = {
        question.pk: question
        for question in NodeAssessmentQuestion.objects.filter(
            pk__in=question_ids,
            node=node,
            status=NodeAssessmentQuestion.STATUS_PUBLICADA,
        ).prefetch_related("choices")
    }

    # El total real es la cantidad de preguntas enviadas
    total = len(questions)
    if total == 0:
        raise ValueError("No se encontraron preguntas válidas para este intento.")

    attempt_number = get_next_attempt_number(user, node, level)
    score = 0
    answer_objects = []

    for question_id, choice_id in answers_dict.items():
        question = questions.get(question_id)
        if not question:
            continue

        selected_choice = None
        is_correct = False

        if choice_id is not None:
            try:
                selected_choice = question.choices.get(pk=choice_id)
                is_correct = selected_choice.is_correct
            except NodeAssessmentChoice.DoesNotExist:
                pass

        if is_correct:
            score += 1

        answer_objects.append(
            NodeAssessmentAnswer(
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct,
            )
        )

    passed = (score / total) >= PASS_THRESHOLD if total > 0 else False

    attempt = NodeAssessmentAttempt.objects.create(
        user=user,
        node=node,
        level=level,
        score=score,
        total=total,
        passed=passed,
        attempt_number=attempt_number,
    )

    for answer in answer_objects:
        answer.attempt = attempt
    NodeAssessmentAnswer.objects.bulk_create(answer_objects)

    return attempt


def get_node_mastery(user, node):
    """Calcula el dominio de un usuario sobre un nodo (0 a 3 estrellas)."""
    if not user.is_authenticated:
        return {
            "stars": 0,
            "levels_info": {
                1: {"passed": False},
                2: {"passed": False},
                3: {"passed": False},
            }
        }

    levels_info = {}
    stars = 0

    for level in (1, 2, 3):
        info = get_attempts_info(user, node, level)
        levels_info[level] = info
        if info["passed"]:
            stars += 1

    return {
        "stars": stars,
        "levels_info": levels_info,
    }
