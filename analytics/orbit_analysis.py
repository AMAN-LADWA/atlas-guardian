# analytics/orbit_analysis.py
from datetime import datetime
from astropy.time import Time

def classify_orbit(elements: dict) -> dict:
    e = elements.get("eccentricity")
    inc = elements.get("inclination_deg")

    orbit_type = "unknown"
    if e is not None:
        if e < 1:
            orbit_type = "elliptic (bound)"
        elif abs(e - 1.0) < 0.01:
            orbit_type = "parabolic"
        else:
            orbit_type = "hyperbolic (interstellar)"

    retrograde = None
    if inc is not None:
        retrograde = inc > 90

    return {
        "orbit_type": orbit_type,
        "retrograde": retrograde,
    }


def days_to_perihelion(elements: dict) -> float | None:
    tp_jd = elements.get("tp_jd")
    if tp_jd is None:
        return None

    now = Time(datetime.utcnow()).jd
    return tp_jd - now
