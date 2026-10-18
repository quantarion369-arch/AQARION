"""Regression tests for the binary observable closure-gap formula."""
import importlib.util
import unittest
from itertools import product
from pathlib import Path

SOURCE = Path(__file__).with_name("closure_gap_replay.py")
SPEC = importlib.util.spec_from_file_location("closure_formula_contract", SOURCE)
replay = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(replay)


class FormulaContractTests(unittest.TestCase):
    def test_all_1022_words_as_lists_and_tuples(self):
        count = 0
        for n in range(1, 10):
            for word in product((0, 1), repeat=n):
                expected = replay.gap(replay.cyc(n), word)
                for value in (list(word), tuple(word)):
                    with self.subTest(word=word, container=type(value).__name__):
                        self.assertEqual(replay.formula(value), expected)
                count += 1
        self.assertEqual(count, 1022)

    def test_zero_words_have_observable_gap_zero(self):
        for n in range(1, 10):
            with self.subTest(n=n):
                self.assertEqual(replay.formula([0] * n), 0)
                self.assertEqual(replay.gap(replay.cyc(n), (0,) * n), 0)

    def test_one_words_have_gap_zero(self):
        for n in range(1, 10):
            with self.subTest(n=n):
                self.assertEqual(replay.formula([1] * n), 0)

    def test_empty_and_nonbinary_inputs_rejected(self):
        for invalid in ([], (), [2], [-1, 1], [0, 2, 1]):
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    replay.formula(invalid)

    def test_six_cycle_gap_two(self):
        word = [0, 0, 0, 1, 1, 1]
        self.assertEqual(replay.stable_size(replay.cyc(6), word), 6)
        self.assertEqual(replay.gap(replay.cyc(6), word), 2)
        self.assertEqual(replay.formula(word), 2)

    def test_existing_regression_fixtures(self):
        replay.check_regression_witnesses()


if __name__ == "__main__":
    unittest.main(verbosity=2)
