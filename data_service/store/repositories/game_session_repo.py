from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from data_service.quiz.models import (
    GameSession,
    Question,
    PlayerGameSession,
    GameSessionAnswer,
)
from data_service.quiz.schemes import GameSessionSchema
from data_service.store.repositories.base_repo import BaseRepository


class GameSessionRepository(BaseRepository):
    async def save_game(self, data: dict[str, Any], session_hash: str):
        game_session = GameSessionSchema().load(data)
        game_session.session_hash = session_hash
        self.session.add(game_session)
        await self.session.commit()
        await self.session.refresh(game_session)
        return game_session

    async def get_by_hash(self, session_hash: str) -> GameSession | None:
        stmt = select(GameSession).where(
            GameSession.session_hash == session_hash
        )

        return await self.session.scalar(stmt)

    async def get_last_session(self, chat_id: int) -> GameSession | None:
        stmt = (
            select(GameSession)
            .where(GameSession.chat_id == chat_id)
            .order_by(GameSession.finished_at.desc())
            .options(
                joinedload(GameSession.question),
                joinedload(GameSession.player_assoc).joinedload(
                    PlayerGameSession.player
                )
            )
            .limit(1)
        )

        return await self.session.scalar(stmt)
