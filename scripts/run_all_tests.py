"""
InsightBI AI — Master Test Orchestrator (scripts/run_all_tests.py)
Executes all 9 component test suites sequentially.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.run_etl_tests import run_all_etl_tests
from tests.run_analytics_tests import run_all_analytics_tests
from tests.run_powerbi_tests import run_all_powerbi_tests
from tests.run_ml_tests import run_all_ml_tests
from tests.run_api_tests import run_all_api_tests
from tests.run_copilot_tests import run_all_copilot_tests
from tests.run_reporting_tests import run_all_reporting_tests
from tests.run_rbac_tests import run_all_rbac_tests
from tests.run_docker_tests import run_all_docker_tests
from tests.test_coverage_report import reporter

def main():
    print("\n🚀 STARTING INSIGHTBI AI MASTER TEST SUITE EXECUTION...\n")

    suites = [
        ("1. ETL Data Pipeline Suite", run_all_etl_tests, 3),
        ("2. Analytics & Warehouse Suite", run_all_analytics_tests, 3),
        ("3. Power BI DAX & M Suite", run_all_powerbi_tests, 3),
        ("4. ML Prediction Engine Suite", run_all_ml_tests, 3),
        ("5. FastAPI REST API Suite", run_all_api_tests, 3),
        ("6. AI Copilot Engine Suite", run_all_copilot_tests, 3),
        ("7. Reporting & Export Suite", run_all_reporting_tests, 4),
        ("8. Enterprise Auth & RBAC Suite", run_all_rbac_tests, 3),
        ("9. Docker Infrastructure Suite", run_all_docker_tests, 3)
    ]

    for name, runner, count in suites:
        print(f"\n========================================================")
        print(f"EXECUTING: {name}")
        print(f"========================================================")
        try:
            runner()
            reporter.record_suite(name, count, 0)
        except Exception as e:
            print(f"❌ {name} FAILED with error: {e}")
            reporter.record_suite(name, 0, count)

    reporter.print_summary()

if __name__ == "__main__":
    main()
