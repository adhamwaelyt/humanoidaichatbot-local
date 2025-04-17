import json
import csv
import os
from datetime import datetime

def save_chat(history, filename):
    os.makedirs("chats", exist_ok=True)

    # Save as JSON
    with open(f"chats/{filename}.json", "w") as f:
        json.dump(history, f, indent=4)

    # Save as CSV
    csv_path = f"chats/{filename}.csv"
    with open(csv_path, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "user", "bot"])
        writer.writeheader()
        for entry in history:
            writer.writerow({
                "timestamp": datetime.now().isoformat(timespec='seconds'),
                "user": entry["user"],
                "bot": entry["bot"]
            })
