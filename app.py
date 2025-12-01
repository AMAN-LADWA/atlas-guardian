import os
import sys
import streamlit as st

# Ensure project root is in sys.path so `agent.*` imports work from views
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(page_title="ATLAS Guardian", layout="wide")

# Top navigation HTML/CSS
NAV_CSS = """
<style>
:root{--nav-bg:#0b3d91;--nav-fg:#ffffff}
.topnav{background:var(--nav-bg);padding:10px 16px;color:var(--nav-fg);display:flex;align-items:center;gap:12px}
.topnav a{color:var(--nav-fg);text-decoration:none;padding:6px 10px;border-radius:6px}
.topnav a:hover{background:rgba(255,255,255,0.08)}
.brand{font-weight:700;margin-right:8px}
</style>
<div class="topnav">
  <div class="brand">🛰️ ATLAS Guardian</div>
  <div class="links">
    <a href="?hero">Home</a>
    <a href="?orbit">Live Orbit</a>
    <a href="?tools">Agent Tools</a>
    <a href="?history">History & Graphs</a>
    <a href="?reports">Reports</a>
  </div>
</div>
"""

st.markdown(NAV_CSS, unsafe_allow_html=True)

# Simple routing using query params: ?hero, ?orbit, ?tools, ?history, ?reports
# use `st.query_params` (stable API replacing experimental_get_query_params)
params = st.query_params

def _pick_view(params):
    if "orbit" in params:
        return "orbit"
    if "tools" in params:
        return "tools"
    if "history" in params:
        return "history"
    if "reports" in params:
        return "reports"
    # default or explicit hero
    return "hero"

view = _pick_view(params)

# Import views lazily (after sys.path setup)
from views import hero as view_hero
from views import orbit as view_orbit
from views import tools as view_tools
from views import history as view_history
from views import reports as view_reports

if view == "hero":
    view_hero.show_hero()
elif view == "orbit":
    view_orbit.show_orbit()
elif view == "tools":
    view_tools.show_tools()
elif view == "history":
    view_history.show_history()
elif view == "reports":
    view_reports.show_reports()
else:
    view_hero.show_hero()
