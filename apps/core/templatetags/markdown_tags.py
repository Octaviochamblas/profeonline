import json as _json
import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
import bleach
import markdown as md

register = template.Library()

# Detecta marcadores de paso tipo " 2. " (número de 1-2 dígitos seguido de
# punto y espacio). El espacio obligatorio tras el punto evita falsos positivos
# con decimales como "83.815" (que no llevan espacio tras el punto).
_STEP_RE = re.compile(r"\s+(\d{1,2})\.\s+")


@register.filter(name="format_steps")
def format_steps(value):
    """Formatea explicaciones de quiz: pone cada paso numerado en su propia
    línea y respeta saltos existentes. Escapa el HTML por seguridad."""
    if not value:
        return ""
    text = str(value).strip()
    # Inserta un salto antes de cada paso numerado embebido en el texto.
    text = _STEP_RE.sub(lambda m: "\n" + m.group(1) + ". ", text)
    # Colapsa saltos múltiples y escapa, luego convierte saltos en <br>.
    text = re.sub(r"\n{2,}", "\n", text)
    html = escape(text).replace("\n", "<br>")
    return mark_safe(html)

ALLOWED_TAGS = [
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "h2",
    "h3",
    "h4",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "td": ["align"],
    "th": ["align"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]

_LATEX_DELIMITER_TOKENS = {
    r"\(": "@@LATEX_INLINE_OPEN@@",
    r"\)": "@@LATEX_INLINE_CLOSE@@",
    r"\[": "@@LATEX_BLOCK_OPEN@@",
    r"\]": "@@LATEX_BLOCK_CLOSE@@",
}

_INLINE_MATH_PROTECTED_RE = re.compile(r"(\$[^$]+\$)")
_RAW_MATH_PAREN = r"-?\([0-9A-Za-z^+\-*/ ]+\)(?:\d*[A-Za-z](?:\d+)?(?:\^\d+)?)*"
_RAW_MATH_BRACK = r"-?\[[0-9A-Za-z^+\-*/ ]+\]"
_RAW_MATH_BRACE = r"-?\{[0-9A-Za-z^+\-*/ \[\]\(\)]+\}"
_RAW_MATH_SQRT = r"√\([0-9A-Za-z^+\-*/ ]+\)"
_RAW_MATH_COMPACT_PRODUCT = r"-?\d*[A-Za-z]{1,6}\([0-9A-Za-z^+\-*/ ]+\)"
_RAW_MATH_FUNCTION = r"[A-Za-z]\([0-9A-Za-z^+\-*/ ]+\)"
_RAW_MATH_VAR = r"-?(?:\d*[A-Za-z](?:\d+)?(?:\^\d+)?)+"
_RAW_MATH_NUM = r"-?\d+(?:/\d+)?"
_RAW_MATH_TOKEN = (
    rf"(?:{_RAW_MATH_SQRT}|{_RAW_MATH_COMPACT_PRODUCT}|{_RAW_MATH_FUNCTION}|"
    rf"{_RAW_MATH_PAREN}|{_RAW_MATH_BRACK}|{_RAW_MATH_BRACE}|"
    rf"{_RAW_MATH_VAR}|{_RAW_MATH_NUM})"
)
_RAW_ALGEBRA_SPAN_RE = re.compile(
    rf"(?<![$\\])(?P<formula>{_RAW_MATH_TOKEN}(?:\s*[+\-*/=]\s*{_RAW_MATH_TOKEN})+)"
)
_RAW_SET_BLOCK_RE = re.compile(
    r"(?<![$\\])(?P<formula>\|[A-Za-z](?:\\[A-Za-z]|[∩∪][A-Za-z])?\|(?:\s*=\s*-?\d+)?)"
)
_RAW_SET_ASSIGN_RE = re.compile(
    r"(?<![$\\])(?P<formula>[A-Z]\s*=\s*\{\{[^{}]+\},\s*[^{}]+\}|[A-Z]\s*=\s*\{[^{}]+\})"
)
_RAW_CHAINED_PARENS_RE = re.compile(
    rf"(?<![$\\])(?P<formula>(?:-?\([0-9A-Za-z^+\-*/ ]+\)){{2,}}(?:\s*=\s*{_RAW_MATH_TOKEN})?)"
)
_RAW_COMPACT_PRODUCT_RE = re.compile(rf"(?<![$\\])(?P<formula>{_RAW_MATH_COMPACT_PRODUCT})")
_RAW_GROUP_RE = re.compile(
    r"(?<![$\\])(?P<formula>-?\([0-9A-Za-z^+\-*/ ]+\)(?:\d*[A-Za-z](?:\d+)?(?:\^\d+)?)*)"
)
_RAW_COLON_SPAN_RE = re.compile(r"(?P<label>:\s*)(?P<formula>[^.!?]+)(?P<punct>[.!?])")
_DEGREE_SIGN = "\N{DEGREE SIGN}"


@register.filter(name="to_json")
def to_json_filter(value):
    return _json.dumps(value, ensure_ascii=False)


_PASO_RE = re.compile(r"^(Paso\s*\d+\s*:)\s*", re.UNICODE)


@register.filter(name="procedure_summary")
def procedure_summary(value):
    """Junta los pasos del procedimiento en una línea corta, sin 'Paso N:'.

    Toma las primeras 6 palabras de cada paso para expresar la acción clave.
    Ejemplo: "Identificar los componentes → Representar el conjunto → Validar"
    """
    if not value:
        return ""
    parts = []
    for step in value:
        text = _PASO_RE.sub("", str(step)).strip()
        words = text.split()
        snippet = " ".join(words[:6])
        if len(words) > 6:
            snippet += "…"
        parts.append(snippet)
    return " → ".join(parts)


@register.filter(name="bold_step")
def bold_step(value):
    """Si el texto empieza con 'Paso N:', lo envuelve en <strong>."""
    if not value:
        return ""
    text = escape(str(value))
    result = _PASO_RE.sub(
        lambda m: '<strong class="learn-procedure__step-label">' + m.group(1) + "</strong> ",
        text,
    )
    return mark_safe(result)


@register.filter(name="markdown")
def markdown_filter(value):
    if not value:
        return ""

    text = str(value)
    for delimiter, token in _LATEX_DELIMITER_TOKENS.items():
        text = text.replace(delimiter, token)

    html = md.markdown(text, extensions=["fenced_code", "tables", "nl2br"])
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=False,
    )

    for delimiter, token in _LATEX_DELIMITER_TOKENS.items():
        clean_html = clean_html.replace(token, delimiter)

    return mark_safe(clean_html)


def _contains_explicit_math_delimiters(text):
    return "$" in text or r"\(" in text or r"\[" in text


def _looks_like_raw_formula(text):
    candidate = text.strip()
    if not candidate or _contains_explicit_math_delimiters(candidate):
        return False
    long_words = re.findall(r"\b[A-Za-zÁÉÍÓÚáéíóúñÑ]{3,}\b", candidate)
    for word in long_words:
        lowered = word.lower()
        if lowered == "rad":
            continue
        if re.search(rf"{re.escape(word)}\(", candidate):
            continue
        return False
    if not re.search(r"[0-9A-Za-z|]", candidate):
        return False
    return bool(
        re.search(r"[=+*/^|\\{}\[\]()]|\d[A-Za-z]|[A-Za-z]\d|-\d", candidate)
    )


def _normalize_raw_formula(text):
    formula = str(text).strip()
    formula = formula.replace("∩", r" \cap ")
    formula = formula.replace("∪", r" \cup ")
    formula = formula.replace("∈", r" \in ")
    formula = formula.replace("∉", r" \notin ")
    formula = formula.replace("π", r"\pi")
    formula = re.sub(r"√\(([^)]+)\)", r"\\sqrt{\1}", formula)
    formula = re.sub(
        r"(?<=\b[A-Za-z])\\(?=[A-Za-z]\b)",
        r" \\setminus ",
        formula,
    )
    formula = re.sub(r"(\d+)" + _DEGREE_SIGN, r"\1^\\circ", formula)
    formula = formula.replace("{", r"\{").replace("}", r"\}")
    formula = re.sub(r"\s{2,}", " ", formula).strip()
    return f"${formula}$"


def _wrap_raw_formula_match(match):
    formula = match.group("formula")
    if not _looks_like_raw_formula(formula):
        return formula
    return _normalize_raw_formula(formula)


def _wrap_raw_formula_after_colon(match):
    formula = match.group("formula")
    if not _looks_like_raw_formula(formula):
        return match.group(0)
    return (
        f"{match.group('label')}{_normalize_raw_formula(formula)}"
        f"{match.group('punct')}"
    )


def _apply_outside_inline_math(text, pattern, replacement):
    parts = _INLINE_MATH_PROTECTED_RE.split(text)
    for index, part in enumerate(parts):
        if index % 2 == 0:
            parts[index] = pattern.sub(replacement, part)
    return "".join(parts)


def _auto_mathify_inline_text(value):
    text = str(value)
    if _contains_explicit_math_delimiters(text):
        return text

    text = _apply_outside_inline_math(text, _RAW_SET_ASSIGN_RE, _wrap_raw_formula_match)
    text = _apply_outside_inline_math(text, _RAW_SET_BLOCK_RE, _wrap_raw_formula_match)
    text = _apply_outside_inline_math(text, _RAW_COMPACT_PRODUCT_RE, _wrap_raw_formula_match)
    text = _apply_outside_inline_math(text, _RAW_CHAINED_PARENS_RE, _wrap_raw_formula_match)
    text = _apply_outside_inline_math(text, _RAW_COLON_SPAN_RE, _wrap_raw_formula_after_colon)
    text = _apply_outside_inline_math(text, _RAW_ALGEBRA_SPAN_RE, _wrap_raw_formula_match)
    return _apply_outside_inline_math(text, _RAW_GROUP_RE, _wrap_raw_formula_match)


@register.filter(name="markdown_inline")
def markdown_inline_filter(value):
    html = str(markdown_filter(_auto_mathify_inline_text(value)))
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return mark_safe(html)
