import re
from django import template
from django.utils.safestring import mark_safe
import markdown as md

register = template.Library()

def escape_html_tags(text):
    if not isinstance(text, str):
        return text
    # Escape `<` if followed by a tag name character, slash, exclamation, or question mark.
    # This prevents the browser from interpreting user input as raw HTML.
    return re.sub(r'<(?=[a-zA-Z/!?])', '&lt;', text)

@register.filter(name="markdown")
def markdown_filter(value):
    if not value:
        return ""
    
    # Escape raw HTML tags
    safe_value = escape_html_tags(value)
    
    # Render markdown to HTML
    html = md.markdown(safe_value, extensions=["fenced_code", "tables", "nl2br"])
    
    # Clean javascript: protocols in href attributes of the output HTML to prevent XSS
    html = re.sub(r'href\s*=\s*["\']\s*javascript:', 'href="#invalid-scheme-', html, flags=re.IGNORECASE)
    
    return mark_safe(html)

