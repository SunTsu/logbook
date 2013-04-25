from django import template

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from re import compile

register = template.Library()
@register.filter(needs_autoescape=True)
def urlizetags(text, autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    pattern = compile(r"(#(\w+))")
    result = pattern.sub(r'<a href="/logbook/tag/\2/">\1</a>', text)
    print result
    return mark_safe(result)


