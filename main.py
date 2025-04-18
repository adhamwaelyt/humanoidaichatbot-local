import os
from core.chat_engine import chat_loop
from core.selector import choose_from_list, list_downloaded_models
from utils.hf_downloader import download_model
from utils.preset_loader import load_preset, create_preset, prompt_preset_menu

if __name__ == "__main__":
    os.makedirs("chatbot/data/models", exist_ok=True)
    os.makedirs("chatbot/data/presets", exist_ok=True)
    os.makedirs("chatbot/data/chats", exist_ok=True)

    print("🧠 Choose a model source:")
    print("1. Use a model I already downloaded")
    print("2. Download a new model from Hugging Face")
    source_choice = input("Pick one: ").strip()

    if source_choice == "1":
        model_list = list_downloaded_models("chatbot/data/models")
        if not model_list:
            print("❌ No downloaded models found.")
            exit()
        model_choice = choose_from_list("Available Downloaded Models", model_list)
        model_path = os.path.join("chatbot/data/models", model_choice)

    elif source_choice == "2":
        model_choice = input("🔧 Paste the Hugging Face model name (e.g. tiiuae/falcon-rw-1b): ").strip()
        model_path = download_model(model_choice, "chatbot/data/models")
        if model_path is None:
            print("❌ Failed to download model.")
            exit()
    else:
        print("❌ Invalid option.")
        exit()

    preset_action = prompt_preset_menu()
    if preset_action == "2":
        create_preset()

    preset_files = [f for f in os.listdir("chatbot/data/presets") if f.endswith(".json")]
    if not preset_files:
        print("❌ No presets found. Please create one first.")
        exit()

    preset_choice = choose_from_list("Available Presets", preset_files)
    persona = os.path.splitext(preset_choice)[0].replace("_", " ").title()

    session_name = input("💬 Enter a session name (e.g. ali_amelia_night): ").strip().lower().replace(" ", "_")

    chat_loop(
        model_path,
        f"chatbot/data/presets/{preset_choice}",
        session_name,
        persona
    )
