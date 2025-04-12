import asyncio
import os
from logging import getLogger

from bot_manager.handlers.update_handler import UpdateHandler
from bot_manager.poller import BotPoller
from bot_manager.token_manager import TokenManager
from shared.client.telegram import TelegramClient
from shared.config import Config
from shared.poller import Poller


class BotManager:
    def __init__(self, config: Config):
        self.logger = getLogger(self.__class__.__name__)
        self.config: Config = config
        self.token_manager: TokenManager | None = None
        self.poller: Poller | None = None
        self.update_handler: UpdateHandler | None = None
        self.client: TelegramClient | None = None
        self._shutdown_event: asyncio.Event | None = None

    async def start(self):
        self._shutdown_event = asyncio.Event()
        await self._start_token_manager()
        await self._start_telegram_client()
        await self._start_bot_poller()

    async def stop(self):
        await self.poller.stop()
        await self.client.stop()
        await self.token_manager.stop()

    async def _start_token_manager(self):
        self.token_manager = TokenManager(os.getenv("JWT_SECRET"))
        await self.token_manager.start()

    async def _start_telegram_client(self):
        self.client = TelegramClient()
        await self.client.start()
        self.update_handler = UpdateHandler(self.client)

    async def _start_bot_poller(self):
        self.poller = BotPoller(
            self.config.broker.type, self.update_handler.handle_updates
        )
        await self.poller.start()

    async def waiting_for_shutdown(self) -> None:
        await self._shutdown_event.wait()
