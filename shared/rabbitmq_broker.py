import os
from asyncio import CancelledError
from collections.abc import Callable
from logging import getLogger
from typing import Any

import aio_pika

LOGGER_NAME = "rabbitmq"
DEFAULT_URL = "amqp://guest:guest@127.0.0.1/"
DEFAULT_QUEUE_NAME = "telegram"
MESSAGE_ENCODING = "utf-8"


class RabbitMQBroker:
    def __init__(self):
        self.logger = getLogger(LOGGER_NAME)
        self.url = os.getenv("RABBITMQ_URL", default=DEFAULT_URL)
        self.queue_name = os.getenv("RABBITMQ_QUEUE_NAME", default=DEFAULT_QUEUE_NAME)
        self.connection: aio_pika.Connection | None = None
        self.channel: aio_pika.Channel | None = None
        self.queue: aio_pika.Queue | None = None

    async def start(self) -> None:
        """Создает соединение, канал и декларирует очередь"""
        try:
            if not self.connection:
                self.connection = await aio_pika.connect_robust(url=self.url)
                self.logger.info("RabbitMQ connection successfully established")
            if not self.channel:
                self.channel = self.connection.channel()
                self.logger.info("RabbitMQ channel successfully created")
            if not self.queue:
                self.queue = self.channel.declare_queue(self.queue_name, durable=True)
                self.logger.info("RabbitMQ queue declared successfully")
        except aio_pika.exceptions.AMQPConnectionError as e:
            self.logger.error("RabbitMQ connection error: %s", str(e))
            raise
        except Exception as e:
            self.logger.error("Unexpected starting RabbitMQ error: %s", str(e))
            raise

    async def stop(self) -> None:
        """Закрывает канал и соединение"""
        if self.channel:
            await self.channel.close()
            self.logger.info("RabbitMq channel closed")
        if self.connection:
            await self.connection.close()
            self.logger.info("RabbitMq connection closed")

    async def publish(self, message: str) -> None:
        """Публикует сообщение в очередь
        Args:
            message (str): сообщение для публикации
        """
        if not self.connection:
            await self.start()
        try:
            await self.channel.default_exchange.publish(
                routing_key=self.queue_name,
                message=aio_pika.Message(
                    body=message.encode(MESSAGE_ENCODING),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                )
            )
            self.logger.info("Message successfully published\nMessage: %s", message)
        except Exception as e:
            self.logger.error("Unexpected error publishing message: %s", str(e))

    async def consume(self, callback: Callable[[str], Any]) -> None:
        """Читает сообщение из очереди
        Args:
            callback: функция для обработки принятого сообщения
        """
        if not self.queue:
            await self.start()

        async with self.queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    async with message.process():
                        await callback(message.body.decode(MESSAGE_ENCODING))
                        # await message.ack() # for test only
                except CancelledError:
                    self.logger.info("Message consumption cancelled")
                    raise
                except Exception as e:
                    self.logger.error("Error handling consuming message: %s", str(e))
                    await message.nack(requeue=False)
