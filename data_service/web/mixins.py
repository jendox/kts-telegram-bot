from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_response import StreamResponse

from data_service.web.jwt_utils import UserRole


class RoleRequiredMixin:
    required_roles: set[str] = {UserRole.ADMIN}

    async def _iter(self) -> StreamResponse:
        actor = getattr(self.request, "actor", None)
        if not actor or actor.get("role") not in self.required_roles:
            raise HTTPUnauthorized

        return await super()._iter()
