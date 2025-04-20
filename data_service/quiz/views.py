import json

from aiohttp.web_exceptions import HTTPConflict, HTTPInternalServerError, HTTPNotFound
from aiohttp_apispec import request_schema, response_schema
from sqlalchemy.exc import IntegrityError

from data_service.quiz.schemes import (
    ListQuestionSchema,
    QuestionDeleteSchema,
    QuestionSchema,
    GameSessionSaveRequestSchema,
    GameSessionSaveResponseSchema,
    LastGameSessionResponseSchema,
    LastGameSessionRequestSchema,
)
from data_service.quiz.utils import generate_session_hash, get_session_hash_base
from data_service.web.app import View
from data_service.web.decorators import required_roles
from data_service.web.jwt_utils import UserRole
from data_service.web.mixins import RoleRequiredMixin
from data_service.web.utils import json_response


@required_roles(UserRole.ADMIN)
class QuestionAddView(RoleRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema, 200)
    async def post(self):
        try:
            question = await self.store.question_accessor.create_question(
                self.data["title"], self.data["answers"]
            )
        except IntegrityError as e:
            data = {"error": str(e)}
            if e.orig.pgcode == "23505":
                raise HTTPConflict(text=json.dumps(data)) from e
            raise HTTPInternalServerError(text=json.dumps(data)) from e
        return json_response(data=QuestionSchema().dump(question))


@required_roles(UserRole.ADMIN)
class QuestionDeleteView(RoleRequiredMixin, View):
    @request_schema(QuestionDeleteSchema)
    async def post(self):
        await self.store.question_accessor.delete_question(self.data["id"])
        return json_response()


@required_roles(UserRole.ADMIN)
class QuestionListView(RoleRequiredMixin, View):
    @response_schema(ListQuestionSchema, 200)
    async def get(self):
        questions = await self.store.question_accessor.get_all_questions()
        return json_response(
            data=ListQuestionSchema().dump({"questions": questions})
        )


@required_roles(UserRole.ADMIN, UserRole.BOT)
class QuestionRandomView(RoleRequiredMixin, View):
    @response_schema(QuestionSchema, 200)
    async def get(self):
        question = await self.store.question_accessor.get_random_question()
        return json_response(data=QuestionSchema().dump(question))


@required_roles(UserRole.ADMIN, UserRole.BOT)
class GameSessionSaveView(RoleRequiredMixin, View):
    @request_schema(GameSessionSaveRequestSchema)
    @response_schema(GameSessionSaveResponseSchema, 200)
    async def post(self):
        hash_base = get_session_hash_base(self.data)
        session_hash = generate_session_hash(hash_base)

        if await self.store.game_session_service.is_session_exists(
                session_hash
        ):
            raise HTTPConflict(text="Game session already exists")

        await self.store.game_session_service.ensure_players_exist(
            self.data["players"]
        )
        game_session = await self.store.game_session_accessor.save_game(
            self.data, session_hash
        )

        return json_response(
            data=GameSessionSaveResponseSchema().dump(game_session)
        )


@required_roles(UserRole.ADMIN, UserRole.BOT)
class LastGameSessionView(RoleRequiredMixin, View):
    @request_schema(LastGameSessionRequestSchema, location="querystring")
    @response_schema(LastGameSessionResponseSchema, 200)
    async def get(self):
        game_session = await self.store.game_session_accessor.get_last_session(
            self.data.get("chat_id")
        )
        if not game_session:
            raise HTTPNotFound(text="There is no finished games in this chat yet")
        return json_response(
            data=LastGameSessionResponseSchema().dump(game_session)
        )
