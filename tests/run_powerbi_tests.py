import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_powerbi_dax import test_dax_formula_equivalents

def run_all_powerbi_tests():
    print("Running Power BI DAX formula verification test...")
    test_dax_formula_equivalents()
    print("✓ test_dax_formula_equivalents PASSED!")
    print("\n🎉 ALL POWER BI DAX TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_powerbi_tests()
