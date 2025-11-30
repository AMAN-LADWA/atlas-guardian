"""
Streamlit dashboard scaffold for ATLAS reports.
This app imports the AtlasAgent and runs the pipeline for a user-specified object id.
"""
import streamlit as st
from agent.atlas_agent import AtlasAgent

st.set_page_config(page_title="ATLAS Guardian Dashboard")

st.title("ATLAS Guardian")

agent = AtlasAgent()

object_id = st.text_input("Object ID", value="2025-AB")
if st.button("Run pipeline"):
    with st.spinner("Running pipeline..."):
        report = agent.run_pipeline(object_id)

    st.subheader("Human Summary")
    st.write(report.get("human_summary"))

    st.subheader("Scientific Summary")
    st.write(report.get("scientific_summary"))

    st.metric("Anomaly Score", f"{report.get('anomaly_score', 0.0):.2f}")

    st.subheader("Full Report")
    st.json(report)

st.markdown("\n\n---\n\nThis dashboard is a scaffold. Replace stubs with real integrations for production.")
