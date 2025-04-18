import time
import random
from rich import print

def format_reply(reply):
    reply = reply.strip().replace("\n", " ").replace("  ", " ")
    if not reply.endswith((".", "!", "?")):
        reply += "."
    reply = reply[0].upper() + reply[1:]
    return f'"{reply}"'

def get_emoji(text):
    text = text.lower()
    if any(word in text for word in ["love", "miss", "babe", "cutie"]):
        return "😍"
    elif any(word in text for word in ["lol", "funny", "lmao"]):
        return "😂"
    elif any(word in text for word in ["mad", "angry"]):
        return "😠"
    elif any(word in text for word in ["sad", "sorry"]):
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