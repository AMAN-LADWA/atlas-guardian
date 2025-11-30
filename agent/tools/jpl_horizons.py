import requests
import datetime

BASE_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
TARGET_DES = "C/2025 N1"   # 3I/ATLAS official designation


def _call_horizons(extra_params: dict):
    """
    Low-level JPL Horizons API caller.
    Uses DES=C/2025 N1; which is 3I/ATLAS.
    """
    params = {
        "format": "json",
        "COMMAND": f"'DES={TARGET_DES};'",
    }
    params.update(extra_params)

    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    data = resp.json()

    # Basic sanity check
    if "result" in data and "No matches found" in data["result"]:
        raise ValueError("Horizons: no matches found for 3I/ATLAS (C/2025 N1)")

    return data


def get_orbit_elements() -> str:
    """
    Get orbital elements block as text (contains EC, QR, IN, OM, W, etc.).
    Your AtlasAgent.parse_orbit() will parse this.
    """
    data = _call_horizons({
        "OBJ_DATA": "YES",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "ELEMENTS",
        "OUT_UNITS": "AU-D",
        "ELEM_LABELS": "YES",
        "REF_PLANE": "ECLIPTIC",
    })
    return data.get("result", "")


def get_ephemeris(days: int = 5) -> str:
    """
    Simple RA/Dec ephemeris for the next `days` days from Earth center.
    """
    today = datetime.date.today()
    stop = today + datetime.timedelta(days=days)

    data = _call_horizons({
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "'500@399'",          # geocentric
        "START_TIME": today.isoformat(),
        "STOP_TIME": stop.isoformat(),
        "STEP_SIZE": "1 d",
        "QUANTITIES": "1,20",           # RA/Dec, range, range-rate
    })
    return data.get("result", "")
