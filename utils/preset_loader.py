import json
import os

def load_preset(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load preset: {e}")
        return None

def create_preset():
    print("\n🎨 Create a Detailed Personality Preset")
    name = input("🎭 Preset name (e.g., flirty_friend): ").strip().lower().replace(" ", "_")
    description = input("📝 Short description of this personality: ")
    role = input("👤 Persona's role or relationship (e.g., best friend, crush, assistant): ")
    tone = input("🎙️ Overall tone/style (e.g., playful, gentle, sarcastic): ")
    quirks = input("✨ Unique traits or quirks (e.g., uses emojis, loves teasing): ")
    examples = input("💬 Example replies (comma-separated): ").split(',')
    prompt = input("🧠 Base system prompt text (defines AI behavior): ")
    temperature = float(input("🔥 Response randomness (0.1 = focused, 1.0 = creative): "))
    max_length = int(input("📏 Max length of replies (tokens): "))

    preset = {
        "name": name,
        "description": description,
        "role": role,
        "tone": tone,
        "quirks": quirks,
        "example_replies": [e.strip() for e in examples if e.strip()],
        "system_prompt": prompt,
        "temperature": temperature,
        "max_length": max_length
    }

    os.makedirs("chatbot/data/presets", exist_ok=True)
    path = os.path.join("chatbot/data/presets", f"{name}.json")

    with open(path, "w") as f:
        json.dump(preset, f, indent=2)

    print(f"✅ Preset saved as: [bold green]{path}[/bold green]\n")

def prompt_preset_menu():
    print("\n🎛️ Preset Options:")
    print("1. Load existing preset")
    print("2. Create a new preset")
    choice = input("Select an option: ").strip()
    return choice
