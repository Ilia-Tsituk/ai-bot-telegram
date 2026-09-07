"""Tracks when each user was last seen, so the bot knows who is currently active."""

from datetime import datetime

_last_seen = {}


def update_attention(user_id: str) -> None:
    _last_seen[user_id] = datetime.now()


def get_last_seen(user_id: str):
    return _last_seen.get(user_id)


def get_known_users() -> list:
    return list(_last_seen.keys())


def is_user_active(user_id: str, minutes: int = 30) -> bool:
    if user_id not in _last_seen:
        return False

    delta = datetime.now() - _last_seen[user_id]
    return delta.total_seconds() < minutes * 60
