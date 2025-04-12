from logging import getLogger

from bot_manager.dataservice_client import DataServiceClient
from shared.client.telegram import TelegramClient
from shared.client.types import Message


class MessageHandler:
    def __init__(self, client: TelegramClient, dsv_client: DataServiceClient):
        self.logger = getLogger(self.__class__.__name__)
        self.telegram_client = client
        self.dsv_client = dsv_client

    async def handle_message(self, message: Message):
        try:
            data = await self.dsv_client.get_random_question()
            self.logger.info("Handle message: %s", message)
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))
