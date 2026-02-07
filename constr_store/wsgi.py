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

# WhiteNoise для static и media файлов
application = WhiteNoise(
    application,
    static_root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'),
    static_prefix='/static/',
    autorefresh=True
)

# Добавляем media файлы
application.add_files(
    os.path.join(os.path.dirname(__file__), '..', 'media'),
    prefix='/media/'
)
