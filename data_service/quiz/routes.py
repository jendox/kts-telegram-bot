import typing

from data_service.quiz.views import (
    CreateQuestionView,
    DeleteQuestionView,
    LastGameSessionView,
    ListQuestionsView,
    RandomQuestionView,
    SaveGameSessionView,
)

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/quiz.random_question", RandomQuestionView)
    app.router.add_view("/quiz.list_questions", ListQuestionsView)
    app.router.add_view("/quiz.add_question", CreateQuestionView)
    app.router.add_view("/quiz.delete_question", DeleteQuestionView)
    app.router.add_view("/quiz.save_game", SaveGameSessionView)
    app.router.add_view("/quiz.last_game", LastGameSessionView)
