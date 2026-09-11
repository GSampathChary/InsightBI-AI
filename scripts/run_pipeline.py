"""
InsightBI AI — ETL Pipeline CLI Execution Script
Run with: python scripts/run_pipeline.py
"""

import sys
import os
import json

# Ensure project root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from etl.pipeline import run_etl_pipeline

def main():
    print("🚀 Executing InsightBI AI Production ETL Pipeline...")
    results = run_etl_pipeline()

    print("\n📊 DATA QUALITY REPORT SUMMARY:")
    print("-" * 50)
    qr = results["quality_report"]
    print(f"Total Rows Processed: {qr['total_rows_processed']:,}")
    print(f"Valid Rows:           {qr['valid_rows']:,}")
    print(f"Invalid Rows:         {qr['invalid_rows']:,}")
    print(f"Duplicates Removed:   {qr['duplicates_removed']:,}")
    print(f"Nulls Detected:       {qr['nulls_detected']:,}")
    print(f"Overall Quality Score:{qr['quality_score_percent']}%")
    print("-" * 50)
    print("Details:", json.dumps(qr["details"], indent=2))
    print("\n✅ ETL Pipeline Completed Successfully!")

if __name__ == "__main__":
    main()
