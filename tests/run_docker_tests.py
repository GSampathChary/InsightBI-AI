import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tests.test_docker_config import (
    test_docker_compose_structure,
    test_dockerfiles_exist,
    test_env_example_template
)

def run_all_docker_tests():
    print("Running Docker test: test_docker_compose_structure...")
    test_docker_compose_structure()
    print("✓ test_docker_compose_structure PASSED!")

    print("Running Docker test: test_dockerfiles_exist...")
    test_dockerfiles_exist()
    print("✓ test_dockerfiles_exist PASSED!")

    print("Running Docker test: test_env_example_template...")
    test_env_example_template()
    print("✓ test_env_example_template PASSED!")

    print("\n🎉 ALL DOCKER & PRODUCTION CONFIGURATION TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_docker_tests()
