from sqlalchemy import select, update

from data_service.quiz.models import User
from data_service.store.repositories.base_repo import BaseRepository


class UserRepository(BaseRepository):
    async def get_by_telegram_id(self, telegram_id: str) -> User | None:
        return await self.session.scalar(
            select(User).where(User.telegram_id == telegram_id)
        )

    async def get_by_username(self, username: str) -> list[User] | None:
        await self.session.scalars(
            select(User).where(User.username == username)
        )

    async def create_user(
        self,
        telegram_id: str,
        username: str | None = None,
        full_name: str | None = None,
    ) -> User:
        user = User(
            telegram_id=telegram_id, username=username, full_name=full_name
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_username(
        self, telegram_id: str, new_username: str
    ) -> None:
        await self.session.execute(
            update(User)
            .where(User.telegram_id == telegram_id)
            .values(username=new_username)
        )
        await self.session.commit()
