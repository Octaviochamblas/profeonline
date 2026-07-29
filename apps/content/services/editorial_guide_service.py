"""Shared editorial guide invariants for pipelines and maintenance scripts."""

from __future__ import annotations

import re

from django.urls import reverse


LEGACY_REQUIRED_GUIDE_SECTIONS = (
    "Resumen inicial",
    "Explicación formal",
    "Explicación en palabras simples",
    "Definiciones clave",
    "Propiedades y relaciones importantes",
    "Ejemplo guiado",
    "Procedimiento",
    "Errores frecuentes y cómo corregirlos",
    "Al terminar debes poder",
)
REQUIRED_GUIDE_SECTIONS = (
    "Resumen inicial",
    "Explicación en palabras simples",
    "Explicación formal",
    "Definiciones clave",
    "Propiedades y relaciones importantes",
    "Ejemplo guiado",
    "Procedimiento",
    "Errores frecuentes y cómo corregirlos",
    "Al terminar debes poder",
)
THEORETICAL_RESOURCE_PROFILE = "teorico-interactivo-v1"
THEORETICAL_SUMMARY_BLOCKS = (
    "Pregunta de activación",
    "Propósito",
    "Antes de comenzar",
    "Recorrido",
)
THEORETICAL_EXAMPLE_BLOCKS = (
    "1. Qué se hace",
    "2. Por qué se hace así",
    "3. Qué regla lo permite",
    "4. Cómo se comprueba",
)
THEORETICAL_PROCEDURE_BLOCKS = (
    "Método general",
    "Variaciones que debes reconocer",
)
THEORETICAL_ERROR_BLOCKS = (
    "No confundir",
    "Errores frecuentes",
)
FINAL_HEADING = "## Al terminar debes poder"
DEFINITIONS_HEADING = "## Definiciones clave"
INFOGRAPHIC_MARKDOWN = re.compile(
    r"^!\[[^\]]*\]\(/recursos/[^\)]*(?:/infografia/|\?asset=infographic)[^\)]*\)\s*$\n?",
    re.MULTILINE,
)
CONCEPT_IMAGE_MARKDOWN = re.compile(
    r"^!\[[^\]]*\]\(/recursos/[^\)]*\?asset=concept[^\)]*\)\s*$\n?",
    re.MULTILINE,
)
GENERIC_CLOSING = re.compile(
    r"\b(explicar el concepto con tus palabras|reconocerlo en una situación cotidiana|resolver ejercicios simples)\b",
    re.IGNORECASE,
)


def _sections(content: str) -> list[str]:
    return re.findall(r"^##\s+(.+?)\s*$", content, flags=re.MULTILINE)


def validate_guide_structure(content: str) -> None:
    sections = _sections(content)
    if sections not in (
        list(REQUIRED_GUIDE_SECTIONS),
        list(LEGACY_REQUIRED_GUIDE_SECTIONS),
    ):
        raise ValueError("La guía debe contener exactamente las nueve secciones editoriales y en su orden canónico.")
    for heading in sections:
        match = re.search(
            rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )
        if not match or not match.group(1).strip():
            raise ValueError(f"La sección '{heading}' no puede estar vacía.")


def _section_content(content: str, heading: str) -> str:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
        content,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1).strip() if match else ""


def _subsection_headings(content: str) -> list[str]:
    return re.findall(r"^###\s+(.+?)\s*$", content, flags=re.MULTILINE)


def _require_subsections(content: str, expected: tuple[str, ...], label: str) -> None:
    if _subsection_headings(content) != list(expected):
        names = ", ".join(f"'{name}'" for name in expected)
        raise ValueError(f"{label} debe contener {names} en ese orden.")


def validate_theoretical_resource_profile(
    content: str,
    profile: str,
    checkpoints: list[dict] | None,
) -> None:
    if not profile:
        return
    if profile != THEORETICAL_RESOURCE_PROFILE:
        raise ValueError(
            f"Perfil teórico desconocido; usa guide.profile='{THEORETICAL_RESOURCE_PROFILE}'."
        )
    if _sections(content) != list(REQUIRED_GUIDE_SECTIONS):
        raise ValueError("El perfil teórico exige el orden canónico vigente.")
    if re.search(
        r"\[\[(?:COMPLETAR|PENDIENTE|TEMA|EJEMPLO)(?::[^\]]*)?\]\]|\bPLACEHOLDER\b|^TODO:",
        content,
        flags=re.MULTILINE,
    ):
        raise ValueError("La guía teórica contiene marcadores sin completar.")

    summary = _section_content(content, "Resumen inicial")
    plain = _section_content(content, "Explicación en palabras simples")
    formal = _section_content(content, "Explicación formal")
    example = _section_content(content, "Ejemplo guiado")
    procedure = _section_content(content, "Procedimiento")
    errors = _section_content(content, "Errores frecuentes y cómo corregirlos")
    _require_subsections(summary, THEORETICAL_SUMMARY_BLOCKS, "Resumen inicial")
    _require_subsections(example, THEORETICAL_EXAMPLE_BLOCKS, "Ejemplo guiado")
    _require_subsections(procedure, THEORETICAL_PROCEDURE_BLOCKS, "Procedimiento")
    _require_subsections(errors, THEORETICAL_ERROR_BLOCKS, "Errores frecuentes")

    activation = re.search(
        r"^### Pregunta de activación\s*$\n(.*?)(?=^###\s)",
        summary,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not activation or not re.search(r"[?¿]", activation.group(1)):
        raise ValueError("La activación debe formular una pregunta real.")
    if len(plain.split()) < 30:
        raise ValueError("La explicación sencilla debe desarrollar una interpretación comprensible.")
    formal_signal = re.compile(
        r"(?<!\\)\$|\b(definición|se define|regla|principio|ley|teorema|criterio|convención|notación)\b",
        flags=re.IGNORECASE,
    )
    if len(formal.split()) < 30 or not formal_signal.search(formal):
        raise ValueError(
            "La explicación formal debe incluir una definición, regla, principio, criterio o notación."
        )
    if checkpoints is None:
        raise ValueError("El perfil teórico exige exactamente tres comprobaciones intermedias.")


def validate_closing(content: str) -> None:
    match = re.search(r"^## Al terminar debes poder\s*$\n(.*)\Z", content, flags=re.MULTILINE | re.DOTALL)
    closing = match.group(1).strip() if match else ""
    if len(closing.split()) < 28 or GENERIC_CLOSING.search(closing):
        raise ValueError(
            "El cierre debe ser un párrafo concreto: contenido específico, procedimiento y criterio de comprobación."
        )


def infographic_markdown(resource) -> str:
    if not resource.infographic_key:
        return ""
    version = resource.infographic_key.rsplit("/", 1)[-1].split(".", 1)[0]
    url = reverse("content:resource_detail", kwargs={"slug": resource.slug})
    alt = resource.infographic_alt_text or f"Infografía de repaso: {resource.title}"
    return f"![{alt}]({url}?asset=infographic&v={version})"


def concept_image_markdown(resource) -> str:
    if not resource.concept_image_key:
        return ""
    version = resource.concept_image_key.rsplit("/", 1)[-1].split(".", 1)[0]
    url = reverse("content:resource_detail", kwargs={"slug": resource.slug})
    alt = resource.concept_image_alt_text or f"Explicación visual integrada: {resource.title}"
    return f"![{alt}]({url}?asset=concept&v={version})"


def insert_concept_image_after_explanations(content: str, resource) -> str:
    markdown = concept_image_markdown(resource)
    if not markdown:
        raise ValueError("El recurso aún no tiene una imagen conceptual persistida.")
    if DEFINITIONS_HEADING not in content:
        raise ValueError("La guía no contiene la sección de definiciones requerida.")
    without_previous = CONCEPT_IMAGE_MARKDOWN.sub("", content).rstrip()
    before, after = without_previous.split(DEFINITIONS_HEADING, 1)
    return f"{before.rstrip()}\n\n{markdown}\n\n{DEFINITIONS_HEADING}{after}"


def insert_infographic_before_closing(content: str, resource) -> str:
    markdown = infographic_markdown(resource)
    if not markdown:
        raise ValueError("El recurso aún no tiene una infografía persistida.")
    if FINAL_HEADING not in content:
        raise ValueError("La guía no contiene la sección final requerida.")
    without_previous = INFOGRAPHIC_MARKDOWN.sub("", content).rstrip()
    before, after = without_previous.split(FINAL_HEADING, 1)
    return f"{before.rstrip()}\n\n{markdown}\n\n{FINAL_HEADING}{after}"


def has_current_infographic(content: str, resource) -> bool:
    markdown = infographic_markdown(resource)
    return bool(markdown and markdown in content)
