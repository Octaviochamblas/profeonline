"""Orquestación idempotente del pipeline educativo basado en transcripción."""

import json
import hashlib
import os
import re

from django.conf import settings
from django.db import IntegrityError, transaction

from apps.content.models import (
    Choice,
    PublicationItem,
    Question,
    QuizGuide,
    ResourceQuizConfig,
    Subject,
    Topic,
)
from apps.content.models.resource_quiz_config import default_quiz_counts
from apps.content.services.ai_generation_service import (
    _call_gemini_api,
    _call_openai_api,
    _save_questions,
    generate_question_candidates,
)
from apps.content.services.guide_service import normalize_text

MIN_TRANSCRIPT_CHARS = 300
MIN_TRANSCRIPT_WORDS = 50
MAX_REGENERATION_ROUNDS = 3

PIPELINE_MODES = (
    (1, "practice", "preparacion"),
    (1, "eval", "evaluacion"),
    (2, "practice", "preparacion"),
    (2, "eval", "evaluacion"),
    (3, "practice", "preparacion"),
    (3, "eval", "evaluacion"),
)

EDITORIAL_MODES = ("preparacion", "evaluacion", "ambas")
EDITORIAL_QUESTIONS_PER_MODE = 10
EDITORIAL_QUESTION_TOTAL = 90


class PipelineError(RuntimeError):
    pass


def editorial_quiz_counts():
    """Matriz visible: 10 exclusivas + 10 comunes disponibles por modo."""
    return {
        str(level): {
            "practice": {"pool": 20, "shown": 5},
            "eval": {"pool": 20, "shown": 5 if level < 3 else 3},
        }
        for level in (1, 2, 3)
    }


def _question_fingerprint(text):
    return " ".join(normalize_text(text).lower().split())


def validate_editorial_package(payload):
    """Valida el paquete completo antes de realizar cualquier escritura."""
    if not isinstance(payload, dict):
        raise PipelineError("El paquete editorial debe ser un objeto JSON.")

    metadata = payload.get("metadata")
    guide = payload.get("guide")
    questions = payload.get("questions")
    required_metadata = (
        "resource_title",
        "youtube_title",
        "resource_description",
        "youtube_description",
        "introduction",
        "guide_title",
        "pedagogical_document",
    )
    if not isinstance(metadata, dict):
        raise PipelineError("Falta metadata válida en el paquete editorial.")
    missing = [key for key in required_metadata if not normalize_text(metadata.get(key, ""))]
    if missing:
        raise PipelineError(f"Metadata incompleta: {', '.join(missing)}.")
    if not isinstance(guide, dict) or not normalize_text(guide.get("content", "")):
        raise PipelineError("La guía editorial debe incluir content.")
    if not isinstance(questions, list) or len(questions) != EDITORIAL_QUESTION_TOTAL:
        raise PipelineError(
            f"El paquete debe contener exactamente {EDITORIAL_QUESTION_TOTAL} preguntas."
        )

    counts = {
        (level, mode): 0
        for level in (1, 2, 3)
        for mode in EDITORIAL_MODES
    }
    seen = set()
    normalized_questions = []
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            raise PipelineError(f"Pregunta {index}: estructura inválida.")
        try:
            level = int(question.get("level"))
        except (TypeError, ValueError):
            level = 0
        mode = str(question.get("mode", "")).strip()
        text = normalize_text(question.get("text", ""))
        explanation = normalize_text(question.get("explanation", ""))
        choices = question.get("choices")
        if level not in (1, 2, 3) or mode not in EDITORIAL_MODES:
            raise PipelineError(f"Pregunta {index}: nivel o modo inválido.")
        if not text or not explanation:
            raise PipelineError(f"Pregunta {index}: faltan enunciado o explicación.")
        fingerprint = _question_fingerprint(text)
        if fingerprint in seen:
            raise PipelineError(f"Pregunta {index}: enunciado duplicado.")
        seen.add(fingerprint)
        if not isinstance(choices, list) or len(choices) != 4:
            raise PipelineError(f"Pregunta {index}: debe tener exactamente cuatro alternativas.")
        normalized_choices = []
        correct_count = 0
        choice_texts = set()
        for choice_index, choice in enumerate(choices, start=1):
            if not isinstance(choice, dict):
                raise PipelineError(
                    f"Pregunta {index}, alternativa {choice_index}: estructura inválida."
                )
            choice_text = normalize_text(choice.get("text", ""))
            is_correct = bool(choice.get("is_correct"))
            if not choice_text or choice_text.lower() in choice_texts:
                raise PipelineError(
                    f"Pregunta {index}: alternativas vacías o duplicadas."
                )
            choice_texts.add(choice_text.lower())
            correct_count += int(is_correct)
            normalized_choices.append(
                {"text": choice_text, "is_correct": is_correct}
            )
        if correct_count != 1:
            raise PipelineError(
                f"Pregunta {index}: debe tener exactamente una alternativa correcta."
            )
        counts[(level, mode)] += 1
        normalized_questions.append(
            {
                "level": level,
                "mode": mode,
                "text": text,
                "explanation": explanation,
                "choices": normalized_choices,
                "cognitive_type": normalize_text(question.get("cognitive_type", "")),
            }
        )

    invalid_counts = {
        f"N{level}/{mode}": count
        for (level, mode), count in counts.items()
        if count != EDITORIAL_QUESTIONS_PER_MODE
    }
    if invalid_counts:
        detail = ", ".join(f"{key}={value}" for key, value in invalid_counts.items())
        raise PipelineError(f"Distribución editorial inválida: {detail}.")

    normalized_metadata = {
        key: normalize_text(metadata[key])
        for key in required_metadata
    }
    normalized_metadata["thumbnail_title"] = normalize_text(
        metadata.get("thumbnail_title", metadata["resource_title"])
    )
    normalized_metadata["editorial_source"] = "codex"
    normalized_metadata["question_distribution"] = {
        str(level): {
            mode: EDITORIAL_QUESTIONS_PER_MODE for mode in EDITORIAL_MODES
        }
        for level in (1, 2, 3)
    }
    return {
        "metadata": normalized_metadata,
        "guide": {
            "title": normalize_text(guide.get("title", metadata["guide_title"])),
            "description": normalize_text(guide.get("description", "")),
            "content": normalize_text(guide["content"]),
        },
        "questions": normalized_questions,
    }


@transaction.atomic
def apply_editorial_package(item, payload):
    """Reemplaza solo borradores seguros del ítem y deja questions_ready."""
    item = PublicationItem.objects.select_for_update().select_related("resource").get(pk=item.pk)
    if item.state == PublicationItem.STATE_PUBLISHED:
        raise PipelineError("El ítem ya está publicado y no admite reemplazo editorial.")
    if item.resource is None:
        raise PipelineError("El ítem no tiene un recurso asociado.")
    if not transcript_is_sufficient(item.resource.transcript):
        raise PipelineError("La transcripción es insuficiente para aplicar el paquete editorial.")

    package = validate_editorial_package(payload)
    existing = item.questions.all()
    protected = existing.exclude(status="borrador").exists() or existing.filter(
        attempt_answers__isnull=False
    ).exists() or existing.filter(error_reports__isnull=False).exists()
    if protected:
        raise PipelineError(
            "El ítem contiene preguntas publicadas, respondidas o reportadas; no se reemplazaron."
        )
    existing.delete()

    guide, _ = QuizGuide.objects.update_or_create(
        canonical_resource=item.resource,
        defaults={
            "title": package["guide"]["title"],
            "description": package["guide"]["description"],
            "source_filename": item.source_filename,
            "content_text": package["guide"]["content"],
            "is_active": False,
        },
    )
    guide.resources.add(item.resource)

    question_objects = []
    for order, question in enumerate(package["questions"], start=1):
        generation_key = hashlib.sha256(
            (
                f"{question['level']}|{question['mode']}|"
                f"{_question_fingerprint(question['text'])}"
            ).encode("utf-8")
        ).hexdigest()
        question_objects.append(
            Question(
                resource=item.resource,
                publication_item=item,
                level=question["level"],
                mode=question["mode"],
                text=question["text"],
                explanation=question["explanation"],
                status="borrador",
                order=order,
                generation_key=generation_key,
                audit_data={
                    "accepted": True,
                    "audited_by": "codex_editorial_package",
                    "cognitive_type": question["cognitive_type"],
                },
            )
        )
    created_questions = Question.objects.bulk_create(question_objects)
    choices = []
    for question, question_data in zip(created_questions, package["questions"]):
        for order, choice in enumerate(question_data["choices"], start=1):
            choices.append(
                Choice(
                    question=question,
                    text=choice["text"],
                    is_correct=choice["is_correct"],
                    order=order,
                )
            )
    Choice.objects.bulk_create(choices)

    item.canonical_guide = guide
    item.metadata = package["metadata"]
    item.target_counts = editorial_quiz_counts()
    item.state = PublicationItem.STATE_QUESTIONS_READY
    item.resume_state = ""
    item.last_error = ""
    item.save(
        update_fields=[
            "canonical_guide",
            "metadata",
            "target_counts",
            "state",
            "resume_state",
            "last_error",
            "updated_at",
        ]
    )
    return item


def _generated_text(value):
    """Convierte respuestas JSON estructuradas de la IA en texto pedagógico."""
    if isinstance(value, str):
        return normalize_text(value)
    if isinstance(value, list):
        parts = [_generated_text(item) for item in value]
        return "\n".join(f"- {part}" for part in parts if part)
    if isinstance(value, dict):
        sections = []
        for key, content in value.items():
            text = _generated_text(content)
            if text:
                heading = str(key).replace("_", " ").strip().title()
                sections.append(f"### {heading}\n{text}")
        return "\n\n".join(sections)
    if value is None:
        return ""
    return normalize_text(str(value))


def transcript_is_sufficient(transcript):
    text = normalize_text(transcript or "")
    return len(text) >= MIN_TRANSCRIPT_CHARS and len(text.split()) >= MIN_TRANSCRIPT_WORDS


def _provider_json(prompt):
    gemini_key = getattr(settings, "GEMINI_API_KEY", None) or os.environ.get("GEMINI_API_KEY", "")
    openai_key = getattr(settings, "OPENAI_API_KEY", None) or os.environ.get("OPENAI_API_KEY", "")
    if gemini_key:
        return _call_gemini_api(prompt, gemini_key)
    if openai_key:
        return _call_openai_api(prompt, openai_key)
    raise PipelineError("No hay GEMINI_API_KEY ni OPENAI_API_KEY configurada.")


def generate_canonical_document(item):
    resource = item.resource
    transcript = normalize_text(resource.transcript)
    taxonomy = item.taxonomy or {}
    prompt = f"""Eres editor pedagógico de ProfeOnline. Construye un documento canónico usando
PRINCIPALMENTE la transcripción real. No agregues conceptos, ejercicios ni afirmaciones ausentes.
Si el contenido no permite completar un campo con fidelidad, devuelve error en vez de inventar.

TRANSCRIPCIÓN:
{transcript[:14000]}

CONTEXTO DECLARADO:
Asignatura: {taxonomy.get("subject_slug", "")}
Tema: {taxonomy.get("topic_slug", "")}
Nivel: {taxonomy.get("education_level", "")}
Indicaciones del profesor: {item.instructions}

Devuelve únicamente JSON con estas claves de texto:
resource_title, youtube_title, resource_description, youtube_description,
introduction, guide_title, pedagogical_document.
El documento pedagógico debe incluir objetivos, conceptos efectivamente tratados,
procedimientos/ejemplos presentes, errores advertidos y límites de contenido."""
    data = _provider_json(prompt)
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], dict):
        data = data[0]
    if not isinstance(data, dict):
        raise PipelineError("La IA no devolvió un documento canónico válido.")
    required = (
        "resource_title",
        "youtube_title",
        "resource_description",
        "youtube_description",
        "introduction",
        "guide_title",
        "pedagogical_document",
    )
    document = {key: _generated_text(data.get(key, "")) for key in required}
    missing = [key for key in required if not document[key]]
    if missing:
        raise PipelineError(f"Documento canónico incompleto: {', '.join(missing)}.")
    if not _has_source_overlap(document["pedagogical_document"], transcript):
        raise PipelineError("El documento canónico no demuestra fidelidad suficiente a la transcripción.")
    return document


def _significant_words(text):
    return {
        word
        for word in re.findall(r"[a-záéíóúñü]{5,}", (text or "").lower())
        if word not in {"sobre", "desde", "entre", "donde", "porque", "tambien", "estos", "estas"}
    }


def _has_source_overlap(text, source):
    source_words = _significant_words(source)
    if not source_words:
        return False
    return len(_significant_words(text) & source_words) >= 8


def _question_text(candidate):
    return normalize_text(candidate.get("text") or candidate.get("enunciado") or "")


def _question_choices(candidate):
    return candidate.get("choices") or candidate.get("alternativas") or candidate.get("options") or []


def _literal_fingerprint(text):
    return " ".join(text.lower().split())


def _structural_fingerprint(text):
    value = _literal_fingerprint(text)
    value = re.sub(r"\b\d+(?:[.,]\d+)?\b", "<n>", value)
    value = re.sub(r"\b[a-z]\b", "<v>", value)
    return value


def local_candidate_errors(candidate, seen_literal, seen_structural):
    errors = []
    text = _question_text(candidate)
    choices = _question_choices(candidate)
    explanation = normalize_text(candidate.get("explanation") or candidate.get("explicacion") or "")
    if not text:
        errors.append("enunciado vacío")
    if len(choices) != 4:
        errors.append("no tiene exactamente cuatro alternativas")
    choice_texts = []
    correct = 0
    for choice in choices:
        if not isinstance(choice, dict):
            errors.append("alternativa sin estructura")
            continue
        choice_texts.append(normalize_text(choice.get("text") or choice.get("texto") or ""))
        correct += bool(choice.get("is_correct") or choice.get("correcta"))
    if correct != 1:
        errors.append("no tiene exactamente una respuesta correcta")
    if len(set(choice_texts)) != len(choice_texts) or any(not value for value in choice_texts):
        errors.append("alternativas vacías o repetidas")
    if not explanation:
        errors.append("explicación vacía")
    literal = _literal_fingerprint(text)
    structural = _structural_fingerprint(text)
    if literal in seen_literal:
        errors.append("duplicado literal")
    if structural in seen_structural:
        errors.append("duplicado estructural")
    return errors


def audit_question_candidates(item, level, mode, candidates):
    resource = item.resource
    guide = item.canonical_guide
    payload = json.dumps(candidates, ensure_ascii=False)
    prompt = f"""Actúa como segundo auditor independiente. Evalúa cada candidato contra la
transcripción y la guía canónica. Acepta solo si: es fiel, está dentro de la guía, tiene una única
respuesta correcta, distractores plausibles, explicación correcta, dificultad N{level} adecuada,
y aporta diversidad cognitiva sin duplicar estructura.

TRANSCRIPCIÓN:
{resource.transcript[:10000]}

GUÍA CANÓNICA:
{guide.content_text[:7000]}

MODO: {mode}
CANDIDATOS:
{payload}

Devuelve solo JSON: {{"decisions":[{{"index":0,"accepted":true,
"reasons":[],"cognitive_type":"comprension"}}]}}. Debe haber una decisión por candidato."""
    result = _provider_json(prompt)
    if isinstance(result, dict):
        decisions = result.get("decisions") or result.get("auditoria") or []
    elif isinstance(result, list):
        decisions = result
    else:
        decisions = []
    by_index = {
        int(decision["index"]): decision
        for decision in decisions
        if isinstance(decision, dict) and str(decision.get("index", "")).isdigit()
    }

    existing = list(
        Question.objects.filter(resource=resource)
        .exclude(status="archivada")
        .values_list("text", flat=True)
    )
    seen_literal = {_literal_fingerprint(text) for text in existing}
    seen_structural = {_structural_fingerprint(text) for text in existing}
    accepted = []
    audit_data = {}
    for index, candidate in enumerate(candidates):
        local_errors = local_candidate_errors(candidate, seen_literal, seen_structural)
        decision = by_index.get(index, {})
        reasons = list(decision.get("reasons") or []) + local_errors
        is_accepted = bool(decision.get("accepted")) and not reasons
        if is_accepted:
            text = _question_text(candidate)
            seen_literal.add(_literal_fingerprint(text))
            seen_structural.add(_structural_fingerprint(text))
            accepted.append(candidate)
            audit_data[len(accepted) - 1] = {
                "accepted": True,
                "cognitive_type": decision.get("cognitive_type") or candidate.get("cognitive_type", ""),
                "audited_by": "second_stage_ai",
            }
    return accepted, audit_data


def _target_counts(item):
    if item.target_counts:
        return item.target_counts
    config = ResourceQuizConfig.objects.filter(resource=item.resource).first()
    return config.counts if config else default_quiz_counts()


def prepare_context_and_metadata(item, generator=None):
    resource = item.resource
    if resource is None:
        raise PipelineError("El ítem no tiene Resource asociado.")
    if not transcript_is_sufficient(resource.transcript):
        item.resume_state = PublicationItem.STATE_UPLOADED
        item.state = PublicationItem.STATE_TRANSCRIPT_PENDING
        item.last_error = "Transcripción ausente o insuficiente; no se generó contenido."
        item.save(update_fields=["resume_state", "state", "last_error", "updated_at"])
        return False

    if item.state != PublicationItem.STATE_CONTEXT_READY:
        item.state = PublicationItem.STATE_CONTEXT_READY
        item.last_error = ""
        item.save(update_fields=["state", "last_error", "updated_at"])

    generator = generator or generate_canonical_document
    document = generator(item)
    with transaction.atomic():
        guide, _ = QuizGuide.objects.update_or_create(
            canonical_resource=resource,
            defaults={
                "title": document["guide_title"],
                "description": "Documento pedagógico canónico generado desde la transcripción.",
                "source_filename": item.source_filename,
                "content_text": document["pedagogical_document"],
                "is_active": False,
            },
        )
        guide.resources.add(resource)
        target_counts = _target_counts(item)
        item.canonical_guide = guide
        item.metadata = document
        item.target_counts = target_counts
        item.state = PublicationItem.STATE_METADATA_READY
        item.last_error = ""
        item.save(
            update_fields=[
                "canonical_guide",
                "metadata",
                "target_counts",
                "state",
                "last_error",
                "updated_at",
            ]
        )
    return True


def generate_and_audit_questions(
    item,
    candidate_generator=None,
    auditor=None,
    max_rounds=MAX_REGENERATION_ROUNDS,
):
    if item.state != PublicationItem.STATE_METADATA_READY:
        raise PipelineError("El ítem debe estar en metadata_ready.")
    candidate_generator = candidate_generator or generate_question_candidates
    auditor = auditor or audit_question_candidates
    counts = _target_counts(item)
    education_level = item.taxonomy.get("education_level") or (
        getattr(item.resource.topic, "education_level", "") if item.resource.topic_id else ""
    ) or "media"

    for level, config_mode, model_mode in PIPELINE_MODES:
        target = int(counts.get(str(level), {}).get(config_mode, {}).get("pool", 0))
        existing = item.questions.filter(
            level=level,
            mode=model_mode,
        ).exclude(status="archivada").count()
        deficit = max(0, target - existing)
        rounds = 0
        while deficit and rounds < max_rounds:
            rounds += 1
            candidates = candidate_generator(
                resource=item.resource,
                level=level,
                mode=model_mode,
                count=deficit,
                education_level=education_level,
                transcript=item.resource.transcript,
                reference_guides=item.canonical_guide.content_text,
            )
            accepted, audit_data = auditor(item, level, model_mode, candidates)
            if not accepted:
                continue
            try:
                with transaction.atomic():
                    created = _save_questions(
                        item.resource,
                        level,
                        model_mode,
                        accepted[:deficit],
                        status="borrador",
                        publication_item=item,
                        audit_data_by_index=audit_data,
                    )
            except IntegrityError:
                created = []
            deficit -= len(created)
        if deficit:
            raise PipelineError(
                f"No se cubrió N{level}/{model_mode}: faltan {deficit} tras {max_rounds} rondas."
            )

    item.state = PublicationItem.STATE_QUESTIONS_READY
    item.last_error = ""
    item.save(update_fields=["state", "last_error", "updated_at"])
    return True


def process_publication_item(item, **kwargs):
    """Avanza un ítem hasta questions_ready; es seguro reintentarlo."""
    if item.state == PublicationItem.STATE_PUBLISHED:
        return item
    if item.state == PublicationItem.STATE_FAILED and item.resume_state:
        item.state = item.resume_state
        item.save(update_fields=["state", "updated_at"])
        item.refresh_from_db()
    if item.state in {
        PublicationItem.STATE_UPLOADED,
        PublicationItem.STATE_TRANSCRIPT_PENDING,
        PublicationItem.STATE_CONTEXT_READY,
    }:
        if not prepare_context_and_metadata(item, kwargs.get("metadata_generator")):
            return item
        item.refresh_from_db()
    if item.state == PublicationItem.STATE_METADATA_READY:
        generate_and_audit_questions(
            item,
            candidate_generator=kwargs.get("candidate_generator"),
            auditor=kwargs.get("auditor"),
            max_rounds=kwargs.get("max_rounds", MAX_REGENERATION_ROUNDS),
        )
        item.refresh_from_db()
    return item


def finalize_publication(item):
    """Publica el conjunto local; el agente debe confirmar antes el video en YouTube."""
    if item.state == PublicationItem.STATE_PUBLISHED:
        return item
    if item.state != PublicationItem.STATE_QUESTIONS_READY:
        raise PipelineError("El ítem todavía no está validado por completo.")
    if item.youtube_privacy != "public":
        raise PipelineError("YouTube aún no confirmó privacidad pública.")
    if not item.canonical_guide_id or not item.metadata:
        raise PipelineError("Falta guía canónica o metadatos.")

    counts = _target_counts(item)
    distribution = item.metadata.get("question_distribution", {})
    if distribution:
        expected = sum(
            int(distribution.get(str(level), {}).get(mode, 0))
            for level in (1, 2, 3)
            for mode in EDITORIAL_MODES
        )
    else:
        expected = sum(
            int(counts.get(str(level), {}).get(config_mode, {}).get("pool", 0))
            for level, config_mode, _mode in PIPELINE_MODES
        )
    valid_questions = item.questions.filter(
        status="borrador",
        audit_data__accepted=True,
    )
    if valid_questions.count() != expected:
        raise PipelineError("La cobertura auditada no coincide con la matriz objetivo.")

    with transaction.atomic():
        valid_questions.update(status="publicada")
        config, _ = ResourceQuizConfig.objects.get_or_create(resource=item.resource)
        config.counts = counts
        config.autopublish = False
        config.save(update_fields=["counts", "autopublish"])
        item.resource.title = item.metadata["resource_title"]
        item.resource.description = item.metadata["resource_description"]
        item.resource.content = item.metadata["introduction"]
        item.resource.is_published = True
        update_fields = ["title", "description", "content", "is_published"]
        subject_slug = item.taxonomy.get("subject_slug")
        topic_slug = item.taxonomy.get("topic_slug")
        if subject_slug:
            subject = Subject.objects.filter(slug=subject_slug, is_active=True).first()
            if subject:
                item.resource.subject = subject
                update_fields.append("subject")
        if topic_slug:
            topic_qs = Topic.objects.filter(slug=topic_slug, is_active=True)
            if item.resource.subject_id:
                topic_qs = topic_qs.filter(subject=item.resource.subject)
            topic = topic_qs.first()
            if topic:
                item.resource.topic = topic
                update_fields.append("topic")
        item.resource.save(
            update_fields=update_fields
        )
        item.canonical_guide.is_active = True
        item.canonical_guide.save(update_fields=["is_active"])
        item.state = PublicationItem.STATE_PUBLISHED
        item.last_error = ""
        item.save(update_fields=["state", "last_error", "updated_at"])
    return item
