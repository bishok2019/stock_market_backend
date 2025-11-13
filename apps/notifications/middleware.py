import logging
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()
logger = logging.getLogger(__name__)


@database_sync_to_async
def get_user_from_token(token_key):
    try:
        token = AccessToken(token_key)
        user_id = token.payload.get("user_id")
        user = User.objects.get(id=user_id)
        logger.info(f"User authenticated: {user.id}")
        return user
    except Exception as e:
        logger.error(f"Token authentication failed: {str(e)}")
        return AnonymousUser()


class JWTAuthMiddleware:
    """JWT authentication middleware for WebSocket connections"""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Get token from query string
        query_string = scope.get("query_string", b"").decode()
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]

        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
