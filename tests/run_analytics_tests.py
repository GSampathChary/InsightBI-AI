import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_analytics import test_compute_overall_kpis, test_compute_sales_trends, test_business_insights_generation, test_analytics_service_summary

def run_all_analytics_tests():
    print("Running analytics test: test_compute_overall_kpis...")
    test_compute_overall_kpis()
    print("✓ test_compute_overall_kpis PASSED!")

    print("Running analytics test: test_compute_sales_trends...")
    test_compute_sales_trends()
    print("✓ test_compute_sales_trends PASSED!")

    print("Running analytics test: test_business_insights_generation...")
    test_business_insights_generation()
    print("✓ test_business_insights_generation PASSED!")

    print("Running analytics test: test_analytics_service_summary...")
    test_analytics_service_summary()
    print("✓ test_analytics_service_summary PASSED!")

    print("\n🎉 ALL ANALYTICS ENGINE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_analytics_tests()
