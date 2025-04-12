from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validates,
)


class UserTelegramIdSchema(Schema):
    telegram_id = fields.Str(required=True)


class UserSchema(Schema):
    id = fields.Int(required=False)
    telegram_id = fields.Str(required=True)
    username = fields.Str(required=False)
    full_name = fields.Str(required=False)


class AnswerSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    points = fields.Int(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    answers = fields.Nested(AnswerSchema, required=True, many=True)

    @validates("answers")
    def validate_answers(self, value):
        if len(value) != 5:
            raise ValidationError("Should be 5 answers")

        titles = [answer["title"].lower() for answer in value]
        if len(titles) != len(set(titles)):
            raise ValidationError("Duplicate answer titles found")

        points = [answer["points"] for answer in value]
        if len(points) != len(set(points)):
            raise ValidationError("Duplicate answer points found")


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)


class ChatStateSchema(Schema):
    chat_id = fields.Str(required=True)
    state = fields.Str(required=True)


class QuestionDeleteSchema(Schema):
    id = fields.Int(required=True)
