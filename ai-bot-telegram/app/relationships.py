"""Tracks a simple relationship "level" per user, based on how many messages they've exchanged."""

_relationships = {}


def get_relationship(user_id: str) -> dict:
    return _relationships.get(
        user_id,
        {"level": 0, "status": "stranger"}
    )


def update_relationship(user_id: str) -> dict:
    relation = get_relationship(user_id)
    relation["level"] += 1

    if relation["level"] >= 100:
        relation["status"] = "best_friend"
    elif relation["level"] >= 50:
        relation["status"] = "friend"
    elif relation["level"] >= 20:
        relation["status"] = "close"
    else:
        relation["status"] = "stranger"

    _relationships[user_id] = relation
    return relation
