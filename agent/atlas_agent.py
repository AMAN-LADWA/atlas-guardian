from agent.tools.jpl_horizons import get_orbit_elements
from analytics.orbit_analysis import classify_orbit, days_to_perihelion

import json
import datetime
import re

class AtlasAgent:

    def __init__(self, memory=None):
        self.memory = memory

    def fetch_orbit(self):
        raw = get_orbit_elements()
        return raw

    def parse_orbit(self, raw_text):
        """
        Extract key orbital elements from the JPL Horizons output
        for ATLAS (C/2025 N1). We only look at the header block
        *before* the $$SOE ephemeris table.
        """

        # Only use the part before the ephemeris table
        header = raw_text.split("$$SOE")[0]
        patterns = {
            "epoch_jd":          r"EPOCH=\s*([0-9\.\+Ee\-]+)",
            "eccentricity":      r"EC=\s*([0-9\.\+Ee\-]+)",
            "perihelion_dist":   r"QR=\s*([0-9\.\+Ee\-]+)",
            "inclination_deg":   r"IN=\s*([0-9\.\+Ee\-]+)",
            "ascending_node_deg":r"OM=\s*([0-9\.\+Ee\-]+)",
            "arg_perihelion_deg":r"\bW=\s*([0-9\.\+Ee\-]+)",
            "tp_jd":             r"TP=\s*([0-9\.\+Ee\-]+)",
            "semi_major_axis_au":r"\bA=\s*([0-9\.\+Ee\-]+)",
            "mean_anomaly_deg":  r"MA=\s*([0-9\.\+Ee\-]+)",
        }
        xyz_pattern = (
            r"X=\s*([\-0-9.E\+]+)\s+"
            r"Y=\s*([\-0-9.E\+]+)\s+"
            r"Z=\s*([\-0-9.E\+]+)"
            )

        elements = {}

        for key, pattern in patterns.items():
            match = re.search(pattern, header)
            if match:
                # store as float; you can keep as string if you prefer
                try:
                    elements[key] = float(match.group(1))
                except ValueError:
                    elements[key] = match.group(1)
        # Extract heliocentric XYZ
        match = re.search(xyz_pattern, header)
        if match_xyz:
            for axis, idx in zip(("X", "Y", "Z"), (1, 2, 3)):
                val = match_xyz.group(idx)
                try:
                    elements[axis] = float(val)
                except ValueError:
                    elements[axis] = val

        return elements

    def generate_report(self, elements):
        now = datetime.datetime.utcnow()

        classification = classify_orbit(elements)
        dt_peri = days_to_perihelion(elements)

        report = {
            "timestamp": now.isoformat(),
            "object": "3I/ATLAS (C/2025 N1)",
            "orbit_elements": elements,
            "analysis": {
                "classification": classification,
                "days_to_perihelion": dt_peri
            },
        }

        return json.dumps(report, indent=4)

    def run(self):
        raw = self.fetch_orbit()
        parsed = self.parse_orbit(raw)
        report = self.generate_report(parsed)
        return report
