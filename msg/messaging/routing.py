# messaging/routing.py

from django.urls import path
from .consumers import PersonalChatConsumer

websocket_urlpatterns = [
    path(r'ws/messages/<user_name>/', PersonalChatConsumer.as_asgi()),
]
