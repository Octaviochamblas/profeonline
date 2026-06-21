"""Reglas conservadoras y versionadas para títulos públicos de recursos."""

import re
import unicodedata


TITLE_CLEANUP_VERSION = 1

# Alias editoriales que no coinciden literalmente con el nombre canónico del tema.
REDUNDANT_PREFIXES_BY_TOPIC = {
    "lenguaje-y-expresiones-algebraicas": (
        "Lenguaje Algebraico",
        "Lenguaje Algebraica",
    ),
    "funciones-de-varias-variables-y-optimizacion": (
        "Cálculo III Multivariable",
    ),
}

_SITE_SUFFIX_RE = re.compile(
    r"\s*(?:[|—–-]\s*)?@?ProfeOnline\.cl\s*$",
    flags=re.IGNORECASE,
)
_LEADING_SEPARATOR_RE = re.compile(r"^\s*[:|—–-]+\s*")
_NUMBERED_EXERCISE_RE = re.compile(
    r"^(?P<number>\d+(?:[.\s]\d+)?[A-Za-z]?)"
    r"\s*[:.-]?\s*(?P<marker>ejercicios?)"
    r"(?P<separator>\s*[:.-])?\s*(?P<rest>.*)$",
    flags=re.IGNORECASE,
)


def _strip_redundant_prefix(title, prefix):
    def folded(value):
        return "".join(
            character
            for character in unicodedata.normalize("NFKD", value or "")
            if not unicodedata.combining(character)
        ).casefold()

    if not prefix or folded(title[:len(prefix)]) != folded(prefix):
        return title
    tail = title[len(prefix):]
    if not tail or _LEADING_SEPARATOR_RE.match(tail):
        return _LEADING_SEPARATOR_RE.sub("", tail, count=1)
    if re.match(r"^\s*\d", tail):
        return tail.strip()
    return title


def clean_resource_title_v1(
    title,
    *,
    subject_name="",
    topic_name="",
    topic_slug="",
):
    """Devuelve un título compacto sin alterar su numeración pedagógica."""
    cleaned = _SITE_SUFFIX_RE.sub("", title or "").strip()

    aliases = REDUNDANT_PREFIXES_BY_TOPIC.get(topic_slug or "", ())
    prefixes = sorted(
        {*aliases, subject_name or "", topic_name or ""},
        key=len,
        reverse=True,
    )
    for prefix in prefixes:
        cleaned = _strip_redundant_prefix(cleaned, prefix)

    cleaned = re.sub(r"^Clase\s+(?=\d)", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r"^(\d+(?:[.\s]\d+)?[A-Za-z]?)\s*:\s*",
        r"\1 ",
        cleaned,
    )

    exercise_match = _NUMBERED_EXERCISE_RE.match(cleaned)
    if exercise_match:
        marker = exercise_match.group("marker")
        separator = exercise_match.group("separator")
        # "EJERCICIOS" funciona como etiqueta editorial. En cambio,
        # "1.5 Ejercicios de suma" es parte natural del título y se conserva.
        if marker.isupper() or separator:
            cleaned = (
                f"{exercise_match.group('number')} "
                f"{exercise_match.group('rest')}"
            )

    cleaned = re.sub(r"\s*\|\s*", " · ", cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(" :|—–-")


# Nombre público estable para consumidores actuales. Las migraciones importan
# explícitamente la versión para no cambiar de regla accidentalmente.
clean_resource_title = clean_resource_title_v1
