from urllib.parse import parse_qs
from channels.exceptions import DenyConnection
from .async_services import get_user_by_auth_token
from channels.middleware import BaseMiddleware

class AuthTokenMiddleware(BaseMiddleware):

    async def __call__(self, scope, receive, send):

        query_str = scope.get("query_string", b"").decode()
        token_list = parse_qs(query_str).get("token")

        if not token_list:
            raise DenyConnection()
        
        token = token_list[0]
        user = await get_user_by_auth_token(token)

        if not user:
            raise DenyConnection()
        
        scope["user"] = user
        return await super().__call__(scope, receive, send)