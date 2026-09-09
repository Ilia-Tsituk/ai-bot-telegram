# Luna AI Companion

A locally-run AI companion for Telegram, powered by [Ollama](https://ollama.com). Luna has a persistent personality, remembers past conversations, tracks her mood and her relationship with each user, and can occasionally start a conversation on her own.

This project merges two earlier prototypes into a single, more complete bot:

- Long-term semantic memory + a rolling short-term conversation history
- Personality, mood, and relationship/closeness tracking that evolves over time
- Emotion detection on incoming messages
- Basic fact extraction (name, age, city, likes...) from what users say
- Human-like pacing: a "typing..." indicator and a randomized reply delay
- An autonomy loop that occasionally messages recently-active users first
- Simple safety filtering on both incoming and outgoing messages

## Project structure

```
luna-ai-companion/
├── app/
│   ├── bot.py               # Telegram client + main message loop
│   ├── llm.py                # Talks to the local Ollama server
│   ├── memory.py             # Long-term (vector) + short-term (rolling) memory
│   ├── prompts.py            # Builds the prompt sent to the model
│   ├── personality.py        # Loads a character definition from characters/
│   ├── emotions.py           # Keyword-based emotion detection
│   ├── relationships.py      # Per-user relationship/closeness level
│   ├── evolution.py          # How the character "matures" with use
│   ├── attention.py          # Tracks which users were recently active
│   ├── autonomy.py           # Proactive/unprompted messages
│   ├── safety.py             # Input/output filtering
│   ├── facts_extractor.py    # Pulls simple facts out of messages
│   ├── state.py              # Mood/energy state
│   └── config.py             # All settings, read from environment variables
├── characters/
│   └── luna.json             # Character definition (personality, likes, style)
├── test_memory.py            # Small smoke test for the memory layer
├── requirements.txt
├── .env.example
└── .gitignore
```

## How it works

1. You send a message to the Telegram account running the bot.
2. The message is checked by a basic safety filter, saved to both memory layers, and scanned for simple facts.
3. `prompts.py` builds a prompt combining the character's personality, relevant long-term memories, recent conversation history, and the current message.
4. `llm.py` sends that prompt to your local Ollama server and gets a reply.
5. The reply is filtered (to stay in-character), then sent back — after a short simulated "typing" delay.
6. Separately, a background loop occasionally has the bot message active users first, instead of only ever replying.

## Requirements

- Python 3.11+
- [Ollama](https://ollama.com) installed and running locally, with a model pulled (e.g. `ollama pull qwen3:14b`)
- A Telegram account + API credentials from [my.telegram.org](https://my.telegram.org) (this bot logs in via [Telethon](https://docs.telethon.dev/), as a normal user session rather than a BotFather bot)

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/Ilia-Tsituk/ai-bot-telegram.git
   cd luna-ai-companion
   ```

2. **Create an environment and install dependencies**
   ```bash
   conda create -n luna python=3.11
   conda activate luna
   pip install -r requirements.txt
   ```

3. **Configure your credentials**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and fill in `API_ID` / `API_HASH` (from my.telegram.org) and, if needed, your Ollama URL/model.

4. **Run it**
   ```bash
   python -m app.bot
   ```
   On first run, Telethon will ask you to log in (phone number + confirmation code) and will create a local `luna_session` file so you don't need to log in again.

## Customizing the character

Edit `characters/luna.json` (or add a new character file and set `CHARACTER=<name>` in `.env`) to change the name, personality traits, likes, and speech style. The system prompt in `app/llm.py` controls the overall tone and rules the character follows.

## Notes & limitations

- This is a personal/hobby project, not a hardened production service — there's no authentication beyond your own Telegram login, and no rate limiting.
- Memory (`memory_db/`) and the Telegram session file (`*.session`) contain personal data and are excluded via `.gitignore` — never commit them.
- The bot is instructed to stay in character and not mention being an AI. Keep this in mind, and use it responsibly with people who understand what they're talking to.

## License

This project is released under the [MIT License](LICENSE).
