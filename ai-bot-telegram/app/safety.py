"""Basic guardrails applied before/after talking to the LLM."""

BLOCKED_WORDS = [
    "hack",
    "malware",
    "virus",
    "exploit",
]

# Phrases we don't want the character to say, since it's meant to stay in-persona.
FORBIDDEN_PHRASES = [
    "I am an AI",
    "I am a bot",
    "I'm an artificial intelligence",
    "As an AI language model",
]


def can_reply(text: str) -> bool:
    """Simple pre-check run on the incoming message before it's sent to the LLM."""
    if not text:
        return False

    text_lower = text.lower()

    for word in BLOCKED_WORDS:
        if word in text_lower:
            return False

    return True


def filter_response(response: str) -> str:
    """Strips out phrases that would break the character's persona."""
    if not response:
        return ""

    result = response

    for phrase in FORBIDDEN_PHRASES:
        result = result.replace(phrase, "")

    return result.strip()
