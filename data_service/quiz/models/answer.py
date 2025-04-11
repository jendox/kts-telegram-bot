from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from data_service.quiz.models.question import Question
from data_service.store.database.sqlalchemy_base import (
    BaseModel,
    prim_inc_an,
)


class Answer(BaseModel):
    __tablename__ = "answers"

    id: Mapped[prim_inc_an]
    title: Mapped[str]
    points: Mapped[int]
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    question: Mapped[Question] = relationship(
        "Question", back_populates="answers"
    )

    __table_args__ = (
        CheckConstraint("points > 0 AND points <= 100", name="points_range"),
    )

    @validates("points")
    def validate_points(self, key, value):
        if not (0 < value <= 100):
            raise ValueError("Points must be between 0 and 100")
        return value
