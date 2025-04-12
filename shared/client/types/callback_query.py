from dataclasses import dataclass

from shared.client.types.message import Message
from shared.client.types.user import User

__all__ = (
    "CallbackQuery",
    "CallbackQueryReply",
)


@dataclass
class CallbackQuery:
    id: str
    from_: User
    chat_instance: str
    message: Message | None = None
    inline_message_id: str | None = None
    data: str | None = None
    game_short_name: str | None = None


@dataclass
class CallbackQueryReply:
    callback_query_id: str
    text: str | None = None
    show_alert: bool | None = None
    url: str | None = None
    cache_time: str | None = None
