"""
InsightBI AI — ML Pipeline CLI Execution Script
Run with: python scripts/run_ml_pipeline.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml.pipeline import run_ml_pipeline

def main():
    print("🤖 Executing InsightBI AI Machine Learning Pipeline...")
    res = run_ml_pipeline()

    print("\n📊 MACHINE LEARNING PIPELINE SUMMARY:")
    print("-" * 50)
    print(f"90-Day Forecast Predictions Generated: {res.get('forecast_count', 0):,}")
    print(f"Customer RFM Segments Computed:       {res.get('segments_count', 0):,}")
    print(f"Revenue Anomalies Detected:           {res.get('anomalies_count', 0):,}")
    print(f"Forecasting Model Metrics (MAE/MAPE): {res.get('forecast_metrics', {})}")
    print("-" * 50)
    print("\n✅ Machine Learning Engine Execution Finished!")

if __name__ == "__main__":
    main()
