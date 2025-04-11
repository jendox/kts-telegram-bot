from data_service.base.base_accessor import BaseAccessor, with_session
from data_service.store.repositories.question_repo import QuestionRepository
from data_service.store.repositories.user_repo import UserRepository


class QuestionAccessor(BaseAccessor):
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


class UserAccessor(BaseAccessor):
    @with_session
    async def get_by_telegram_id(self, session, telegram_id: str):
        repo = UserRepository(session)
        return await repo.get_by_telegram_id(telegram_id)
