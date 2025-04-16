from logging import getLogger

from bot.game.manager import GameManager
from bot.services import DataServiceClient
from shared.client.schemes import UpdateSchema
from shared.client.telegram import TelegramClient
from shared.client.types import CallbackQuery, CallbackQueryReply, Message
from shared.storage import Storage


class Dispatcher:
    def __init__(
        self, tg: TelegramClient, dsv: DataServiceClient, storage: Storage
    ):
        self.logger = getLogger(self.__class__.__name__)
        self.tg = tg
        self.dsv = dsv
        self.storage = storage
        self.game_manager = GameManager(tg, dsv, storage)

    async def handle_updates(self, message: str):
        self.logger.info("Handle update: %s", message)
        try:
            update = UpdateSchema().loads(message)
            if update.message is not None:
                await self._handle_message(update.message)
            elif update.callback_query is not None:
                await self._handle_callback(update.callback_query)
            else:
                raise ValueError("Unsupported updates type")
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))

    async def _handle_message(self, message: Message):
        try:
            self.logger.info("Handle message: %s", message)
            await self.game_manager.process_message(message)
        except Exception as e:
            self.logger.error("Error handling update: %s", str(e))

    async def _handle_callback(self, callback_query: CallbackQuery):
        try:
            self.logger.info("Handle callback_query: %s", callback_query)
            await self.tg.answer_callback_query(
                CallbackQueryReply(callback_query_id=callback_query.id)
            )
            await self.game_manager.process_callback(callback_query)
        except Exception as e:
            self.logger.error("Error handling callback_query: %s", str(e))
