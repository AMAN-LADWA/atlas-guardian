import json
from datetime import datetime
from agent.atlas_agent import AtlasAgent


def fetch_orbit_tool():
    agent = AtlasAgent()
    raw_report = agent.run()
    return json.loads(raw_report)


def compare_orbits_tool(old: dict, new: dict):
    old_el = old.get("orbit_elements", {})
    new_el = new.get("orbit_elements", {})

    diff = {}
    for key in new_el:
        if key in old_el:
            try:
                diff[key] = new_el[key] - old_el[key]
            except:
                pass

    return diff


def detect_anomalies_tool(diff: dict):
    anomalies = {}

    thresholds = {
        "eccentricity": 0.001,
        "inclination_deg": 0.01,
        "ascending_node_deg": 0.01,
        "arg_perihelion_deg": 0.01,
        "semi_major_axis_au": 0.0001,
        "tp_jd": 0.001,
    }

    for key, threshold in thresholds.items():
        val = diff.get(key)
        if val is None:
            continue

        if abs(val) > threshold:
            anomalies[key] = val

    return anomalies
