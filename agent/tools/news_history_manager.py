import json
import os
from datetime import datetime

ROOT = os.getenv("GITHUB_WORKSPACE", os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATA_PATH = os.path.join(ROOT, "data", "news_history.json")
HISTORY_PATH = DATA_PATH
# Keywords STRICTLY matching 3I/ATLAS
STRICT_KEYWORDS = [
    "3i atlas",
    "c/2025 n1",
    "c 2025 n1",
    "interstellar comet atlas",
    "atlas comet"
]


def ensure_file():
    """Create file if it doesn't exist."""
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump([], f)


def load_history():
    ensure_file()
    with open(HISTORY_PATH, "r") as f:
        return json.load(f)


def save_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def filter_strict_atlas_articles(articles):
    """Return only articles strictly mentioning 3I/ATLAS."""
    filtered = []
    for a in articles:
        text = (a["title"] + " " + a["content"]).lower()
        if any(kw in text for kw in STRICT_KEYWORDS):
            filtered.append(a)
    return filtered


def append_today_articles(articles):
    """
    Store strictly-relevant articles for today's date.
    Do NOT store duplicates.
    """
    ensure_file()
    history = load_history()

    today = datetime.utcnow().strftime("%Y-%m-%d")

    # Filter strictly about ATLAS
    relevant = filter_strict_atlas_articles(articles)

    if not relevant:
        return False  # nothing new

    # Check if today's entry exists
    for entry in history:
        if entry["date"] == today:
            # Append unique articles
            existing_links = {a["url"] for a in entry["articles"]}
            new_articles = [
                a for a in relevant if a["url"] not in existing_links
            ]
            entry["articles"].extend(new_articles)
            save_history(history)
            return True

    # If new date
    history.append({
        "date": today,
        "articles": relevant
    })
    save_history(history)
    return True
