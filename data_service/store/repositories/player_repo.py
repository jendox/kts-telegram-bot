from sqlalchemy import select

from data_service.quiz.models import Player
from data_service.store.repositories.base_repo import BaseRepository


class PlayerRepository(BaseRepository):
    async def get_or_create(self, id_: int, name: str) -> Player:
        player = await self.session.scalar(
            select(Player).where(Player.id == id_)
        )
        if not player:
            player = Player(id=id_, name=name)
            self.session.add(player)
            await self.session.commit()
            await self.session.refresh(player)
        return player
