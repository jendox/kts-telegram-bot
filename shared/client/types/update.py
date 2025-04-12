from dataclasses import dataclass

from shared.client.types.callback_query import CallbackQuery
from shared.client.types.message import Message

__all__ = ("Update",)


@dataclass
class Update:
    update_id: int
    message: Message | None = None
    callback_query: CallbackQuery | None = None
