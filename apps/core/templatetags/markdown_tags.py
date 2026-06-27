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


@register.filter(name="to_json")
def to_json_filter(value):
    return _json.dumps(value, ensure_ascii=False)


@register.filter(name="markdown")
def markdown_filter(value):
    if not value:
        return ""

    html = md.markdown(value, extensions=["fenced_code", "tables", "nl2br"])
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=False,
    )

    return mark_safe(clean_html)
