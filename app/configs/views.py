from app.configs.handler import CreateConfigsHandler
from core.bases.views import BaseView


class ConfigsViews(BaseView):

    async def post(self):
        self.method = CreateConfigsHandler.handle
        self.handler = CreateConfigsHandler(request=self.request)
        return await self._handle()