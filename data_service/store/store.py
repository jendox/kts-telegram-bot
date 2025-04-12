import typing

from data_service.store.admin.accessor import AdminAccessor
from data_service.store.database import Database
from data_service.store.quiz.accessor import QuestionAccessor, UserAccessor

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app
        self.question_accessor = QuestionAccessor(app)
        self.user_accessor = UserAccessor(app)
        self.admin_accessor = AdminAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
