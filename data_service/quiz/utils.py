import hashlib
import json
from typing import Any


def get_session_hash_base(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "chat_id": data["chat_id"],
        "created_at": data["created_at"],
        "question_id": data["question"]["id"],
        "players_ids": sorted([p["id"] for p in data["players"]]),
        "answers_ids": sorted([a["id"] for a in data["given_answers"]]),
    }


def generate_session_hash(base: dict[str, Any]) -> str:
    json_string = json.dumps(base)

    return hashlib.sha256(json_string.encode()).hexdigest()
