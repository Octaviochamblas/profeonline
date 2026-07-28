"""Shared editorial guide invariants for pipelines and maintenance scripts."""

from __future__ import annotations

import re

from django.urls import reverse


REQUIRED_GUIDE_SECTIONS = (
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
    if _sections(content) != list(REQUIRED_GUIDE_SECTIONS):
        raise ValueError("La guía debe contener exactamente las nueve secciones editoriales y en su orden canónico.")
    for heading in REQUIRED_GUIDE_SECTIONS:
        match = re.search(
            rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )
        if not match or not match.group(1).strip():
            raise ValueError(f"La sección '{heading}' no puede estar vacía.")


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
