# Terminal AI Chatbot (Humanoid AI Chatbot V0.1)

A powerful, fully offline terminal-based AI chatbot designed to feel human. This emotionally aware assistant is built for realistic conversation, long-term memory, dynamic mood simulation, and local LLM model support. Built entirely in Python 🧠💬

---

## 🚀 Features

### 🧠 Long-Term Memory (Per Persona & Session)
- Remembers facts you tell it using `remember:` (e.g. `remember: my favorite color is blue`)
- Automatically saves and loads chat context from past sessions
- Supports multiple saved conversations per persona

### 😏 Mood & Emotion Simulation
- Dynamically detects your tone (angry, sad, flirty, curious...)
- Displays live emotional state with emoji and intensity
- Changes its responses to match the mood
- Emotion history saved per session

### 💬 Realistic & Humanlike Responses
- Smart grammar, punctuation, and speech formatting
- Wraps replies in quotes, e.g., "I'm happy you're here."
- Typing delay animation for realism (`typing...` effect)

### 🧑‍🎤 Persona & Session Management
- Choose different personalities (e.g., flirty, serious, assistant)
- Each persona has their own memory and mood
- Use `/switch` or `/loadsession` to jump between conversations

### ✍️ Preset Creator (Terminal-Based)
- Build your own AI personas directly from the terminal
- Adjust system prompts, temperature, and response length easily

### 🔁 Model Switching + HuggingFace Downloader
- Download models from HuggingFace by pasting the model name
- Use any compatible GGUF or CausalLM transformer
- Automatically detects model type and loads accordingly

### 🧾 Smart Logging (JSON + CSV)
- Saves all chats to `chats/` in both readable and structured formats
- Perfect for reviewing sessions or training data

### ⚡ Works Fully Offline
- Compatible with local models (e.g., GGUF from HuggingFace)
- No API calls, no internet required

---

## 📥 Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Bot

```bash
python chatbot.py
```

You'll be prompted to:
- Choose a model (paste or select from local)
- Choose a personality preset
- Name the chat session

Then you're chatting ✨

---

## 📂 File Structure

```
project/
├── chatbot.py             # Main app
├── memory_system.py       # Long-term memory engine
├── mood_system.py         # Emotional simulation engine
├── requirements.txt       # All dependencies
├── utils/                 # Model, preset, and file handling
├── presets/               # Personality profiles (JSON)
├── models/                # Local model storage (GGUF/HF)
├── chats/                 # Chat logs
├── mood_bank/             # Mood states per persona/session
```

---

## 📌 Planned Features (V0.2 and beyond)

- 🎙️ Voice Input/Output (Jarvis mode)
- 📱 GUI interface with chat bubble view
- 🧠 Persistent memory threading (true lifelong memory)
- 📊 Emotion graphing over time
- 🪄 Local fine-tuning via feedback
- 🔊 Typing sounds + interactive prompt sounds
- 🗣️ Multilingual personality presets

---

## 🤝 Contributing
This is just the beginning. Open to:
- Preset submissions
- Prompt engineers
- Python contributors

Feel free to fork, modify, and contribute!

---

## 🧑‍💻 Credits
Built with ❤️ by **Ali** — ChatGPT-powered coder, dreamer, and builder of custom offline AI.

---

## 🪪 License
MIT License – use freely, modify completely. You built this.
