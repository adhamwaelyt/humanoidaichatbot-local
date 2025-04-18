import os
import json
from datetime import datetime
from collections import defaultdict

MOOD_PATH = "chatbot/data/mood_bank"
os.makedirs(MOOD_PATH, exist_ok=True)

def mood_file_path(persona, session):
    safe = f"{persona}_{session}".lower().replace(" ", "_")
    return os.path.join(MOOD_PATH, f"{safe}.json")

def load_mood(persona, session):
    path = mood_file_path(persona, session)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"mood": "neutral", "intensity": 0.0, "history": []}

def save_mood(persona, session, mood_data):
    path = mood_file_path(persona, session)
    with open(path, "w") as f:
        json.dump(mood_data, f, indent=2)

MOOD_KEYWORDS = {
    "angry": ["annoying", "stupid", "hate", "shut up"],
    "sad": ["miss you", "lonely", "depressed", "sad", "cry"],
    "flirty": ["cute", "hot", "babe", "kiss", "i like you"],
    "friendly": ["hey", "hi", "how are you"],
    "curious": ["what", "why", "how", "explain", "tell me"],
    "neutral": ["okay", "fine", "sure"]
}

MOOD_EMOJIS = {
    "angry": "😠", "sad": "😢", "flirty": "😏", "friendly": "😊",
    "curious": "🤭", "neutral": "😐"
}

MOOD_RESPONSES = {
    "angry": "Respond firmly but controlled.",
    "sad": "Be empathetic and comforting.",
    "flirty": "Be playful and teasing.",
    "friendly": "Be warm and casual.",
    "curious": "Be detailed and helpful.",
    "neutral": "Respond normally."
}

def detect_mood(user_input, current_mood):
    score = defaultdict(int)
    input_lower = user_input.lower()

    for mood, keywords in MOOD_KEYWORDS.items():
        for word in keywords:
            if word in input_lower:
                score[mood] += 1

    if not score:
        return current_mood["mood"], current_mood["intensity"]

    detected = max(score, key=score.get)
    new_intensity = min(1.0, current_mood["intensity"] + 0.2)

    return detected, new_intensity

def update_mood(persona, session, user_input):
    mood_data = load_mood(persona, session)
    mood, intensity = detect_mood(user_input, mood_data)

    mood_data["mood"] = mood
    mood_data["intensity"] = round(intensity, 2)
    mood_data["history"].append({"input": user_input, "mood": mood, "time": datetime.now().isoformat()})
    save_mood(persona, session, mood_data)

    return mood, intensity

def inject_mood(persona, session):
    mood_data = load_mood(persona, session)
    mood = mood_data["mood"]
    intensity = mood_data["intensity"]
    emoji = MOOD_EMOJIS.get(mood, "😐")
    advice = MOOD_RESPONSES.get(mood, "Respond normally.")

    return f"Current Mood: {mood.title()} {emoji} ({intensity})\nMood Guidance: {advice}\n"

def show_mood_terminal(persona, session):
    mood_data = load_mood(persona, session)
    emoji = MOOD_EMOJIS.get(mood_data["mood"], "😐")
    print(f"[italic]\U0001F9E0 {persona}'s mood: {emoji} {mood_data['mood'].title()} ({mood_data['intensity']})[/italic]")