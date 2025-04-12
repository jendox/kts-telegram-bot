from aiohttp_apispec import request_schema, response_schema

from data_service.admin.schemes import AdminSchema
from data_service.web.app import View
from data_service.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema)
    async def post(self):
        admin = await self.store.admin_accessor.login(
            request=self.request,
            email=self.data["email"],
            password=self.data["password"]
        )
        return json_response(data=AdminSchema().dump(admin))


class AdminCurrentView(View):
    async def get(self):
        admin = await self.store.admin_accessor.current(self.request)
        return json_response(data=AdminSchema().dump(admin))


class AdminLogoutView(View):
    async def get(self):
        await self.store.admin_accessor.logout(self.request)
        return json_response()
