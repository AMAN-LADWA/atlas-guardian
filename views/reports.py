import streamlit as st
from agent.tools.correlation_engine import run_correlation_analysis

def show_reports():
    st.title("📡 Correlation Engine — ATLAS Guardian")
    if st.button("Run Analysis"):
        with st.spinner("Processing news & orbital data..."):
            report = run_correlation_analysis()
        st.markdown(report)
