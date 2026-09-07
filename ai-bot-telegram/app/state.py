"""Tracks the character's current internal state (mood, energy)."""

from datetime import datetime

_state = {
    "mood": "neutral",
    "energy": 100,
    "last_update": None,
}


def get_state() -> dict:
    return _state


def update_state(mood: str = None, energy: int = None) -> dict:
    if mood:
        _state["mood"] = mood

    if energy is not None:
        _state["energy"] = energy

    _state["last_update"] = datetime.now()
    return _state


def decrease_energy(amount: int = 1) -> int:
    _state["energy"] = max(0, _state["energy"] - amount)
    return _state["energy"]


def recover_energy(amount: int = 5) -> int:
    _state["energy"] = min(100, _state["energy"] + amount)
    return _state["energy"]
