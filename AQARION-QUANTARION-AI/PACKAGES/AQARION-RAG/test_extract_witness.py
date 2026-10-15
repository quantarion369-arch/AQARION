#!/usr/bin/env python3
import unittest
from extract_witness import extract_diagnostic
from wire_corpus_assessment import to_assess_witness
from assess import READINGS, make_claim, assess

class ExtractDiagnosticTests(unittest.TestCase):
    def test_extracts_candidate(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5 unstable")
        self.assertIsNone(reason)
        self.assertEqual(candidate["c"], 0.5)
        self.assertEqual(candidate["reported_label"], "unstable")
        self.assertEqual(candidate["verification_status"], "SYNTACTIC_CANDIDATE_ONLY")

    def test_rejects_missing_family(self):
        candidate, reason = extract_diagnostic("c = 0.5 unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_family_marker")

    def test_rejects_missing_parameter(self):
        candidate, reason = extract_diagnostic("quadratic unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_parameter_c")

    def test_rejects_missing_label(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "missing_stability_label")

    def test_rejects_conflicting_labels(self):
        candidate, reason = extract_diagnostic("quadratic c = 0.5 stable but unstable")
        self.assertIsNone(candidate)
        self.assertEqual(reason, "conflicting_stability_labels")

class AssessmentTests(unittest.TestCase):
    def claim(self):
        return make_claim("universal bounded-orbit stability", lambda w: True, READINGS["bounded_orbit"])

    def test_lying_label_does_not_change_verdict(self):
        witness = to_assess_witness({
            "id": "T1", "family": "quadratic", "c": 0.5,
            "reported_label": "stable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "REFUTED")
        self.assertEqual(decisive, ["T1"])

    def test_stable_parameter_is_not_decisive(self):
        witness = to_assess_witness({
            "id": "T2", "family": "quadratic", "c": 0.2,
            "reported_label": "unstable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "OPEN")
        self.assertEqual(decisive, [])

    def test_corpus_candidate_refutes_universal_claim(self):
        witness = to_assess_witness({
            "id": "T3", "family": "quadratic", "c": 1.5,
            "reported_label": "unstable",
        })
        verdict, decisive = assess(self.claim(), [witness])
        self.assertEqual(verdict, "REFUTED")
        self.assertEqual(decisive, ["T3"])

if __name__ == "__main__":
    unittest.main()

class DualReadingTests(unittest.TestCase):
    def test_both_readings_refute_c_half(self):
        from assess import READINGS, make_claim, assess
        from wire_corpus_assessment import to_assess_witness
        witness = to_assess_witness({
            "id": "D1",
            "family": "quadratic",
            "c": 0.5,
            "reported_label": "stable",
        })
        for reading in READINGS:
            claim = make_claim(
                "universal " + reading + " stability",
                lambda w: True,
                READINGS[reading],
            )
            verdict, decisive = assess(claim, [witness])
            self.assertEqual(verdict, "REFUTED")
            self.assertEqual(decisive, ["D1"])
