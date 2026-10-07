"""Check evidence states for empty and nonempty contract domains."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import Mock


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "examples"
    / "contract_collision_lab.py"
)
SPEC = importlib.util.spec_from_file_location(
    "contract_evidence_under_test", SOURCE
)
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)


class ContractEvidenceTests(unittest.TestCase):
    def test_empty_equality_has_no_evidence(self):
        candidate = Mock(return_value=0)
        result = LAB.check_contract(candidate, "equality", [])

        self.assertIsNone(result["accepted_on_tested_domain"])
        self.assertEqual(result["evidence_status"], "no_evidence")
        self.assertEqual(result["inputs_checked"], 0)
        self.assertIsNone(result["first_counterexample"])
        candidate.assert_not_called()

    def test_empty_parity_has_no_evidence(self):
        candidate = Mock(return_value=0)
        result = LAB.check_contract(candidate, "parity", [])

        self.assertIsNone(result["accepted_on_tested_domain"])
        self.assertEqual(result["evidence_status"], "no_evidence")
        self.assertEqual(result["inputs_checked"], 0)
        candidate.assert_not_called()

    def test_empty_iterator_has_no_evidence(self):
        candidate = Mock(return_value=0)
        result = LAB.check_contract(candidate, "equality", iter(()))

        self.assertIsNone(result["accepted_on_tested_domain"])
        self.assertEqual(result["evidence_status"], "no_evidence")
        self.assertEqual(result["inputs_checked"], 0)
        candidate.assert_not_called()

    def test_nonempty_acceptance_reports_evidence(self):
        result = LAB.check_contract(
            LAB.reference, "equality", iter([-1, 0, 1])
        )

        self.assertIs(result["accepted_on_tested_domain"], True)
        self.assertEqual(
            result["evidence_status"], "accepted_on_tested_domain"
        )
        self.assertEqual(result["inputs_checked"], 3)
        self.assertIsNone(result["first_counterexample"])

    def test_counterexample_reports_evidence(self):
        candidate = Mock(side_effect=LAB.offset_mutation)
        result = LAB.check_contract(
            candidate, "equality", [0, 1, 2]
        )

        self.assertIs(result["accepted_on_tested_domain"], False)
        self.assertEqual(
            result["evidence_status"], "counterexample_found"
        )
        self.assertEqual(result["inputs_checked"], 1)
        self.assertEqual(result["first_counterexample"]["input"], 0)
        candidate.assert_called_once_with(0)

    def test_parity_acceptance_remains_distinct(self):
        result = LAB.check_contract(
            LAB.subtract_mutation, "parity", range(-2, 3)
        )

        self.assertIs(result["accepted_on_tested_domain"], True)
        self.assertEqual(
            result["evidence_status"], "accepted_on_tested_domain"
        )
        self.assertEqual(result["inputs_checked"], 5)

    def test_unknown_empty_contract_still_raises(self):
        candidate = Mock(return_value=0)

        with self.assertRaisesRegex(ValueError, "Unknown contract:"):
            LAB.check_contract(candidate, "unknown", iter(()))

        candidate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
