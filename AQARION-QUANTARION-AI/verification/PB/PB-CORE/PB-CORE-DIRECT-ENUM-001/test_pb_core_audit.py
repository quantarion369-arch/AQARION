import unittest

from pb_core_audit import (
    aggregate_formula,
    core_relations,
    direct_relations,
    is_pullback_fixed,
    partitions,
    partition_numbers,
    periodic_core,
    relation_set_mismatch,
)

class PartitionTests(unittest.TestCase):
    def test_bell_counts_through_six(self):
        expected = {1: 1, 2: 2, 3: 5, 4: 15, 5: 52, 6: 203}
        for n, count in expected.items():
            with self.subTest(n=n):
                ps = tuple(partitions(n))
                self.assertEqual(len(ps), count)
                self.assertEqual(len(set(ps)), count)
                self.assertTrue(all(p[0] == 0 for p in ps))

    def test_empty_partition(self):
        self.assertEqual(tuple(partitions(0)), ((),))

    def test_rejects_negative(self):
        with self.assertRaises(ValueError):
            tuple(partitions(-1))

class DirectPredicateTests(unittest.TestCase):
    def test_identity_fixes_every_equivalence(self):
        t = (0, 1, 2)
        ps = tuple(partitions(3))
        self.assertEqual(direct_relations(t, ps), set(ps))

    def test_constant_map_only_universal_relation_survives(self):
        t = (0, 0, 0)
        ps = tuple(partitions(3))
        accepted = direct_relations(t, ps)
        self.assertEqual(accepted, {(0, 0, 0)})

    def test_biconditional_not_just_forward_preservation(self):
        # For a constant map, every equivalence is forward-preserved because
        # all images coincide; the pullback relation is universal, so a
        # non-universal equivalence fails the reverse implication.
        t = (0, 0, 0)
        labels = (0, 1, 2)
        forward_preserved = all(
            (labels[x] != labels[y]) or (labels[t[x]] == labels[t[y]])
            for x in range(3)
            for y in range(3)
        )
        self.assertTrue(forward_preserved)
        self.assertFalse(is_pullback_fixed(t, labels))

class RetractionTests(unittest.TestCase):
    def test_two_cycle_reaches_core_without_fixing_it_at_exponent_one(self):
        t = (1, 0)
        core, _, _ = periodic_core(t)
        self.assertEqual(core, (0, 1))
        r1 = tuple(t[x] for x in range(2))
        self.assertEqual(set(r1), set(core))
        self.assertNotEqual(tuple(r1[v] for v in core), core)

    def test_chosen_retraction_fixes_core_and_commutes(self):
        # 0->1->2->1 and 3->1; core is the 2-cycle {1,2}.
        t = (1, 2, 1, 1)
        core, r, exponent = periodic_core(t)
        self.assertGreaterEqual(exponent, 2)
        self.assertEqual(set(r), set(core))
        self.assertTrue(all(r[v] == v for v in core))
        self.assertTrue(all(r[t[x]] == t[r[x]] for x in range(len(t))))

    def test_mismatch_diagnostic_identifies_relations_in_each_difference(self):
        diagnostic = relation_set_mismatch(
            (0, 0), {(0, 0)}, {(0, 1)}, {"core_size": 1}
        )
        self.assertIsNotNone(diagnostic)
        self.assertEqual(diagnostic["map"], (0, 0))
        self.assertEqual(diagnostic["direct_only"], [(0, 0)])
        self.assertEqual(diagnostic["constructed_only"], [(0, 1)])
        self.assertIsNone(relation_set_mismatch((0,), {(0,)}, {(0,)}))

    def test_direct_and_constructed_relation_sets_on_shapes(self):
        examples = [
            (0, 1, 2),       # identity
            (0, 0, 0),       # constant
            (1, 0),          # 2-cycle
            (1, 2, 1, 1),    # transient chain into a 2-cycle
            (1, 0, 3, 2),    # two cycles
        ]
        for t in examples:
            n = len(t)
            by_size = {m: tuple(partitions(m)) for m in range(1, n + 1)}
            with self.subTest(t=t):
                direct = direct_relations(t, by_size[n])
                constructed, _ = core_relations(t, by_size)
                self.assertEqual(direct, constructed)

class FormulaTests(unittest.TestCase):
    def test_partition_numbers(self):
        p = partition_numbers(6)
        self.assertEqual(p, [1, 1, 2, 3, 5, 7, 11])

    def test_known_aggregate_totals(self):
        expected = [None, 1, 6, 51, 592, 8565, 148896]
        p = partition_numbers(6)
        for n in range(1, 7):
            with self.subTest(n=n):
                self.assertEqual(aggregate_formula(n, p), expected[n])

if __name__ == "__main__":
    unittest.main(verbosity=2)
