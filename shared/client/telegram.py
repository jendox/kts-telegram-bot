import asyncio
import json
import os
from logging import getLogger
from typing import Any

from aiohttp import ClientSession
from aiohttp.web_exceptions import HTTPBadRequest, HTTPUnauthorized, HTTPForbidden, HTTPConflict, \
    HTTPInternalServerError

API_URL = "https://api.telegram.org/"

REQUEST_MAX_TRIES = 5

LOGGER_NAME = "telegram_client"


class ApiMethods:
    get_updates = "getUpdates"
    send_message = "sendMessage"
    answer_callback_query = "answerCallbackQuery"


class TelegramClient:
    def __init__(self):
        self.logger = getLogger(LOGGER_NAME)
        self.token: str | None = None
        self.session: ClientSession | None = None

    async def start(self) -> None:
        """Запускает телеграм клиент - создает сессию"""
        try:
            self.token = os.getenv("BOT_TOKEN", default=None)
            self.session = ClientSession(base_url=API_URL)
            self.logger.info("Telegram client successfully started")
        except Exception as e:
            self.logger.error("Error starting telegram client: %s", str(e))
            raise

    async def stop(self) -> None:
        """Останавливает телеграм клиент - закрывает сессию"""
        if self.session:
            await self.session.close()
            self.logger.info("Telegram client stopped")

    async def _make_request(self, route: str, **kwargs) -> Any:
        """Делает запрос к серверу телеграм
        Args:
            route (str): api к которому делается запрос
            kwargs: параметры
        """
        url = f"/bot{self.token}/{route}"
        self.logger.debug("Making request to %s with params: %s", kwargs, url)
        for tries_count in range(REQUEST_MAX_TRIES):
            async with self.session.post(url, **kwargs) as response:
                data = await response.json()
                if data.get("ok") is True:
                    return data.get("result")
                description = data.get("description")
                parameters = data.get("parameters")

                if (
                        parameters is not None
                        and "retry_after" in parameters
                        and tries_count < REQUEST_MAX_TRIES
                ):
                    await asyncio.sleep(parameters.get("retry_after"))
                    continue

                text = json.dumps(
                    {"description": description, "parameters": parameters}
                )

                if response.status == 400:
                    raise HTTPBadRequest(text=text)
                if response.status in (401, 404):
                    raise HTTPUnauthorized(text=text)
                if response.status == 403:
                    raise HTTPForbidden(text=text)
                if response.status == 409:
                    raise HTTPConflict(text=text)
                if response.status >= 500:
                    raise HTTPInternalServerError(text=text)
                raise HTTPInternalServerError(text=text)
        return None

    async def get_updates(
            self,
            offset: int = 0,
            limit: int = 100,
            timeout: int = 0,
            allowed_updates: list[str] = ("message", "callback_query")
    ) -> list[dict[str, Any]]:
        """Получает обновления с сервера телеграм
        Args:
            offset (int): identifier of the first update to be returned
            limit (int): limits the number of updates to be retrieved
            timeout (int): timeout in seconds for long polling (should be positive)
            allowed_updates: a json-serialized list of the update types you want your bot to receive
        Return:
            список обновлений
        """
        return await self._make_request(
            ApiMethods.get_updates,
            json={
                "offset": offset,
                "limit": limit,
                "timeout": timeout,
                "allowed_updates": allowed_updates
            }
        )
