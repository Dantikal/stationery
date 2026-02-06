from django import template
from django.conf import settings

register = template.Library()

@register.filter
def media_url(value):
    """Return media URL that works in both development and production"""
    if not value:
        return ''
    
    # Debug logging
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"media_url input: '{value}', DEBUG: {settings.DEBUG}")
    
    # Remove ALL leading prefixes
    if value.startswith('/media/'):
        value = value[7:]  # Remove '/media/'
    elif value.startswith('media/'):
        value = value[6:]  # Remove 'media/'
    elif value.startswith('/static/media/'):
        value = value[13:]  # Remove '/static/media/'
    elif value.startswith('static/media/'):
        value = value[12:]  # Remove 'static/media/'
    
    # Return correct URL based on environment
    if settings.DEBUG:
        result = f'/media/{value}'
    else:
        result = f'/static/media/{value}'  # Исправляем на /static/media/
    
    logger.info(f"media_url output: '{result}'")
    return result
