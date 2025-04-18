# Humanoid AI Chatbot (V0.2)

A powerful, fully offline AI chatbot that feels human — now with both **terminal** and **GUI** versions. Built for emotional realism, memory, mood, persona switching, and local LLM model support 🧠💬

---

## 🚀 Features

### 🧠 Long-Term Memory
- Remembers facts using `remember:` (e.g. `remember: my favorite drink is coffee`)
- Memory is persona-specific and session-aware
- Memory auto-injected into conversations

### 😏 Mood & Emotion Engine
- Detects emotional cues (angry, sad, flirty, etc.)
- Adjusts tone and response style accordingly
- Tracks emotional history over sessions

### 🧑‍🎤 Persona & Presets
- Fully customizable presets (role, tone, quirks)
- Terminal-based builder & GUI creation tool
- Per-persona memory and mood

### 🧾 Structured Chat History
- Saves to both `.json` and `.csv` in `data/chats/`
- Easy to review or train future models

### 🖥️ GUI Version (Dark Mode)
- Chat in a rich window interface with:
  - Emoji and typing effects
  - Dropdowns for models/presets
  - Tabs for settings, memory, and mood
  - Live status + session switching

### 💬 Terminal Version
- Type to chat with mood & memory context
- Use commands like `/switch` or `/loadsession`

### 📥 Model Handling
- Supports Hugging Face or local GGUF models
- Auto-detects transformers vs. GGUF
- Built-in downloader
- Delete or switch models any time

---

## 📁 File Structure

```
HumanoidAI/
├── gui.py                 # GUI entry point
├── chatbot.py             # Terminal entry point
├── requirements.txt
├── core/                  # Core components (chat engine, UI logic)
├── systems/               # Mood & memory engines
├── utils/                 # Preset/model utilities
├── data/
│   ├── models/            # Local LLM models
│   ├── presets/           # Persona configuration
│   ├── chats/             # Chat logs
│   └── mood_bank/         # Mood logs
```

---

## ▶️ How to Use

### 1. Install requirements:
```bash
pip install -r requirements.txt
```

### 2. Run GUI version:
```bash
python gui.py
```

### 3. Run terminal version:
```bash
python chatbot.py
```

---

## 💡 Upcoming Features

- 🎙️ Voice Mode (Jarvis-style mic & TTS)
- 📊 Mood graph tab in GUI
- 🧠 Real-time memory editing
- 🗣️ Multilingual persona support
- 🌐 Web interface (local-only Flask app)
- 📁 Drag-and-drop GGUF support

---

## 💥 Known Issues & Changes

GUI does not work, will be fixed in the next update.
Changed the files to be easier to work with and fixed issues with libraries, timing, and code errors.
Properly works now.

## 🤝 Contributing

Want to build new presets, add voice, or improve the GUI? Pull requests welcome!

---

## 🧑‍💻 Built by Ali

Terminal + GUI AI coded from scratch with Python and imagination 💡

---

## 🪪 License

MIT License — fork it, remix it, make it your own.
