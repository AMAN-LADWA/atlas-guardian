import streamlit as st
import json
from groq import Groq
import os
from agent.atlas_agent import AtlasAgent
from agent.tools.history_manager import get_history

st.title("🤖 ATLAS Guardian — AI Chat Agent")

agent = AtlasAgent()
report = json.loads(agent.run())

user_query = st.text_input("Ask a question about 3I/ATLAS:")

def get_llm_followup_answer(payload: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "LLM disabled — set GROQ_API_KEY."

    client = Groq(api_key=api_key)

    sys_prompt = (
        "You are ATLAS Guardian, an analytical interstellar intelligence system. "
        "Use the data and history to answer clearly, scientifically, and concisely."
    )

    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": payload},
        ],
    )

    return resp.choices[0].message.content.strip()

if st.button("Ask"):
    history = get_history()
    payload = json.dumps({
        "query": user_query,
        "current_orbit": report,
        "history": history[-10:],
    }, indent=2)

    answer = get_llm_followup_answer(payload)
    st.markdown("### 🧠 Agent Response")
    st.write(answer)
