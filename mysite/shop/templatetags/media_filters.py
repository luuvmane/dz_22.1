from django import template

register = template.Library()


@register.filter
def media_url(path):
    return f'/media/{path}'
