import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.tools.daily_reporter import generate_daily_report

st.title("📰 Daily ATLAS Intelligence Report")

if st.button("Generate Report"):
    with st.spinner("Compiling data and querying Groq LLM..."):
        report = generate_daily_report()
    st.markdown(report)
