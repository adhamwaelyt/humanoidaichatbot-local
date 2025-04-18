
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import shutil
import sys
from datetime import datetime

# Add local path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.model_loader import load_model
from utils.preset_loader import load_preset, create_preset
from utils.hf_downloader import download_model
from systems.memory import remember_fact, inject_memory_prompt, load_chat_history, save_chat_history
from systems.mood import update_mood, inject_mood

class Gui:
    def __init__(self, root):
        self.root = root
        self.root.title("Humanoid AI Chatbot")
        self.root.geometry("720x600")
        self.root.configure(bg="#1e1e1e")

        self.model = None
        self.preset = None
        self.persona = None
        self.session = None

        self.tabs = ttk.Notebook(self.root)
        self.chat_tab = tk.Frame(self.tabs, bg="#1e1e1e")
        self.settings_tab = tk.Frame(self.tabs, bg="#1e1e1e")
        self.memory_tab = tk.Frame(self.tabs, bg="#1e1e1e")
        self.mood_tab = tk.Frame(self.tabs, bg="#1e1e1e")
        self.tabs.add(self.chat_tab, text="🧠 Chat")
        self.tabs.add(self.settings_tab, text="⚙️ Settings")
        self.tabs.add(self.memory_tab, text="📚 Memory")
        self.tabs.add(self.mood_tab, text="📊 Mood")
        self.tabs.pack(expand=1, fill="both")

        self.chat_log = tk.Text(self.chat_tab, bg="#252526", fg="white", wrap="word", state="disabled")
        self.chat_log.pack(padx=10, pady=10, fill="both", expand=True)
        self.entry = tk.Entry(self.chat_tab, bg="#333333", fg="white", state="disabled")
        self.entry.pack(padx=10, pady=5, fill="x")
        self.entry.bind("<Return>", self.send_message)
        self.status_label = tk.Label(self.chat_tab, text="🔌 Not connected", bg="#1e1e1e", fg="gray")
        self.status_label.pack(pady=5)

        tk.Label(self.settings_tab, text="Select Model:", bg="#1e1e1e", fg="white").pack()
        self.model_var = tk.StringVar()
        self.model_menu = ttk.OptionMenu(self.settings_tab, self.model_var, "")
        self.model_menu.pack(pady=5)

        tk.Label(self.settings_tab, text="Select Preset:", bg="#1e1e1e", fg="white").pack()
        self.preset_var = tk.StringVar()
        self.preset_menu = ttk.OptionMenu(self.settings_tab, self.preset_var, "")
        self.preset_menu.pack(pady=5)

        ttk.Button(self.settings_tab, text="Start Chatbot", command=self.manual_setup).pack(pady=10)
        ttk.Button(self.settings_tab, text="Download New Model", command=self.download_model_prompt).pack(pady=5)
        ttk.Button(self.settings_tab, text="Delete Selected Model", command=self.delete_selected_model).pack(pady=5)
        ttk.Button(self.settings_tab, text="Create New Preset", command=self.create_new_preset).pack(pady=5)
        ttk.Button(self.settings_tab, text="Delete Selected Preset", command=self.delete_selected_preset).pack(pady=5)

        self.refresh_dropdowns()

    def manual_setup(self):
        model_name = self.model_var.get()
        preset_name = self.preset_var.get()
        if not model_name or not preset_name:
            self.status_label.config(text="❌ Please select both model and preset.", fg="red")
            return
        self.status_label.config(text="⏳ Loading model...", fg="orange")
        self.root.update_idletasks()
        try:
            self.model = load_model(f"chatbot/data/models/{model_name}")
            self.preset = load_preset(f"chatbot/data/presets/{preset_name}")
        except Exception as e:
            self.status_label.config(text=f"❌ Failed to load: {e}", fg="red")
            return
        self.persona = os.path.splitext(preset_name)[0].replace("_", " ").title()
        self.session = "gui_session"
        self.status_label.config(text=f"✅ {self.persona} is ready. Type to chat.", fg="lime")
        self.entry.config(state="normal")

    def send_message(self, event):
        user_input = self.entry.get().strip()
        if not user_input:
            return
        self.entry.delete(0, tk.END)
        self.append_chat(f"You: {user_input}")
        memory_result = remember_fact(user_input, self.persona)
        if memory_result:
            self.append_chat(f"{self.persona}: {memory_result}")
            return
        update_mood(self.persona, self.session, user_input)
        memory_prompt = inject_memory_prompt(self.persona)
        mood_prompt = inject_mood(self.persona, self.session)
        history = load_chat_history(self.session)[-8:]
        chat_history = "\n".join([f"You: {h['user']}\n{self.persona}: {h['bot']}" for h in history])
        full_prompt = f"{self.preset['system_prompt']}\n{mood_prompt}{memory_prompt}{chat_history}\nYou: {user_input}\n{self.persona}:"
        response = self.model(full_prompt, max_length=self.preset["max_length"], temperature=self.preset["temperature"])[0]['generated_text']
        reply = response.split(f"{self.persona}:")[-1].strip().capitalize()
        self.append_chat(f"{self.persona}: {reply}")
        history.append({"user": user_input, "bot": reply, "time": datetime.now().isoformat()})
        save_chat_history(self.session, history)

    def append_chat(self, text):
        self.chat_log.config(state="normal")
        self.chat_log.insert("end", f"{text}\n\n")
        self.chat_log.config(state="disabled")
        self.chat_log.yview_moveto(1.0)

    def download_model_prompt(self):
        model_name = simpledialog.askstring("Download Model", "Enter Hugging Face model name:")
        if not model_name:
            return
        try:
            result = download_model(model_name, "chatbot/data/models")
            if result:
                messagebox.showinfo("Success", f"✅ Model downloaded to: {result}")
                self.refresh_dropdowns()
            else:
                messagebox.showerror("Failed", "❌ Model download failed.")
        except Exception as e:
            messagebox.showerror("Error", f"❌ {str(e)}")

    def delete_selected_model(self):
        model_name = self.model_var.get()
        if not model_name:
            return messagebox.showwarning("Warning", "Please select a model to delete.")
        confirm = messagebox.askyesno("Delete Model", f"Are you sure you want to delete '{model_name}'?")
        if confirm:
            try:
                shutil.rmtree(os.path.join("chatbot/data/models", model_name))
                messagebox.showinfo("Deleted", f"🗑️ Model '{model_name}' deleted.")
                self.refresh_dropdowns()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Could not delete model: {e}")

    def create_new_preset(self):
        create_preset()
        self.refresh_dropdowns()

    def delete_selected_preset(self):
        preset_name = self.preset_var.get()
        if not preset_name:
            return messagebox.showwarning("Warning", "Please select a preset to delete.")
        confirm = messagebox.askyesno("Delete Preset", f"Are you sure you want to delete '{preset_name}'?")
        if confirm:
            try:
                os.remove(os.path.join("chatbot/data/presets", preset_name))
                messagebox.showinfo("Deleted", f"🗑️ Preset '{preset_name}' deleted.")
                self.refresh_dropdowns()
            except Exception as e:
                messagebox.showerror("Error", f"❌ Could not delete preset: {e}")

    def refresh_dropdowns(self):
        models = os.listdir("chatbot/data/models")
        presets = [f for f in os.listdir("chatbot/data/presets") if f.endswith(".json")]
        self.model_menu["menu"].delete(0, "end")
        for model in models:
            self.model_menu["menu"].add_command(label=model, command=lambda value=model: self.model_var.set(value))
        if models:
            self.model_var.set(models[0])
        self.preset_menu["menu"].delete(0, "end")
        for preset in presets:
            self.preset_menu["menu"].add_command(label=preset, command=lambda value=preset: self.preset_var.set(value))
        if presets:
            self.preset_var.set(presets[0])

if __name__ == "__main__":
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()
