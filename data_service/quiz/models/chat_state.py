from sqlalchemy.orm import Mapped, mapped_column

from data_service.store.database.sqlalchemy_base import (
    BaseModel,
)


class ChatState(BaseModel):
    __tablename__ = "chat_states"

    chat_id: Mapped[str] = mapped_column(primary_key=True)
    state: Mapped[str]
