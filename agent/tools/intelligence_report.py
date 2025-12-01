import json
import math
from datetime import datetime
from agent.atlas_agent import AtlasAgent
from agent.tools.history_manager import get_history as load_orbit_history
from agent.tools.news_history_manager import load_history as load_news_history
from agent.tools.correlation_engine import extract_claims_groq, correlate_claims_with_orbit
from groq import Groq


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def distance(a, b):
    return math.sqrt(
        (a[0] - b[0]) ** 2 +
        (a[1] - b[1]) ** 2 +
        (a[2] - b[2]) ** 2
    )


def compute_orbit_drift(latest, previous):
    """Compute numerical differences between two orbit snapshots."""
    if previous is None:
        return {}

    drift = {}
    keys = ["eccentricity", "inclination_deg", "perihelion_dist", "semi_major_axis_au"]

    for k in keys:
        if k in latest and k in previous:
            drift[k] = latest[k] - previous[k]

    # position drift
    if all(k in latest for k in ["X", "Y", "Z"]) and all(k in previous for k in ["X", "Y", "Z"]):
        drift["delta_position"] = distance(
            (latest["X"], latest["Y"], latest["Z"]),
            (previous["X"], previous["Y"], previous["Z"])
        )

    return drift


# ---------------------------------------------------------
# Core Report Builder
# ---------------------------------------------------------

def build_structured_report():
    """
    Creates the raw JSON dataset for the daily intelligence report.
    Includes:
    - orbit
    - drift
    - distances
    - news
    - claims extracted via Groq
    - correlation results via correlation_engine
    """
    agent = AtlasAgent()
    raw_json = agent.run()
    parsed = json.loads(raw_json)
    latest = parsed["orbit_elements"]

    # Orbit history for drift computation
    history = load_orbit_history()
    previous = history[-1]["elements"] if history else None
    drift = compute_orbit_drift(latest, previous)

    # Distances
    sun_distance = math.sqrt(latest["X"]**2 + latest["Y"]**2 + latest["Z"]**2)
    earth_distance = math.sqrt((latest["X"] - 1)**2 + latest["Y"]**2 + latest["Z"]**2)

    # News history + claims
    news_hist = load_news_history()

    all_articles = []
    if news_hist:
        for day in news_hist:
            for article in day["articles"]:
                all_articles.append({
                    "title": article["title"],
                    "content": article["content"],
                })

    claims = extract_claims_groq(all_articles)
    correlation_results = correlate_claims_with_orbit(claims, parsed, history)

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "orbit": latest,
        "drift": drift,
        "sun_distance_au": sun_distance,
        "earth_distance_au": earth_distance,
        "news_history": news_hist,
        "claims": claims,
        "correlation": correlation_results
    }


# ---------------------------------------------------------
# Natural Language Report from Groq
# ---------------------------------------------------------

def generate_natural_report(structured_data):
    client = Groq()

    prompt = f"""
You are ATLAS Guardian, an astronomy intelligence system.

Summarize the following JSON into a clear,
NASA/JPL-style daily intelligence report about interstellar object 3I/ATLAS.

JSON:
{json.dumps(structured_data, indent=2)}

Your output MUST include:
1. Orbit summary
2. Numerical drift analysis
3. Distances (Sun & Earth)
4. Summary of new news events
5. Extracted claims + correlation verdicts
6. Anomaly rating (0 to 10)
7. Final overall assessment

Avoid unnecessary speculation. Be scientific and concise.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message["content"]


# ---------------------------------------------------------
# Public API
# ---------------------------------------------------------

def generate_daily_report():
    structured = build_structured_report()
    text_summary = generate_natural_report(structured)

    return {
        "structured": structured,
        "summary": text_summary
    }
