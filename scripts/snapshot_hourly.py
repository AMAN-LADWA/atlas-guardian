import json
import os
from datetime import datetime

from agent.atlas_agent import AtlasAgent
from agent.tools.news_collector import collect_all_articles
from agent.tools.news_history_manager import save_history as save_news_history, load_history as load_news_history
from agent.tools.history_manager import save_history as save_orbit_history, get_history as load_orbit_history


def run_snapshot():
    # 1. Fetch orbit snapshot
    agent = AtlasAgent()
    raw_json = agent.run()
    parsed = json.loads(raw_json)

    timestamp = datetime.utcnow().isoformat()

    orbit_entry = {
        "timestamp": timestamp,
        "elements": parsed["orbit_elements"]
    }

    # Save orbit history
    orbit_history = load_orbit_history()
    orbit_history.append(orbit_entry)
    save_orbit_history(orbit_history)

    print(f"[OK] Orbit snapshot stored at {timestamp}")

    # 2. Collect news
    articles = collect_all_articles()

    # Filter: Only include articles containing “ATLAS” or “3I”
    relevant = []
    for a in articles:
        if "atlas" in a["title"].lower() or "atlas" in a["content"].lower() or "3i" in a["title"].lower():
            relevant.append(a)

    if relevant:
        news_history = load_news_history()
        news_history.append({
            "date": timestamp,
            "articles": relevant
        })
        save_news_history(news_history)
        print(f"[OK] Stored {len(relevant)} relevant news articles")

    else:
        print("[INFO] No ATLAS-related news found")


if __name__ == "__main__":
    run_snapshot()
