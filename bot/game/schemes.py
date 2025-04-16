from marshmallow import EXCLUDE, fields

from bot.core.fsm import State
from bot.game.types import Answer, GameSession, Player, Question
from shared.client.schemes.base import BaseSchema


class AnswerSchema(BaseSchema):
    class Meta:
        model = Answer
        unknown = EXCLUDE

    title = fields.Str(required=True)
    points = fields.Int(required=True)


class QuestionSchema(BaseSchema):
    class Meta:
        model = Question
        unknown = EXCLUDE

    title = fields.Str(required=True)
    answers = fields.Nested(AnswerSchema, required=True, many=True)


class PlayerSchema(BaseSchema):
    class Meta:
        model = Player

    id = fields.Int(required=True)
    name = fields.Str(required=True)
    points = fields.Int(required=True)
    is_active = fields.Bool(required=True)


class GameSessionSchema(BaseSchema):
    class Meta:
        model = GameSession

    chat_id = fields.Int(required=True)
    state = fields.Method(
        required=True,
        serialize="serialize_state",
        deserialize="deserialize_state",
    )
    created_at = fields.DateTime(allow_none=True)
    finished_at = fields.DateTime(allow_none=True)
    players = fields.Nested(PlayerSchema, many=True, required=True)
    question = fields.Nested(QuestionSchema, allow_none=True)
    active_player = fields.Nested(PlayerSchema, allow_none=True)
    given_answers = fields.List(fields.Str())

    def serialize_state(self, obj):
        return obj.state.name if obj.state else None

    def deserialize_state(self, value):
        return State(value) if value else None
