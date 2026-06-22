"""Generation and selection services for the visible structured question bank."""

import random
import sys
from collections import defaultdict

from django.conf import settings
from django.db import transaction

from apps.content.models import Choice, Question, ResourceExerciseItem

MAX_GENERATION_COUNT = 50


def _generate_mock_visible_bank_candidates(exercise_item, resource, count):
    """Return deterministic candidates for tests and local development without keys."""
    difficulties = ["basica", "intermedia", "avanzada", "desafio"]
    return [
        {
            "text": (
                f"Pregunta simulada {index + 1} para el ítem "
                f"'{exercise_item.title}' sobre '{resource.title}'."
            ),
            "explanation": f"Explicación detallada {index + 1}.\n1. Paso uno.\n2. Paso dos.",
            "difficulty": difficulties[index % len(difficulties)],
            "hint": f"Pista simulada para la pregunta {index + 1}.",
            "choices": [
                {"text": f"Respuesta correcta {index + 1}", "is_correct": True},
                {"text": f"Distractor A {index + 1}", "is_correct": False},
                {"text": f"Distractor B {index + 1}", "is_correct": False},
                {"text": f"Distractor C {index + 1}", "is_correct": False},
            ],
        }
        for index in range(count)
    ]


def _validate_candidates(candidates, expected_count):
    if not isinstance(candidates, list) or len(candidates) != expected_count:
        raise ValueError("La IA no devolvió la cantidad exacta de preguntas solicitada.")

    validated = []
    for candidate in candidates:
        text = str(candidate.get("text", "")).strip()
        explanation = str(candidate.get("explanation", "")).strip()
        # Normaliza variantes acentuadas de la IA ('Básica'→'basica') a la clave canónica.
        difficulty = Question.normalize_difficulty(candidate.get("difficulty"))
        hint = str(candidate.get("hint", "")).strip()
        raw_choices = candidate.get("choices", [])

        if not text or not explanation or not difficulty or not hint:
            raise ValueError("Estructura de pregunta incompleta en la respuesta de la IA.")
        if not isinstance(raw_choices, list) or len(raw_choices) != 4:
            raise ValueError("Cada pregunta debe contener exactamente 4 alternativas.")

        choices = []
        for raw_choice in raw_choices:
            choice_text = str(raw_choice.get("text", "")).strip()
            if not choice_text:
                raise ValueError("El texto de la alternativa no puede estar vacío.")
            choices.append(
                {
                    "text": choice_text,
                    "is_correct": raw_choice.get("is_correct") is True,
                }
            )
        if len({choice["text"] for choice in choices}) != 4:
            raise ValueError("Las alternativas no pueden tener textos duplicados.")
        correct_choices = [choice for choice in choices if choice["is_correct"]]
        if len(correct_choices) != 1:
            raise ValueError("Debe haber exactamente una alternativa correcta por pregunta.")

        validated.append(
            {
                "text": text,
                "explanation": explanation,
                "difficulty": difficulty,
                "hint": hint,
                "choices": choices,
                "canonical_answer": correct_choices[0]["text"],
            }
        )
    return validated


def generate_visible_bank_questions(
    *,
    exercise_item,
    resource,
    learning_guide,
    count=None,
    api_key=None,
) -> list[Question]:
    """Generate validated draft questions for one item/resource link."""
    topic = resource.topic
    if not topic.structured_bank_enabled or not topic.is_active:
        raise ValueError("El tema no está activo o no tiene habilitado el banco estructurado.")
    if exercise_item.topic_id != topic.id or exercise_item.status != "aprobado":
        raise ValueError("El ítem debe estar aprobado y pertenecer al tema del recurso.")
    if not resource.is_published:
        raise ValueError("El recurso debe estar publicado.")
    if learning_guide.topic_id != topic.id:
        raise ValueError("La guía de aprendizaje no pertenece al tema.")
    if learning_guide.status != "publicada" or learning_guide.visibility != "publica":
        raise ValueError("La guía de aprendizaje debe estar publicada y ser pública.")

    try:
        resource_link = ResourceExerciseItem.objects.get(
            exercise_item=exercise_item,
            resource=resource,
        )
    except ResourceExerciseItem.DoesNotExist as exc:
        raise ValueError("No existe vínculo entre el ítem y el recurso.") from exc

    active_count = Question.objects.filter(
        exercise_item=exercise_item,
        resource=resource,
        scope="banco_visible",
        status__in=["borrador", "publicada"],
    ).count()
    quota = resource_link.practice_quota or exercise_item.detected_exercise_count
    if count is None:
        count = max(0, quota - active_count)
    try:
        count = int(count)
    except (TypeError, ValueError) as exc:
        raise ValueError("La cantidad debe ser un número entero.") from exc
    if count < 0 or count > MAX_GENERATION_COUNT:
        raise ValueError(f"La cantidad debe estar entre 0 y {MAX_GENERATION_COUNT}.")
    if count == 0:
        return []

    is_testing = "test" in sys.argv or getattr(settings, "TESTING", False)
    configured_key = (
        api_key
        or getattr(settings, "GEMINI_API_KEY", "")
        or getattr(settings, "OPENAI_API_KEY", "")
    )
    if is_testing or not configured_key:
        if settings.DEBUG or is_testing:
            candidates = _generate_mock_visible_bank_candidates(
                exercise_item, resource, count
            )
        else:
            raise ValueError("No se configuraron las llaves de los proveedores IA.")
    else:
        from apps.content.services.ai_generation_service import (
            generate_question_candidates,
        )

        candidates = generate_question_candidates(
            resource=resource,
            level=exercise_item.level,
            mode="preparacion",
            count=count,
            api_key=api_key,
            custom_instructions=(
                "Incluye obligatoriamente difficulty, hint y explanation. "
                "difficulty debe ser basica, intermedia, avanzada o desafio, "
                "calibrada al nivel educativo del recurso. Devuelve exactamente "
                "cuatro alternativas y una sola correcta."
            ),
        )

    validated = _validate_candidates(candidates, count)
    created = []
    with transaction.atomic():
        locked_link = ResourceExerciseItem.objects.select_for_update().get(
            pk=resource_link.pk
        )
        current_active = Question.objects.filter(
            exercise_item=exercise_item,
            resource=resource,
            scope="banco_visible",
            status__in=["borrador", "publicada"],
        ).count()
        current_quota = (
            locked_link.practice_quota or exercise_item.detected_exercise_count
        )
        validated = validated[: max(0, current_quota - current_active)]
        last_order = (
            Question.objects.filter(
                exercise_item=exercise_item,
                resource=resource,
                scope="banco_visible",
            )
            .order_by("-order")
            .values_list("order", flat=True)
            .first()
            or 0
        )

        for index, candidate in enumerate(validated, start=1):
            question = Question.objects.create(
                resource=resource,
                level=exercise_item.level,
                mode="preparacion",
                text=candidate["text"],
                explanation=candidate["explanation"],
                status="borrador",
                order=last_order + index,
                exercise_item=exercise_item,
                question_type="alternativa",
                difficulty=candidate["difficulty"],
                hint=candidate["hint"],
                canonical_answer=candidate["canonical_answer"],
                scope="banco_visible",
                learning_guide=learning_guide,
            )
            Choice.objects.bulk_create(
                [
                    Choice(
                        question=question,
                        text=choice["text"],
                        is_correct=choice["is_correct"],
                        order=choice_index,
                    )
                    for choice_index, choice in enumerate(
                        candidate["choices"], start=1
                    )
                ]
            )
            created.append(question)
        if created:
            learning_guide.resources.add(resource)
    return created


def select_visible_practice_questions(
    *,
    topic,
    item_id=None,
    resource_id=None,
    count=10,
    seed=None,
) -> list[Question]:
    """Select public visible-bank questions without academic side effects."""
    count = min(max(1, int(count)), 20)
    queryset = Question.objects.filter(
        status="publicada",
        scope="banco_visible",
        resource__topic=topic,
        resource__is_published=True,
        resource__topic__is_active=True,
        resource__topic__structured_bank_enabled=True,
        exercise_item__topic=topic,
        exercise_item__status="aprobado",
        learning_guide__topic=topic,
        learning_guide__status="publicada",
        learning_guide__visibility="publica",
    )
    if item_id:
        queryset = queryset.filter(exercise_item_id=item_id)
    if resource_id:
        queryset = queryset.filter(resource_id=resource_id)

    questions = list(
        queryset.select_related("resource", "exercise_item", "learning_guide")
        .prefetch_related("choices")
    )
    rng = random.Random(seed)
    rng.shuffle(questions)
    if item_id or resource_id:
        return questions[:count]

    groups = defaultdict(list)
    for question in questions:
        groups[(question.exercise_item_id, question.difficulty)].append(question)
    keys = sorted(groups)
    selected = []
    index = 0
    while len(selected) < count and keys:
        keys = [key for key in keys if groups[key]]
        if not keys:
            break
        key = keys[index % len(keys)]
        selected.append(groups[key].pop())
        index += 1
    return selected
