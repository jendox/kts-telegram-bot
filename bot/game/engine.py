from bot.game.constants import MIN_PLAYERS, GameState
from bot.game.types import GameSession, Player, Question


class GameEngine:
    def __init__(self, session: GameSession):
        self._session = session

    @property
    def chat_id(self):
        return self._session.chat_id

    def start(self, question: Question):
        self._session.question = question
        self._session.state = GameState.WAITING_FOR_PUSH_BUTTON

    def assign_active_player(self, player: Player):
        self._session.current_player = player
        self._session.state = GameState.WAITING_FOR_ANSWER

    def clear_active_player(self):
        self._session.current_player = None
        self._session.state = GameState.WAITING_FOR_PUSH_BUTTON

    def is_active_player(self, player_id: int) -> bool:
        return (
            self._session.current_player
            and self._session.current_player.id == player_id
        )

    def award_points(self, player_id: int, text: str) -> int:
        points = self._session.points_by_answer(text)
        if points:
            self._session.award_points(player_id, points)
        return points

    def is_answer_correct(self, text: str) -> bool:
        return self._session.is_answer_correct(text)

    def is_already_answered(self, text: str) -> bool:
        return self._session.is_already_answered(text)

    def add_given_answer(self, text: str) -> bool:
        return self._session.add_given_answer(text)

    def eliminate_player(self, player_id: int):
        self._session.eliminate_player(player_id)

    def count_active_players(self):
        return self._session.count_active_players()

    def set_finish_time(self):
        self._session.set_finish_time()

    def is_game_continued(self):
        active_players = self.count_active_players()
        return (
            active_players > 0
            and active_players >= MIN_PLAYERS - 1
            and self._session.count_given_answers()
            < len(self._session.question.answers)
        )
