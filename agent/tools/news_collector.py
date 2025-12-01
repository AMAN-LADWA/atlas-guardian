import requests
import feedparser
from agent.tools.news_history_manager import append_today_articles


NEWSAPI_KEY = None  # optional, set later if you want
SPACE_QUERY = "C/2025 N1 OR ATLAS comet OR interstellar object"


# ----------------------
# 1. NewsAPI collector
# ----------------------
KEYWORDS = ["comet", "atlas", "c/2025", "interstellar", "astronomy", "space", "nasa"]

def filter_relevant_articles(articles):
    filtered = []
    for a in articles:
        text = (a["title"] + " " + a["content"]).lower()
        if any(kw in text for kw in KEYWORDS):
            filtered.append(a)
    return filtered

def get_newsapi_articles():
    if not NEWSAPI_KEY:
        return []

    url = (
        "https://newsapi.org/v2/everything?"
        f"q={SPACE_QUERY}&"
        "sortBy=publishedAt&"
        f"apiKey={NEWSAPI_KEY}"
    )

    resp = requests.get(url)
    data = resp.json()

    if "articles" not in data:
        return []

    return [
        {
            "source": a.get("source", {}).get("name"),
            "title": a.get("title"),
            "url": a.get("url"),
            "content": a.get("description") or "",
        }
        for a in data["articles"]
    ]


# ----------------------
# 2. RSS collectors
# ----------------------
RSS_FEEDS = [
    "https://www.space.com/feeds/all",
    "https://www.nasa.gov/rss/dyn/breaking_news.rss",
    "https://www.sciencedaily.com/rss/space_time.xml",
    "https://phys.org/rss-feed/space-news/astronomy/",
]


def get_rss_articles():
    articles = []

    for feed_url in RSS_FEEDS:
        parsed = feedparser.parse(feed_url)

        for entry in parsed.entries[:10]:  # last 10 entries from each feed
            articles.append(
                {
                    "source": parsed.feed.get("title", "RSS"),
                    "title": entry.get("title"),
                    "url": entry.get("link"),
                    "content": entry.get("summary", ""),
                }
            )

    return articles


# ----------------------
# 3. Combined collector
# ----------------------
def collect_all_articles():
    newsapi = get_newsapi_articles()
    rss = get_rss_articles()
    combined = newsapi + rss

    # store strictly relevant articles
    append_today_articles(combined)

    return combined

