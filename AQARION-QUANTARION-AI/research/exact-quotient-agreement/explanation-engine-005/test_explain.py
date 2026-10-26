"""Focused exact explanation tests; no census."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "exact_explanation", HERE / "explain.py"
)
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

CASES = {
    "A": ((2,3,0,1), (0,0,1,1), (2,2,0,2,0,0)),
    "B": ((0,2,1,3), (0,0,1,1), (2,4,1,3,0,1)),
    "C": ((0,0,1,2), (0,1,0,0), (2,4,1,4,1,0)),
}

class ExplanationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {
            name: engine.explain(T, labels)
            for name, (T, labels, _) in CASES.items()
        }

    def test_three_distinct_mechanisms(self):
        keys = (
            "k", "stable_class_count", "defect_rank",
            "eventual_linear_dimension", "later_linear_growth",
            "eventual_linear_deficiency",
        )
        for name, (_, _, expected) in CASES.items():
            with self.subTest(example=name):
                self.assertEqual(
                    tuple(self.results[name][k] for k in keys),
                    expected,
                )

    def test_existing_compatible_quotient(self):
        self.assertTrue(self.results["A"]["compatible"])
        self.assertEqual(
            tuple(self.results["A"]["initial_quotient"]), (1,0)
        )
        self.assertIsNone(
            self.results["A"]["first_ordered_witness"]
        )

    def test_stable_class_not_raw_state_annihilators(self):
        for name in ("A", "C"):
            self.assertEqual(
                self.results[name]["annihilator_basis"], []
            )
            self.assertEqual(
                self.results[name]["first_product_repair"]["status"],
                "not_needed",
            )

    def test_annihilator_and_product_pairing(self):
        result = self.results["B"]
        repair = result["first_product_repair"]
        z = list(map(Q, result["annihilator_basis"][0]))
        values = list(map(
            Q, repair["values_on_stable_classes"]
        ))
        self.assertNotEqual(
            sum(a*b for a, b in zip(z, values)), 0
        )
        self.assertEqual(
            (repair["rank_before"], repair["rank_after"]),
            (3,4),
        )
        self.assertTrue(repair["complete_repair"])
        C = [
            [Q(v) for v in row]
            for row in result["linear_closure_certificate"]["basis"]
        ]
        self.assertTrue(all(
            sum(z[x]*C[x][j] for x in range(4)) == 0
            for j in range(3)
        ))

    def test_round_profiles_and_certificates(self):
        expected = {
            "A": [(2,2), (2,2)],
            "B": [(2,2), (4,3), (4,3)],
            "C": [(2,2), (3,3), (4,4), (4,4)],
        }
        for name, result in self.results.items():
            with self.subTest(example=name):
                self.assertEqual([
                    (r["partition_blocks"], r["linear_dimension"])
                    for r in result["round_profile"]
                ], expected[name])
                checks = result['linear_closure_certificate']['checks']
                self.assertEqual(set(checks), {
                    'initial_observables_contained',
                    'koopman_invariant',
                    'basis_independent',
                    'basis_from_named_time_shifts',
                })
                for check_name in checks:
                    self.assertIs(checks[check_name], True, check_name)
                self.assertEqual(
                    result["constraint_redundancy"]
                    + result["delayed_refinement_increase"],
                    result["eventual_linear_deficiency"]
                    + result["later_linear_growth"],
                )

    def test_relabeling_and_single_state(self):
        result = engine.explain(
            (2,3,0,1), (-7,-7,42,42)
        )
        self.assertEqual(
            result["normalized_labels"], [0,0,1,1]
        )
        single = engine.explain((0,), (99,))
        self.assertEqual(
            (single["stable_class_count"],
             single["eventual_linear_dimension"]),
            (1,1),
        )

    def test_reject_malformed_inputs(self):
        invalid = [
            ((), ()), ((0,), ()), ((1,), (0,)),
            ((True,), (0,)), ((0,), (False,)),
            ((0,), ("a",)), ((0.0,), (0,)),
            (tuple(range(17)), (0,)*17),
        ]
        for T, labels in invalid:
            with self.subTest(T=T, labels=labels):
                with self.assertRaises(ValueError):
                    engine.explain(T, labels)

if __name__ == "__main__":
    unittest.main(verbosity=2)
