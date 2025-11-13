"""
ASGI config for stock_market_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

from apps.notifications.middleware import JWTAuthMiddleware
from apps.notifications.routing import websocket_urlpatterns

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_market_backend.settings")


# For Session Based authentication

# application = ProtocolTypeRouter(
#     {
#         "http": get_asgi_application(),
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(websocket_urlpatterns),
#             ),
#         ),
#     }
# )

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns),
        ),
    }
)
