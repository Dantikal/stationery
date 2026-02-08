"""
WSGI config for constr_store project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'constr_store.settings')

application = get_wsgi_application()

# WhiteNoise для static файлов
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'),
    prefix='/static/',
    autorefresh=True
)

# Добавляем media файлы из постоянного хранилища
media_root = '/opt/render/project/src/media' if not os.environ.get('DJANGO_DEBUG') else os.path.join(os.path.dirname(__file__), '..', 'media')
application.add_files(media_root, prefix='/media/')
