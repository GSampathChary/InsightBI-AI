import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_rbac import (
    test_rbac_matrix_integrity,
    test_audit_logging,
    test_auth_refresh_token
)

def run_all_rbac_tests():
    print("Running RBAC test: test_rbac_matrix_integrity...")
    test_rbac_matrix_integrity()
    print("✓ test_rbac_matrix_integrity PASSED!")

    print("Running RBAC test: test_audit_logging...")
    test_audit_logging()
    print("✓ test_audit_logging PASSED!")

    print("Running RBAC test: test_auth_refresh_token...")
    test_auth_refresh_token()
    print("✓ test_auth_refresh_token PASSED!")

    print("\n🎉 ALL ENTERPRISE AUTH & RBAC TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_rbac_tests()
