"""
InsightBI AI — ETL Pipeline Orchestrator (etl/pipeline.py)
Orchestrates Extract -> Transform -> Validate -> Load pipeline with logging & quality summary.
"""

import os
import json
import logging
from typing import Dict, Any
from etl.extract import extract_data
from etl.transform import transform_data
from etl.validate import validate_data
from etl.load import load_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("insightbi.etl.pipeline")

class ETLPipeline:
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir

    def run(self) -> Dict[str, Any]:
        logger.info("=" * 60)
        logger.info("Starting InsightBI AI ETL Pipeline Execution...")
        logger.info("=" * 60)

        # 1. Extract
        logger.info("[STEP 1/4] Extracting raw datasets...")
        raw_data = extract_data(data_dir=self.data_dir)

        # 2. Transform
        logger.info("[STEP 2/4] Transforming datasets & computing metrics...")
        transformed_data = transform_data(raw_data)

        # 3. Validate & Quality Checks
        logger.info("[STEP 3/4] Validating records & checking data quality...")
        validated_data, quality_report = validate_data(transformed_data)

        # 4. Load
        logger.info("[STEP 4/4] Loading cleaned data into storage...")
        load_success = load_data(validated_data)

        logger.info("=" * 60)
        logger.info(f"ETL Pipeline Finished! Data Quality Score: {quality_report['quality_score_percent']}%")
        logger.info("=" * 60)

        return {
            "success": True,
            "quality_report": quality_report,
            "db_load_success": load_success
        }

def run_etl_pipeline(data_dir: str = None) -> Dict[str, Any]:
    pipeline = ETLPipeline(data_dir=data_dir)
    return pipeline.run()
