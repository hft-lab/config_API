from aiohttp import web


def login_required(func):
    async def wrapper(self):
        if not self.request.user:
            return web.json_response(
                {'code': 0, 'message': 'Auth required'},
                status=401
            )
        return await func(self)
    return wrapper


def admin_required(func):
    async def wrapper(self):
        if not self.request.user['role'] in ['admin', 'super_admin']:
            return web.json_response(
                {'code': 0, 'message': 'Permission denied'},
                status=403
            )
        return await func(self)
    return wrapper
