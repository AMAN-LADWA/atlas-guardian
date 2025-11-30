import streamlit as st

st.set_page_config(
    page_title="ATLAS Guardian – Mission Control",
    layout="wide",
)

st.title("🛰️ ATLAS Guardian – Mission Control")
st.write(
    "Welcome to the ATLAS Guardian dashboard. "
    "Use the left sidebar to navigate between system modules."
)

st.markdown("""
### Modules
- **Live Orbit** – Real-time JPL/Horizons orbit data  
- **Agent Tools** – Snapshot, compare, anomaly detection  
- **AI Chat Agent** – Ask the ATLAS Guardian anything  
- **History & Graphs** – Drift, timelines, scientific charts  
""")
