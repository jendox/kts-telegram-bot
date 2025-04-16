import asyncio
from collections.abc import Awaitable, Callable
from logging import getLogger

from bot.game.constants import (
    ANSWER_KEYBOARD,
    CALLBACK_DATA,
    MIN_PLAYERS,
    START_MESSAGE,
    WAITING_TIME,
    GameCommand,
    GameState,
)
from bot.game.engine import GameEngine
from bot.game.messages import Messages
from bot.game.session import SessionManager
from bot.game.types import GameSession, Player
from bot.game.utils import extract_command
from bot.services import DataServiceClient
from shared.client.telegram import TelegramClient
from shared.client.types import CallbackQuery, Message, MessageReply
from shared.storage import Storage


class GameManager:
    def __init__(
        self, tg: TelegramClient, dsv: DataServiceClient, storage: Storage
    ):
        self.logger = getLogger(self.__class__.__name__)
        self.tg = tg
        self.dsv_client = dsv
        self.session_manager = SessionManager(storage)
        self.waiting_timers = {}
        self.handlers: dict[
            GameCommand, Callable[[Message], Awaitable[None]]
        ] = {
            GameCommand.START: self._handle_start,
            GameCommand.JOIN: self._handle_join,
            GameCommand.STATUS: self._handle_status,
            GameCommand.STOP: self._handle_stop,
        }

    async def process_message(self, message: Message):
        if message.entities is not None:
            try:
                await self._process_command(message)
            except ValueError as e:
                self.logger.debug("Error: %s", str(e))
                await self.tg.send_message(
                    MessageReply(
                        message.chat.id, "Я пока не знаю такой команды..."
                    )
                )
        else:
            chat_id = message.chat.id
            user_id = message.from_.id
            session = await self.session_manager.get_session(chat_id)
            if (
                session
                and session.is_game_state(GameState.WAITING_FOR_ANSWER)
                and GameEngine(session).is_active_player(user_id)
            ):
                await self._process_answer(session, message.text)

    async def process_callback(self, callback_query: CallbackQuery):
        if callback_query.data == CALLBACK_DATA:
            chat_id = callback_query.message.chat.id
            player = Player(
                callback_query.from_.id, callback_query.from_.username
            )
            session = await self.session_manager.get_session(chat_id)

            if not session.active_player:
                GameEngine(session).assign_active_player(player)
                await self.session_manager.set_session(session)

                await self.tg.send_message(
                    MessageReply(
                        chat_id=chat_id,
                        text=Messages.player_pressed_first(player.name),
                    )
                )

    async def _process_command(self, message: Message):
        command = GameCommand.from_string(extract_command(message))
        if command and command in self.handlers:
            await self.handlers[command](message)

    async def _handle_start(self, message: Message):
        await self.tg.send_message(
            MessageReply(
                chat_id=message.chat.id,
                text=START_MESSAGE,
            )
        )

    async def _handle_join(self, message: Message):
        chat_id = message.chat.id
        session = await self.session_manager.get_session(chat_id)
        if not session:
            await self._init_game(
                chat_id, message.from_.id, message.from_.first_name
            )
            return
        if session.is_game_state(GameState.WAITING_FOR_PLAYERS):
            await self._add_player(
                session, message.from_.id, message.from_.first_name
            )
            return
        await self.tg.send_message(
            MessageReply(chat_id=chat_id, text=Messages.game_already_started())
        )

    async def _handle_status(self, message: Message):
        """Отправляет текущий статус игры"""
        chat_id = message.chat.id
        session = await self.session_manager.get_session(chat_id)
        if session and not session.is_game_state(GameState.WAITING_FOR_PLAYERS):
            text = Messages.game_status(session)
        else:
            text = Messages.game_not_started()
        await self.tg.send_message(MessageReply(chat_id=chat_id, text=text))

    async def _handle_stop(self, message: Message):
        chat_id = message.chat.id
        session = await self.session_manager.get_session(chat_id)
        if (
            session
            and not session.is_game_state(GameState.WAITING_FOR_PLAYERS)
            and not session.is_player_eliminated(message.from_.id)
        ):
            await self._stop_game(session)
        else:
            await self.tg.send_message(
                MessageReply(chat_id=chat_id, text=Messages.game_not_started())
            )

    async def _start_game(self, session: GameSession):
        question = await self.dsv_client.get_random_question()
        if question is not None:
            GameEngine(session).start(question)
            await self.session_manager.set_session(session)
            await self.tg.send_message(
                MessageReply(
                    chat_id=session.chat_id,
                    text=Messages.question_prompt(question.title),
                    reply_markup=ANSWER_KEYBOARD,
                )
            )
        else:
            await self.session_manager.clear_session(session.chat_id)
            await self.tg.send_message(
                MessageReply(
                    chat_id=session.chat_id,
                    text=Messages.question_fetch_failed(),
                )
            )

    async def _init_game(self, chat_id: int, user_id: int, username: str):
        """Инициализирует новую игровую сессию и устанавливает таймер"""
        await self.session_manager.new_session(chat_id, user_id, username)
        task = asyncio.create_task(self._wait_and_start(chat_id))
        self.waiting_timers[chat_id] = task

        await self.tg.send_message(
            MessageReply(
                chat_id=chat_id,
                text=Messages.game_created(username, WAITING_TIME),
            )
        )

    async def _stop_game(self, session: GameSession):
        session.set_finish_time()
        await self.dsv_client.save_result()
        await self.session_manager.clear_session(session.chat_id)
        await self.tg.send_message(
            MessageReply(
                chat_id=session.chat_id, text=Messages.game_finished(session)
            )
        )

    async def _add_player(
        self, session: GameSession, user_id: int, username: str
    ):
        session.add_player(user_id, username)
        await self.session_manager.set_session(session)
        await self.tg.send_message(
            MessageReply(
                chat_id=session.chat_id,
                text=Messages.player_joined(username, len(session.players)),
            )
        )

    async def _wait_and_start(self, chat_id: int):
        await asyncio.sleep(WAITING_TIME)
        session = await self.session_manager.get_session(chat_id)

        if session is None or not session.is_game_state(
            GameState.WAITING_FOR_PLAYERS
        ):
            return

        if session.is_ready_to_start():
            await self._start_game(session)
        else:
            await self.tg.send_message(
                MessageReply(
                    chat_id=chat_id, text=Messages.not_enough_players()
                )
            )
            await self.session_manager.clear_session(session.chat_id)

    async def _process_answer(self, session: GameSession, answer: str):
        engine = GameEngine(session)
        if engine.is_answer_correct(answer):
            points = engine.award_points(session.active_player.id, answer)
            engine.add_given_answer(answer)
            text = Messages.answer_correct(session.active_player.name, points)
        else:
            engine.eliminate_player(session.active_player.id)
            text = Messages.answer_wrong(session.get_active_player_name())

        engine.clear_active_player()
        await self.session_manager.set_session(session)
        await self.tg.send_message(
            MessageReply(
                chat_id=engine.chat_id, text=text, reply_markup=ANSWER_KEYBOARD
            )
        )
        if engine.count_active_players() < MIN_PLAYERS:
            await self._stop_game(session)
