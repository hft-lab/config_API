import base64
import orjson

class BaseHandler:

    def __init__(self, request):
        self.request = request

    @property
    def db_engine(self):
        return self.request.app['db']

    @classmethod
    def parse(cls, schema, data):
        return schema().load(data)

    @classmethod
    def dump(cls, schema, data, many=True):
        return schema().dump(data, many=many)

    @classmethod
    def dumps(cls, schema, data, many=True):
        return schema().dumps(data, many=many)

    @classmethod
    def decode(cls, query):
        try:
            return orjson.loads(base64.b64decode(query))
        except ValueError:
            raise ValueError('Invalid base64 encoding.')

