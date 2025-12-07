import json
import os
from datetime import datetime

MEMORY_FILE = "conversation_memory.json"  # You can increase this if needed
data=[]
def load_memory():
    global data
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data # Limit to latest messages
        except json.JSONDecodeError:
            return []

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def append_to_memory( mode, user_input, llm_response):
    global data
    timestamp = datetime.now().isoformat()
    data.append({
        "timestamp": timestamp,
        "mode":mode,
        "user": user_input,
        "soul": llm_response
    })
    save_memory(data)
    return data


