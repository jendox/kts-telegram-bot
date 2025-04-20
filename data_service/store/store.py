import typing

from data_service.store.admin.accessor import AdminAccessor
from data_service.store.database import Database
from data_service.store.quiz.accessor import (
    QuestionAccessor,
    GameSessionAccessor,
    PlayerAccessor,
)
from data_service.store.quiz.services import GameSessionService

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.app = app
        self.question_accessor = QuestionAccessor(app)
        self.player_accessor = PlayerAccessor(app)
        self.game_session_accessor = GameSessionAccessor(app)
        self.admin_accessor = AdminAccessor(app)

        self.game_session_service = GameSessionService(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
