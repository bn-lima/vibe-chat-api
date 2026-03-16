import os
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vibe_chat.settings')

from django.core.asgi import get_asgi_application

asgi_application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from chat.middleware import AuthTokenMiddleware
from chat.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthTokenMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})
