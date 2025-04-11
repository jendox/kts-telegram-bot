from sqlalchemy.orm import Mapped, mapped_column

from data_service.store.database.sqlalchemy_base import (
    BaseModel,
    prim_inc_an,
)


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[prim_inc_an]
    telegram_id: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
