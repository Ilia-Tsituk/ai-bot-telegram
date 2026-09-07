"""Occasionally lets the bot start a conversation on its own with active users."""

import random

from app.config import PROACTIVE_MESSAGE_CHANCE

MESSAGES = [
    "Hey 😊",
    "How's your day going?",
    "Was just thinking about you 🙂",
    "What are you up to?",
    "Hope everything's alright.",
    "Random thought: what's the last thing that made you laugh?",
]


def should_start_conversation() -> bool:
    return random.random() < PROACTIVE_MESSAGE_CHANCE


def generate_proactive_message() -> str:
    return random.choice(MESSAGES)
