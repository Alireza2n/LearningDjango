from django import template

register = template.Library()


@register.filter
def jdate(value, format="%Y-%m-%d"):
    """
    Formats date based on `format`
    """
    return value.strftime(format)
