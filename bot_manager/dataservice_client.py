import os

from aiohttp import ClientSession

from bot_manager.token_manager import TokenManager
from bot_manager.types import QuestionSchema, Question


class DataServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token_manager: TokenManager | None = None
        self.client: ClientSession | None = None

    async def _headers(self):
        token = await self.token_manager.token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def start(self):
        await self._start_token_manager()
        self.client = ClientSession(base_url=self.base_url)

    async def stop(self):
        if self.token_manager:
            await self.token_manager.stop()
        if self.client:
            await self.client.close()

    async def _start_token_manager(self):
        self.token_manager = TokenManager(os.getenv("JWT_SECRET"))
        await self.token_manager.start()

    async def get_random_question(self) -> Question | None:
        headers = await self._headers()
        result = await self.client.get(
            url="/quiz.random_question", headers=headers
        )
        if result.status == 200:
            data = await result.json()
            return QuestionSchema().load(data["data"])
        return None
