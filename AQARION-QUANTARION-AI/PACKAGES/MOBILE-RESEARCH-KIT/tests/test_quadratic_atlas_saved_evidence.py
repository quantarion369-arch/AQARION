import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "verify_quadratic_atlas.py"
REPORT = ROOT / "tests" / "fixtures" / "quadratic_atlas_q2.json"

spec = importlib.util.spec_from_file_location(
    "quadratic_saved_evidence_verifier", TOOL
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SavedEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(REPORT.read_text(encoding="utf-8"))

    def setUp(self):
        self.report = copy.deepcopy(self.original)

    def find_row(self, predicate):
        for group in self.report["results"]:
            for row in group["candidates"]:
                if predicate(row):
                    return row
        self.fail("required fixture row is missing")

    def test_excessive_bounds_fail_before_results_access(self):
        for bound in (module.MAX_COEFFICIENT_BOUND + 1, 10 ** 100):
            with self.subTest(bound=bound):
                report = copy.deepcopy(self.original)
                report["coefficient_bound"] = bound
                del report["results"]
                with self.assertRaisesRegex(
                    ValueError, "coefficient bound exceeds verifier limit"
                ):
                    module.verify(report)

    def test_invalid_bound_types_are_rejected(self):
        for bound in (True, -1, 1.5, '3', None):
            with self.subTest(bound=bound):
                report = copy.deepcopy(self.original)
                report["coefficient_bound"] = bound
                with self.assertRaisesRegex(ValueError, "invalid coefficient bound"):
                    module.verify(report)

    def test_candidate_count_checked_before_row_access(self):
        self.report["results"][0]["candidates"] = [None]
        with self.assertRaisesRegex(ValueError, "candidate count mismatch"):
            module.verify(self.report)

    def test_original_report_passes(self):
        self.assertEqual(module.verify(self.report), {
            "cases": 343,
            "accepted": 75,
            "rejection_witnesses": 268,
            "equivalence_comparisons": 27,
        })

    def test_corrupted_recorded_output_fails(self):
        row = self.find_row(
            lambda row: row["first_counterexample"] is not None
        )
        row["first_counterexample"]["candidate_output"] += 1
        with self.assertRaisesRegex(ValueError, "counterexample mismatch"):
            module.verify(self.report)

    def test_missing_rejection_witness_fails(self):
        row = self.find_row(
            lambda row: row["first_counterexample"] is not None
        )
        row["first_counterexample"] = None
        with self.assertRaisesRegex(ValueError, "counterexample mismatch"):
            module.verify(self.report)

    def test_corrupted_equivalence_comparison_fails(self):
        row = self.find_row(
            lambda row: row["equivalence_certificate"] is not None
        )
        row["equivalence_certificate"][0]["candidate_residue"] += 1
        with self.assertRaisesRegex(
            ValueError, "equivalence comparison mismatch"
        ):
            module.verify(self.report)

    def test_corrupted_summary_fails(self):
        self.report["summaries"][0]["accepted"] += 1
        with self.assertRaisesRegex(ValueError, "summary mismatch"):
            module.verify(self.report)

    def test_duplicate_candidate_fails(self):
        rows = self.report["results"][0]["candidates"]
        rows[1] = copy.deepcopy(rows[0])
        with self.assertRaisesRegex(
            ValueError, "missing or duplicate candidates"
        ):
            module.verify(self.report)


if __name__ == "__main__":
    unittest.main()
