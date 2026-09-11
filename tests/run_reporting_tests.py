import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_reporting import (
    test_pdf_exporter,
    test_csv_exporter,
    test_report_scheduler,
    test_reports_api_endpoints
)

def run_all_reporting_tests():
    print("Running Reporting test: test_pdf_exporter...")
    test_pdf_exporter()
    print("✓ test_pdf_exporter PASSED!")

    print("Running Reporting test: test_csv_exporter...")
    test_csv_exporter()
    print("✓ test_csv_exporter PASSED!")

    print("Running Reporting test: test_report_scheduler...")
    test_report_scheduler()
    print("✓ test_report_scheduler PASSED!")

    print("Running Reporting test: test_reports_api_endpoints...")
    test_reports_api_endpoints()
    print("✓ test_reports_api_endpoints PASSED!")

    print("\n🎉 ALL ADVANCED ANALYTICS & REPORTING TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_reporting_tests()
