"""
Daily report generator.
Produces a small dict containing scientific and human summaries and anomaly score.
"""
from typing import Dict, Any
import datetime
from analytics.anomaly_detection import score_anomaly


def make_scientific_summary(object_id: str, analytics: Dict[str, Any]) -> str:
    return f"Object {object_id}: SMA delta {analytics.get('sma_delta_km')}, ecc delta {analytics.get('ecc_delta')}"


def make_human_summary(scientific: str, anomaly_score: float) -> str:
    level = "LOW"
    if anomaly_score > 0.7:
        level = "HIGH"
    elif anomaly_score > 0.3:
        level = "MEDIUM"
    return f"{scientific}. Anomaly level: {level} ({anomaly_score:.2f})"


def write_daily_report(object_id: str, analytics: Dict[str, Any]) -> Dict[str, Any]:
    anomaly_score = score_anomaly(analytics)
    scientific = make_scientific_summary(object_id, analytics)
    human = make_human_summary(scientific, anomaly_score)
    report = {
        "object_id": object_id,
        "date": datetime.datetime.utcnow().isoformat(),
        "scientific_summary": scientific,
        "human_summary": human,
        "anomaly_score": anomaly_score,
        "analytics": analytics,
    }
    # TODO: persist report (DB, object store, vector DB)
    return report
