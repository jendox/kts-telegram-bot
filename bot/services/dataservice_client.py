import os

from aiohttp import ClientSession

from bot.game.schemes import GameSessionSchema, QuestionSchema
from bot.game.types import GameSession, Question
from bot.services.token_manager import TokenManager

__all__ = ("DataServiceClient",)


class DataServiceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token_manager: TokenManager | None = None
        self.client: ClientSession | None = None

    async def _headers(self):
        token = await self.token_manager.token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    async def start(self):
        self.token_manager = TokenManager(os.getenv("JWT_SECRET"))
        await self.token_manager.start()
        self.client = ClientSession(base_url=self.base_url)

    async def stop(self):
        if self.token_manager:
            await self.token_manager.stop()
        if self.client:
            await self.client.close()

    async def get_random_question(self) -> Question | None:
        headers = await self._headers()
        result = await self.client.get(
            url="/quiz.random_question", headers=headers
        )
        if result.status == 200:
            data = await result.json()
            return QuestionSchema().load(data["data"])
        return None

    async def save_game(self, session: GameSession):
        data = GameSessionSchema().dump(session)
        headers = await self._headers()
        await self.client.post(
            url="/quiz.save_game", headers=headers, json=data
        )

    async def get_last_game(self, chat_id: int):
        headers = await self._headers()
        result = await self.client.get(
            url=f"/quiz.last_game?chat_id={chat_id}", headers=headers
        )
        if result.status == 200:
            data = await result.json()
            return GameSessionSchema().load(data["data"])
        return None
