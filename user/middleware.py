# myapp/middleware.py
from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

User = get_user_model()

@database_sync_to_async
def get_user_from_token(token_key):
    try:
        # Create AccessToken instance
        access_token = AccessToken(token_key)
        
        # Explicitly verify the token (includes expiration check)
        access_token.verify()
        
        # If we get here, token is valid and not expired
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        
        # Double-check that user is active
        if user.is_active:
            return user
        else:
            return AnonymousUser()
            
    except (InvalidToken, TokenError, User.DoesNotExist, KeyError, Exception) as e:
        # Log the error for debugging
        print(f"Token validation failed: {e}")
        return AnonymousUser()
class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode("utf8"))
        token = query_string.get('token', [None])[0]

        if token:
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.app(scope, receive, send)
