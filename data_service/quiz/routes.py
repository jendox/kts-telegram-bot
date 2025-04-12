import typing

from data_service.quiz.views import (
    QuestionAddView,
    QuestionDeleteView,
    QuestionRandomView,
    UserView, QuestionListView,
)

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/quiz.random_question", QuestionRandomView)
    app.router.add_view("/quiz.list_questions", QuestionListView)
    app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.delete_question", QuestionDeleteView)
    app.router.add_view("/quiz.user", UserView)
