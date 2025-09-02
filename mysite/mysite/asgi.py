import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path  
import fileupload.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            fileupload.routing.websocket_urlpatterns
        )
    ),
})