from marshmallow import EXCLUDE, fields, post_load

from shared.client.schemes.base import BaseSchema
from shared.client.schemes.chat import ChatSchema
from shared.client.schemes.keyboard import InlineKeyboardMarkupSchema
from shared.client.schemes.user import UserSchema
from shared.client.types import (
    Message,
    MessageEntity,
    MessageReply,
    ReplyParameters,
)

__all__ = (
    "MessageEntitySchema",
    "MessageReplySchema",
    "MessageSchema",
    "ReplyParametersSchema",
)


class MessageEntitySchema(BaseSchema):
    class Meta:
        model = MessageEntity
        unknown = EXCLUDE

    type = fields.Str(required=True)
    offset = fields.Int(required=True)
    length = fields.Int(required=True)
    user = fields.Nested(UserSchema, allow_none=True)


class MessageSchema(BaseSchema):
    class Meta:
        model = Message
        unknown = EXCLUDE

    message_id = fields.Int(required=True)
    date = fields.Int(required=True)
    chat = fields.Nested(ChatSchema, required=True)
    from_ = fields.Nested(UserSchema, data_key="from", allow_none=True)
    text = fields.Str(allow_none=True)
    entities = fields.List(fields.Nested(MessageEntitySchema), allow_none=True)
    reply_markup = fields.Field(allow_none=True)


class ReplyParametersSchema(BaseSchema):
    class Meta:
        model = ReplyParameters

    message_id = fields.Int(required=True)
    chat_id = fields.Raw(allow_none=True)
    quote_parse_mode = fields.Str(allow_none=True)


class MessageReplySchema(BaseSchema):
    class Meta:
        model = MessageReply

    chat_id = fields.Int(required=True)
    text = fields.Str(required=True)
    parse_mode = fields.Str(allow_none=True)
    reply_markup = fields.Nested(InlineKeyboardMarkupSchema, allow_none=True)
    reply_parameters = fields.Nested(ReplyParametersSchema, allow_none=True)

    @post_load
    def make_message_reply(self, data, **kwargs):
        return MessageReply(**data)
