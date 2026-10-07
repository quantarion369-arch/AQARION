"""Targeted quadratic oracle and semantic-mutation regression tests."""

import copy
import unittest
from unittest.mock import patch

from examples import quadratic_contract_atlas as atlas
from tools import verify_quadratic_atlas as verifier


def overly_strict_exact_classifier(c, a, b, q):
    """Deliberate mutant: incorrectly removes the factor of two."""
    atlas.validate_modulus(q)
    return (
        b % q == 0
        and (c + a - 2) % q == 0
        and (c - 1) % q == 0
    )


class QuadraticOracleSeparationTests(unittest.TestCase):
    def test_even_modulus_witness_family(self):
        for q in (2, 4, 6, 8, 10, 12):
            c = 1 + q // 2
            a = 1 - q // 2
            b = 0

            with self.subTest(q=q, c=c, a=a, b=b):
                self.assertTrue(atlas.exact_classifier(c, a, b, q))
                self.assertTrue(
                    atlas.evaluate(c, a, b, q, range(q))["accepted"]
                )
                self.assertTrue(
                    atlas.evaluate(c, a, b, q, (0, 1, 2))["accepted"]
                )
                self.assertFalse(atlas.strict_classifier(c, a, b, q))
                self.assertFalse(
                    overly_strict_exact_classifier(c, a, b, q)
                )

    def test_canonical_witness_has_three_route_agreement(self):
        row = atlas.analyze_candidate(3, -1, 0, 4)

        self.assertTrue(row["complete_acceptance"])
        self.assertTrue(row["exact_acceptance"])
        self.assertTrue(row["three_point_acceptance"])
        self.assertTrue(row["primary_routes_agree"])
        self.assertTrue(row["strict_false_rejection"])
        self.assertIsNone(row["first_counterexample"])

    def test_generator_detects_injected_classifier_mutation(self):
        baseline = atlas.analyze_candidate(3, -1, 0, 4)
        self.assertTrue(baseline["primary_routes_agree"])

        with patch.object(
            atlas,
            "exact_classifier",
            side_effect=overly_strict_exact_classifier,
        ):
            mutated = atlas.analyze_candidate(3, -1, 0, 4)

        self.assertTrue(mutated["complete_acceptance"])
        self.assertTrue(mutated["three_point_acceptance"])
        self.assertFalse(mutated["exact_acceptance"])
        self.assertFalse(mutated["primary_routes_agree"])

        restored = atlas.analyze_candidate(3, -1, 0, 4)
        self.assertTrue(restored["primary_routes_agree"])

    def test_mutated_generator_report_fails_verifier(self):
        baseline = atlas.build_report([4], 3)
        self.assertTrue(baseline["all_checks_passed"])
        verifier.verify(baseline)

        with patch.object(
            atlas,
            "exact_classifier",
            side_effect=overly_strict_exact_classifier,
        ):
            mutated = atlas.build_report([4], 3)

        self.assertFalse(mutated["all_checks_passed"])
        self.assertGreater(
            mutated["summaries"][0]["primary_disagreements"],
            0,
        )

        with self.assertRaisesRegex(ValueError, "exact_acceptance mismatch"):
            verifier.verify(mutated)

        restored = atlas.build_report([4], 3)
        self.assertTrue(restored["all_checks_passed"])
        verifier.verify(restored)

    def test_verifier_rejects_tampered_exact_flag(self):
        baseline = atlas.build_report([4], 3)
        verifier.verify(baseline)

        tampered = copy.deepcopy(baseline)
        witness_row = next(
            row
            for row in tampered["results"][0]["candidates"]
            if (row["c"], row["a"], row["b"]) == (3, -1, 0)
        )
        witness_row["exact_acceptance"] = False

        with self.assertRaisesRegex(ValueError, "exact_acceptance mismatch"):
            verifier.verify(tampered)

    def test_verifier_rejects_tampered_contract_metadata(self):
        baseline = atlas.build_report([4], 3)
        verifier.verify(baseline)

        tampered = copy.deepcopy(baseline)
        tampered["reference"] = "TOTALLY_DIFFERENT_FUNCTION"
        tampered["candidate"] = "TOTALLY_DIFFERENT_CANDIDATE"

        with self.assertRaisesRegex(
            ValueError, "unexpected reference contract"
        ):
            verifier.verify(tampered)

    def test_verifier_does_not_call_generator_classifier(self):
        report = atlas.build_report([4], 3)

        with patch.object(
            atlas,
            "exact_classifier",
            side_effect=AssertionError(
                "Verifier must not call the generator classifier"
            ),
        ):
            totals = verifier.verify(report)

        self.assertEqual(totals["cases"], 343)


if __name__ == "__main__":
    unittest.main()
