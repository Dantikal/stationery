from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_url(value):
    """Return media URL that works in both development and production"""
    if not value:
        return ''
    
    # Remove leading /media/ if present
    if value.startswith('/media/'):
        value = value[7:]  # Remove '/media/'
    
    # Return correct URL based on environment
    if settings.DEBUG:
        return f'/media/{value}'
    else:
        return f'/static/media/{value}'
