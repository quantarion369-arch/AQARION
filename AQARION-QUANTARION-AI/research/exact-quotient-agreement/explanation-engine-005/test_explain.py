"""Focused exact explanation tests; no census."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest
from copy import deepcopy
from itertools import permutations

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


def _independent_rank(rows):
    a = [[Q(x) for x in row] for row in rows]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        for i in range(r + 1, len(a)):
            factor = a[i][col] / a[r][col]
            a[i] = [x - factor*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r

def _independent_determinant(a):
    n = len(a)
    total = Q(0)
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j]
                         for i in range(n) for j in range(i + 1, n))
        term = Q((-1) ** inversions)
        for i, j in enumerate(order):
            term *= Q(a[i][j])
        total += term
    return total

def _independent_multiply(a, b):
    return [[sum((Q(a[i][h])*Q(b[h][j]) for h in range(len(b))), Q(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def _independent_normalize(values):
    ids = {}
    return tuple(ids.setdefault(value, len(ids)) for value in values)

def _independent_indicator(T, labels, description):
    values = []
    for x in range(len(T)):
        for _ in range(description["time"]):
            x = T[x]
        values.append(Q(labels[x] == description["normalized_block"]))
    return values

def _rows_from_columns(columns):
    return [list(row) for row in zip(*columns)]

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
                T, labels, _ = CASES[name]
                self._replay_certificate(T, labels, result)
                self._check_replay_negative_controls(T, labels, result)
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


    def _replay_certificate(self, T, original_labels, result):
        labels = _independent_normalize(original_labels)
        n, k = len(T), len(set(labels))
        self.assertEqual(result["normalized_labels"], list(labels))
        partition = labels
        trace = [list(partition)]
        while True:
            nxt = _independent_normalize([
                (partition[x], partition[T[x]]) for x in range(n)
            ])
            if nxt == partition:
                break
            partition = nxt
            trace.append(list(partition))
        self.assertEqual(result["refinement_trace"], trace)
        self.assertEqual(result["stable_class_labels"], list(partition))
        m = len(set(partition))
        self.assertEqual(result["k"], k)
        self.assertEqual(result["stable_class_count"], m)

        certificate = result["linear_closure_certificate"]
        C = [[Q(x) for x in row] for row in certificate["basis"]]
        d = result["eventual_linear_dimension"]
        self.assertEqual(len(C), n)
        self.assertTrue(all(len(row) == d for row in C))
        self.assertEqual(_independent_rank(C), d)

        A = [[Q(x) for x in row]
             for row in certificate["initial_coordinates"]]
        M = [[Q(x) for x in row]
             for row in certificate["evolution_coordinates"]]
        self.assertEqual(len(A), d)
        self.assertTrue(all(len(row) == k for row in A))
        self.assertEqual(len(M), d)
        self.assertTrue(all(len(row) == d for row in M))
        B = [[Q(labels[x] == b) for b in range(k)] for x in range(n)]
        self.assertEqual(_independent_multiply(C, A), B)
        self.assertEqual(_independent_multiply(C, M), [C[T[x]] for x in range(n)])

        descriptions = certificate["basis_generation"]
        self.assertEqual(len(descriptions), d)
        for j, description in enumerate(descriptions):
            self.assertEqual(set(description), {"time", "normalized_block"})
            self.assertIs(type(description["time"]), int)
            self.assertTrue(0 <= description["time"] <= n)
            self.assertIs(type(description["normalized_block"]), int)
            self.assertTrue(0 <= description["normalized_block"] < k)
            self.assertEqual(
                [C[x][j] for x in range(n)],
                _independent_indicator(T, labels, description),
            )

        minor_rows = certificate["minor_rows"]
        self.assertEqual(len(minor_rows), d)
        self.assertEqual(len(set(minor_rows)), d)
        self.assertTrue(all(type(i) is int and 0 <= i < n for i in minor_rows))
        determinant = _independent_determinant([C[i] for i in minor_rows])
        self.assertNotEqual(determinant, 0)
        self.assertEqual(determinant, Q(certificate["minor_determinant"]))

        representatives = [partition.index(b) for b in range(m)]
        class_rows = [C[x] for x in representatives]
        for x in range(n):
            self.assertEqual(C[x], class_rows[partition[x]])
        annihilators = [
            [Q(x) for x in row] for row in result["annihilator_basis"]
        ]
        self.assertEqual(len(annihilators), m - d)
        self.assertTrue(all(len(row) == m for row in annihilators))
        self.assertEqual(_independent_rank(annihilators), m - d)
        self.assertEqual(result["eventual_linear_deficiency"], m - d)
        for z in annihilators:
            for j in range(d):
                self.assertEqual(sum(z[b]*class_rows[b][j]
                                     for b in range(m)), 0)

    def _check_replay_negative_controls(self, T, labels, result):
        for field in ("initial_coordinates", "evolution_coordinates",
                      "basis_generation", "minor_determinant", "annihilator_basis"):
            altered = deepcopy(result)
            certificate = altered["linear_closure_certificate"]
            if field in ("initial_coordinates", "evolution_coordinates"):
                certificate[field][0][0] = str(Q(certificate[field][0][0]) + 1)
            elif field == "basis_generation":
                certificate[field][0]["normalized_block"] = result["k"]
            elif field == "minor_determinant":
                certificate[field] = str(Q(certificate[field]) + 1)
            elif altered[field]:
                altered[field][0][0] = str(Q(altered[field][0][0]) + 1)
            else:
                altered[field] = [["1"] * result["stable_class_count"]]
            with self.assertRaises(AssertionError, msg=field):
                self._replay_certificate(T, labels, altered)

    def test_incomplete_first_product_and_temporal_repair(self):
        T = (1, 0, 3, 1, 0, 4)
        labels = (0, 1, 0, 1, 0, 0)
        result = engine.explain(T, labels)
        self._replay_certificate(T, labels, result)
        self._check_replay_negative_controls(T, labels, result)
        self.assertEqual(
            [len(set(p)) for p in result["refinement_trace"]], [2, 4, 6]
        )
        self.assertEqual(result["linear_dimension_trace"], [2, 3, 4, 4])
        self.assertEqual(
            (result["stable_class_count"], result["eventual_linear_dimension"],
             result["defect_rank"], result["eventual_linear_deficiency"]),
            (6, 4, 1, 2),
        )

        columns = [
            _independent_indicator(T, labels, {"time": t, "normalized_block": b})
            for t in range(len(T)) for b in range(2)
        ]
        W = _rows_from_columns(columns)
        self.assertEqual(_independent_rank(W), 4)
        dimensions = []
        for t in range(len(T)):
            dimensions.append(_independent_rank(
                _rows_from_columns(columns[:2*(t + 1)])
            ))
            if t and dimensions[-1] == dimensions[-2]:
                break
        self.assertEqual(dimensions, [2, 3, 4, 4])

        repair = result["first_product_repair"]
        self.assertEqual(repair["status"], "rank_increasing")
        self.assertEqual(repair["left"], {"time": 0, "normalized_block": 0})
        self.assertEqual(repair["right"], {"time": 1, "normalized_block": 0})
        left = _independent_indicator(T, labels, repair["left"])
        right = _independent_indicator(T, labels, repair["right"])
        v = [a*b for a, b in zip(left, right)]
        self.assertEqual(v, list(map(Q, (0, 0, 0, 0, 1, 1))))

        stable = result["stable_class_labels"]
        representatives = [stable.index(b) for b in range(6)]
        self.assertEqual(
            list(map(Q, repair["values_on_stable_classes"])),
            [v[x] for x in representatives],
        )
        self.assertEqual(_independent_rank(
            [row + [v[x]] for x, row in enumerate(W)]
        ), 5)
        self.assertEqual((repair["rank_before"], repair["rank_after"]), (4, 5))
        self.assertIs(repair["complete_repair"], False)

        Kv = [v[T[x]] for x in range(len(T))]
        f10 = _independent_indicator(T, labels, {"time": 1, "normalized_block": 0})
        f20 = _independent_indicator(T, labels, {"time": 2, "normalized_block": 0})
        self.assertEqual(Kv, [a*b for a, b in zip(f10, f20)])
        self.assertEqual(Kv, list(map(Q, (0, 0, 0, 0, 0, 1))))
        self.assertEqual(_independent_rank(
            [row + [v[x], Kv[x]] for x, row in enumerate(W)]
        ), 6)

        products = [
            [a*b for a, b in zip(columns[i], columns[j])]
            for i in range(len(columns)) for j in range(i, len(columns))
        ]
        self.assertEqual(_independent_rank(
            _rows_from_columns(columns + products)
        ), 6)
        self.assertEqual(
            (result["constraint_redundancy"],
             result["delayed_refinement_increase"],
             result["later_linear_growth"]), (1, 2, 1),
        )
        self.assertEqual(
            result["constraint_redundancy"] + result["delayed_refinement_increase"],
            result["eventual_linear_deficiency"] + result["later_linear_growth"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
