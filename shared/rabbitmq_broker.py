import os
from logging import getLogger

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

    async def start(self):
        try:
            if not self.connection:
                self.connection = await aio_pika.connect_robust(url=self.url)
            if not self.channel:
                self.channel = self.connection.channel()
            if not self.queue:
                self.queue = self.channel.declare_queue(self.queue_name, durable=True)
            self.logger.info("RabbitMQ connection successfully established")
        except aio_pika.exceptions.AMQPConnectionError as e:
            self.logger.error("RabbitMQ connection error: %s", str(e))
            raise
        except Exception as e:
            self.logger.error("Unexpected starting RabbitMQ error: %s", str(e))
            raise

    async def stop(self):
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()
            self.logger.info("RabbitMq connection closed")
