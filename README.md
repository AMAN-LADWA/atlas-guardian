# 🛰️ ATLAS GUARDIAN  
### **Real-Time Interstellar Monitoring & AI-Driven Analysis**  
A mission-style dashboard and autonomous AI agent tracking the interstellar object **3I/ATLAS (C/2025 N1)** using real NASA/JPL data, real-world news signals, and Groq-powered analysis.

---

## 🌌 Overview

**ATLAS Guardian** is a real-time monitoring system that:

- Fetches **true orbital data** from NASA JPL Horizons  
- Stores and analyzes **historical orbital drift**  
- Tracks **news, RSS feeds, and scientific articles**  
- Extracts **claims and speculation** using Groq LLM  
- Correlates online claims with **actual orbital physics**  
- Generates **daily intelligence briefs**  
- (Upcoming) Posts automatic updates to **X/Twitter**  
- (Upcoming) Displays a **3D cinematic solar-system visualization**

It is designed as a **NASA/JPL-style console**, combining:
- Astrodynamics  
- Agentic AI  
- Autonomous monitoring  
- Clean mission-control UI  

Built entirely for free using:
- Streamlit Cloud  
- Groq API  
- GitHub Actions  
- NASA Horizons  

---

# 🚀 Current Status (Working Now)
## https://atlas-guardian-3j9ef7jjxbtuwyfzamjama.streamlit.app/
### ✅ **1. Modular Restructured Architecture**
App rebuilt into a clean structure:
app.py (router + navbar)
views/ (UI pages)
agent/ (data engines + AI tools)
automation/ (future daily jobs)
data/ (history storage)

Ready for expansion.

---

### ✅ **2. Real-Time Orbit Retrieval**
Connects to NASA JPL Horizons and fetches:
- Eccentricity  
- Inclination  
- Semi-major axis  
- Perihelion distance  
- Hyperbolic classification  
- Cartesian XYZ position  
- Non-gravitational force parameters  

---

### ✅ **3. Historical Drift Tracking**
Each orbit snapshot is stored locally:
data/history.json


Allows:
- Drift analysis  
- Timeline reconstruction  
- Change detection  
- Trend graphs (WIP)

---

### ✅ **4. News + RSS Aggregation**
Legally fetches public articles from:
- Space.com  
- NASA RSS  
- SciTechDaily  
- Phys.org  
- Custom feeds  

---

### ✅ **5. Groq-Powered Correlation Engine**
The system now has a full working module:

**Correlation Engine**
- Extracts structured claims from news  
- Evaluates each claim using real orbital data  
- Detects support / contradiction / no correlation  
- Considers:
  - Orbital drift  
  - Non-gravitational parameters  
  - Perihelion timing changes  
  - Hyperbolic behavior  
- Produces a clean Markdown report  

This is the “intelligence analysis brain” of ATLAS Guardian.

---

# 🔭 In Progress / Coming Next

These are the **planned features** that will turn ATLAS Guardian into a full-scale autonomous observatory system.

### 🔷 **1. Hero Page — 3D Orbit Visual (High Priority)**
A cinematic Plotly-3D rendering of:
- Sun  
- Earth  
- Moon  
- ATLAS position  
- Hyperbolic orbit curve  
- Starfield background  
- Real-time XYZ coordinates  
- Side mission telemetry  

This will become the **main landing page**.

---

### 🔷 **2. Top Navigation Bar (NASA/JPL Mission Console Style)**
Removing Streamlit sidebar, replacing it with:
ATLAS GUARDIAN | Hero View | Orbit Data | Tools | History | Reports

Already supported by the new router.

---

### 🔷 **3. Autonomous X/Twitter Bot**
Using GitHub Actions:
- Runs daily  
- Fetches orbit  
- Checks for real drift  
- Summarizes news  
- Runs correlation engine  
- Posts automated intelligence brief  
- Only posts if there is real orbital change  

This will be fully **free**.

---

### 🔷 **4. Full Daily Intelligence Brief (Online)**
A page to view the full expanded agent-generated report:
- Orbit status  
- Drift timeline  
- Correlation findings  
- News summary  
- Risk assessment  
- “Today’s anomaly index”

---

### 🔷 **5. Auto-Update History + Daily Cron Jobs**
GitHub Actions will:
- Pull repository  
- Run orbit fetcher  
- Append to history.json  
- Commit updated data  
- Run analytics  
- Update X bot

This creates a fully autonomous **long-term monitoring pipeline**.

---

### 🔷 **6. Advanced Visual Analytics**
Using orbit history to show:
- Eccentricity vs time  
- Inclination drift  
- NGF (A1/A2/A3) behavior  
- Perihelion delta  
- Interactive correlation graphs  


---

# 🛠️ Tech Stack

### **Backend**
- Python  
- Groq LLM (Llama 3.3 70B)  
- NASA JPL Horizons API  
- Feedparser (RSS)

### **Frontend**
- Streamlit  
- Plotly (3D visualizations)  
- Custom HTML/CSS injector

### **Automation**
- GitHub Actions  
- X/Twitter API (planned)

### **Storage**
- JSON (history timeline)  
- GitHub commits (auto)  

---

# 🔥 Roadmap Summary

### **DONE**
✔ Architectural restructuring  
✔ Real-time orbit fetcher  
✔ History tracking  
✔ News collector  
✔ RSS ingest  
✔ Correlation engine  
✔ Streamlit Cloud deploy

### **NEXT**
🔜 Hero View (3D visualization)  
🔜 Navbar UI overhaul  
🔜 Daily reporter  
🔜 Autonomous X posting  
🔜 Graphs + analytics panel  

---

# 📸 Screenshots (Placeholders)

[Hero 3D View — Coming Soon]
[Orbit Data Panel]
[Correlation Engine Output]
[Historical Drift Graphs]


---

# 🧑‍🚀 Author  
Built by **Aman Ladwa**  
A real-time AI observatory project exploring the physics and public narrative of interstellar object **3I/ATLAS**.

---

# ⭐ Contributions  
Issues and pull requests welcome.  
Future upgrades will turn this into a fully autonomous interstellar monitoring system.
