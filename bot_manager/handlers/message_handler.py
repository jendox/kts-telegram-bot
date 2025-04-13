from logging import getLogger

from shared.client.telegram import TelegramClient
from shared.client.types import Message


class MessageHandler:
    def __init__(self, tg_client: TelegramClient):
        self.logger = getLogger(self.__class__.__name__)
        self.tg_client = tg_client

    async def handle_message(self, message: Message):
        try:
            self.logger.info("Handle message: %s", message)
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))

    async def command_handler(self):
        pass
