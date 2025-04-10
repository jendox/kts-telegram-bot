from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

__all__ = ("MessageBroker",)


class MessageBroker(ABC):
    @abstractmethod
    async def start(self) -> None:
        """Инициализация"""

    @abstractmethod
    async def publish(self, message: str) -> None:
        """Публикация сообщения в очередь"""

    @abstractmethod
    async def consume(self, callback: Callable[[Any], Any]) -> None:
        """Подписка на очередь и обработка сообщений"""

    @abstractmethod
    async def stop(self) -> None:
        """Закрытие соединений"""
