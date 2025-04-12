from aiohttp.web_exceptions import HTTPUnauthorized
from aiohttp.web_response import StreamResponse


class AuthRequiredMixin:
    async def _iter(self) -> StreamResponse:
        if self.request.admin is None:
            raise HTTPUnauthorized

        return await super()._iter()
