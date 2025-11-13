from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/private/", consumers.PrivateNotificationConsumer.as_asgi()),
    path("ws/public/", consumers.NotificationConsumer.as_asgi()),
]
