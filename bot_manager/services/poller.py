import asyncio
from asyncio import Task
from collections.abc import Callable
from logging import getLogger
from typing import Any

from shared.broker import BrokerType, MessageBroker, get_broker

__all__ = ("BotPoller",)

from shared.poller import Poller


class BotPoller(Poller):
    def __init__(
        self, broker_type: BrokerType, update_handler: Callable[[str], Any]
    ):
        self.logger = getLogger(self.__class__.__name__)
        self.broker_type = broker_type
        self.broker: MessageBroker | None = None
        self.update_handler: Callable[[str], Any] = update_handler
        self.poll_task: Task | None = None

    async def start(self) -> None:
        self.broker = get_broker(self.broker_type)
        await self.broker.start()
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self) -> None:
        if not self.poll_task:
            await self.poll_task
        if self.broker:
            await self.broker.stop()

    async def poll(self) -> None:
        self.logger.info("Start polling update from RabbitMQ")
        await asyncio.create_task(self.broker.consume(self.update_handler))
        self.logger.info("Stop polling updates from RabbitMQ")
