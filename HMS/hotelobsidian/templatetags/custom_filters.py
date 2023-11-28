from django import template

register = template.Library()

@register.filter
def ends_with_number(value):
    parts = value.split('/')
    return parts[-2].isdigit()