"""Servicio de guías de referencia.

Convierte cualquier material subido (PDF, Word, texto) a un texto plano,
normalizado y compacto (barato en tokens), y arma el bloque de "guías de
referencia" que se inyecta en el prompt para que la IA mimetice el estilo de
ejercicios y use el contenido de la guía.
"""

import io
import logging
import re

logger = logging.getLogger(__name__)

# Tope de caracteres de guías que se inyectan por recurso (economía de tokens).
MAX_GUIDE_CHARS = 4000


def normalize_text(raw, max_chars=None):
    """Limpia y compacta texto: normaliza saltos, colapsa espacios y recorta."""
    if not raw:
        return ""
    text = raw.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)            # espacios repetidos -> uno
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = re.sub(r"\n{3,}", "\n\n", text)         # 3+ saltos -> doble
    text = text.strip()
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
    return text


def extract_guide_text(data, filename=""):
    """Extrae texto plano de un material (bytes o str) según su extensión.

    Soporta .txt/.md (directo), .pdf (pypdf) y .docx (python-docx). Si el formato
    no se reconoce, intenta decodificar como texto. Devuelve el texto NO normalizado
    (usar ``normalize_text`` después) o "" si no se pudo.
    """
    if isinstance(data, str):
        return data

    name = (filename or "").lower()
    if name.endswith(".pdf"):
        return _extract_pdf(data)
    if name.endswith(".docx"):
        return _extract_docx(data)
    # .txt, .md o desconocido -> intentar como texto.
    try:
        return data.decode("utf-8", errors="ignore")
    except (AttributeError, UnicodeDecodeError):
        return ""


def _extract_pdf(data):
    try:
        from pypdf import PdfReader
    except ImportError:
        logger.warning("guide: 'pypdf' no instalado; no se puede extraer PDF.")
        return ""
    try:
        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as exc:  # noqa: BLE001 - degradar con elegancia
        logger.info("guide: fallo extrayendo PDF: %s", exc)
        return ""


def _extract_docx(data):
    try:
        from docx import Document
    except ImportError:
        logger.warning("guide: 'python-docx' no instalado; no se puede extraer .docx.")
        return ""
    try:
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as exc:  # noqa: BLE001
        logger.info("guide: fallo extrayendo docx: %s", exc)
        return ""


def guides_for_resource(resource):
    """Guías activas aplicables a un recurso (directo, por tema o por asignatura)."""
    from django.db.models import Q

    from apps.content.models import QuizGuide

    if resource is None:
        return QuizGuide.objects.none()

    filtros = Q(resources=resource)
    if getattr(resource, "topic_id", None):
        filtros |= Q(topics=resource.topic_id)
    if getattr(resource, "subject_id", None):
        filtros |= Q(subjects=resource.subject_id)

    return QuizGuide.objects.filter(is_active=True).filter(filtros).distinct()


def build_reference_block(resource, max_chars=MAX_GUIDE_CHARS):
    """Texto combinado de las guías de un recurso para el prompt, o "" si no hay."""
    guides = list(guides_for_resource(resource))
    if not guides:
        return ""

    partes = []
    presupuesto = max_chars
    for guide in guides:
        if presupuesto <= 0:
            break
        fragmento = normalize_text(guide.content_text, max_chars=presupuesto)
        if fragmento:
            partes.append(f"[{guide.title}]\n{fragmento}")
            presupuesto -= len(fragmento)

    return "\n\n".join(partes)
