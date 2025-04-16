from datetime import datetime

from sqlalchemy import ForeignKey, BigInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from data_service.quiz.models import Answer, Question
from data_service.store.database.sqlalchemy_base import (
    BaseModel,
    prim_inc_an,
)


class Player(BaseModel):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    name: Mapped[str] = mapped_column(nullable=True)
    game_session_assoc: Mapped[list["PlayerGameSession"]] = relationship(
        "PlayerGameSession",
        back_populates="player",
        cascade="all, delete-orphan",
    )


class GameSession(BaseModel):
    __tablename__ = "game_sessions"

    id: Mapped[prim_inc_an]
    created_at: Mapped[datetime]
    finished_at: Mapped[datetime]
    question_id: Mapped[int] = mapped_column(
        ForeignKey("questions.id", ondelete="CASCADE")
    )
    question: Mapped[Question] = relationship("Question")

    player_assoc: Mapped[list["PlayerGameSession"]] = relationship(
        "PlayerGameSession",
        back_populates="game_session",
        cascade="all, delete-orphan",
    )
    given_answers_assoc: Mapped[list["GameSessionAnswer"]] = relationship(
        "GameSessionAnswer", back_populates="game_session", cascade="all, delete-orphan"
    )

    session_hash: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)

    __table_args__ = (
        UniqueConstraint("session_hash", name="uq_game_session_hash"),
    )


class PlayerGameSession(BaseModel):
    __tablename__ = "player_game_sessions"

    id: Mapped[prim_inc_an]
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id", ondelete="CASCADE")
    )
    game_session_id: Mapped[int] = mapped_column(
        ForeignKey("game_sessions.id", ondelete="CASCADE")
    )
    points: Mapped[int] = mapped_column(default=0)

    player = relationship("Player", back_populates="game_session_assoc")
    game_session = relationship("GameSession", back_populates="player_assoc")


class GameSessionAnswer(BaseModel):
    __tablename__ = "game_session_answers"

    id: Mapped[prim_inc_an]
    game_session_id: Mapped[int] = mapped_column(ForeignKey("game_sessions.id", ondelete="CASCADE"))
    answer_id: Mapped[int] = mapped_column(ForeignKey("answers.id", ondelete="CASCADE"))

    game_session: Mapped["GameSession"] = relationship("GameSession", back_populates="given_answers_assoc")
    answer: Mapped["Answer"] = relationship("Answer")
