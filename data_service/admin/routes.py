import typing

from data_service.admin.views import AdminLoginView, AdminLogoutView, AdminCurrentView

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


def setup_routes(app: "Application"):
    app.router.add_view("/admin.login", AdminLoginView)
    app.router.add_view("/admin.logout", AdminLogoutView)
    app.router.add_view("/admin.current", AdminCurrentView)
