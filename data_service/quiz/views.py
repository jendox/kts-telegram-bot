from aiohttp_apispec import request_schema, response_schema

from data_service.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    UserSchema,
    UserTelegramIdSchema, QuestionDeleteSchema,
)
from data_service.web.app import View
from data_service.web.mixins import AuthRequiredMixin
from data_service.web.utils import json_response


class QuestionDeleteView(AuthRequiredMixin, View):
    @request_schema(QuestionDeleteSchema)
    async def post(self):
        await self.store.question_accessor.delete_question(
            self.data["id"]
        )
        return json_response()


class QuestionListView(View):
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.question_accessor.get_all_questions()
        return json_response(
            data=ListQuestionSchema().dump({"questions": questions})
        )


class QuestionRandomView(View):
    @response_schema(QuestionSchema)
    async def get(self):
        question = await self.store.question_accessor.get_random_question()
        return json_response(data=QuestionSchema().dump(question))


class UserView(View):
    @request_schema(UserTelegramIdSchema)
    @response_schema(UserSchema)
    async def get(self):
        telegram_id = self.querystring.get("telegram_id", None)
        user = await self.store.user_accessor.get_by_telegram_id(telegram_id)
        return json_response(data=UserSchema().dump(user))
