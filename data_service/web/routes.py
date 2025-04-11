from aiohttp.web_app import Application


def setup_routes(app: Application):
    from data_service.quiz.routes import setup_routes as quiz_setup_routes

    quiz_setup_routes(app)
