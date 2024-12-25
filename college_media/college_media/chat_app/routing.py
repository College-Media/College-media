from django.urls import path
from chat_app import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:receiver_id>/', consumers.ChatConsumer.as_asgi()),
    path('ws/notification/', consumers.Notifications.as_asgi()),
    path('ws/messages/', consumers.MessageConsumer.as_asgi()),
    
]