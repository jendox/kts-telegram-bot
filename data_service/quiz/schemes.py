from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validates,
    EXCLUDE, post_load,
)

from data_service.quiz.models import GameSession, GameSessionAnswer, PlayerGameSession


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


class QuestionDeleteSchema(Schema):
    id = fields.Int(required=True)


class PlayerSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    points = fields.Int(required=True)


class RawDateTimeField(fields.DateTime):
    def _deserialize(self, value, attr, data, **kwargs):
        try:
            super()._deserialize(value, attr, data, **kwargs)
        except ValidationError:
            raise
        return value


class GameSessionRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    created_at = RawDateTimeField(required=True)
    finished_at = RawDateTimeField(required=True)
    question = fields.Nested(QuestionSchema, required=True)
    given_answers = fields.Nested(AnswerSchema, many=True)
    players = fields.Nested(PlayerSchema, many=True)


class GameSessionResponseSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)


class GameSessionSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    created_at = fields.DateTime(required=True)
    finished_at = fields.DateTime(required=True)
    question = fields.Nested(QuestionSchema, required=True)
    given_answers = fields.Nested(AnswerSchema, many=True)
    players = fields.Nested(PlayerSchema, many=True)

    @post_load
    def make_game_session(self, data, **kwargs):
        given_answers = data.pop("given_answers", [])
        players = data.pop("players", [])
        question = data.pop("question")

        return GameSession(
            created_at=data["created_at"],
            finished_at=data["finished_at"],
            question_id=question["id"],
            given_answers_assoc=[
                GameSessionAnswer(answer_id=a["id"]) for a in given_answers
            ],
            player_assoc=[
                PlayerGameSession(player_id=p["id"], points=p["points"]) for p in players
            ],
        )
