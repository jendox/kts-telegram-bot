from logging import getLogger

from bot_manager.handlers.callback_handler import CallbackHandler
from bot_manager.handlers.message_handler import MessageHandler
from shared.client.schemes import UpdateSchema
from shared.client.telegram import TelegramClient


class UpdateHandler:
    def __init__(self, client: TelegramClient):
        self.logger = getLogger(self.__class__.__name__)
        self.telegram_client = client
        self.message_handler = MessageHandler(client)
        self.callback_handler = CallbackHandler(client)

    async def handle_updates(self, message: str):
        self.logger.info("Handle update: %s", message)
        try:
            update = UpdateSchema().loads(message)
            if update.message is not None:
                await self.message_handler.handle_message(update.message)
            elif update.callback_query is not None:
                await self.callback_handler.handle_callback(
                    update.callback_query
                )
            else:
                raise ValueError("Unsupported updates type")
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))
