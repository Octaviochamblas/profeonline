from django import template
from django.utils.safestring import mark_safe
import bleach
import markdown as md

register = template.Library()

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
