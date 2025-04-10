import asyncio
import json
from asyncio import Task
from logging import getLogger
from typing import Any

from aiohttp.web_exceptions import HTTPConflict, HTTPUnauthorized

from shared.client.telegram import TelegramClient
from shared.rabbitmq_broker import RabbitMQBroker

LOGGER_NAME = "telegram_poller"
POLL_TIMEOUT = 2


class TelegramPoller:
    def __init__(self):
        self.logger = getLogger(LOGGER_NAME)
        self.client: TelegramClient | None = None
        self.broker: RabbitMQBroker | None = None
        self.poll_task: Task | None = None
        self.is_running: bool = False
        self._shutdown_event: asyncio.Event | None = None

    async def waiting_for_shutdown(self) -> None:
        await self._shutdown_event.wait()

    async def start(self) -> None:
        """Создает брокер сообщений и клиента телеграм и запускает поллер"""
        self.broker = RabbitMQBroker()
        await self.broker.start()
        self.client = TelegramClient()
        await self.client.start()
        self._shutdown_event = asyncio.Event()
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        """Останавливает поллер и закрывает соединения"""
        self.is_running = False
        await self._stop_poll_task()
        if self.client:
            await self.client.stop()
        if self.broker:
            await self.broker.stop()

    async def poll(self) -> None:
        """Поллер обновлений с сервера телеграм"""
        self.logger.info("Start polling updates from Telegram server")

        offset = 0
        while self.is_running:
            try:
                updates = await self.client.get_updates(offset=offset, timeout=POLL_TIMEOUT)
                if updates:
                    offset = await self._process_updates(updates)
            except (HTTPConflict, HTTPUnauthorized) as e:
                self.logger.error("Error getting updates: %s", e)
                self._shutdown_event.set()
                raise
            except Exception as e:
                self.logger.error("Polling error: %s, retrying...", e)
                await asyncio.sleep(1)

    async def _process_updates(self, updates: list[dict[str, Any]]) -> None:
        """Создает таски для помещения обновлений в очередь RabbitMQ"""
        tasks = [self._queue_update(update) for update in updates]
        await asyncio.gather(*tasks)
        return max(update["update_id"] for update in updates) + 1

    async def _queue_update(self, update: dict[str, Any]) -> None:
        """Помещает обновление в очередь RabbitMQ"""
        try:
            message = json.dumps(update)
            await self.broker.publish(message)
        except Exception as e:
            self.logger.error(
                "Unexpected error sending a message to the broker queue: %s", e
            )

    async def _stop_poll_task(self) -> None:
        """Останавливает задачу поллинга"""
        try:
            if self.poll_task is not None:
                await asyncio.wait_for(self.poll_task, timeout=POLL_TIMEOUT)
        except TimeoutError:
            self.logger.warning("Forcing shutdown after timeout")

        if self.poll_task and not self.poll_task.done():
            self.poll_task.cancel()
            try:
                await self.poll_task
            except asyncio.CancelledError:
                self.logger.info("Polling task cancelled")
            except Exception as e:
                self.logger.error("Error canceling poller task: %s", e)
