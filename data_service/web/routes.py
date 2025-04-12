from aiohttp.web_app import Application


def setup_routes(app: Application):
    from data_service.admin.routes import setup_routes as admin_setup_routes
    from data_service.quiz.routes import setup_routes as quiz_setup_routes

    quiz_setup_routes(app)
    admin_setup_routes(app)
