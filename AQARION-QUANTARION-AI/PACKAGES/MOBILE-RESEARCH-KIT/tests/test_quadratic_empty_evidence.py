import unittest
from examples import quadratic_contract_atlas as atlas


class QuadraticEmptyEvidenceTests(unittest.TestCase):
    def test_empty_sample_has_no_evidence(self):
        for domain in ([], iter(())):
            result = atlas.evaluate(3, -1, 0, 4, domain)
            self.assertIsNone(result["accepted"])
            self.assertEqual(result["evidence_status"], "no_evidence")
            self.assertEqual(result["inputs_checked"], 0)
            self.assertEqual(result["comparisons"], [])
            self.assertIsNone(result["first_counterexample"])

    def test_single_zero_is_not_empty(self):
        result = atlas.evaluate(1, 0, 0, 4, [0])
        self.assertIs(result["accepted"], True)
        self.assertEqual(result["evidence_status"], "observed")
        self.assertEqual(result["inputs_checked"], 1)
        self.assertFalse(
            atlas.evaluate(1, 0, 0, 4, range(4))["accepted"]
        )

    def test_nonempty_rejection_stays_boolean(self):
        result = atlas.evaluate(1, 0, 0, 4, [1])
        self.assertIs(result["accepted"], False)
        self.assertEqual(result["evidence_status"], "observed")
        self.assertIsNotNone(result["first_counterexample"])


if __name__ == "__main__":
    unittest.main()
