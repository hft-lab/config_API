import aiohttp_cors
from aiohttp import web

from config import Config
from app.configs import views as configs_views


class HTTP:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'

    @classmethod
    def get_allow_methods(cls):
        return [cls.GET, cls.POST, cls.PUT, cls.DELETE]


ROUTES = (
    [HTTP.POST, f'{Config.API_URL}configs', configs_views.ConfigsViews],
)


def setup_routes(app: web.Application) -> None:
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=HTTP.get_allow_methods()
        )
    })

    for route in ROUTES:
        cors.add(app.router.add_route(*route))
