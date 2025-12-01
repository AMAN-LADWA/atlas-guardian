import streamlit as st
import numpy as np
import json
import plotly.graph_objects as go

from agent.atlas_agent import AtlasAgent
from agent.tools.news_history_manager import load_history
from agent.tools.intelligence_report import generate_daily_report



# -------------------------------------------------------
# Utility functions
# -------------------------------------------------------

def generate_starfield(n_points=300):
    """Random starfield around the origin."""
    return (
        np.random.uniform(-5, 5, n_points),
        np.random.uniform(-5, 5, n_points),
        np.random.uniform(-5, 5, n_points),
    )


def generate_sphere(radius=1, detail=25):
    """Generate sphere mesh."""
    u = np.linspace(0, 2 * np.pi, detail)
    v = np.linspace(0, np.pi, detail)
    x = radius * np.outer(np.cos(u), np.sin(v))
    y = radius * np.outer(np.sin(u), np.sin(v))
    z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
    return x, y, z


def generate_orbit_path(start_xyz, direction=(1, 0.3, 0.2), length=2.0, steps=80):
    """Approx hyperbolic path for visual effect."""
    d = np.array(direction)
    d = d / np.linalg.norm(d)

    t = np.linspace(-length, length, steps)
    xs = start_xyz[0] + d[0] * t
    ys = start_xyz[1] + d[1] * t
    zs = start_xyz[2] + d[2] * t

    return xs, ys, zs


# -------------------------------------------------------
# HERO PAGE
# -------------------------------------------------------

def show_hero():
    st.title("🛰️ ATLAS Guardian — Real-Time 3D Orbit Visualization")

    # -------------------------------------------------------
    # 1. Fetch orbit using correct JSON-producing run()
    # -------------------------------------------------------
    agent = AtlasAgent()
    raw_json = agent.run()  # returns JSON string
    try:
        parsed = json.loads(raw_json)
    except json.JSONDecodeError:
        st.error("Could not decode ATLAS agent JSON output.")
        st.code(raw_json)
        return

    # parsed is already the orbit dict based on your atlas_agent.py
    orbit = parsed.get("orbit_elements", {})

    X = orbit.get("X")
    Y = orbit.get("Y")
    Z = orbit.get("Z")

    if X is None or Y is None or Z is None:
        st.error("ATLAS XYZ coordinates missing from agent output.")
        st.write("Parsed orbit:", orbit)
        return

    atlas_xyz = np.array([X, Y, Z])

    # -------------------------------------------------------
    # 2. Generate scene components
    # -------------------------------------------------------

    # starfield
    stars_x, stars_y, stars_z = generate_starfield()

    # Sun
    sun_x, sun_y, sun_z = generate_sphere(radius=0.25)

    # Earth (centered at ~1 AU on x axis)
    earth_radius = 0.10
    earth_x, earth_y, earth_z = generate_sphere(radius=earth_radius)

    # Moon (scaled up to be visually identifiable)
    moon_scale = 1
    moon_radius = 0.00257 * 50
    moon_x, moon_y, moon_z = generate_sphere(radius=0.03 * moon_scale)

    # Earth orbit (1 AU circle)
    theta = np.linspace(0, 2 * np.pi, 400)
    earth_orbit_x = np.cos(theta) * 1
    earth_orbit_y = np.sin(theta) * 1
    earth_orbit_z = np.zeros_like(theta)

    # Moon orbit scaled
    moon_orbit_x = 1 + moon_radius * np.cos(theta)
    moon_orbit_y = 0 + moon_radius * np.sin(theta)
    moon_orbit_z = np.zeros_like(theta)

    # ATLAS approximate hyperbolic path
    atlas_path_x, atlas_path_y, atlas_path_z = generate_orbit_path(atlas_xyz)

    # -------------------------------------------------------
    # 3. Build Plotly Figure
    # -------------------------------------------------------
    fig = go.Figure()

    # starfield
    fig.add_trace(go.Scatter3d(
        x=stars_x, y=stars_y, z=stars_z,
        mode="markers",
        marker=dict(size=1, color="white", opacity=0.8),
        name="Stars"
    ))

    # Sun
    fig.add_trace(go.Surface(
        x=sun_x, y=sun_y, z=sun_z,
        colorscale=[[0, "yellow"], [1, "gold"]],
        showscale=False,
        name="Sun"
    ))

    # Earth orbit
    fig.add_trace(go.Scatter3d(
        x=earth_orbit_x,
        y=earth_orbit_y,
        z=earth_orbit_z,
        mode="lines",
        line=dict(color="blue", width=2),
        name="Earth Orbit"
    ))

    # Earth
    fig.add_trace(go.Surface(
        x=earth_x + 1,
        y=earth_y,
        z=earth_z,
        colorscale=[[0, "blue"], [1, "lightblue"]],
        showscale=False,
        name="Earth"
    ))

    # Moon orbit
    fig.add_trace(go.Scatter3d(
        x=moon_orbit_x,
        y=moon_orbit_y,
        z=moon_orbit_z,
        mode="lines",
        line=dict(color="gray", width=1),
        name="Moon Orbit"
    ))

    # Moon (position at orbit angle 0)
    fig.add_trace(go.Surface(
        x=moon_x + 1 + moon_radius,
        y=moon_y,
        z=moon_z,
        colorscale=[[0, "gray"], [1, "white"]],
        showscale=False,
        name="Moon"
    ))

    # ATLAS position
    fig.add_trace(go.Scatter3d(
        x=[X], y=[Y], z=[Z],
        mode="markers",
        marker=dict(size=7, color="cyan"),
        name="3I/ATLAS"
    ))

    # ATLAS orbit line
    fig.add_trace(go.Scatter3d(
        x=atlas_path_x,
        y=atlas_path_y,
        z=atlas_path_z,
        mode="lines",
        line=dict(color="cyan", width=4),
        name="ATLAS Path"
    ))

    # -------------------------------------------------------
    # 4. Camera & Layout (auto-scale to include ATLAS)
    # -------------------------------------------------------

    max_range = max(abs(X), abs(Y), abs(Z), 1.5)

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-max_range, max_range]),
            yaxis=dict(visible=False, range=[-max_range, max_range]),
            zaxis=dict(visible=False, range=[-max_range, max_range]),
            bgcolor="black",
        ),
        paper_bgcolor="black",
        height=650,
        margin=dict(r=0, l=0, b=0, t=0),
        showlegend=False,
    )

    fig.update_layout(
        scene_camera=dict(eye=dict(x=2.2, y=1.4, z=1.5))
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------------
    # 5. News timeline
    # -------------------------------------------------------

    st.markdown("---")
    st.subheader("📰 ATLAS News Timeline")

    history = load_history()

    if not history:
        st.info("No ATLAS-related news articles stored yet.")
        return

    history_sorted = sorted(history, key=lambda x: x["date"], reverse=True)

    for entry in history_sorted:
        st.markdown(f"### {entry['date']}")
        for a in entry["articles"]:
            st.markdown(f"**{a['title']}**")
            st.markdown(f"[Read more]({a['url']})")
            st.caption(a["source"])
            st.markdown("---")
    st.markdown("---")

    st.subheader("📡 Daily Intelligence Report")

    try:
        rep = generate_daily_report()
        st.markdown(rep["summary"])
    except Exception as e:
        st.error("Could not generate AI report.")
        st.exception(e)
        return
        