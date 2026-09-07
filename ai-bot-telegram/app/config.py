import os
from dotenv import load_dotenv

load_dotenv()

# =====================
# Telegram (Telethon - logs in as a regular user account, not a bot)
# =====================
# Get these at https://my.telegram.org
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")

# =====================
# Ollama
# =====================
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL = os.getenv("MODEL", "qwen3:14b")

# =====================
# Character
# =====================
CHARACTER = os.getenv("CHARACTER", "luna")

# =====================
# Memory
# =====================
MEMORY_PATH = os.getenv("MEMORY_PATH", "memory_db")
SHORT_TERM_HISTORY_LENGTH = 12  # number of recent messages kept in short-term memory per user

# =====================
# Behaviour
# =====================
MAX_RESPONSE_LENGTH = 500
TEMPERATURE = 0.9
TOP_P = 0.9
TOP_K = 40
REPEAT_PENALTY = 1.15
MAX_TOKENS = 100

# Random delay range (seconds) before replying, to feel more natural
REPLY_DELAY_MIN = 2
REPLY_DELAY_MAX = 6

# Probability (0-1) of sending an unprompted message to a recently active user
PROACTIVE_MESSAGE_CHANCE = 0.05
PROACTIVE_CHECK_INTERVAL_SECONDS = 900  # how often the autonomy loop checks in
