from django import template

register = template.Library()

@register.filter("to_str")
def to_str(value):
    return str(value)