"""Pulls simple structured facts (name, age, city, likes...) out of free text messages."""

import re

PATTERNS = {
    "name": r"(?:my name is|i am called|i'm called)\s+([A-Za-zÀ-ÿ]+)",
    "age": r"(?:i am|i'm)\s+(\d{1,3})\s*(?:years old)?",
    "city": r"(?:i live in)\s+([A-Za-zÀ-ÿ\s]+)",
    "likes": r"(?:i like|i love)\s+(.+)",
}


def extract_facts(text: str) -> dict:
    facts = {}

    for key, pattern in PATTERNS.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            facts[key] = match.group(1).strip()

    return facts
