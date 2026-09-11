"""
InsightBI AI — Test Coverage Report Generator (tests/test_coverage_report.py)
Generates structured coverage and health metrics across all test modules.
"""

from typing import List, Dict, Any

class CoverageReportGenerator:
    def __init__(self):
        self.results = []

    def record_suite(self, suite_name: str, passed_count: int, failed_count: int):
        total = passed_count + failed_count
        rate = (passed_count / total * 100.0) if total > 0 else 0.0
        self.results.append({
            "suite_name": suite_name,
            "passed": passed_count,
            "failed": failed_count,
            "total": total,
            "success_rate": rate
        })

    def print_summary(self):
        print("\n" + "=" * 80)
        print("                   INSIGHTBI AI — MASTER TEST COVERAGE REPORT")
        print("=" * 80)
        print(f"{'Test Suite Module':<35} | {'Passed':<8} | {'Failed':<8} | {'Pass Rate':<10}")
        print("-" * 80)

        total_p = 0
        total_f = 0

        for item in self.results:
            total_p += item["passed"]
            total_f += item["failed"]
            print(f"{item['suite_name']:<35} | {item['passed']:<8} | {item['failed']:<8} | {item['success_rate']:>6.1f}%")

        overall_total = total_p + total_f
        overall_rate = (total_p / overall_total * 100.0) if overall_total > 0 else 0.0
        print("-" * 80)
        print(f"{'TOTAL COMPONENT COVERAGE':<35} | {total_p:<8} | {total_f:<8} | {overall_rate:>6.1f}%")
        print("=" * 80 + "\n")

reporter = CoverageReportGenerator()
