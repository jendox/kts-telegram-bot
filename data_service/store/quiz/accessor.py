from typing import Any

from data_service.base.base_accessor import BaseAccessor, with_session
from data_service.store.repositories.game_session_repo import (
    GameSessionRepository,
)
from data_service.store.repositories.player_repo import PlayerRepository
from data_service.store.repositories.question_repo import QuestionRepository


class QuestionAccessor(BaseAccessor):
    @with_session
    async def create_question(
        self, session, title: str, answers: list[dict[str, Any]]
    ):
        repo = QuestionRepository(session)
        return await repo.create(title, answers)

    @with_session
    async def get_all_questions(self, session):
        repo = QuestionRepository(session)
        return await repo.get_all()

    @with_session
    async def get_random_question(self, session):
        repo = QuestionRepository(session)
        return await repo.get_random()

    @with_session
    async def get_by_id(self, session, question_id: int):
        repo = QuestionRepository(session)
        return await repo.get_by_id(question_id)

    @with_session
    async def delete_question(self, session, question_id: int):
        repo = QuestionRepository(session)
        return await repo.delete(question_id)


class GameSessionAccessor(BaseAccessor):
    @with_session
    async def save_game(self, session, data: dict[str, Any], session_hash: str):
        repo = GameSessionRepository(session)
        return await self.safe_execute(repo.save_game(data, session_hash))

    @with_session
    async def get_by_hash(self, session, session_hash: str):
        repo = GameSessionRepository(session)
        return await self.safe_execute(repo.get_by_hash(session_hash))

    @with_session
    async def get_last_session(self, session, chat_id: int):
        repo = GameSessionRepository(session)
        return await self.safe_execute(repo.get_last_session(chat_id))


class PlayerAccessor(BaseAccessor):
    @with_session
    async def get_or_create(self, session, id_: int, name: str):
        repo = PlayerRepository(session)
        return await self.safe_execute(repo.get_or_create(id_, name))
