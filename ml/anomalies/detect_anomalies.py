"""
InsightBI AI — ML Anomaly Detection (ml/anomalies/detect_anomalies.py)
Isolation Forest anomaly detection engine identifying sales spikes, drops, and unusual transaction patterns.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class AnomalyDetector:
    def __init__(self, contamination: float = 0.03):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.model_path = os.path.join(MODEL_DIR, "anomaly_detector.pkl")

    def detect(self, df_sales: pd.DataFrame) -> pd.DataFrame:
        if df_sales.empty:
            return pd.DataFrame()

        df = df_sales.copy()
        if "date" not in df.columns and "date_id" in df.columns:
            df["date"] = pd.to_datetime(df["date_id"].astype(str), format="%Y%m%d", errors="coerce")

        daily = df.groupby(["date", "date_id"]).agg(
            total_revenue=("revenue", "sum"),
            total_orders=("order_id", "nunique"),
            total_profit=("profit", "sum")
        ).reset_index()

        if len(daily) < 10:
            return pd.DataFrame()

        features = daily[["total_revenue", "total_orders", "total_profit"]]
        preds = self.model.fit_predict(features)
        scores = self.model.decision_function(features)

        daily["is_anomaly"] = (preds == -1)
        daily["anomaly_score"] = np.round(scores, 4)

        mean_rev = daily["total_revenue"].mean()
        std_rev = daily["total_revenue"].std()

        anomalies = daily[daily["is_anomaly"]].copy()

        results = []
        for _, row in anomalies.iterrows():
            rev = float(row["total_revenue"])
            z_score = (rev - mean_rev) / (std_rev + 1e-6)

            if abs(z_score) > 2.5:
                severity = "High"
            elif abs(z_score) > 1.5:
                severity = "Medium"
            else:
                severity = "Low"

            if rev > mean_rev:
                explanation = f"Revenue spike detected: ${rev:,.2f} is {z_score:.1f} standard deviations above historical mean (${mean_rev:,.2f})."
            else:
                explanation = f"Revenue dip detected: ${rev:,.2f} is {abs(z_score):.1f} standard deviations below historical mean (${mean_rev:,.2f})."

            results.append({
                "date_id": int(row["date_id"]),
                "metric": "Daily Revenue",
                "actual_value": round(rev, 2),
                "expected_value": round(float(mean_rev), 2),
                "anomaly_score": float(row["anomaly_score"]),
                "severity": severity,
                "explanation": explanation
            })

        joblib.dump(self.model, self.model_path)
        return pd.DataFrame(results)

def detect_sales_anomalies(df_sales: pd.DataFrame) -> pd.DataFrame:
    detector = AnomalyDetector()
    return detector.detect(df_sales)
