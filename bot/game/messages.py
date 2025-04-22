from bot.game.types import GameSession


class Messages:
    @staticmethod
    def game_created(username: str, wait_time: int) -> str:
        return (
            f"🎲 *Новая игра!* {username} начал(а) игру\n"
            f"⏳ Ждем игроков *{wait_time} секунд*..."
        )

    @staticmethod
    def player_joined(username: str, total_players: int) -> str:
        return (
            f"➕ *{username}* присоединился(лась) к игре\n"
            f"👥 Всего игроков: *{total_players}*"
        )

    @staticmethod
    def game_already_started() -> str:
        return (
            "🚫 *Игра уже идет!*\n"
            "⏳ Подождите, пока завершится текущая партия."
        )

    @staticmethod
    def player_pressed_first(username: str, seconds: int) -> str:
        return (
            f"⚡️ *{username}* нажал(а) кнопку первым!\n"
            f"💬 Сейчас он(а) отвечает.\n"
            f"⏳ На ответ {seconds} секунд."
        )

    @staticmethod
    def waiting_for_answer(username: str) -> str:
        return f"⏳ *Ждем ответ от {username}...*"

    @staticmethod
    def answer_correct(username: str, points: int) -> str:
        return (
            f"✅ *Верно!* {username} получает *{points} очков* 👏\n"
            "Продолжаем игру!"
        )

    @staticmethod
    def answer_already_given(username: str) -> str:
        return (
            f"🤔 *{username}, ты прав(а), но такой ответ уже был!*\n"
            "🎯 Попробуй угадать другой!"
        )

    @staticmethod
    def answer_wrong(username: str) -> str:
        return f"❌ *Увы! Неправильно.*\n" f"{username} выбывает из игры."

    @staticmethod
    def answer_time_run_out(username: str) -> str:
        return (
            f"❌ *Увы! Закончилось время для ответа.*\n"
            f"{username} выбывает из игры."
        )

    @staticmethod
    def not_enough_players() -> str:
        return (
            "😕 *Недостаточно игроков для начала игры.*\n" "🚫 Игра отменена."
        )

    @staticmethod
    def question_fetch_failed() -> str:
        return (
            "❗️ *Не удалось начать игру.*\n"
            "😕 Произошла ошибка при получении вопроса.\n"
            "🔁 Попробуйте еще раз через несколько секунд."
        )

    @staticmethod
    def game_finished(session: GameSession) -> str:
        return (
            f"{Messages.game_status(session)}\n"
            f"🏁 *Игра завершена!*\n"
            f"Спасибо за участие 🎉"
        )

    @staticmethod
    def question_prompt(question_text: str) -> str:
        return (
            f"🧠 *Вопрос:*\n_{question_text}_\n\n"
            f"👆 *Кто первым нажмёт кнопку — тот и отвечает!*"
        )

    @staticmethod
    def game_status(session: GameSession) -> str:
        """Создает текст для сообщения в телеграм"""
        lines = [f"🔹 Вопрос: {session.question.title}", "", "🔸 Ответы:"]

        guessed_titles = [a.title for a in session.given_answers]

        for i, answer in enumerate(session.question.answers, 1):
            if answer.title in guessed_titles:
                lines.append(f"{i}. 🟢 {answer.title} — {answer.points}")
            else:
                lines.append(f"{i}. 🔴 ——————")

        lines.append("")
        lines.append("👥 Игроки:")
        # for player in sorted(
        #     session.players, key=lambda p: p.points, reverse=True
        # ):
        #     lines.append(f"• {player.name}: {player.points} очков")
        lines.extend(
            [
                f"• {player.name}: {player.points} очков"
                for player in sorted(
                    session.players, key=lambda p: p.points, reverse=True
                )
            ]
        )

        return "\n".join(lines)

    @staticmethod
    def last_game_summary_message(session: GameSession) -> str:
        start = session.created_at.strftime("%H:%M:%S")
        end = session.finished_at.strftime("%H:%M:%S")

        lines = [
            "📊 *Результат последней игры в этом чате*",
            "",
            f"🧠 *Вопрос:* {session.question.title}",
            "",
            f"🕰 *Игра началась:* {start}",
            f"🏁 *Игра завершена:* {end}",
            "",
            "🏆 *Результаты:*",
        ]

        sorted_players = sorted(
            session.players, key=lambda p: p.points, reverse=True
        )

        for i, player in enumerate(sorted_players, 1):
            lines.append(f"{i}. *{player.name}* — {player.points} очков")

        return "\n".join(lines)

    @staticmethod
    def no_game_summary_message() -> str:
        return (
            "😕 В этом чате ещё не проводились игры.\n"
            "🎮 Нажмите /join, чтобы начать первую!"
        )

    @staticmethod
    def game_not_started() -> str:
        return (
            "🕓 *Игра ещё не началась.*\n"
            "Нажмите /join, чтобы присоединиться!"
        )

    @staticmethod
    def unknown_command() -> str:
        return "😕 Я пока не знаю такой команды...\n" "👆 Попробуй еще раз"
