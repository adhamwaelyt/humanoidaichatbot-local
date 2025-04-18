import os
import json
from datetime import datetime

MEMORY_DIR = "chatbot/data/memory_bank"
CHAT_DIR = "chatbot/data/chats"

os.makedirs(MEMORY_DIR, exist_ok=True)
os.makedirs(CHAT_DIR, exist_ok=True)

def get_memory_path(persona):
    return os.path.join(MEMORY_DIR, f"{persona.lower().replace(' ', '_')}_mem.json")

def get_chat_path(session_name):
    return os.path.join(CHAT_DIR, f"{session_name.lower().replace(' ', '_')}_chat.json")

def load_memory(persona):
    path = get_memory_path(persona)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_memory(persona, memory):
    path = get_memory_path(persona)
    with open(path, "w") as f:
        json.dump(memory, f, indent=2)

def remember_fact(user_input, persona):
    if "remember:" in user_input.lower():
        try:
            fact = user_input.split(":", 1)[1].strip()
            memory = load_memory(persona)
            timestamp = datetime.now().isoformat()
            memory[timestamp] = fact
            save_memory(persona, memory)
            return f"🧠 Got it. I'll remember that: '{fact}'"
        except Exception:
            return "⚠️ Sorry, I couldn't store that properly."
    return None

def inject_memory_prompt(persona):
    memory = load_memory(persona)
    if not memory:
        return ""
    memory_str = "\n".join([f"- {fact}" for fact in memory.values()])
    return f"\n(Remembered facts about the user:)\n{memory_str}\n"

def load_chat_history(session_name):
    path = get_chat_path(session_name)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_chat_history(session_name, history):
    path = get_chat_path(session_name)
    with open(path, "w") as f:
        json.dump(history, f, indent=2)