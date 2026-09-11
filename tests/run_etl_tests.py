import sys
import os

# Add root directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_etl import test_extract_module, test_transform_financial_calculations, test_data_validation_rules, test_full_pipeline_run

def run_all_etl_tests():
    print("Running ETL test: test_extract_module...")
    test_extract_module()
    print("✓ test_extract_module PASSED!")

    print("Running ETL test: test_transform_financial_calculations...")
    test_transform_financial_calculations()
    print("✓ test_transform_financial_calculations PASSED!")

    print("Running ETL test: test_data_validation_rules...")
    test_data_validation_rules()
    print("✓ test_data_validation_rules PASSED!")

    print("Running ETL test: test_full_pipeline_run...")
    test_full_pipeline_run()
    print("✓ test_full_pipeline_run PASSED!")

    print("\n🎉 ALL ETL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_etl_tests()
