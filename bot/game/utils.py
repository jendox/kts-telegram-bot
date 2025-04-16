import re

from shared.client.types import Message


def extract_command(message: Message) -> str | None:
    """Получает список команд в сообщении и возвращает первую
    Args:
        message (Message): сообщение телеграм
    Raises:
        KeyError: если команды не найдены
    """
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
                commands.append(match.group(1).lower())
    try:
        return commands[0]
    except KeyError:
        return None
