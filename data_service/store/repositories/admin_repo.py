from sqlalchemy import select

from data_service.admin.models import Admin
from data_service.store.repositories.base_repo import BaseRepository


class AdminRepository(BaseRepository):
    async def get_by_email(self, email: str) -> Admin | None:
        stmt = select(Admin).where(Admin.email == email)
        return await self.session.scalar(stmt)

    async def create(self, email: str, password: str) -> Admin:
        admin = Admin(
            email=email,
            password=Admin.hash_password(password)
        )
        self.session.add(admin)
        await self.session.commit()
        await self.session.refresh(admin)
        return admin
