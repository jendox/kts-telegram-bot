from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None


@dataclass
class Chat:
    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_forum: bool | None = None


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
class CallbackQuery:
    id: str
    from_: User
    chat_instance: str
    message: Message | None = None
    inline_message_id: str | None = None
    data: str | None = None
    game_short_name: str | None = None


@dataclass
class Update:
    update_id: int
    message: Message | None = None
    callback_query: CallbackQuery | None = None


@dataclass
class RequestedUpdate:
    offset: int | None = None
    limit: int = 100
    timeout: int = 0
    allowed_updates: list[str] | None = None
