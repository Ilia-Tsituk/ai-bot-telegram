def detect_emotion(text: str) -> str:
    """Very lightweight keyword-based emotion detection for the incoming message."""
    text = text.lower()

    happy = [
        "😂", "🤣", "😄", "😁", "😊",
        "happy", "great", "love", "cool", "awesome"
    ]

    sad = [
        "😭", "😢", "😞", "sad",
        "depressed", "cry", "down"
    ]

    angry = [
        "😡", "🤬", "angry",
        "hate", "idiot", "furious"
    ]

    for word in happy:
        if word in text:
            return "happy"

    for word in sad:
        if word in text:
            return "sad"

    for word in angry:
        if word in text:
            return "angry"

    return "neutral"
