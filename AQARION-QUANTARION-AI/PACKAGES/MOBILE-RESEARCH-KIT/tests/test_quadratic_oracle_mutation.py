import unittest
from unittest.mock import patch

from examples import quadratic_contract_atlas as atlas
from tools import verify_quadratic_atlas as verifier


def mutant(c, a, b, q):
    return (
        b % q == 0
        and (c + a - 2) % q == 0
        and (c - 1) % q == 0
    )


class QuadraticOracleMutationTests(unittest.TestCase):
    def test_mutation_detection_and_restoration(self):
        baseline = atlas.build_report([4], 3)
        self.assertTrue(baseline["all_checks_passed"])
        verifier.verify(baseline)

        with patch.object(atlas, "exact_classifier", mutant):
            row = atlas.analyze_candidate(3, -1, 0, 4)
            self.assertTrue(row["complete_acceptance"])
            self.assertTrue(row["three_point_acceptance"])
            self.assertFalse(row["exact_acceptance"])
            self.assertFalse(row["primary_routes_agree"])

            report = atlas.build_report([4], 3)
            self.assertFalse(report["all_checks_passed"])

            with self.assertRaisesRegex(
                ValueError, "exact_acceptance mismatch"
            ):
                verifier.verify(report)

        restored = atlas.build_report([4], 3)
        self.assertTrue(restored["all_checks_passed"])
        verifier.verify(restored)


if __name__ == "__main__":
    unittest.main()
