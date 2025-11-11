from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/private/", consumers.NotificationConsumer.as_asgi()),
    # path("ws/public/", consumers.PublicNotificationConsumer.as_asgi()),
]
