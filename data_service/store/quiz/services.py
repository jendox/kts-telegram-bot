import typing
from typing import Any

if typing.TYPE_CHECKING:
    from data_service.web.app import Application


class GameSessionService:
    def __init__(self, app: "Application"):
        self.app = app

    async def ensure_players_exist(self, players: list[dict[str, Any]]):
        for player in players:
            await self.app.store.player_accessor.get_or_create(
                player["id"], player["name"]
            )

    async def is_session_exists(self, session_hash: str) -> bool:
        session = await self.app.store.game_session_accessor.get_by_hash(
            session_hash
        )
        return session is not None
