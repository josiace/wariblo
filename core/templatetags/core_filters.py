from django import template

register = template.Library()

@register.filter
def replace(value, arg):
    """
    Replace all occurrences of a substring with another substring.
    Usage: {{ value|replace:'old|new' }}
    """
    if not value:
        return value
    old, new = arg.split('|', 1)
    return str(value).replace(old, new)
