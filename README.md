# ATLAS Guardian (scaffold)

This repository is a scaffold for the ATLAS Agent pipeline: agent tools -> analytics -> reports -> dashboard.

Structure

- `agent/` - orchestrator, tools and memory (vector DB) interfaces
  - `atlas_agent.py` - top-level pipeline orchestrator
  - `tools/` - tool stubs (`jpl_horizons.py`, `mpc_fetcher.py`)
  - `memory/` - vector DB placeholder (`vector_db.py`)
- `analytics/` - orbit analysis and anomaly detection logic
- `reports/` - report generation
- `dashboard/` - Streamlit dashboard scaffold
- `main.py` - CLI runner
- `requirements.txt` - minimal dependencies

Quickstart (Windows PowerShell)

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the dashboard:

```powershell
streamlit run dashboard/app.py
```

Run the CLI for a single object:

```powershell
python main.py 2025-AB
```

Next steps

- Replace the JPL/MPC stubs with real API calls or `astroquery`
- Integrate a vector DB (Pinecone / Supabase) in `agent/memory/vector_db.py`
- Add unit tests for `analytics/` functions
- Add CI and linting

