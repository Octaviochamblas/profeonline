import json as _json
import re
import uuid

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
    "img",
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
    "img": ["src", "alt", "title", "width", "height"],
    "td": ["align"],
    "th": ["align"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


@register.filter(name="to_json")
def to_json_filter(value):
    return _json.dumps(value, ensure_ascii=False)


_PASO_RE = re.compile(r"^(Paso\s*\d+\s*:|\d+\.\s*)", re.UNICODE)


@register.filter(name="procedure_summary")
def procedure_summary(value):
    """Junta los pasos del procedimiento en una línea corta, sin 'Paso N:'.

    Toma las primeras 6 palabras de cada paso para expresar la acción clave.
    Ejemplo: "Identificar los componentes → Representar el conjunto → Validar"
    """
    if not value:
        return ""
    steps = to_steps_filter(value)
    parts = []
    for step in steps:
        text = _PASO_RE.sub("", str(step)).strip()
        words = text.split()
        snippet = " ".join(words[:6])
        if len(words) > 6:
            snippet += "…"
        parts.append(snippet)
    return " → ".join(parts)


@register.filter(name="to_steps")
def to_steps_filter(value):
    """Asegura que un procedimiento (sea lista o texto multilínea) se convierta
    en una lista de pasos limpia, evitando que un string se itere carácter por
    carácter en los templates.
    """
    if not value:
        return []
    if isinstance(value, list):
        return [str(s).strip() for s in value if str(s).strip()]
    if isinstance(value, str):
        lines = [line.strip() for line in value.splitlines() if line.strip()]
        return lines
    return [str(value)]


@register.filter(name="bold_step")
def bold_step(value):
    """Si el texto empieza con 'Paso N:' o 'N.', lo envuelve en <strong>."""
    if not value:
        return ""
    text = escape(str(value))
    result = _PASO_RE.sub(
        lambda m: '<strong class="learn-procedure__step-label">' + m.group(1).strip() + "</strong> ",
        text,
    )
    return mark_safe(result)


# Delimitadores LaTeX soportados por KaTeX (ver static/js/katex-init.js).
# Python-Markdown escapa por defecto '(' y ')' — sin esta protección
# "\(...\)" pierde las barras y KaTeX ya no reconoce el bloque como fórmula.
_MATH_SPAN_RE = re.compile(
    r"\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|\$(?:[^$\n]|\\\$)*?\$",
    re.DOTALL,
)


@register.filter(name="markdown")
def markdown_filter(value):
    if not value:
        return ""

    text = str(value)
    math_spans = []
    nonce = uuid.uuid4().hex

    def _stash(match):
        math_spans.append(match.group(0))
        return f"{nonce}MATH{len(math_spans) - 1}X"

    protected = _MATH_SPAN_RE.sub(_stash, text)
    html = md.markdown(protected, extensions=["fenced_code", "tables", "nl2br"])

    for i, span in enumerate(math_spans):
        html = html.replace(f"{nonce}MATH{i}X", span)

    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=False,
    )

    return mark_safe(clean_html)


@register.filter(name="markdown_inline")
def markdown_inline_filter(value):
    """Como |markdown pero sin envolver el resultado en <p>: para texto corto
    de una línea (enunciado de pregunta, alternativa) donde un bloque no
    encaja dentro de <legend>/<span>."""
    html = str(markdown_filter(value))
    if html.startswith("<p>") and html.endswith("</p>") and "<p>" not in html[3:-4]:
        return mark_safe(html[3:-4])
    return mark_safe(html)


_IMG_RE = re.compile(r"(!\[.*?\]\(.*?\))")
_QUE_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:\*\*)?QU[EÉ](?:\s*\([^)]*\))?(?:\*\*)?\s*:\s*(?:\*\*)?\s*(.*?)(?=(?:\n\s*(?:\*\*)?C[OÓ]MO(?:\s*\([^)]*\))?(?:\*\*)?\s*:\s*(?:\*\*)?)|$)",
    re.DOTALL | re.IGNORECASE,
)
_COMO_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:\*\*)?C[OÓ]MO(?:\s*\([^)]*\))?(?:\*\*)?\s*:\s*(?:\*\*)?\s*(.*)$",
    re.DOTALL | re.IGNORECASE,
)


@register.filter(name="parse_al_terminar")
def parse_al_terminar_filter(value):
    """Parsea el campo 'al_terminar_debes_poder' extrayendo imágenes iniciales,
    intro, y separando 'QUÉ' (objetivo) y 'CÓMO' (mecanismo) para enmarcarlos
    en tarjetas visuales dedicadas.
    """
    if not value:
        return {"is_structured": False, "raw": ""}

    text = str(value).strip()
    images = _IMG_RE.findall(text)
    clean_text = _IMG_RE.sub("", text).strip()

    m_que = _QUE_PATTERN.search(clean_text)
    m_como = _COMO_PATTERN.search(clean_text)

    if not m_que and not m_como:
        return {"is_structured": False, "raw": text}

    intro = ""
    if m_que and m_que.start() > 0:
        intro = clean_text[: m_que.start()].strip()
    elif not m_que and m_como and m_como.start() > 0:
        intro = clean_text[: m_como.start()].strip()

    que_text = m_que.group(1).strip() if m_que else ""
    como_text = m_como.group(1).strip() if m_como else ""

    que_text = re.sub(r"^\*\*\s*", "", que_text)
    como_text = re.sub(r"^\*\*\s*", "", como_text)

    return {
        "is_structured": True,
        "images": images,
        "intro": intro,
        "que": que_text,
        "como": como_text,
        "raw": text,
    }
