from aiohttp_apispec import request_schema, response_schema

from data_service.quiz.schemes import (
    ListQuestionSchema,
    QuestionDeleteSchema,
    QuestionSchema,
    UserSchema,
    UserTelegramIdSchema,
)
from data_service.web.app import View
from data_service.web.decorators import required_roles
from data_service.web.jwt_utils import UserRole
from data_service.web.mixins import RoleRequiredMixin
from data_service.web.utils import json_response


@required_roles(UserRole.ADMIN)
class QuestionDeleteView(RoleRequiredMixin, View):
    @request_schema(QuestionDeleteSchema)
    async def post(self):
        await self.store.question_accessor.delete_question(self.data["id"])
        return json_response()


@required_roles(UserRole.ADMIN, UserRole.BOT)
class QuestionListView(RoleRequiredMixin, View):
    @response_schema(ListQuestionSchema)
    async def get(self):
        questions = await self.store.question_accessor.get_all_questions()
        return json_response(
            data=ListQuestionSchema().dump({"questions": questions})
        )


@required_roles(UserRole.ADMIN, UserRole.BOT)
class QuestionRandomView(RoleRequiredMixin, View):
    @response_schema(QuestionSchema)
    async def get(self):
        question = await self.store.question_accessor.get_random_question()
        return json_response(data=QuestionSchema().dump(question))


@required_roles(UserRole.ADMIN, UserRole.BOT)
class UserView(RoleRequiredMixin, View):
    @request_schema(UserTelegramIdSchema)
    @response_schema(UserSchema)
    async def get(self):
        telegram_id = self.querystring.get("telegram_id", None)
        user = await self.store.user_accessor.get_by_telegram_id(telegram_id)
        return json_response(data=UserSchema().dump(user))
