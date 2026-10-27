import copy
import json
from pathlib import Path
import runpy
import unittest

ROOT = Path(__file__).resolve().parents[1]
FEATURE = ROOT / "features" / "extremal_inspector"
M = runpy.run_path(str(FEATURE / "recognizer.py"))
construct = M["terminal_repair_certificate"]
verify = M["verify_terminal_repair"]


class TestTerminalRepair(unittest.TestCase):
    def test_cubic_and_four_bit_top_term(self):
        for d in (3, 4):
            truth = [int(x == (1 << d) - 1) for x in range(1 << d)]
            certificate = construct(truth)
            self.assertTrue(verify(truth, certificate))
            self.assertEqual(
                certificate["temporal_product_coordinates"], [d]
            )
            self.assertEqual(certificate["parity_moment"], (-1) ** d)
            self.assertEqual(certificate["full_rank_degree"], d - 1)

    def test_quadratic_terminal(self):
        truth = [
            ((x >> 2) & 1) * ((x >> 1) & 1)
            for x in range(8)
        ]
        certificate = construct(truth)
        self.assertEqual(
            certificate["temporal_product_coordinates"], [2, 3]
        )
        self.assertEqual(certificate["parity_moment"], -1)
        self.assertTrue(verify(truth, certificate))

    def test_xor_uses_real_multilinear_coefficients(self):
        truth = [
            ((x >> 2) & 1) ^ ((x >> 1) & 1)
            for x in range(8)
        ]
        certificate = construct(truth)
        self.assertEqual(certificate["coefficient"], -2)
        self.assertEqual(certificate["parity_moment"], 2)
        self.assertTrue(verify(truth, certificate))

    def test_constants_and_literals_have_no_repair(self):
        for d in range(1, 5):
            n = 1 << d
            tables = [[0] * n, [1] * n]
            tables += [
                [((x >> j) & 1) ^ b for x in range(n)]
                for j in range(d) for b in (0, 1)
            ]
            for truth in tables:
                self.assertIsNone(construct(truth))

    def test_malformed_truth_tables(self):
        for truth in (None, [], [0, 1, 0], [0, 2], [False, 1]):
            with self.assertRaises(ValueError):
                construct(truth)

    def test_tampered_coefficient_and_moment_rejected(self):
        truth = [0] * 7 + [1]
        original = construct(truth)
        for field in ("coefficient", "parity_moment"):
            altered = copy.deepcopy(original)
            altered[field] += 1
            self.assertFalse(verify(truth, altered))

    def test_tampered_feature_and_types_rejected(self):
        truth = [0] * 7 + [1]
        for alteration in (
            {"temporal_product_coordinates": [0]},
            {"nonlinear_support": [0, 1]},
            {"full_rank": True},
            {"parity_moment": True},
        ):
            certificate = construct(truth)
            certificate.update(alteration)
            self.assertFalse(verify(truth, certificate))

    def test_all_boolean_functions_through_dimension_three(self):
        checked = 0
        certificates = 0
        for d in range(1, 4):
            n = 1 << d
            for mask in range(1 << n):
                truth = [(mask >> x) & 1 for x in range(n)]
                certificate = construct(truth)
                checked += 1
                if certificate is not None:
                    self.assertTrue(verify(truth, certificate))
                    self.assertLessEqual(
                        certificate["temporal_product_degree"], d - 1
                    )
                    certificates += 1
        self.assertEqual(checked, 276)
        self.assertEqual(certificates, 258)

    def test_enriched_saved_cases(self):
        data = json.loads(
            (FEATURE / "build-002" / "cases.json").read_text()
        )
        seen = set()
        for case in data["cases"].values():
            result = case["recognition"]
            if result["classification"] != "NONLITERAL_TERMINAL":
                continue
            self.assertTrue(verify(
                result["terminal_truth_table"],
                result["repair_certificate"],
            ))
            seen.add(tuple(case["T"]))
        self.assertEqual(len(seen), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
