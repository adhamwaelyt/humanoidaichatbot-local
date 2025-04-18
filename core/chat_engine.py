import os
import time
import random
from datetime import datetime
from systems.memory import remember_fact, inject_memory_prompt, load_chat_history, save_chat_history
from systems.mood import update_mood, inject_mood, show_mood_terminal
from utils.model_loader import load_model
from utils.preset_loader import load_preset
from core.formatter import format_reply, type_out, typing_animation, get_emoji
from rich import print


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
            save_chat_history(session_name, history)
            break

        if user.lower() == "/switch":
            print("[yellow]↩️ Session ended. Switching now...[/yellow]")
            save_chat_history(session_name, history)
            return

        if user.lower() == "/loadsession":
            new_session = input("📂 Enter new session name: ").strip().lower().replace(" ", "_")
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