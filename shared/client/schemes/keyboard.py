from marshmallow import fields, post_load

from shared.client.schemes.base import BaseSchema
from shared.client.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

__all__ = (
    "InlineKeyboardButtonSchema",
    "InlineKeyboardMarkupSchema",
)


class InlineKeyboardButtonSchema(BaseSchema):
    class Meta:
        model = InlineKeyboardButton

    text = fields.Str(required=True)
    callback_data = fields.Str(required=True)

    @post_load
    def make_button(self, data, **kwargs):
        return InlineKeyboardButton(**data)


class InlineKeyboardMarkupSchema(BaseSchema):
    class Meta:
        model = InlineKeyboardMarkup

    inline_keyboard = fields.List(
        fields.List(fields.Nested(InlineKeyboardButtonSchema), required=True)
    )

    @post_load
    def make_markup(self, data, **kwargs):
        return InlineKeyboardMarkup(**data)

    """
    markup_data = {
        "inline_keyboard": [
            [{"text": "Button 1", "callback_data": "action1"}],
            [{"text": "Button 2", "callback_data": "action2"}]
        ]
    }
    """
