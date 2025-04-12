from dataclasses import dataclass

from marshmallow import Schema, fields, post_load, EXCLUDE


@dataclass
class Answer:
    title: str
    points: int


@dataclass
class Question:
    title: str
    answers: list[Answer]


class AnswerSchema(Schema):
    class Meta:
        model = Answer
        unknown = EXCLUDE

    title = fields.Str(required=True)
    points = fields.Int(required=True)

    @post_load
    def make_answer(self, data, **kwargs):
        return Answer(**data)


class QuestionSchema(Schema):
    class Meta:
        model = Question
        unknown = EXCLUDE

    title = fields.Str(required=True)
    answers = fields.Nested(AnswerSchema, required=True, many=True)

    @post_load
    def make_question(self, data, **kwargs):
        return Question(**data)
