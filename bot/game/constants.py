import enum

from bot.core.fsm import State, StateGroups
from shared.client.schemes.keyboard import InlineKeyboardMarkupSchema

CALLBACK_DATA = "answer"
WAITING_TIME = 20
MIN_PLAYERS = 2


class GameState(StateGroups):
    WAITING_FOR_PLAYERS = State("WAITING_FOR_PLAYERS")
    WAITING_FOR_PUSH_BUTTON = State("WAITING_FOR_PUSH_BUTTON")
    WAITING_FOR_ANSWER = State("WAITING_FOR_ANSWER")


class GameCommand(enum.Enum):
    START = "start"
    JOIN = "join"
    STATISTICS = "statistics"
    STOP = "stop"

    @classmethod
    def from_string(cls, raw: str):
        try:
            return cls(raw)
        except ValueError:
            return None


START_MESSAGE = """
👋 Привет! Это игра **100 к 1** 🎯

📋 Краткие правила:
• Играют от **2 игроков**
• Выпадает случайный вопрос
• Кто первым нажмёт кнопку — отвечает
• ✅ Верный ответ — начисляем очки
• ❌ Неверный — игрок выбывает

🔘 Команды:
• /join — присоединиться к игре
• /statistics — посмотреть статистику игры
• /stop — завершить игру

Удачи! 😉
"""

ANSWER_KEYBOARD = InlineKeyboardMarkupSchema().load(
    {
        "inline_keyboard": [
            [{"text": "Ответить", "callback_data": CALLBACK_DATA}]
        ]
    }
)
