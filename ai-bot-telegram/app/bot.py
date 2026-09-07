import asyncio
import random

from telethon import TelegramClient, events

from app.config import (
    API_ID,
    API_HASH,
    REPLY_DELAY_MIN,
    REPLY_DELAY_MAX,
    PROACTIVE_CHECK_INTERVAL_SECONDS,
)

from app.personality import load_character

from app.memory import (
    save_memory,
    search_memory,
    add_to_history,
    get_recent_history,
)

from app.prompts import build_prompt
from app.llm import generate
from app.emotions import detect_emotion
from app.facts_extractor import extract_facts

from app.relationships import get_relationship, update_relationship
from app.evolution import evolve_personality
from app.attention import update_attention, get_known_users
from app.autonomy import should_start_conversation, generate_proactive_message

from app.safety import can_reply, filter_response
from app.state import update_state, decrease_energy


# ==========================
# Telegram client
# (Telethon logs in as a regular user account rather than a bot, so
#  messages come from a normal Telegram profile - see README for setup)
# ==========================

client = TelegramClient("luna_session", API_ID, API_HASH)


# ==========================
# Load character
# ==========================

character = load_character()
print(f"{character['name']} loaded")


# ==========================
# Message handler
# ==========================

@client.on(events.NewMessage)
async def handler(event):
    try:
        # Ignore our own messages
        if event.out:
            return

        user_id = str(event.sender_id)
        message = event.text

        if not message:
            return

        print(f"USER {user_id}: {message}")

        # Safety check
        if not can_reply(message):
            return

        # Track activity
        update_attention(user_id)

        # Long-term + short-term memory
        save_memory(user_id, message)
        add_to_history(user_id, "User", message)

        # Pull out any simple facts (name, age, city, likes...) for later use
        facts = extract_facts(message)
        if facts:
            print(f"Facts extracted for {user_id}: {facts}")

        # Emotion + internal state
        emotion = detect_emotion(message)
        update_state(mood=emotion)

        # Relationship progress
        relation = update_relationship(user_id)
        closeness = evolve_personality()

        # Build the prompt
        prompt = build_prompt(character, user_id, message)
        prompt += f"""

Current emotion: {emotion}
Relationship: {relation['status']} (closeness: {closeness})

Answer naturally as {character['name']}.
"""

        # Simulate someone actually typing before replying
        async with client.action(event.chat_id, "typing"):
            await asyncio.sleep(random.uniform(REPLY_DELAY_MIN, REPLY_DELAY_MAX))

            response = generate(prompt)
            response = filter_response(response)

        if not response:
            return

        # Save the reply to both memory layers
        save_memory(user_id, f"{character['name']}: {response}")
        add_to_history(user_id, character["name"], response)

        decrease_energy()

        print(f"{character['name'].upper()}:", response)
        await event.respond(response)

    except Exception as e:
        print("MESSAGE ERROR:", e)


# ==========================
# Autonomy loop
# Occasionally messages recently-active users first, instead of only
# ever replying.
# ==========================

async def autonomy_loop():
    while True:
        await asyncio.sleep(PROACTIVE_CHECK_INTERVAL_SECONDS)

        for user_id in get_known_users():
            if should_start_conversation():
                try:
                    message = generate_proactive_message()
                    await client.send_message(int(user_id), message)
                    add_to_history(user_id, character["name"], message)
                    print(f"{character['name']} proactively messaged {user_id}: {message}")
                except Exception as e:
                    print("AUTONOMY ERROR:", e)


# ==========================
# Start
# ==========================

async def main():
    await client.start()
    print(f"{character['name'].upper()} ONLINE")

    asyncio.create_task(autonomy_loop())

    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
