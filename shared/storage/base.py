from abc import abstractmethod

__all__ = ("Storage",)


class Storage:
    def __init__(self, url: str):
        self.url = url

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self):
        pass

    @abstractmethod
    async def set(self, name: str, key: str, value: str):
        pass

    @abstractmethod
    async def get(self, name: str, key: str):
        pass

    @abstractmethod
    async def clear(self, name: str):
        pass
