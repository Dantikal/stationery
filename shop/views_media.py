from django.http import HttpResponse, Http404
from django.conf import settings
import os
import mimetypes

def serve_media(request, path):
    """Обслуживает media файлы в продакшене"""
    if not settings.DEBUG:
        # В продакшене обслуживаем media файлы
        media_root = settings.MEDIA_ROOT
        file_path = os.path.join(media_root, path)
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Определяем MIME тип
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'
            
            # Читаем файл
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=mime_type)
                response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
                return response
        else:
            raise Http404("Файл не найден")
    else:
        raise Http404("Media файлы обслуживаются Django в DEBUG режиме")
