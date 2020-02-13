from django import template
from django.template.defaultfilters import yesno
from django.utils.safestring import SafeString, mark_safe

from lib.templatetags.custom_filters import nz

register = template.Library()


@register.simple_tag
def get_subset(iterable, index):
    """
    Returns a subset of an iterable
    """
    try:
        value = iterable[int(index)]
    except IndexError or TypeError:
        if TypeError:
            print("index provided is of an invalid type")
        if IndexError:
            print("value does not exist at the index provided")
        value = None

    return value


@register.simple_tag
def add(value, arg):
    return float(nz(value, 0)) + float(nz(arg, 0))


@register.simple_tag
def subtract(value, arg):
    return float(nz(value, 0)) - float(nz(arg, 0))


@register.simple_tag
def echo(value):
    return value
