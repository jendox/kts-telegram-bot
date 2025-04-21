import datetime
from dataclasses import dataclass, field

from bot.core.fsm import State
from bot.game.constants import MIN_PLAYERS, GameState


@dataclass
class Answer:
    id: int
    title: str
    points: int


@dataclass
class Question:
    id: int
    title: str
    answers: list[Answer]


@dataclass
class Player:
    id: int
    name: str
    points: int = 0
    is_active: bool = True


@dataclass
class GameSession:
    chat_id: int = None
    state: State = field(default_factory=GameState)
    created_at: datetime.datetime = None
    finished_at: datetime.datetime = None
    players: list[Player] = field(default_factory=list)
    question: Question = None
    current_player: Player = None
    given_answers: list[Answer] = field(default_factory=list)

    def is_ready_to_start(self) -> bool:
        return len(self.players) >= MIN_PLAYERS

    def is_player_eliminated(self, user_id: int) -> bool:
        player = self.get_player_by_id(user_id)
        return not player.is_active if player else True

    def get_active_player_name(self) -> str | None:
        return self.current_player.name if self.current_player else None

    def get_player_by_id(self, user_id: int) -> Player | None:
        return next((p for p in self.players if p.id == user_id), None)

    def add_player(self, user_id: int, username: str):
        if not any(p.id == user_id for p in self.players):
            self.players.append(Player(user_id, username))

    def _find_answer(self, text: str) -> Answer | None:
        normalized = text.strip().capitalize()
        return next(
            (a for a in self.question.answers if a.title == normalized), None
        )

    def points_by_answer(self, text: str) -> int:
        answer = self._find_answer(text)
        return answer.points if answer else 0

    def award_points(self, user_id: int, points: int):
        player = self.get_player_by_id(user_id)
        if player:
            player.points += points

    def is_answer_correct(self, text: str) -> bool:
        return self._find_answer(text) is not None

    def is_already_answered(self, text: str) -> bool:
        answer = self._find_answer(text)
        return answer in self.given_answers

    def add_given_answer(self, text: str) -> bool:
        answer = self._find_answer(text)
        if answer not in self.given_answers:
            self.given_answers.append(answer)
            return True
        return False

    def is_game_state(self, state: State) -> bool:
        return self.state == state

    def eliminate_player(self, user_id: int):
        player = self.get_player_by_id(user_id)
        if player:
            player.is_active = False

    def count_active_players(self) -> int:
        return sum(p.is_active for p in self.players)

    def count_given_answers(self) -> int:
        return len(self.given_answers)

    def set_finish_time(self):
        self.finished_at = datetime.datetime.now()


@dataclass
class LastGameSession:
    created_at: datetime.datetime = None
    finished_at: datetime.datetime = None
    players: list[Player] = field(default_factory=list)
    question: Question = None
