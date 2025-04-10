from sqlalchemy.orm import Mapped, relationship

from database.models.answer import Answer
from database.sqlalchemy_base import BaseModel, prim_inc_an, uniq_str_an


class Question(BaseModel):
    __tablename__ = "questions"

    id: Mapped[prim_inc_an]
    title: Mapped[uniq_str_an]

    answers: Mapped[list[Answer]] = relationship(
        "Answer", back_populates="question", cascade="all, del-orphan"
    )
