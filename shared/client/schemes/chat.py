from marshmallow import EXCLUDE, fields

from shared.client.schemes.base import BaseSchema
from shared.client.types import Chat

__all__ = ("ChatSchema",)


class ChatSchema(BaseSchema):
    class Meta:
        model = Chat
        unknown = EXCLUDE

    id = fields.Int(required=True)
    type = fields.Str(required=True)
    title = fields.Str(allow_none=True)
    username = fields.Str(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    is_forum = fields.Bool(allow_none=True)
