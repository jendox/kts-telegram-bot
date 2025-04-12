import random
from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload

from data_service.quiz.models import Answer, Question
from data_service.store.repositories.base_repo import BaseRepository


class QuestionRepository(BaseRepository):
    async def get_by_id(self, question_id: int) -> Question | None:
        stmt = (select(Question).where(Question.id == question_id)).options(
            joinedload(Question.answers)
        )
        return await self.session.scalar(stmt)

    async def get_all(self) -> Sequence[Question]:
        stmt = select(Question).options(joinedload(Question.answers))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_random(self) -> Question | None:
        stmt = select(Question.id)
        result = await self.session.execute(stmt)
        ids = result.scalars().all()
        if ids:
            return await self.get_by_id(random.choices(ids)[0])

        return None

    async def create(
        self, title: str, answers: list[dict[str, Any]]
    ) -> Question | None:
        answers = [
            Answer(title=answer["title"], points=answer["points"])
            for answer in answers
        ]
        question = Question(title=title, answers=answers)
        self.session.add(question)
        await self.session.commit()
        return question

    async def delete(self, question_id: int) -> None:
        stmt = delete(Question).where(Question.id == question_id)
        await self.session.execute(stmt)
        await self.session.commit()
