import json
import typing

from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware
from aiohttp_session import get_session

from data_service.admin.models import Admin
from data_service.web.jwt_utils import UserRole, decode_jwt

# from data_service.admin.models import AdminModel
from data_service.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from data_service.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
    except HTTPUnprocessableEntity as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPException as e:
        return error_json_response(
            http_status=e.status,
            status=HTTP_ERROR_CODES[e.status],
            message=str(e),
            # data=json.loads(e.text) if e.text else {}
        )
    except Exception as e:
        request.app.logger.error("Exception", exc_info=e)
        return error_json_response(
            http_status=500, status="internal server error", message=str(e)
        )

    return response


@middleware
async def auth_middleware(request: "Request", handler):
    # session = await get_session(request)
    # request.admin = Admin.from_session(session)
    # return await handler(request)
    request.actor = None

    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth.removeprefix("Bearer ").strip()
        payload = decode_jwt(token)
        if payload:
            # request.actor = payload
            request.actor = {
                "role": UserRole(payload.get("role"))
                if payload.get("role")
                else None,
                "id": payload.get("sub"),
            }
            return await handler(request)

    session = await get_session(request)
    admin = Admin.from_session(session)
    if admin:
        request.actor = {"role": UserRole.ADMIN, "id": admin.id}
    return await handler(request)


def setup_middlewares(app: "Application"):
    app.middlewares.append(auth_middleware)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
