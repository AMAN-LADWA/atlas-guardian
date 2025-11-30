"""
Simple anomaly detection heuristics for the scaffold.
Replace with an ML model or statistical detector as needed.
"""
from typing import Dict, Any


def score_anomaly(analytics: Dict[str, Any]) -> float:
    """Compute a 0.0-1.0 anomaly score from analytics dict.

    Heuristic example:
    - normalize sma_delta_km by 10 km
    - normalize ecc_delta by a factor
    - combine and clamp
    """
    if not analytics:
        return 0.0

    score = 0.0
    sma = analytics.get("sma_delta_km", 0.0)
    ecc = analytics.get("ecc_delta", 0.0)

    score += min(abs(sma) / 10.0, 1.0)
    score += min(abs(ecc) * 10.0, 1.0)

    # If magnitude change is extreme, bump score
    mag = analytics.get("magnitude", {})
    mag_delta = mag.get("delta", 0.0) if isinstance(mag, dict) else 0.0
    if abs(mag_delta) > 0.5:
        score += 0.5

    # normalize to [0,1]
    return max(0.0, min(score / 2.0, 1.0))
