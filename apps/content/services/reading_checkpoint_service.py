"""Validation for formative checkpoints embedded in editorial guides."""

from __future__ import annotations

import re

from apps.content.services.checkpoint_matching import explanation_mentions_answer

CHECKPOINT_PLACEMENTS = (
    "after_concept_image",
    "after_guided_example",
    "after_errors",
)
CLASS_REFERENCE = re.compile(
    r"\b(según (?:la )?clase|esta clase|según el video|en el video|"
    r"modo (?:preparación|evaluación))\b",
    re.IGNORECASE,
)


def _text(value) -> str:
    return " ".join(str(value or "").split())


def normalize_reading_checkpoints(value) -> list[dict]:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError("La guía debe incluir exactamente tres comprobaciones intermedias.")

    normalized = []
    seen_questions = set()
    seen_placements = set()
    for index, checkpoint in enumerate(value, start=1):
        if not isinstance(checkpoint, dict):
            raise ValueError(f"Comprobación {index}: estructura inválida.")
        placement = _text(checkpoint.get("placement"))
        question = _text(checkpoint.get("question"))
        explanation = _text(checkpoint.get("explanation"))
        reinforcement_section = _text(checkpoint.get("reinforcement_section"))
        choices = checkpoint.get("choices")

        if placement not in CHECKPOINT_PLACEMENTS or placement in seen_placements:
            raise ValueError(f"Comprobación {index}: ubicación inválida o repetida.")
        if not question or question.casefold() in seen_questions:
            raise ValueError(f"Comprobación {index}: enunciado vacío o duplicado.")
        if CLASS_REFERENCE.search(question) or CLASS_REFERENCE.search(explanation):
            raise ValueError(f"Comprobación {index}: no puede referirse a la clase, video o modo.")
        if not explanation or not reinforcement_section:
            raise ValueError(f"Comprobación {index}: faltan explicación o ruta de refuerzo.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"Comprobación {index}: debe tener exactamente cuatro alternativas.")

        normalized_choices = []
        seen_choices = set()
        correct_count = 0
        correct_text = ""
        for choice_index, choice in enumerate(choices, start=1):
            if not isinstance(choice, dict):
                raise ValueError(f"Comprobación {index}, alternativa {choice_index}: estructura inválida.")
            choice_text = _text(choice.get("text"))
            choice_key = choice_text.casefold()
            is_correct = choice.get("is_correct") is True
            if not choice_text or choice_key in seen_choices:
                raise ValueError(f"Comprobación {index}: alternativas vacías o repetidas.")
            if CLASS_REFERENCE.search(choice_text):
                raise ValueError(
                    f"Comprobación {index}: una alternativa se refiere a la clase, video o modo."
                )
            seen_choices.add(choice_key)
            correct_count += int(is_correct)
            if is_correct:
                correct_text = choice_text
            normalized_choices.append({"text": choice_text, "is_correct": is_correct})

        if correct_count != 1:
            raise ValueError(f"Comprobación {index}: debe tener exactamente una alternativa correcta.")
        if not explanation_mentions_answer(correct_text, explanation):
            raise ValueError(
                f"Comprobación {index}: la explicación debe mencionar la alternativa correcta."
            )

        seen_questions.add(question.casefold())
        seen_placements.add(placement)
        normalized.append(
            {
                "placement": placement,
                "question": question,
                "choices": normalized_choices,
                "explanation": explanation,
                "reinforcement_section": reinforcement_section,
            }
        )

    if seen_placements != set(CHECKPOINT_PLACEMENTS):
        raise ValueError("Las comprobaciones no cubren las tres ubicaciones canónicas.")
    return normalized
