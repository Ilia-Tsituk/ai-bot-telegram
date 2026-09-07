"""Quick manual smoke test for the long-term memory layer.

Run with: python test_memory.py
"""

from app.memory import save_memory, search_memory

save_memory("demo_user", "My name is Alex and I love going to the gym.")
save_memory("demo_user", "My favorite drink is coffee.")

results = search_memory("demo_user", "What do I like?")

print(results)
