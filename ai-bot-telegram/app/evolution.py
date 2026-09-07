"""Tracks how the character's overall personality "matures" over time/usage."""

_personality_level = 0


def evolve_personality() -> str:
    global _personality_level
    _personality_level += 1

    if _personality_level < 20:
        return "shy"
    elif _personality_level < 50:
        return "friendly"
    elif _personality_level < 100:
        return "close"
    else:
        return "very_close"


def get_personality_level() -> int:
    return _personality_level
