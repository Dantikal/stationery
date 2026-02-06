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

# Configure WhiteNoise to serve both static and media files
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'),
    prefix='/static/'
)

# Add media files support
application.add_files(
    root=os.path.join(os.path.dirname(__file__), '..', 'media'),
    prefix='/media/'
)
