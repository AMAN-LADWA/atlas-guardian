import streamlit as st
from agent.tools.daily_reporter import generate_daily_report

st.title("📰 Daily ATLAS Intelligence Report")

if st.button("Generate Report"):
    with st.spinner("Compiling data and querying Groq LLM..."):
        report = generate_daily_report()
    st.markdown(report)
