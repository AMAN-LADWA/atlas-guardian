import streamlit as st
import json
from agent.atlas_agent import AtlasAgent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tools.agent_tools import (
    fetch_orbit_tool,
    compare_orbits_tool,
    detect_anomalies_tool,
)
from agent.tools.history_manager import (
    store_snapshot,
    get_last_snapshot,
    get_history,
)

st.title("🛠 Agent Tools")

# Fetch new orbit
st.subheader("Fetch Latest Orbit")
if st.button("Fetch Now"):
    data = fetch_orbit_tool()
    st.json(data)

# Store snapshot
st.subheader("Store Snapshot")
if st.button("Save Current Orbit"):
    data = fetch_orbit_tool()
    store_snapshot(data)
    st.success("Snapshot saved!")

# Compare with last
st.subheader("Compare With Previous")
if st.button("Compare"):
    last = get_last_snapshot()
    if last is None:
        st.warning("No previous snapshot stored.")
    else:
        current = fetch_orbit_tool()
        diff = compare_orbits_tool(last, current)
        st.json(diff)

# Anomaly detection
st.subheader("Detect Anomalies")
if st.button("Check"):
    last = get_last_snapshot()
    if last is None:
        st.warning("Store at least one snapshot.")
    else:
        current = fetch_orbit_tool()
        diff = compare_orbits_tool(last, current)
        anomalies = detect_anomalies_tool(diff)
        st.json(anomalies)
