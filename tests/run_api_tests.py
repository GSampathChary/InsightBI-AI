import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_api import (
    test_root_endpoint,
    test_health_endpoint,
    test_auth_registration_and_login,
    test_dashboard_summary_endpoint,
    test_sales_overview_endpoint,
    test_analytics_endpoints
)

def run_all_api_tests():
    print("Running API test: test_root_endpoint...")
    test_root_endpoint()
    print("✓ test_root_endpoint PASSED!")

    print("Running API test: test_health_endpoint...")
    test_health_endpoint()
    print("✓ test_health_endpoint PASSED!")

    print("Running API test: test_auth_registration_and_login...")
    test_auth_registration_and_login()
    print("✓ test_auth_registration_and_login PASSED!")

    print("Running API test: test_dashboard_summary_endpoint...")
    test_dashboard_summary_endpoint()
    print("✓ test_dashboard_summary_endpoint PASSED!")

    print("Running API test: test_sales_overview_endpoint...")
    test_sales_overview_endpoint()
    print("✓ test_sales_overview_endpoint PASSED!")

    print("Running API test: test_analytics_endpoints...")
    test_analytics_endpoints()
    print("✓ test_analytics_endpoints PASSED!")

    print("\n🎉 ALL FASTAPI REST API TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_api_tests()
