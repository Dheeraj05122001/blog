from django import template
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.utils.safestring import mark_safe

register = template.Library()

def truncate_html_chars(value, arg):
    """
    Strip HTML tags and truncate plain text content to 'arg' characters.
    """
    try:
        arg = int(arg)
    except ValueError:
        return value  # fallback if arg is not a number

    plain_text = strip_tags(value)
    truncated = Truncator(plain_text).chars(arg, truncate='...')
    return mark_safe(truncated)

# Register filter manually (no decorator)
register.filter('truncate_html_chars', truncate_html_chars)
