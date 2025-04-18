from huggingface_hub import hf_hub_download, HfApi
from rich.progress import Progress
import os

def download_model(model_name: str, save_path: str = "chatbot/data/models/"):
    print(f"🔍 Looking up files for [bold]{model_name}[/bold]...")

    local_dir = os.path.join(save_path, model_name.replace("/", "_"))
    os.makedirs(local_dir, exist_ok=True)

    api = HfApi()
    try:
        files = api.list_repo_files(model_name)
    except Exception as e:
        print(f"[red]❌ Error listing files for {model_name}:[/red] {e}")
        return None

    if any(f.endswith(".bin") or f.endswith(".safetensors") for f in files):
        print("[yellow]⚠️ Detected this is a Transformers model – download will happen on load.[/yellow]")
        return local_dir

    gguf_files = [f for f in files if f.endswith(".gguf")]
    if not gguf_files:
        print(f"[red]❌ No GGUF files found in {model_name}[/red]")
        return None

    with Progress() as progress:
        task = progress.add_task("[green]Downloading GGUF file...", total=len(gguf_files))
        for f in gguf_files:
            print(f"📦 Downloading [cyan]{f}[/cyan]...")
            hf_hub_download(repo_id=model_name, filename=f, local_dir=local_dir, local_dir_use_symlinks=False)
            progress.update(task, advance=1)

    print(f"✅ GGUF model downloaded to [bold green]{local_dir}[/bold green]")
    return local_dir