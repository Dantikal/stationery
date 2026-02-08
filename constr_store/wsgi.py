"""
WSGI config for constr_store project.

It exposes WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constr_store.settings')

# Создаем media директорию при старте (без прав на /var/data)
if not os.environ.get('DJANGO_DEBUG'):
    try:
        media_dir = '/var/data/media'
        os.makedirs(media_dir, exist_ok=True)
    except PermissionError:
        # Если нет прав, используем временную папку
        media_dir = '/tmp/media'
        os.makedirs(media_dir, exist_ok=True)

application = get_wsgi_application()

# WhiteNoise для static файлов
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'),
    prefix='/static/',
    autorefresh=True
)

# Добавляем media файлы
if not os.environ.get('DJANGO_DEBUG'):
    try:
        media_root = '/var/data/media'
        application.add_files(media_root, prefix='/media/')
    except:
        # Если нет прав, используем временную папку
        media_root = '/tmp/media'
        application.add_files(media_root, prefix='/media/')
else:
    media_root = os.path.join(os.path.dirname(__file__), '..', 'media')
    application.add_files(media_root, prefix='/media/')
