import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
