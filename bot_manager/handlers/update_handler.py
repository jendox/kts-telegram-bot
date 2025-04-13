from logging import getLogger

from bot_manager.handlers.callback_handler import CallbackHandler
from bot_manager.handlers.message_handler import MessageHandler
from shared.client.schemes import UpdateSchema
from shared.client.telegram import TelegramClient
from shared.client.types import MessageReply


class UpdateHandler:
    def __init__(self, tg_client: TelegramClient):
        self.logger = getLogger(self.__class__.__name__)
        self.tg_client = tg_client
        self.message_handler = MessageHandler(tg_client)
        self.callback_handler = CallbackHandler(tg_client)

    async def handle_updates(self, message: str):
        self.logger.info("Handle update: %s", message)
        try:
            update = UpdateSchema().loads(message)
            if update.message is not None:
                await self.message_handler.handle_message(update.message)
                await self.tg_client.send_message(
                    MessageReply(
                        chat_id=update.message.chat.id,
                        text=f"Re: {update.message.text}"
                    )
                )
            elif update.callback_query is not None:
                await self.callback_handler.handle_callback(
                    update.callback_query
                )
            else:
                raise ValueError("Unsupported updates type")
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))
