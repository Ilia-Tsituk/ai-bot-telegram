from app.memory import search_memory, get_recent_history


def build_prompt(character: dict, user_id: str, user_message: str) -> str:
    memories = search_memory(user_id, user_message)
    memory_text = "\n".join(f"- {memory}" for memory in memories) if memories else "(none yet)"

    recent_history = get_recent_history(user_id) or "(no recent messages)"

    prompt = f"""
Character description:
{character["description"]}

Personality:
{", ".join(character["personality"])}

Things {character["name"]} likes:
{", ".join(character["likes"])}

Relevant long-term memories:
{memory_text}

Recent conversation:
{recent_history}

User:
{user_message}

Reply as {character["name"]}.
"""

    return prompt
