import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat_app.routing  # Ensure you have `routing.py` in your `chat_app`

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_media.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For HTTP requests
    "websocket": AuthMiddlewareStack(  # For WebSocket requests
        URLRouter(
            chat_app.routing.websocket_urlpatterns
        )
    ),
})
