from sqlalchemy import delete, insert, select, update

from data_service.quiz.models import ChatState
from data_service.store.repositories.base_repo import BaseRepository


class FSMStateRepository(BaseRepository):
    async def get_state(self, chat_id: str) -> str | None:
        return await self.session.scalar(
            select(ChatState).where(ChatState.chat_id == chat_id)
        )

    async def set_state(self, chat_id: str, state: str):
        result = await self.get_state(chat_id)
        if result:
            await self.session.execute(
                update(ChatState)
                .where(ChatState.chat_id == chat_id)
                .values(state=state)
            )
        else:
            await self.session.execute(
                insert(ChatState).values(chat_id=chat_id, state=state)
            )
        await self.session.commit()

    async def clear_state(self, chat_id: str):
        await self.session.execute(
            delete(ChatState).where(ChatState.chat_id == chat_id)
        )
        await self.session.commit()
