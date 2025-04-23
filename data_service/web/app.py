import os

from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from data_service.admin.models import Admin
from data_service.store.database.database import Database
from data_service.store.store import Store, setup_store
from data_service.web.config import Config, setup_config
from data_service.web.logger import setup_logging
from data_service.web.middlewares import setup_middlewares
from data_service.web.routes import setup_routes


class Application(AiohttpApplication):
    config: Config | None = None
    store: Store | None = None
    database: Database | None = None


class Request(AiohttpRequest):
    admin: Admin | None = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self) -> Database:
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

    @property
    def querystring(self) -> dict:
        return self.request.get("querystring", {})


app = Application()


def setup_app() -> Application:
    setup_logging(app)
    setup_config(app)
    session_setup(app, EncryptedCookieStorage(os.getenv("SESSION_KEY")))
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Telegram Bot API", url="/docs/json", swagger_path="/docs"
    )
    setup_middlewares(app)
    setup_store(app)
    return app
