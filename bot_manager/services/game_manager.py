import asyncio
import enum
import re
import time
from logging import getLogger

from bot_manager.core.fsm import FSM, StateGroups, State
from bot_manager.services.dataservice_client import DataServiceClient
from bot_manager.types import QuestionSchema
from shared.client.telegram import TelegramClient
from shared.client.types import CallbackQuery, Message, MessageReply
from shared.storage.redis import RedisStorage


class GameState(StateGroups):
    WAITING = State("WAITING")
    ACTIVE = State("ACTIVE")


class GameCommand(enum.Enum):
    START = "/start"
    JOIN = "/join"
    STATUS = "/status"
    STOP = "/stop"

WAITING_TIME = 1
MIN_PLAYERS = 1


class GameManager:
    def __init__(
            self,
            tg: TelegramClient,
            dsv: DataServiceClient,
            storage: RedisStorage
    ):
        self.logger = getLogger(self.__class__.__name__)
        self.tg = tg
        self.dsv_client = dsv
        self.storage = storage
        self.fsm = FSM(storage)
        self.waiting_timers = {}

    async def _start_game(self, chat_id: int, session: dict):
        question = await self.dsv_client.get_random_question()
        session["state"] = GameState.ACTIVE.name
        session["question"] = QuestionSchema().dump(question)
        await self.fsm.set_data(chat_id, session)
        await self.tg.send_message(MessageReply(
            chat_id=chat_id,
            text=f"Игра начинается! Вопрос: {question.title}"
        ))

    async def _stop_game(self, chat_id: int):
        session = await self.fsm.get_data(chat_id)
        if State(session.get("state")) == GameState.ACTIVE:
            await self.dsv_client.save_result()
            # print result
            await self.tg.send_message(MessageReply(
                chat_id=chat_id,
                text="Игра завершена"
            ))
            await self.fsm.clear_state(chat_id)

    async def process_callback(self, callback_query: CallbackQuery):
        pass

    async def _init_game(self, chat_id: int, user_id: int, username: str):
        session = {
            "state": GameState.WAITING.name,
            "players": {user_id: username},
            "points": {user_id: 0},
            "created_at": time.time()
        }
        await self.fsm.set_data(chat_id, session)
        await self.tg.send_message(
            MessageReply(
                chat_id=chat_id,
                text=f"{username} присоединился к новой попытке!\n"
                     f"Ждем игроков {WAITING_TIME} секунд..."
            )
        )
        task = asyncio.create_task(self._wait_and_start(chat_id))
        self.waiting_timers[chat_id] = task

    async def _add_player(self, session: dict, chat_id: int, user_id: int, username: str):
        session["players"][user_id] = username
        session["points"][user_id] = 0
        await self.tg.send_message(
            MessageReply(
                chat_id=chat_id,
                text=f"{username} присоединился к игре! "
                     f"Сейчас игроков: {len(session['players'])}"
            )
        )

    async def _wait_and_start(self, chat_id: int):
        await asyncio.sleep(WAITING_TIME)
        session = await self.fsm.get_data(chat_id)

        if session is None or State(session.get("state")) != GameState.WAITING:
            return
        players = session.get("players")
        if len(players) >= MIN_PLAYERS:
            await self._start_game(chat_id, session)
        else:
            await self.tg.send_message(MessageReply(
                chat_id=chat_id,
                text="Недостаточно игроков. Игра отменена"
            ))
            await self.fsm.clear_state(str(chat_id))

    async def _handle_join(self, message: Message):
        key = str(message.chat.id)
        session = await self.fsm.get_data(key)
        if not session:
            await self._init_game(
                message.chat.id, message.from_.id, message.from_.username
            )
            return
        if State(session.get("state")) == GameState.WAITING:
            await self._add_player(
                session, message.chat.id, message.from_.id, message.from_.username
            )
            return
        await self.tg.send_message(
            MessageReply(
                chat_id=message.chat.id,
                text="Игра уже идет. Подождите завершения..."
            )
        )

    async def process_message(self, message: Message):
        if message.entities is not None:
            try:
                command = GameCommand(self._extract_command(message))
                await self._process_command(GameCommand(command), message)
            except ValueError as e:
                self.logger.debug("Error: %s", str(e))
                await self.tg.send_message(
                    MessageReply(message.chat.id, "Я пока не знаю такой команды...")
                )
        else:
            pass

    async def _handle_start(self, chat_id: int):
        session = await self.fsm.get_data(chat_id)
        if session is None:
            await self.tg.send_message(
                MessageReply(
                    chat_id=chat_id,
                    text="Привет! Используй /join, чтобы начать игру"
                )
            )

    async def _process_command(self, command: GameCommand, message: Message):
        if command == GameCommand.START:
            await self._handle_start(message.chat.id)
        elif command == GameCommand.JOIN:
            await self._handle_join(message)
        elif command == GameCommand.STATUS:
            pass
        elif command == GameCommand.STOP:
            await self._stop_game(message.chat.id)

    @staticmethod
    def _extract_command(message: Message) -> str | None:
        commands = []
        command_regex = re.compile(r"^/([a-zA-Z0-9_]{1,32})(@[a-zA-Z0-9_]{5,32})?$")
        for entity in message.entities:
            if entity.type == "bot_command":
                start = entity.offset
                end = start + entity.length
                command_text = message.text[start:end]

                command_part = command_text.split(maxsplit=1)[0]
                match = command_regex.match(command_part)

                if match:
                    commands.append(match.group().lower())
        try:
            return commands[0]
        except KeyError:
            return None
