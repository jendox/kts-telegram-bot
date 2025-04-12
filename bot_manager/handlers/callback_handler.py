from logging import getLogger

from shared.client.telegram import TelegramClient
from shared.client.types import CallbackQuery, CallbackQueryReply


class CallbackHandler:
    def __init__(self, client: TelegramClient):
        self.logger = getLogger(self.__class__.__name__)
        self.telegram_client = client

    async def handle_callback(self, callback_query: CallbackQuery):
        try:
            self.logger.info("Handle callback_query: %s", callback_query)
            await self.telegram_client.answer_callback_query(
                CallbackQueryReply(callback_query_id=callback_query.id)
            )
        except Exception as e:
            self.logger.error("Error handling callback_query: %s", str(e))
