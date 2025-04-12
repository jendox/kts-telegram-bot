from marshmallow import EXCLUDE, fields

from shared.client.schemes.base import BaseSchema
from shared.client.schemes.callback_query import CallbackQuerySchema
from shared.client.schemes.message import MessageSchema
from shared.client.types import Update

__all__ = ("UpdateSchema",)


class UpdateSchema(BaseSchema):
    class Meta:
        model = Update
        unknown = EXCLUDE

    update_id = fields.Int(required=True)
    message = fields.Nested(MessageSchema, allow_none=True)
    callback_query = fields.Nested(CallbackQuerySchema, allow_none=True)
