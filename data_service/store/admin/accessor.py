import json
from http import HTTPStatus

from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_session import get_session, new_session

from data_service.admin.models import Admin
from data_service.base.base_accessor import BaseAccessor, with_session
from data_service.store.repositories.admin_repo import AdminRepository
from data_service.web.app import Request


class AdminAccessor(BaseAccessor):
    @with_session
    async def get_by_email(self, session, email: str) -> Admin | None:
        repo = AdminRepository(session)
        return await repo.get_by_email(email)

    @with_session
    async def create(self, session, email: str, password: str) -> Admin:
        repo = AdminRepository(session)
        return await repo.create(email, password)

    async def login(self, request: Request, email: str, password: str) -> Admin:
        session = await get_session(request)
        admin = Admin.from_session(session)
        if admin is None:
            admin = await self.get_by_email(email=email)
            if admin is not None and admin.is_password_valid(password):
                session = await new_session(request)
                admin.to_session(session)
                return admin

            raise HTTPForbidden(
                text=json.dumps(
                    {
                        "http_status": HTTPStatus.FORBIDDEN,
                        "error": "invalid credentials"
                    }
                )
            )

        return admin

    @staticmethod
    async def logout(request: Request):
        session = await get_session(request)
        session.clear()
        session.changed()
