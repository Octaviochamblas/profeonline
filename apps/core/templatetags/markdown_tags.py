from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

@register.filter(name="markdown")
def markdown_filter(value):
    if not value:
        return ""
    # Render markdown to HTML with standard extensions
    html = md.markdown(value, extensions=["fenced_code", "tables", "nl2br"])
    return mark_safe(html)
