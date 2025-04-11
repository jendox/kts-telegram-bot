from http import HTTPStatus

from aiohttp.web_response import json_response
from aiohttp_apispec import response_schema

from data_service.quiz.schemes import ListQuestionSchema, QuestionSchema
from data_service.web.app import View


class QuestionListView(View):
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.question_accessor.get_all_questions()
        return json_response(
            data=ListQuestionSchema().dump({"questions": questions}),
            status=HTTPStatus.OK
        )


class QuestionRandomView(View):
    @response_schema(QuestionSchema)
    async def get(self):
        question = await self.store.question_accessor.get_random_question()
        return json_response(
            data=QuestionSchema().dump(question)
        )
