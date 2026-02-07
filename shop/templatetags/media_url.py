from django import template
from django.conf import settings
import os

register = template.Library()

@register.filter
def media_url(value):
    """Return media URL that works in both development and production"""
    if not value:
        return ''
    
    # Нормализуем путь (убираем дублирующиеся разделители)
    path = value.strip('/')
    
    # Убираем возможные префиксы
    prefixes = ['media/', 'static/media/', 'static/']
    for prefix in prefixes:
        if path.startswith(prefix):
            path = path[len(prefix):]
            break
    
    # Возвращаем правильный путь в зависимости от окружения
    if settings.DEBUG:
        return f'/media/{path}'
    else:
        # В продакшене используем прямой URL к media view
        return f'/media/{path}'