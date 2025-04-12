from dataclasses import dataclass

__all__ = (
    "InlineKeyboardButton",
    "InlineKeyboardMarkup",
)


@dataclass
class InlineKeyboardButton:
    text: str
    callback_data: str


@dataclass
class InlineKeyboardMarkup:
    inline_keyboard: list[list[InlineKeyboardButton]]
