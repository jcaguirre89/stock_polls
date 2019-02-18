import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter("loadjson", is_safe=True)
def loadjson(data):
    return json.loads(data)

@register.filter("format_money", is_safe=True)
def format_money(value):
    try:
        value = float(value)
    except ValueError:
        # '' cannot be converted to float
        return f'${0:,.0f}'
    return f'${value:,.0f}'

@register.filter("format_percent", is_safe=True)
def format_percent(value):
    return f'{value*100:.1f}%'

@register.filter("format_ratio", is_safe=True)
def format_ratio(value):
    """ format numbers to 2 point decimals """
    return f'x{value:,.2f}'

@register.filter("format_none", is_safe=True)
def format_none(value):
    """ format None as an m-dash """
    return value or '---'

@register.filter("iconbool", is_safe=True)
def iconbool(value):
    """Given a boolean value, this filter outputs a bootstrap icon + the
    word "Yes" or "No"

    Example Usage:

        {{ user.has_widget|iconbool }}

    """
    if bool(value):
        result = '<i class="glyphicon glyphicon-ok" style="color: #1fb80b;"></i> Yes'
    else:
        result = '<i class="glyphicon glyphicon-remove" style="color: red;"></i> No'
    return mark_safe(result)