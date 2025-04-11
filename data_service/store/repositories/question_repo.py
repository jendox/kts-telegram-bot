from collections.abc import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from data_service.quiz.models import Answer, Question
from data_service.store.repositories.base_repo import BaseRepository


class QuestionRepository(BaseRepository):
    async def get_by_id(self, question_id: int) -> Question | None:
        stmt = select(Question).where(Question.id == question_id)
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
            import random

            return await self.get_by_id(random.choices(ids))
        return None

    async def create_question(
        self, title: str, answers: Iterable[Answer]
    ) -> Question | None:
        answers = list(answers)

        titles = [a.title.lower().strip() for a in answers]
        if len(titles) != len(set(titles)):
            raise ValueError("Duplicate answer titles found")

        points = [a.points for a in answers]
        if len(points) != len(set(points)):
            raise ValueError("Duplicate answer points found")

        question = Question(title=title, answers=answers)
        self.session.add(question)
        await self.session.commit()
        await self.session.refresh(question)
        return question
