import os
from rich import print

def choose_from_list(prompt, options):
    print(f"\n[bold]{prompt}[/bold]")
    for idx, opt in enumerate(options):
        print(f"{idx + 1}. {opt}")
    while True:
        try:
            choice = int(input("Pick one: ")) - 1
            if 0 <= choice < len(options):
                return options[choice]
        except ValueError:
            pass
        print("[red]Invalid choice. Try again.[/red]")

def list_downloaded_models(model_dir="chatbot/data/models"):
    return [f for f in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, f))]