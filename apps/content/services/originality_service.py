"""Servicio de originalidad determinista para validar plagio textual y marcas en borradores."""

import json
import re
import hashlib
import unicodedata
from datetime import timezone as dt_timezone

# Blocklist de marcas institucionales prohibidas (duplicado de cpech eliminado)
BLOCKLIST_MARCAS = ["santillana", "editorial sm", "cpech", "pedro de valdivia", "pdv", "saint george"]


def _normalize_text(text: str) -> str:
    """Normaliza texto: quita LaTeX, acentos, puntuación y colapsa espacios en minúsculas."""
    if not text:
        return ""

    # 1. Quitar fórmulas LaTeX completas en bloque y en línea
    cleaned = re.sub(r"\$\$.*?\$\$", "", text, flags=re.DOTALL)
    cleaned = re.sub(r"\$.*?\$", "", cleaned, flags=re.DOTALL)

    # 2. Quitar acentos utilizando unicodedata
    cleaned = "".join(
        c for c in unicodedata.normalize("NFD", cleaned)
        if unicodedata.category(c) != "Mn"
    )

    # 3. Remover caracteres no alfanuméricos (manteniendo espacios)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)

    # 4. Pasar a minúsculas y colapsar espacios múltiples
    cleaned = " ".join(cleaned.lower().split())
    return cleaned


def _get_words(text: str) -> list[str]:
    """Divide el texto normalizado en una lista de palabras."""
    return text.split()


def _get_ngrams(words: list[str], n: int) -> set[str]:
    """Genera n-gramas secuenciales a partir de una lista de palabras."""
    ngrams = set()
    if len(words) < n:
        return ngrams
    for i in range(len(words) - n + 1):
        ngrams.add(" ".join(words[i:i+n]))
    return ngrams


def calculate_audit_hash(structured_content: dict, private_guides) -> str:
    """Calcula un hash SHA-256 de auditoría extendido y determinista.

    Combina el JSON canónico del borrador (sort_keys=True) con las huellas de las
    fuentes privadas seleccionadas (ID, updated_at y hash del texto original).
    """
    # 1. Serializar el borrador de forma canónica
    canonical_draft = json.dumps(
        structured_content,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    # 2. Generar huella determinista de las fuentes (ordenadas por ID)
    sorted_guides = sorted(list(private_guides), key=lambda g: g.id)
    sources_fingerprint = ""
    for pg in sorted_guides:
        pg_hash = hashlib.sha256(pg.content_text.encode("utf-8")).hexdigest()
        updated_iso = (
            pg.updated_at.astimezone(dt_timezone.utc).isoformat(timespec="microseconds")
            if pg.updated_at else ""
        )
        sources_fingerprint += f"{pg.id}|{updated_iso}|{pg_hash}\n"

    # 3. Concatenar y calcular hash SHA-256
    combined_string = f"DRAFT:\n{canonical_draft}\nSOURCES:\n{sources_fingerprint}"
    return hashlib.sha256(combined_string.encode("utf-8")).hexdigest()


def check_originality(structured_content: dict, private_guides, threshold: int = 10) -> dict:
    """Verifica la originalidad determinista de un borrador de guía contra las fuentes.

    Busca n-gramas idénticos (10 palabras consecutivas) y marcas prohibidas en
    el borrador. Lanza ValueError si el tamaño del contenido supera límites
    operacionales (sin truncamientos silenciosos).
    """
    # 1. Control de tamaño operativo: calcular longitud total combinada
    draft_str = json.dumps(structured_content)
    total_sources_len = sum(len(pg.content_text) for pg in private_guides)
    total_len = len(draft_str) + total_sources_len

    MAX_OPERATIONAL_LIMIT = 150000
    if total_len > MAX_OPERATIONAL_LIMIT:
        raise ValueError(
            f"El contenido total a validar ({total_len} caracteres) supera el límite "
            f"de seguridad de {MAX_OPERATIONAL_LIMIT} caracteres. Asocia fuentes privadas "
            f"más pequeñas o reduce el borrador."
        )

    # 2. Normalizar el borrador completo (aplanando todos los valores de texto del JSON)
    # Extraer todo el texto de campos clave del JSON
    draft_texts = []
    def extract_texts(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, str) and k not in ["id", "exercise_id", "item_id", "schema_version", "difficulty"]:
                    draft_texts.append(v)
                else:
                    extract_texts(v)
        elif isinstance(obj, list):
            for v in obj:
                extract_texts(v)

    extract_texts(structured_content)
    normalized_draft_fields = [_normalize_text(text) for text in draft_texts]
    draft_ngrams = set()
    for field_text in normalized_draft_fields:
        draft_ngrams.update(_get_ngrams(_get_words(field_text), threshold))

    issues = []

    # 3. Comprobar copia textual por n-gramas
    for pg in private_guides:
        pg_normalized = _normalize_text(pg.content_text)
        pg_words = _get_words(pg_normalized)
        pg_ngrams = _get_ngrams(pg_words, threshold)

        # Intersección de n-gramas
        overlap = draft_ngrams.intersection(pg_ngrams)
        if overlap:
            for item in sorted(list(overlap))[:5]: # reportar máximo 5 incidencias por fuente para no saturar
                issues.append({
                    "type": "copia_textual",
                    "source_id": pg.id,
                    "source_title": pg.title,
                    "fragment": item,
                    "message": f"Coincidencia de {threshold} palabras consecutivas con la fuente '{pg.title}'."
                })

    # 4. Comprobar blocklist de marcas en el borrador normalizado
    normalized_draft_text = " ".join(normalized_draft_fields)
    for marca in BLOCKLIST_MARCAS:
        if re.search(rf"(?<!\w){re.escape(marca)}(?!\w)", normalized_draft_text):
            # Buscar el fragmento original o reportar la marca detectada
            issues.append({
                "type": "marca_prohibida",
                "brand": marca,
                "message": f"Se detectó la marca no autorizada '{marca}' en el contenido."
            })

    passed = len(issues) == 0
    return {
        "passed": passed,
        "issues": issues
    }
