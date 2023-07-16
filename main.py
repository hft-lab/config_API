from aiohttp import web
import uvloop

from app.app import create_application
from config import Config

app = create_application()


def main():
    uvloop.install()
    web.run_app(app, host=Config.HOST, port=Config.PORT)


if __name__ == '__main__':
    main()
