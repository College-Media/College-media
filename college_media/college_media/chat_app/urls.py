# In your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:conversation_id>/', views.chat_view, name='chat'), 
    path('chat',views.loadchat,name='chat'),
    # path('chat/<int:user_id>/messages/', views.load_chat_messages, name='load_chat_messages')    # Profile page
]