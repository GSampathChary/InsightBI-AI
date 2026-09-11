"""
InsightBI AI — ML Customer Segmentation (ml/segmentation/cluster_customers.py)
Computes Recency, Frequency, Monetary (RFM) metrics, applies StandardScaler & KMeans clustering,
and maps customers into RFM segments (VIP, Champions, Loyal, At-Risk, Lost).
"""

import os
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
os.makedirs(MODEL_DIR, exist_ok=True)

class CustomerSegmenter:
    def __init__(self, n_clusters: int = 4):
        self.n_clusters = n_clusters
        self.scaler_path = os.path.join(MODEL_DIR, "customer_scaler.pkl")
        self.kmeans_path = os.path.join(MODEL_DIR, "customer_kmeans.pkl")
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    def compute_rfm_and_cluster(self, df_sales: pd.DataFrame, df_customers: pd.DataFrame = None) -> pd.DataFrame:
        if df_sales.empty:
            return pd.DataFrame()

        df = df_sales.copy()
        if "date" not in df.columns and "date_id" in df.columns:
            df["date"] = pd.to_datetime(df["date_id"].astype(str), format="%Y%m%d", errors="coerce")

        max_date = df["date"].max()

        # Compute RFM
        rfm = df.groupby("customer_id").agg(
            last_date=("date", "max"),
            frequency_count=("order_id", "nunique"),
            monetary_value=("revenue", "sum")
        ).reset_index()

        rfm["recency_days"] = (max_date - rfm["last_date"]).dt.days
        rfm["monetary_value"] = rfm["monetary_value"].round(2)

        # Quintile scoring (1 to 5)
        rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first", ascending=False), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["f_score"] = pd.qcut(rfm["frequency_count"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["m_score"] = pd.qcut(rfm["monetary_value"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
        rfm["rfm_score"] = rfm["r_score"] * 100 + rfm["f_score"] * 10 + rfm["m_score"]

        # Scale features for K-Means
        rfm_features = rfm[["recency_days", "frequency_count", "monetary_value"]]
        scaled_features = self.scaler.fit_transform(rfm_features)

        # Fit K-Means
        clusters = self.kmeans.fit_predict(scaled_features)
        rfm["cluster_id"] = clusters

        # Map cluster centers to human business segments
        cluster_centers = pd.DataFrame(
            self.scaler.inverse_transform(self.kmeans.cluster_centers_),
            columns=["recency_days", "frequency_count", "monetary_value"]
        )
        cluster_centers["cluster_id"] = range(self.n_clusters)
        cluster_centers = cluster_centers.sort_values("monetary_value", ascending=False).reset_index(drop=True)

        segment_names = ["VIP / Champions", "Loyal Customers", "Potential Loyalists", "At-Risk / Lost"]
        cluster_map = {}
        for idx, row in cluster_centers.iterrows():
            cluster_map[int(row["cluster_id"])] = segment_names[min(idx, len(segment_names) - 1)]

        rfm["rfm_segment"] = rfm["cluster_id"].map(cluster_map)

        # Save artifacts
        joblib.dump(self.scaler, self.scaler_path)
        joblib.dump(self.kmeans, self.kmeans_path)

        cols = ["customer_id", "recency_days", "frequency_count", "monetary_value", "r_score", "f_score", "m_score", "rfm_score", "rfm_segment", "cluster_id"]
        return rfm[cols]

def train_customer_segmentation(df_sales: pd.DataFrame, df_customers: pd.DataFrame = None) -> pd.DataFrame:
    segmenter = CustomerSegmenter()
    return segmenter.compute_rfm_and_cluster(df_sales, df_customers)
