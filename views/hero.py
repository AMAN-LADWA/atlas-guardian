import streamlit as st

def show_hero():
    st.title("🛰️ ATLAS Guardian – Mission Control")
    st.write(
        "Welcome to the ATLAS Guardian dashboard. Use the top navigation to switch modules, or the query params (e.g. ?orbit) to deep-link."
    )

    st.markdown("""
- **Live Orbit** — Real-time JPL/Horizons orbit data
- **Agent Tools** — Snapshot, compare, anomaly detection
- **AI Chat Agent** — Ask the ATLAS Guardian anything
- **History & Graphs** — Drift, timelines, scientific charts
- **Reports** — Daily intel and report generation
""")

    st.info("Default landing view. Click a top nav link to continue.")
