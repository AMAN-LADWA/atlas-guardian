import os
import json
from groq import Groq
from agent.tools.news_collector import collect_all_articles
from agent.tools.history_manager import get_history
from agent.atlas_agent import AtlasAgent


def extract_claims_groq(articles):
    """
    Uses Groq to extract structured claims from all news articles.
    Output format:
    {
        "claims": [
            { "type": "...", "summary": "...", "strength": "low/medium/high" },
            ...
        ]
    }
    """
    api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

    article_text = "\n\n".join(
        [f"Title: {a['title']}\nContent: {a['content']}" for a in articles]
    )

    system_prompt = (
        "You are an AI assistant extracting scientific claims from news.\n"
        "Convert the text into a JSON list of claims.\n"
        "Each claim must have: type, summary, strength.\n"
        "Types may include: brightness, acceleration, non_gravitational, orbit_change,"
        "controlled_emission, speculation, etc.\n"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": article_text},
        ],
    )

    try:
        extracted = json.loads(response.choices[0].message.content)
        return extracted.get("claims", [])
    except:
        return []


def correlate_claims_with_orbit(claims, orbit, history):
    """
    Compares extracted claims with real orbital data + drift.
    Produces a structured evaluation.
    """

    # Determine drift from history
    drift_signals = {}

    if len(history) >= 2:
        latest = history[-1]["orbit_elements"]
        prev = history[-2]["orbit_elements"]

        for key in ["eccentricity", "inclination_deg", "semi_major_axis_au", "perihelion_dist"]:
            if key in latest and key in prev:
                delta = latest[key] - prev[key]
                if abs(delta) > 0.0001:
                    drift_signals[key] = delta

    report = []

    for c in claims:
        ctype = c.get("type", "").lower()
        summary = c.get("summary", "")
        strength = c.get("strength", "unknown")

        correlation = "no_match"
        explanation = "No relevant change detected in orbital parameters."

        # BRIGHTNESS / LUMINOSITY
        if "bright" in ctype or "lumin" in ctype:
            if drift_signals:
                correlation = "possible_match"
                explanation = f"Detected orbital drift: {drift_signals}"
            else:
                correlation = "no_match"

        # NON-GRAVITATIONAL ACCELERATION
        if "non" in ctype or "accel" in ctype:
            a1 = orbit["orbit_elements"].get("a1", None)
            if a1 and abs(a1) > 1e-8:
                correlation = "possible_match"
                explanation = f"Non-gravitational parameter A1 present: {a1}"

        # CONTROLLED EMISSION THEORY
        if "control" in ctype:
            if drift_signals:
                correlation = "unlikely_but_not_zero"
                explanation = f"Small drift could be natural; cannot support artificial control."
            else:
                correlation = "unsupported"

        report.append({
            "claim": summary,
            "type": ctype,
            "strength": strength,
            "correlation": correlation,
            "explanation": explanation,
        })

    return report


def run_correlation_analysis():
    """
    High-level function:
    - Fetches data
    - Extracts claims
    - Correlates with orbit
    - Returns formatted text for UI
    """

    agent = AtlasAgent()
    orbit = json.loads(agent.run())
    history = get_history()
    articles = collect_all_articles()

    claims = extract_claims_groq(articles)
    correlations = correlate_claims_with_orbit(claims, orbit, history)

    final_report = "### 🧠 Correlation Analysis\n\n"

    if not correlations:
        return final_report + "No claims found in news articles today."

    for c in correlations:
        final_report += f"""
**Claim:** {c['claim']}
- **Type:** {c['type']}
- **Strength in news:** {c['strength']}
- **Correlation:** {c['correlation']}
- **Explanation:** {c['explanation']}

---
"""

    return final_report
