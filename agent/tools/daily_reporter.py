from groq import Groq
import os
import json
from agent.tools.news_collector import collect_all_articles
from agent.tools.history_manager import get_history
from agent.atlas_agent import AtlasAgent


def generate_daily_report():
    # 1. Fetch space/orbit data
    agent = AtlasAgent()
    orbit_report = json.loads(agent.run())

    # 2. Get last 10 historical snapshots
    history = get_history()[-10:]

    # 3. Collect articles + RSS
    articles = collect_all_articles()

    # Prepare text corpus
    article_text = "\n\n".join(
        [f"Title: {a['title']}\nContent: {a['content']}" for a in articles]
    )

    # 4. Call Groq LLM
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are ATLAS Guardian — an AI system that monitors "
        "interstellar objects and analyzes online scientific and public sentiment. "
        "Create a formal daily intelligence brief."
    )

    user_payload = json.dumps(
        {
            "orbit": orbit_report,
            "history": history,
            "articles": articles,
        },
        indent=2
    )

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Data:\n{user_payload}"},
        ],
    )

    return resp.choices[0].message.content
