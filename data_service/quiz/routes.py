import typing

from data_service.quiz.views import (
    GameSessionSaveView,
    LastGameSessionView,
    QuestionAddView,
    QuestionDeleteView,
    QuestionListView,
    QuestionRandomView,
)

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/quiz.random_question", QuestionRandomView)
    app.router.add_view("/quiz.list_questions", QuestionListView)
    app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.delete_question", QuestionDeleteView)
    app.router.add_view("/quiz.save_game", GameSessionSaveView)
    app.router.add_view("/quiz.last_game", LastGameSessionView)
