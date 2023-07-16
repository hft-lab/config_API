from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_exceptions import HTTPNotFound
from marshmallow import ValidationError

from core.exceptions import AuthorizationError, HandlerError, DatabaseError, NotFoundError


class BaseView(web.View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.status = None
        self.method = None
        self.handler = None

    async def _handle(self, *args, **kwargs):
        try:
            self.data = await self.method(self.handler, *args, **kwargs)
            self.status = 200

        except AuthorizationError:
            self.data = {'code': 0, 'message': 'Token is invalid.'}
            self.status = 401

        except JSONDecodeError:
            self.data = {'code': 1, 'message': 'Invalid json body'}
            self.status = 400

        except ValidationError as error:
            self.data = {'code': 2, 'message': error.messages}
            self.status = 400

        except HandlerError as error:
            self.data = {'code': 3, 'message': error.messages}
            self.status = 400

        except DatabaseError:
            self.data = {'code': 4, 'message': 'Invalid data body'}
            self.status = 400

        except NotFoundError as error:
            self.data = {'code': 5, 'message': error.messages}
            self.status = 404

        except HTTPNotFound as error:
            self.data = {'code': 5, 'message': error.reason}
            self.status = 404

        finally:
            return web.json_response(data=self.data, status=self.status)

