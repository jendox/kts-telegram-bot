import typing

from sqlalchemy.orm import Mapped, relationship

from data_service.store.database.sqlalchemy_base import (
    BaseModel,
    prim_inc_an,
    uniq_str_an,
)

if typing.TYPE_CHECKING:
    from data_service.quiz.models import Answer


class Question(BaseModel):
    __tablename__ = "questions"

    id: Mapped[prim_inc_an]
    title: Mapped[uniq_str_an]

    answers: Mapped[list["Answer"]] = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
