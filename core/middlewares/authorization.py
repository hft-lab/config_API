from aiohttp import web

from core.auth.token import UserToken
from core.exceptions import AuthorizationError


async def auth_middleware(app, handler):
    async def middleware(request):
        request.user = None
        token = request.headers.get('token', None)
        try:
            if not UserToken().check_token(token):
                raise AuthorizationError(messages={'message': 'Token is invalid'})
        except AuthorizationError as error:
            return web.json_response(data=error.messages, status=401)

        return await handler(request)
    return middleware
