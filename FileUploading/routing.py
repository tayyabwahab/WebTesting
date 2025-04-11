# routing.py
from django.urls import path
from FileUploading.consumers import CameraConsumer

websocket_urlpatterns = [
    path('ws/video/', CameraConsumer.as_asgi()),
]
