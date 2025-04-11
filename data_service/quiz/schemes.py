from marshmallow import Schema, fields


class UserTelegramIdSchema(Schema):
    telegram_id = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int(required=False)
    telegram_id = fields.Str(required=True)
    username = fields.Str(required=False)
    full_name = fields.Str(required=False)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    points = fields.Int(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    answers = fields.Nested(AnswerSchema, required=True, many=True)


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)


class ChatStateSchema(Schema):
    chat_id = fields.Str(required=True)
    state = fields.Str(required=True)
