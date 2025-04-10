from marshmallow import EXCLUDE, Schema, fields, post_dump, post_load

from shared.client.types import (
    CallbackQuery,
    Chat,
    Message,
    MessageEntity,
    Update,
    User,
)


class BaseSchema(Schema):
    @post_load
    def make_object(self, data, **kwargs):
        if hasattr(self.Meta, "model"):
            return self.Meta.model(**data)
        return data

    @post_dump
    def remove_none(self, data, **kwargs) -> dict:
        return {k: v for k, v in data.items() if v is not None}


class UserSchema(BaseSchema):
    class Meta:
        model = User
        unknown = EXCLUDE

    id = fields.Int(required=True)
    is_bot = fields.Bool(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(allow_none=True)
    username = fields.Str(allow_none=True)


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


class UpdateSchema(BaseSchema):
    class Meta:
        model = Update
        unknown = EXCLUDE

    update_id = fields.Int(required=True)
    message = fields.Nested(MessageSchema, allow_none=True)
    callback_query = fields.Nested(CallbackQuerySchema, allow_none=True)


class RequestedUpdateSchema(BaseSchema):
    offset = fields.Int(allow_none=True)
    limit = fields.Int(default=100)
    timeout = fields.Int(default=0)
    allowed_updates = fields.List(fields.Str(), allow_none=True)
