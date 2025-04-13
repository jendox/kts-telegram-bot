import asyncio
import os
from logging import getLogger

from bot_manager.dataservice_client import DataServiceClient
from bot_manager.handlers.update_handler import UpdateHandler
from bot_manager.poller import BotPoller
from shared.client.telegram import TelegramClient
from shared.config import Config
from shared.poller import Poller


class BotManager:
    def __init__(self, config: Config):
        self.logger = getLogger(self.__class__.__name__)
        self.config: Config = config
        self.poller: Poller | None = None
        self.update_handler: UpdateHandler | None = None
        self.tg_client: TelegramClient | None = None
        self.dsv_client: DataServiceClient | None = None
        self._shutdown_event: asyncio.Event | None = None

    async def start(self):
        self._shutdown_event = asyncio.Event()
        await self._start_dsv_client()
        await self._start_telegram_client()
        await self._start_bot_poller()

    async def stop(self):
        if self.poller:
            await self.poller.stop()
        if self.tg_client:
            await self.tg_client.stop()
        if self.dsv_client:
            await self.dsv_client.stop()

    async def _start_telegram_client(self):
        self.tg_client = TelegramClient()
        await self.tg_client.start()
        self.update_handler = UpdateHandler(self.tg_client)

    async def _start_bot_poller(self):
        self.poller = BotPoller(
            self.config.broker.type, self.update_handler.handle_updates
        )
        await self.poller.start()

    async def _start_dsv_client(self):
        self.dsv_client = DataServiceClient(os.getenv("API_URL"))
        await self.dsv_client.start()

    async def waiting_for_shutdown(self) -> None:
        await self._shutdown_event.wait()
