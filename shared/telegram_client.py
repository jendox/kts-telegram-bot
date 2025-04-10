import os
from logging import getLogger

from aiohttp import ClientSession

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
        self.client: ClientSession | None = None

    async def start(self):
        try:
            self.token = os.getenv("BOT_TOKEN", default=None)
            self.client = ClientSession(base_url=API_URL)
            self.logger.info("Telegram client successfully started")
        except Exception as e:
            self.logger.error("Error starting telegram client: %s", str(e))
            raise

    async def stop(self):
        if self.client:
            await self.client.close()
            self.logger.info("Telegram client stopped")
