from django import template

register = template.Library()

@register.filter
def get_attr(value):
    try:
        return value.split("|")[0]
    except:
        return value


@register.filter
def get_label(value):
    try:
        return value.split("|")[1]
    except:
        return value
