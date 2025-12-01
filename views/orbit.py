import streamlit as st
import json
from agent.atlas_agent import AtlasAgent


def show_orbit():
    st.title("🛰️ Live Orbit")

    st.markdown("Loading latest orbit data from AtlasAgent...")
    try:
        agent = AtlasAgent()
        raw = agent.run()
        report = json.loads(raw)
    except Exception as e:
        st.error(f"Failed to fetch orbit: {e}")
        return

    orbit = report.get("orbit_elements", {})
    analysis = report.get("analysis", {})

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orbit Elements")
        st.json(orbit)

    with col2:
        st.subheader("Analysis")
        st.json(analysis)

    st.caption(f"Timestamp: {report.get('timestamp')}")

    # Placeholder: load 3D orbit viewer when available
    st.markdown("---")
    st.markdown("**3D Orbit Viewer** — (placeholder) — will load when capabilities available.")
