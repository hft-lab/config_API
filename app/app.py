
from aiohttp import web

from core.services.postgres import setup_postgres, clean_postgres



def create_application():
    app = web.Application()

    app.on_startup.append(setup_postgres)
    app.on_cleanup.append(clean_postgres)

    from routes import setup_routes
    setup_routes(app)

    from core.middlewares.authorization import auth_middleware
    app.middlewares.append(auth_middleware)

    return app
