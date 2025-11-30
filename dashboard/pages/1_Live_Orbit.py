import streamlit as st
from agent.atlas_agent import AtlasAgent
import json

st.title("🛰️ Live Orbit Dashboard")

agent = AtlasAgent()
report = json.loads(agent.run())

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
