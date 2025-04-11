import typing

from data_service.store.database import Database
from data_service.store.quiz.accessor import QuestionAccessor, UserAccessor

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


class Store:
    def __init__(self, app: "Application", session_factory):
        self.app = app
        self.question_accessor = QuestionAccessor(app, session_factory)
        self.user_accessor = UserAccessor(app, session_factory)


def setup_store(app: "Application"):
    app.database = Database(app)

    def init_store(*args, **kwargs):
        session_factory = app.database.session
        app.store = Store(app, session_factory)

    app.on_startup.append(app.database.connect)
    app.on_startup.append(init_store)
    app.on_cleanup.append(app.database.disconnect)
