from abc import ABC, abstractmethod

__all__ = ("Poller",)


class Poller(ABC):
    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def poll(self):
        pass
