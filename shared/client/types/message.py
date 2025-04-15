from dataclasses import dataclass
from typing import Any

from shared.client.types.chat import Chat
from shared.client.types.keyboard import InlineKeyboardMarkup
from shared.client.types.user import User

__all__ = (
    "Message",
    "MessageEntity",
    "MessageReply",
    "ReplyParameters",
)


@dataclass
class MessageEntity:
    type: str
    offset: int
    length: int
    user: User | None = None


@dataclass
class Message:
    message_id: int
    date: int
    chat: Chat
    from_: User | None = None
    text: str | None = None
    entities: list[MessageEntity] | None = None
    reply_markup: Any | None = None


@dataclass
class ReplyParameters:
    message_id: int
    chat_id: int | str | None = None
    quote_parse_mode: str | None = None


@dataclass
class MessageReply:
    chat_id: int
    text: str
    parse_mode: str = "Markdown"
    reply_markup: InlineKeyboardMarkup | None = None
    reply_parameters: ReplyParameters | None = None
