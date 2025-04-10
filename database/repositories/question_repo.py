import random
from collections.abc import Iterable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.models.answer import Answer
from database.models.question import Question
from database.repositories.base_repo import BaseRepository


class QuestionRepository(BaseRepository):
    async def get_by_id(self, question_id: int) -> Question | None:
        return await self.session.scalar(
            select(Question).where(Question.id == question_id)
        )

    async def get_all(self) -> Sequence[Question]:
        stmt = select(Question).options(joinedload(Question.answers))
        result = await self.session.execute(stmt)
        scalar_result = result.unique().scalars()
        return scalar_result.all()

    async def get_random(self) -> Question | None:
        result = await self.session.execute(select(Question.id))
        ids = result.scalars().all()
        question_id = ids[random.randint(0, len(ids))]
        return await self.get_by_id(question_id)

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
