import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.core.wsgi import get_wsgi_application


class MediaFilesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(settings.MEDIA_URL):
            try:
                # Remove MEDIA_URL from path
                file_path = request.path[len(settings.MEDIA_URL):]
                full_path = os.path.join(settings.MEDIA_ROOT, file_path)
                
                # Security check
                if not os.path.abspath(full_path).startswith(os.path.abspath(settings.MEDIA_ROOT)):
                    raise Http404()
                
                if os.path.exists(full_path) and os.path.isfile(full_path):
                    with open(full_path, 'rb') as f:
                        content = f.read()
                    
                    # Determine content type
                    if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                        content_type = 'image/jpeg'
                    elif file_path.endswith('.png'):
                        content_type = 'image/png'
                    elif file_path.endswith('.gif'):
                        content_type = 'image/gif'
                    elif file_path.endswith('.webp'):
                        content_type = 'image/webp'
                    else:
                        content_type = 'application/octet-stream'
                    
                    response = HttpResponse(content, content_type=content_type)
                    return response
                else:
                    raise Http404()
            except Exception:
                pass
        
        response = self.get_response(request)
        return response
