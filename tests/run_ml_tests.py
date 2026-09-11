import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_ml import test_sales_forecaster_training, test_customer_segmentation_clustering, test_anomaly_detection_isolation_forest

def run_all_ml_tests():
    print("Running ML test: test_sales_forecaster_training...")
    test_sales_forecaster_training()
    print("✓ test_sales_forecaster_training PASSED!")

    print("Running ML test: test_customer_segmentation_clustering...")
    test_customer_segmentation_clustering()
    print("✓ test_customer_segmentation_clustering PASSED!")

    print("Running ML test: test_anomaly_detection_isolation_forest...")
    test_anomaly_detection_isolation_forest()
    print("✓ test_anomaly_detection_isolation_forest PASSED!")

    print("\n🎉 ALL MACHINE LEARNING TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_ml_tests()
