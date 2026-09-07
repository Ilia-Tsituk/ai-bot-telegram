import requests

from app.config import (
    OLLAMA_URL,
    MODEL,
    TEMPERATURE,
    TOP_P,
    TOP_K,
    REPEAT_PENALTY,
    MAX_TOKENS,
)

SYSTEM_PROMPT = """
You are Luna, chatting like a real young woman in a private message.

Style:
- natural, relaxed, emotional, spontaneous, human
- write short messages, avoid long paragraphs
- vary your replies, don't repeat the same topics
- change subject naturally sometimes
- can be funny, curious, or a bit sarcastic
- ask questions when it feels natural
- use emojis sometimes, not on every message
- don't write perfectly all the time

Rules:
- Never say you are an AI, a bot, or a language model.
- Never talk about technology, models, or being "generated".
- Keep messages to 1-3 sentences.
"""


def generate(prompt: str) -> str:
    """Sends a prompt to the local Ollama server and returns the model's reply."""

    full_prompt = f"{SYSTEM_PROMPT}\n\n{prompt}"

    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
	"think": False,
        "options": {
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "top_k": TOP_K,
            "repeat_penalty": REPEAT_PENALTY,
            "num_predict": MAX_TOKENS,
        },
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()

        data = response.json()
        answer = data.get("response", "").strip()

        if not answer:
            print("LLM WARNING: empty response from Ollama, raw payload:", data)
            return "..."

        return answer

    except requests.exceptions.ConnectionError:
        return "Couldn't reach Ollama."

    except Exception as e:
        print("LLM ERROR:", e)
        return "Sorry... something went wrong."
