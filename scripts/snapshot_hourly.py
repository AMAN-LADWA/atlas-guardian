import os, sys
print(">>> Using GITHUB_WORKSPACE:", os.getenv("GITHUB_WORKSPACE"))

# Add REPO ROOT to Python path (dynamic, guaranteed to work)
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

print(">>> Repo Root Added:", repo_root)
print(">>> sys.path:", sys.path)

# Now import everything
from agent.atlas_agent import AtlasAgent
from agent.tools.news_collector import collect_all_articles
from agent.tools.news_history_manager import load_history as load_news_history, save_history as save_news_history
from agent.tools.history_manager import load_history as load_orbit_history, save_history as save_orbit_history
from datetime import datetime
import json

def run_snapshot():
    timestamp = datetime.utcnow().isoformat()

    # ORBIT SNAPSHOT
    agent = AtlasAgent()
    parsed = json.loads(agent.run())
    latest_orbit = parsed["orbit_elements"]

    orbit_hist = load_orbit_history()
    orbit_hist.append({
        "timestamp": timestamp,
        "elements": latest_orbit
    })
    save_orbit_history(orbit_hist)
    print(f"[OK] Orbit snapshot stored: {timestamp}")

    # NEWS SNAPSHOT
    articles = collect_all_articles()

    relevant = [
        a for a in articles
        if "atlas" in a["title"].lower() or "atlas" in a["content"].lower() or "3i" in a["title"].lower()
    ]

    if relevant:
        news_hist = load_news_history()
        news_hist.append({
            "date": timestamp,
            "articles": relevant
        })
        save_news_history(news_hist)
        print(f"[OK] Stored {len(relevant)} news articles")
    else:
        print("[INFO] No relevant news")


if __name__ == "__main__":
    run_snapshot()
