import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_copilot import (
    test_nl_to_sql_conversion,
    test_sql_safety_sanitizer,
    test_insight_narrator,
    test_copilot_api_endpoint
)

def run_all_copilot_tests():
    print("Running Copilot test: test_nl_to_sql_conversion...")
    test_nl_to_sql_conversion()
    print("✓ test_nl_to_sql_conversion PASSED!")

    print("Running Copilot test: test_sql_safety_sanitizer...")
    test_sql_safety_sanitizer()
    print("✓ test_sql_safety_sanitizer PASSED!")

    print("Running Copilot test: test_insight_narrator...")
    test_insight_narrator()
    print("✓ test_insight_narrator PASSED!")

    print("Running Copilot test: test_copilot_api_endpoint...")
    test_copilot_api_endpoint()
    print("✓ test_copilot_api_endpoint PASSED!")

    print("\n🎉 ALL AI ANALYTICS COPILOT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_copilot_tests()
