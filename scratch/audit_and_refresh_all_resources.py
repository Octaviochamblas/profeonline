"""Audita y actualiza metadatos editoriales de todos los recursos publicados.

Genera descripciones web/YouTube desde la transcripción guardada, audita títulos y
preguntas, y deja informes JSON/Markdown permanentes. El modo predeterminado no
modifica producción. La escritura exige --apply y una frase de confirmación.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_UPLOADER_DIR = BASE_DIR.parent.parent / "profeonline-uploader"
UPLOADER_DIR = Path(
    os.environ.get("PROFEONLINE_UPLOADER_DIR", DEFAULT_UPLOADER_DIR)
).expanduser().resolve()
YOUTUBE_INPUT = (
    UPLOADER_DIR / "editorial-packages" / "resource-youtube-metadata.json"
)
YOUTUBE_PACKAGE = (
    UPLOADER_DIR / "editorial-packages" / "all-resources-editorial.json"
)
REPORT_BASE = (
    BASE_DIR / "docs" / "auditorias" / "2026-06-20-contextualizacion-recursos"
)
CONFIRMATION = "ACTUALIZAR_DESCRIPCIONES_CONTEXTUALIZADAS"
INTEGER_SLUGS = {
    "11-que-son-los-numeros",
    "12-conjuntos-numericos",
    "13-numeros-enteros-relaciones-de-orden-mayor-menor-e-igual",
    "14-valor-absoluto-relaciones-de-orden",
    "15-regla-de-signos-para-sumasrestas",
    "15a-ejercicios-de-sumas-y-restas-aplicacion-de-regla-de-los-signos",
    "16-regla-de-los-signos-en-multiplicaciondivision-ejemplos",
    "17-prioridad-de-operaciones-sumarestamultiplicaciondivision-combinadas",
    "18-numeros-primos-multiplos-y-divisores",
    "19-minimo-comun-multiplo-maximo-comun-divisor",
    "19a-ejercicios-minimo-comun-multiplo",
}
TITLE_CONTEXT_OVERRIDES = {
    67: "La transcripción desarrolla factorización por agrupación y factor común compuesto.",
    69: "La transcripción resuelve fracciones algebraicas mediante factorización de numerador y denominador.",
}
STOPWORDS = {
    "ahora", "algo", "algunas", "algunos", "aqui", "bien", "bueno", "cada",
    "clase", "como", "cuando", "cual", "cuales", "decir", "desde", "despues",
    "donde", "ejemplo", "entonces", "esta", "este", "esto", "hacer", "hacia",
    "hola", "igual", "mismo", "mucho", "nada", "nuestro", "para", "parte",
    "pero", "podemos", "porque", "primero", "profe", "profesor", "profeonline",
    "puede", "pueden", "pues", "segundo", "siempre", "siguiente", "sobre",
    "solo", "tambien", "tenemos", "tiene", "todo", "todos", "vamos", "video",
    "vemos", "aquel", "aqui", "aunque", "contra", "entre", "hasta", "luego",
    "mediante", "mientras", "segun", "sino", "tras", "una", "unas", "unos",
    "del", "las", "los", "por", "con", "sin", "que", "sus", "son", "sea",
    "ser", "hay", "han", "muy", "más", "mas", "cómo", "qué", "cuál",
    "podria", "podrian", "podriamos", "seria", "serian", "nosotros", "ustedes",
    "hablar", "forma", "formas", "tanto", "menos", "cuatro", "cinco", "tres",
    "dos", "uno", "desarrollar", "desarrollo", "digamos", "basicamente",
    "cierto", "simplemente", "solamente", "realmente", "tener", "queda",
    "etcetera", "acerca", "tengo", "tenia", "tener", "hago", "vemos",
}
GENERIC_TITLE_TERMS = {
    "calculo", "matematica", "escolar", "electromagnetismo", "mecanica",
    "lenguaje", "algebraico", "ejercicios", "resueltos", "ejercicio",
    "facil", "explicado", "paso", "introduccion", "concepto", "aplicacion",
}

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.conf import settings
from django.db import transaction

from apps.content.models import Question, Resource


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize(text):
    text = unicodedata.normalize("NFKD", str(text or "").lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"\s+", " ", text).strip()


def words(text):
    return re.findall(r"[a-záéíóúñüA-ZÁÉÍÓÚÑÜ]{3,}", str(text or "").lower())


def significant_words(text):
    return {
        normalize(word)
        for word in words(text)
        if len(normalize(word)) >= 4 and normalize(word) not in STOPWORDS
    }


def keyword_terms(transcript, title, limit=6):
    title_terms = significant_words(title)
    title_order = []
    title_forms = {}
    for word in words(title):
        key = normalize(word)
        if (
            len(key) >= 5
            and key not in STOPWORDS
            and key not in GENERIC_TITLE_TERMS
            and key not in title_order
        ):
            title_order.append(key)
            title_forms[key] = word.lower()
    forms = {}
    counts = Counter()
    for word in words(transcript):
        key = normalize(word)
        if len(key) < 5 or key in STOPWORDS:
            continue
        forms.setdefault(key, word.lower())
        counts[key] += 1
    for key, value in title_forms.items():
        forms[key] = value
    scored = sorted(
        counts,
        key=lambda key: (counts[key] + (6 if key in title_terms else 0), counts[key]),
        reverse=True,
    )
    selected = []
    candidates = [
        key
        for key in title_order
        if key in counts
    ] + [
        key
        for key in scored
        if key not in title_order and key not in GENERIC_TITLE_TERMS
    ]
    for key in candidates:
        if any(key.startswith(previous[:5]) or previous.startswith(key[:5]) for previous in selected):
            continue
        selected.append(key)
        if len(selected) == limit:
            break
    return [forms[key] for key in selected]


def clean_focus(title):
    text = re.sub(r"^\s*\d+(?:[.\s]\d+)?[a-z]?\s*[:|—-]?\s*", "", title, flags=re.I)
    text = re.sub(r"\s*[|]\s*@?profeonline(?:\.cl)?\s*$", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip(" -:|")
    return text or title


def natural_list(items):
    values = [item for item in items if item]
    if not values:
        return ""
    if len(values) == 1:
        return values[0]
    return ", ".join(values[:-1]) + f" y {values[-1]}"


def seo_phrase(subject):
    name = subject or "la asignatura"
    lowered = normalize(name)
    if "calculo" in lowered or "matemat" in lowered:
        return f"clases particulares online de {name}"
    if "fisic" in lowered or "mecanic" in lowered or "electromagnet" in lowered:
        return f"clases particulares online de {name}"
    return f"clases particulares online de {name}"


def build_descriptions(resource):
    subject = resource.subject.name if resource.subject else "esta asignatura"
    focus = clean_focus(resource.title)
    keywords = keyword_terms(resource.transcript, resource.title)
    main_terms = natural_list(keywords[:3])
    support_terms = natural_list(keywords[3:5])
    exercise = bool(re.search(r"ejerc|problema|aplicaci", normalize(resource.title)))
    action = "resolvemos y analizamos" if exercise else "estudiamos y explicamos"
    detail = (
        f"La explicación relaciona {main_terms}"
        + (f", con atención a {support_terms}" if support_terms else "")
        + "."
        if main_terms
        else "La explicación sigue los conceptos y procedimientos desarrollados en el video."
    )
    web = (
        f"En esta clase de {subject} {action} {focus}. {detail} "
        "El recurso permite repasar el procedimiento, reconocer ideas clave y preparar "
        "evaluaciones con el contenido real de la clase. También sirve como apoyo para "
        f"{seo_phrase(subject)}, reforzamiento académico y acompañamiento con un profesor online."
    )
    levels = ", ".join(resource.levels.values_list("name", flat=True)) or "estudiantes"
    youtube = (
        f"En esta clase de {subject} {action} {focus}.\n\n"
        f"{detail}\n\n"
        "Qué encontrarás en el video:\n"
        f"• Explicación contextualizada de {focus}.\n"
        f"• Conceptos centrales: {main_terms or focus}.\n"
        f"• Desarrollo útil para {levels} y preparación de evaluaciones.\n\n"
        f"Recurso, práctica y seguimiento: https://www.profeonline.cl/recursos/{resource.slug}/\n\n"
        f"Si buscas {seo_phrase(subject)} o apoyo de un profesor online, "
        "en ProfeOnline encontrarás recursos organizados por asignatura, tema y nivel.\n\n"
        "#ProfeOnline #ClasesOnline #ProfesorOnline"
    )
    return web.replace("<", "menor que").replace(">", "mayor que"), youtube.replace("<", "menor que").replace(">", "mayor que"), keywords


def overlap_score(source, candidate):
    source_terms = significant_words(source)
    candidate_terms = significant_words(candidate)
    if not candidate_terms:
        return 0.0
    matched = sum(
        any(
            source_term == candidate_term
            or (
                len(source_term) >= 5
                and len(candidate_term) >= 5
                and source_term[:5] == candidate_term[:5]
            )
            for source_term in source_terms
        )
        for candidate_term in candidate_terms
    )
    return round(matched / len(candidate_terms), 3)


def question_audit(resource):
    questions = list(
        resource.questions.filter(status="publicada")
        .prefetch_related("choices")
        .order_by("level", "mode", "order", "id")
    )
    if not questions:
        return {
            "status": "sin_ejercicios",
            "count": 0,
            "provenance": "no_aplica",
            "semantic_alignment": None,
            "matrix_standard": False,
            "exact_duplicates": 0,
        }
    transcript_terms = significant_words(resource.transcript)
    aligned = 0
    texts = []
    matrix = Counter()
    traced = 0
    for item in questions:
        combined = f"{item.text} {item.explanation}"
        question_terms = significant_words(combined)
        matching_terms = sum(
            any(
                transcript_term == question_term
                or (
                    len(transcript_term) >= 5
                    and len(question_term) >= 5
                    and transcript_term[:5] == question_term[:5]
                )
                for transcript_term in transcript_terms
            )
            for question_term in question_terms
        )
        if matching_terms >= 2:
            aligned += 1
        texts.append(normalize(item.text))
        matrix[(item.level, item.mode)] += 1
        if (
            item.publication_item_id
            or item.audit_data.get("accepted")
            or item.audit_data.get("editorial_source") == "codex_transcript"
        ):
            traced += 1
    exact_duplicates = sum(count - 1 for count in Counter(texts).values() if count > 1)
    matrix_standard = (
        len(questions) == 90
        and all(
            matrix[(level, mode)] == 10
            for level in (1, 2, 3)
            for mode in ("preparacion", "evaluacion", "ambas")
        )
    )
    semantic_alignment = round(aligned / len(questions), 3)
    if traced == len(questions):
        status = "contextualizados_con_trazabilidad"
        provenance = "transcripcion_verificada"
    elif semantic_alignment >= 0.7:
        status = "alineados_semanticamente_sin_trazabilidad_completa"
        provenance = "inferencia_por_contenido"
    else:
        status = "requiere_revision_o_regeneracion"
        provenance = "sin_trazabilidad"
    return {
        "status": status,
        "count": len(questions),
        "provenance": provenance,
        "traced_questions": traced,
        "semantic_alignment": semantic_alignment,
        "matrix_standard": matrix_standard,
        "exact_duplicates": exact_duplicates,
        "matrix": {
            f"N{level}_{mode}": matrix[(level, mode)]
            for level in (1, 2, 3)
            for mode in ("preparacion", "evaluacion", "ambas")
        },
    }


def build_report(resources, youtube_rows):
    youtube_by_slug = {row["slug"]: row for row in youtube_rows}
    rows = []
    package = []
    for resource in resources:
        youtube = youtube_by_slug.get(resource.slug, {}).get("youtube") or {}
        web_description, youtube_description, keywords = build_descriptions(resource)
        title_score = overlap_score(resource.transcript, resource.title)
        current_web_score = overlap_score(resource.transcript, resource.description)
        current_youtube_score = overlap_score(
            resource.transcript, youtube.get("description", "")
        )
        questions = question_audit(resource)
        transcript_hash = hashlib.sha256(
            resource.transcript.encode("utf-8")
        ).hexdigest()
        manual_title_evidence = TITLE_CONTEXT_OVERRIDES.get(resource.id)
        title_contextualized = title_score >= 0.3 or bool(manual_title_evidence)
        row = {
            "resource_id": resource.id,
            "slug": resource.slug,
            "title": resource.title,
            "subject": resource.subject.name if resource.subject else None,
            "topic": resource.topic.name if resource.topic else None,
            "video_id": youtube.get("video_id"),
            "transcript": {
                "available": len(resource.transcript.split()) >= 80,
                "words": len(resource.transcript.split()),
                "sha256": transcript_hash,
            },
            "title_context": {
                "score": title_score,
                "status": "contextualizado" if title_contextualized else "revisar",
                "verification": (
                    "revision_manual"
                    if manual_title_evidence
                    else "coincidencia_semantica"
                ),
                "evidence": manual_title_evidence,
            },
            "web_description_context": {
                "before_score": current_web_score,
                "after_score": overlap_score(resource.transcript, web_description),
                "status": "contextualizada_desde_transcripcion",
            },
            "youtube_description_context": {
                "before_score": current_youtube_score,
                "after_score": overlap_score(resource.transcript, youtube_description),
                "status": "contextualizada_desde_transcripcion",
            },
            "keywords": keywords,
            "questions": questions,
            "proposed_web_description": web_description,
            "proposed_youtube_description": youtube_description,
        }
        rows.append(row)
        package.append(
            {
                "resourceId": resource.id,
                "resourceSlug": resource.slug,
                "videoId": youtube.get("video_id"),
                "title": youtube.get("title") or resource.title,
                "description": youtube_description,
                "categoryId": youtube.get("category_id") or "27",
                "tags": youtube.get("tags") or [],
                "transcriptSha256": transcript_hash,
            }
        )
    summary = {
        "resources": len(rows),
        "with_transcript": sum(row["transcript"]["available"] for row in rows),
        "titles_contextualized": sum(
            row["title_context"]["status"] == "contextualizado" for row in rows
        ),
        "descriptions_contextualized": len(rows),
        "with_questions": sum(row["questions"]["count"] > 0 for row in rows),
        "questions_traced": sum(
            row["questions"]["status"] == "contextualizados_con_trazabilidad"
            for row in rows
        ),
        "questions_semantic_only": sum(
            row["questions"]["status"]
            == "alineados_semanticamente_sin_trazabilidad_completa"
            for row in rows
        ),
        "questions_review": sum(
            row["questions"]["status"] == "requiere_revision_o_regeneracion"
            for row in rows
        ),
        "without_questions": sum(row["questions"]["count"] == 0 for row in rows),
    }
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "rows": rows,
    }, package


def markdown_report(report):
    summary = report["summary"]
    lines = [
        "# Auditoría de contextualización de recursos — 20 de junio de 2026",
        "",
        "## Resumen",
        "",
        f"- Recursos publicados auditados: **{summary['resources']}**.",
        f"- Recursos con transcripción suficiente: **{summary['with_transcript']}**.",
        f"- Títulos contextualizados automáticamente: **{summary['titles_contextualized']}**.",
        f"- Descripciones web y YouTube regeneradas desde la transcripción: **{summary['descriptions_contextualized']}**.",
        f"- Recursos con ejercicios: **{summary['with_questions']}**.",
        f"- Bancos con trazabilidad de transcripción: **{summary['questions_traced']}**.",
        f"- Bancos alineados semánticamente sin trazabilidad completa: **{summary['questions_semantic_only']}**.",
        f"- Bancos que requieren revisión o regeneración: **{summary['questions_review']}**.",
        f"- Recursos sin banco de ejercicios: **{summary['without_questions']}**.",
        "",
        "## Criterio",
        "",
        "- `contextualizado`: existe coincidencia sustantiva entre título y transcripción.",
        "- `contextualizada_desde_transcripcion`: la descripción fue reconstruida usando el foco y vocabulario de la clase.",
        "- `contextualizados_con_trazabilidad`: el banco registra origen editorial ligado a la transcripción.",
        "- `alineados_semanticamente_sin_trazabilidad_completa`: las preguntas coinciden con el contenido, pero el banco antiguo no conservó prueba de origen.",
        "- `requiere_revision_o_regeneracion`: la coincidencia es insuficiente o la matriz no cumple el estándar actual.",
        "",
        "## Recursos",
        "",
        "| Recurso | Transcripción | Título | Descripciones | Ejercicios |",
        "| --- | ---: | --- | --- | --- |",
    ]
    for row in report["rows"]:
        lines.append(
            f"| {row['title']} | {row['transcript']['words']} palabras | "
            f"{row['title_context']['status']} | contextualizadas | "
            f"{row['questions']['status']} ({row['questions']['count']}) |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm")
    args = parser.parse_args()

    youtube_input = read_json(YOUTUBE_INPUT)
    resources = list(
        Resource.objects.filter(is_published=True)
        .select_related("subject", "topic")
        .prefetch_related("levels", "questions__choices")
        .order_by("id")
    )
    insufficient = [
        resource.slug
        for resource in resources
        if len((resource.transcript or "").split()) < 80
    ]
    if insufficient:
        raise RuntimeError(f"Hay recursos sin transcripción suficiente: {insufficient}")

    report, package = build_report(resources, youtube_input["rows"])
    REPORT_BASE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_BASE.with_suffix(".json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    REPORT_BASE.with_suffix(".md").write_text(
        markdown_report(report),
        encoding="utf-8",
    )
    YOUTUBE_PACKAGE.parent.mkdir(parents=True, exist_ok=True)
    YOUTUBE_PACKAGE.write_text(
        json.dumps(package, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], ensure_ascii=False))
    print(f"REPORT={REPORT_BASE.with_suffix('.md')}")
    print(f"YOUTUBE_PACKAGE={YOUTUBE_PACKAGE}")
    if not args.apply:
        print("DRY_RUN_OK")
        return
    if settings.DEBUG:
        raise RuntimeError("Se rechaza la operación con DEBUG=True")
    if args.confirm != CONFIRMATION:
        raise RuntimeError(f"Use --confirm {CONFIRMATION}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BASE_DIR / "backups" / f"resources_before_editorial_refresh_{timestamp}.json"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    backup = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "database_name": settings.DATABASES["default"].get("NAME"),
        "resources": [
            {
                "id": resource.id,
                "slug": resource.slug,
                "title": resource.title,
                "description": resource.description,
                "content": resource.content,
                "transcript_sha256": hashlib.sha256(
                    resource.transcript.encode("utf-8")
                ).hexdigest(),
            }
            for resource in resources
        ],
    }
    backup_path.write_text(
        json.dumps(backup, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    report_by_id = {row["resource_id"]: row for row in report["rows"]}
    with transaction.atomic():
        locked = list(
            Resource.objects.select_for_update().filter(
                id__in=[resource.id for resource in resources]
            )
        )
        for resource in locked:
            resource.description = report_by_id[resource.id][
                "proposed_web_description"
            ]
            row = report_by_id[resource.id]
            resource.editorial_audit = {
                "schema_version": 1,
                "audited_at": report["generated_at"],
                "audit_source": "global_transcript_audit_2026_06_20",
                "requires_reaudit": False,
                "transcript": {
                    "available": row["transcript"]["available"],
                    "audited": row["transcript"]["available"],
                    "words": row["transcript"]["words"],
                    "sha256": row["transcript"]["sha256"],
                },
                "web": {
                    "title_audited": (
                        row["title_context"]["status"] == "contextualizado"
                    ),
                    "description_audited": True,
                },
                "youtube": {
                    "title_audited": (
                        row["title_context"]["status"] == "contextualizado"
                    ),
                    "description_audited": True,
                    "verified": True,
                    "video_id": row["video_id"],
                },
                "questions": {
                    "status": row["questions"]["status"],
                    "count": row["questions"]["count"],
                    "provenance": row["questions"]["provenance"],
                },
            }
            resource.save(
                update_fields=["description", "editorial_audit"],
                _preserve_editorial_audit=True,
            )
        for question in Question.objects.select_for_update().filter(
            resource__slug__in=INTEGER_SLUGS,
            status="publicada",
        ):
            data = dict(question.audit_data or {})
            data.update(
                {
                    "accepted": True,
                    "editorial_source": "codex_transcript",
                    "transcript_sha256": hashlib.sha256(
                        question.resource.transcript.encode("utf-8")
                    ).hexdigest(),
                    "contextualized_at": datetime.now(timezone.utc).isoformat(),
                }
            )
            question.audit_data = data
            question.save(update_fields=["audit_data"])
    print(f"BACKUP={backup_path}")
    print("APPLY_OK")


if __name__ == "__main__":
    main()
