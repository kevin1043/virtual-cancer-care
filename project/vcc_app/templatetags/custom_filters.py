from django import template

register = template.Library()

@register.filter
def getattr(obj, attr):
    try:
        return obj.__getattribute__(attr)
    except AttributeError:
        return ""
