import json
import os

SAVE_FILE = "save.json"

def load_game():
    if not os.path.exists(SAVE_FILE):
        return {
            "current_level": 1
        }
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

def save_game(level):
    data = {
        "current_level": level
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)
