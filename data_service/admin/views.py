from aiohttp_apispec import docs, request_schema, response_schema

from data_service.admin.schemes import AdminSchema
from data_service.web.app import View
from data_service.web.decorators import required_roles
from data_service.web.jwt_utils import UserRole
from data_service.web.mixins import RoleRequiredMixin
from data_service.web.utils import json_response


class AdminLoginView(View):
    @docs(
        tags=["Admin"],
        summary="Authenticate admin",
        description="Authenticate an administrator using email "
        "and password credentials.",
        operation_id="adminLogin",
        responses={
            200: {"description": "Authentication successful."},
            403: {"description": "Invalid credentials provided."},
        },
    )
    @request_schema(AdminSchema)
    @response_schema(AdminSchema)
    async def post(self):
        admin = await self.store.admin_accessor.login(
            request=self.request,
            email=self.data["email"],
            password=self.data["password"],
        )
        return json_response(data=AdminSchema().dump(admin))


@required_roles(UserRole.ADMIN)
class AdminCurrentView(RoleRequiredMixin, View):
    @docs(
        tags=["Admin"],
        summary="Get current admin",
        description="Retrieve information about the currently "
        "authenticated administrator.",
        operation_id="getCurrentAdmin",
        responses={
            200: {"description": "Current administrator information returned."},
            401: {"description": "Authentication required."},
        },
    )
    @response_schema(AdminSchema, 200)
    async def get(self):
        admin = await self.store.admin_accessor.current(self.request)
        return json_response(data=AdminSchema().dump(admin))


@required_roles(UserRole.ADMIN)
class AdminLogoutView(RoleRequiredMixin, View):
    @docs(
        tags=["Admin"],
        summary="Logout admin",
        description="Log out the currently authenticated "
        "administrator and invalidate their session.",
        operation_id="adminLogout",
        responses={
            200: {"description": "Successfully logged out."},
            401: {"description": "Authentication required."},
        },
    )
    async def get(self):
        await self.store.admin_accessor.logout(self.request)
        return json_response()
