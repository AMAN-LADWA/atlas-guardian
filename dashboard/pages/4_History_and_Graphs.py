import streamlit as st
import matplotlib.pyplot as plt
from agent.tools.history_manager import get_history

st.title("📈 Orbit History & Drift Analysis")

history = get_history()

if not history:
    st.info("History empty — save snapshots first.")
    st.stop()


def plot_field(field, label):
    timestamps = []
    values = []

    for entry in history:
        ts = entry["timestamp"]
        val = entry["orbit_elements"].get(field)
        if val is not None:
            timestamps.append(ts)
            values.append(val)

    fig, ax = plt.subplots()
    ax.plot(timestamps, values, marker="o")
    ax.set_title(label)
    ax.set_xlabel("Timestamp")
    ax.set_ylabel(label)
    ax.tick_params(axis="x", rotation=45)

    st.pyplot(fig)


st.subheader("Eccentricity Drift")
plot_field("eccentricity", "Eccentricity")

st.subheader("Inclination Drift")
plot_field("inclination_deg", "Inclination (deg)")

st.subheader("Semi-Major Axis Drift")
plot_field("semi_major_axis_au", "Semi-Major Axis (AU)")

st.subheader("Days to Perihelion Drift")
timestamps = [e["timestamp"] for e in history]
vals = [e["analysis"]["days_to_perihelion"] for e in history]

fig, ax = plt.subplots()
ax.plot(timestamps, vals, marker="o")
ax.set_title("Days to Perihelion")
ax.tick_params(axis="x", rotation=45)

st.pyplot(fig)
