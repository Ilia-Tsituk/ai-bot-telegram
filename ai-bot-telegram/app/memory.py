"""
Two layers of memory:

- Long-term memory: every message is embedded and stored in a persistent
  Chroma collection, so relevant past messages can be retrieved by semantic
  similarity, no matter how long ago they were sent.
- Short-term memory: a small in-memory rolling window of the most recent
  messages per user, used to give the model immediate conversational
  context without a similarity search.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from app.config import MEMORY_PATH, SHORT_TERM_HISTORY_LENGTH

_client = chromadb.PersistentClient(
    path=MEMORY_PATH,
    settings=Settings(anonymized_telemetry=False),
)
_collection = _client.get_or_create_collection("luna_memory")

_embedder = SentenceTransformer("all-MiniLM-L6-v2")

# user_id -> list of {"role": ..., "text": ...}
_short_term_history = {}


# --- Long-term (vector) memory ----------------------------------------------

def save_memory(user_id: str, text: str) -> None:
    embedding = _embedder.encode(text).tolist()

    _collection.add(
        ids=[f"{user_id}_{_collection.count()}"],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"user_id": user_id}],
    )


def search_memory(user_id: str, query: str, limit: int = 5) -> list:
    embedding = _embedder.encode(query).tolist()

    result = _collection.query(
        query_embeddings=[embedding],
        n_results=limit,
        where={"user_id": user_id},
    )

    if not result["documents"]:
        return []

    return result["documents"][0]


def get_all_memories(user_id: str) -> list:
    result = _collection.get(where={"user_id": user_id})
    return result["documents"] if result["documents"] else []


def clear_memory(user_id: str) -> None:
    result = _collection.get(where={"user_id": user_id})
    ids = result["ids"]

    if ids:
        _collection.delete(ids=ids)


# --- Short-term (rolling) memory --------------------------------------------

def add_to_history(user_id: str, role: str, text: str) -> None:
    if user_id not in _short_term_history:
        _short_term_history[user_id] = []

    _short_term_history[user_id].append({"role": role, "text": text})
    _short_term_history[user_id] = _short_term_history[user_id][-SHORT_TERM_HISTORY_LENGTH:]


def get_recent_history(user_id: str) -> str:
    if user_id not in _short_term_history:
        return ""

    lines = [f"{m['role']}: {m['text']}" for m in _short_term_history[user_id]]
    return "\n".join(lines)


def clear_recent_history(user_id: str) -> None:
    _short_term_history.pop(user_id, None)
