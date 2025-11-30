import json
import os
from datetime import datetime

HISTORY_PATH = os.path.join("data", "history.json")


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
