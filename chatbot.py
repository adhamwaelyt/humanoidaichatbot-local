
import sys
import os
import json
import random
import time
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.hf_downloader import download_model
from utils.model_loader import load_model
from utils.presets import load_preset
from utils.memory import save_chat
from mood_system import (
    update_mood,
    inject_mood,
    show_mood_terminal
)
from memory_system import (
    remember_fact,
    inject_memory_prompt,
    load_chat_history,
    save_chat_history,
    get_chat_path
)
from rich import print

def choose_from_list(prompt, options):
    print(f"\n[bold]{prompt}[/bold]")
    for idx, opt in enumerate(options):
        print(f"{idx + 1}. {opt}")
    choice = int(input("Pick one: ")) - 1
    return options[choice]

def list_downloaded_models():
    return [f for f in os.listdir("models") if os.path.isdir(os.path.join("models", f))]

def get_emoji(text):
    if any(x in text.lower() for x in ["love", "miss", "babe", "cutie"]):
        return "😍"
    elif any(x in text.lower() for x in ["lol", "funny", "lmao"]):
        return "😂"
    elif any(x in text.lower() for x in ["mad", "angry"]):
        return "😠"
    elif any(x in text.lower() for x in ["sad", "sorry"]):
        return "😢"
    else:
        return random.choice(["✨", "😏", "👀", "🤭", "❤️"])

def type_out(text, delay=0.012):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def typing_animation(name, duration=1.2):
    print(f"[italic cyan]{name} is typing[/italic cyan]", end="", flush=True)
    dot_count = int(duration / 0.4)
    for _ in range(dot_count):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print("\r" + " " * 40 + "\r", end="", flush=True)

def format_reply(reply):
    reply = reply.strip().replace("\n", " ").replace("  ", " ")
    if not reply.endswith((".", "!", "?")):
        reply += "."
    reply = reply[0].upper() + reply[1:]
    return f"\"{reply}\""

def chat_loop(model_path, preset_path, session_name, persona):
    chat_model = load_model(model_path)
    preset = load_preset(preset_path)
    if preset is None:
        print("[red]❌ Failed to load preset. Make sure the JSON is valid.[/red]")
        return

    history = load_chat_history(session_name)
    print(f"[bold blue]Chat started with {persona}. Type 'exit' to quit, '/switch' or '/loadsession'.[/bold blue]")

    while True:
        user = input("[bold bright_white]You:[/bold bright_white] ").strip()

        if user.lower() == "exit":
            save_chat(history, session_name)
            save_chat_history(session_name, history)
            break

        if user.lower() == "/switch":
            print("[yellow]↩️ Session ended. Switching now...[/yellow]")
            save_chat_history(session_name, history)
            return

        if user.lower() == "/loadsession":
            new_session = input("📂 Enter new session name: ").strip()
            new_session = new_session.lower().replace(" ", "_")
            history = load_chat_history(new_session)
            session_name = new_session
            print(f"[green]✅ Switched to session '{session_name}'[/green]")
            continue

        memory_result = remember_fact(user, persona)
        if memory_result:
            print(memory_result)
            continue

        mood, intensity = update_mood(persona, session_name, user)
        show_mood_terminal(persona, session_name)

        memory_prompt = inject_memory_prompt(persona)
        mood_prompt = inject_mood(persona, session_name)
        recent_turns = history[-8:] if len(history) > 8 else history
        chat_history = "\n".join([f"You: {h['user']}\n{persona}: {h['bot']}" for h in recent_turns])

        full_prompt = f"{preset['system_prompt']}\n{mood_prompt}{memory_prompt}{chat_history}\nYou: {user}\n{persona}:"

        response = chat_model(full_prompt, max_length=preset["max_length"], temperature=preset["temperature"])[0]['generated_text']
        reply = response.split(f"{persona}:")[-1].strip()
        reply = format_reply(reply)
        emoji = get_emoji(reply)

        print(f"\n[bold bright_white]You:[/bold bright_white] [italic]{user}[/italic]")
        typing_animation(persona)
        print(f"[bold magenta]{persona}:[/bold magenta] ", end="")
        type_out(f"{reply} {emoji}", delay=0.012)

        history.append({"user": user, "bot": reply, "time": datetime.now().isoformat()})

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    os.makedirs("presets", exist_ok=True)
    os.makedirs("chats", exist_ok=True)

    print("🧠 Choose a model source:")
    print("1. Use a model I already downloaded")
    print("2. Download a new model from Hugging Face")
    source_choice = input("Pick one: ").strip()

    if source_choice == "1":
        model_list = list_downloaded_models()
        if not model_list:
            print("❌ No downloaded models found.")
            exit()
        model_choice = choose_from_list("Available Downloaded Models", model_list)
        model_path = os.path.join("models", model_choice)

    elif source_choice == "2":
        model_choice = input("🔧 Paste the Hugging Face model name (e.g. tiiuae/falcon-rw-1b): ").strip()
        model_path = download_model(model_choice)
        if model_path is None:
            print("❌ Failed to download model.")
            exit()
    else:
        print("❌ Invalid option.")
        exit()

    preset_files = [f for f in os.listdir("presets") if f.endswith(".json")]
    preset_choice = choose_from_list("Available Presets", preset_files)
    persona = os.path.splitext(preset_choice)[0].replace("_", " ").title()

    session_name = input("💬 Enter a session name (e.g. ali_amelia_night): ").strip().lower().replace(" ", "_")

    chat_loop(
        model_path,
        f"presets/{preset_choice}",
        session_name,
        persona
    )
