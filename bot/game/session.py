import datetime

from bot.core.fsm import FSM
from bot.game.constants import GameState
from bot.game.schemes import GameSessionSchema
from bot.game.types import GameSession, Player
from shared.storage import Storage


class SessionManager:
    def __init__(self, storage: Storage):
        self.fsm = FSM(storage)

    async def new_session(self, chat_id: int, user_id: int, username: str):
        """Создает новую игровую сессию
        Args:
            chat_id: ид чата
            user_id: ид юзера, запустившего игру
            username: имя юзера
        """
        session = GameSession(
            chat_id=chat_id,
            state=GameState.WAITING_FOR_PLAYERS,
            created_at=datetime.datetime.now(),
            players=[Player(user_id, username)],
        )
        await self.set_session(session)

    async def get_session(self, chat_id: int) -> GameSession | None:
        """Загружает игровую сессию из хранилища
        Args:
            chat_id: ид чата
        Returns:
            GameSession | None
        """
        data = await self.fsm.get_state(chat_id)
        return GameSessionSchema().load(data) if data else None

    async def set_session(self, session: GameSession) -> None:
        """Загружает игровую сессию в хранилище
        Args:
            session: данные сессии
        """
        data = GameSessionSchema().dump(session)
        await self.fsm.set_state(session.chat_id, data)

    async def clear_session(self, chat_id: int) -> None:
        """Сбрасывает игровую сессию
        Args:
            chat_id: ид чата
        """
        await self.fsm.clear_state(chat_id)
