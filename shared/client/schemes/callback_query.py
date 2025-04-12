from marshmallow import EXCLUDE, fields

from shared.client.schemes.base import BaseSchema
from shared.client.schemes.message import MessageSchema
from shared.client.schemes.user import UserSchema
from shared.client.types import CallbackQuery

__all__ = (
    "CallbackQueryReplySchema",
    "CallbackQuerySchema",
)


class CallbackQuerySchema(BaseSchema):
    class Meta:
        model = CallbackQuery
        unknown = EXCLUDE

    id = fields.Str(required=True)
    from_ = fields.Nested(UserSchema, data_key="from", required=True)
    chat_instance = fields.Str(required=True)
    message = fields.Nested(MessageSchema, allow_none=True)
    inline_message_id = fields.Str(allow_none=True)
    data = fields.Str(allow_none=True)
    game_short_name = fields.Str(allow_none=True)


class CallbackQueryReplySchema(BaseSchema):
    callback_query_id = fields.Str(required=True)
    text = fields.Str(allow_none=True)
    show_alert = fields.Bool(allow_none=True)
    url = fields.Str(allow_none=True)
    cache_time = fields.Int(allow_none=True)
