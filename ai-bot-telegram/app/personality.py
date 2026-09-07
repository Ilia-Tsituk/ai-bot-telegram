import json
import os

from app.config import CHARACTER

CHARACTERS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "characters"
)


def load_character(name: str = None) -> dict:
    """Load a character definition from characters/<name>.json"""
    name = name or CHARACTER
    path = os.path.join(CHARACTERS_DIR, f"{name}.json")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
