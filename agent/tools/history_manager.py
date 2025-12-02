import json
import os
from datetime import datetime

ROOT = os.getenv("GITHUB_WORKSPACE", os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_PATH = os.path.join(ROOT, "data", "history.json")
HISTORY_PATH = DATA_PATH

def load_history():
    if not os.path.exists(HISTORY_PATH):
        return []

    with open(HISTORY_PATH, "r") as f:
        try:
            return json.load(f)
        except:
            return []


def save_history(history):
    os.makedirs("data", exist_ok=True)
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=4)


def store_snapshot(snapshot):
    history = load_history()
    history.append(snapshot)
    save_history(history)


def get_last_snapshot():
    history = load_history()
    if not history:
        return None
    return history[-1]


def get_history():
    return load_history()
