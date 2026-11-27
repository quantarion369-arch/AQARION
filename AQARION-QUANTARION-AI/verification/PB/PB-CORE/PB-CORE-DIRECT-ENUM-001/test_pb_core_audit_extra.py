import subprocess
import sys
import unittest
from itertools import product
from pathlib import Path
from unittest.mock import patch

import pb_core_audit as audit


SCRIPT = Path(audit.__file__).resolve()


class CanonicalPartitionTests(unittest.TestCase):
    def test_restricted_growth_labels_through_six(self):
        for n in range(1, 7):
            for labels in audit.partitions(n):
                with self.subTest(n=n, labels=labels):
                    self.assertEqual(len(labels), n)
                    self.assertEqual(labels[0], 0)
                    self.assertTrue(
                        all(type(label) is int for label in labels)
                    )
                    self.assertTrue(
                        all(label >= 0 for label in labels)
                    )

                    largest = labels[0]
                    for label in labels[1:]:
                        self.assertLessEqual(label, largest + 1)
                        largest = max(largest, label)

                    self.assertEqual(
                        set(labels),
                        set(range(largest + 1)),
                    )
                    self.assertEqual(
                        audit.normalize_labels(labels),
                        labels,
                    )

    def test_normalization_is_idempotent(self):
        examples = [
            (),
            (8,),
            (8, 8, 3, 9, 3),
            (4, 2, 4, 2),
        ]
        for labels in examples:
            with self.subTest(labels=labels):
                normalized = audit.normalize_labels(labels)
                self.assertEqual(
                    audit.normalize_labels(normalized),
                    normalized,
                )


class RoundTripTests(unittest.TestCase):
    def test_restriction_extension_round_trips_through_three(self):
        by_size = {
            n: tuple(audit.partitions(n))
            for n in range(1, 4)
        }

        for n in range(1, 4):
            for t in product(range(n), repeat=n):
                core, retraction, _ = audit.periodic_core(t)
                index = {
                    vertex: position
                    for position, vertex in enumerate(core)
                }
                core_map = tuple(index[t[v]] for v in core)

                for theta in by_size[len(core)]:
                    if not audit.is_pullback_fixed(core_map, theta):
                        continue

                    extended = audit.normalize_labels(
                        tuple(
                            theta[index[retraction[x]]]
                            for x in range(n)
                        )
                    )
                    restricted = audit.normalize_labels(
                        tuple(extended[v] for v in core)
                    )

                    with self.subTest(t=t, theta=theta):
                        self.assertEqual(restricted, theta)
                        self.assertTrue(
                            audit.is_pullback_fixed(t, extended)
                        )

                direct = audit.direct_relations(t, by_size[n])

                for relation in direct:
                    restricted = audit.normalize_labels(
                        tuple(relation[v] for v in core)
                    )
                    recovered = audit.normalize_labels(
                        tuple(
                            restricted[index[retraction[x]]]
                            for x in range(n)
                        )
                    )

                    with self.subTest(t=t, relation=relation):
                        self.assertEqual(recovered, relation)


class InputAndFailureTests(unittest.TestCase):
    def test_census_rejects_out_of_range_bounds(self):
        for bound in (-1, 0, 7):
            with self.subTest(bound=bound):
                with self.assertRaises(ValueError):
                    audit.census(bound)

    def test_empty_map_is_rejected(self):
        with self.assertRaises(ValueError):
            audit.periodic_core(())

    def test_formula_rejects_nonpositive_size(self):
        for n in (-1, 0):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    audit.aggregate_formula(n)

    def test_census_detects_injected_relation_mismatch(self):
        with patch.object(
            audit,
            "core_relations",
            return_value=(set(), {"injected_failure": True}),
        ):
            with self.assertRaisesRegex(
                AssertionError,
                "audit failed at n=1",
            ):
                audit.census(1)

    def test_cli_invalid_bound_returns_nonzero(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--max-n",
                "0",
            ],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=SCRIPT.parent,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ValueError", result.stderr)
        self.assertEqual(result.stdout.strip(), "")

    def test_injected_census_failure_returns_nonzero_process_exit(self):
        child_code = """
import runpy
import sys
from unittest.mock import patch

script = sys.argv[1]
original_run_path = runpy.run_path

def injected_run_path(path, *args, **kwargs):
    if str(path) == script and kwargs.get("run_name") == "__main__":
        namespace = original_run_path(path)

        def broken_core_relations(t, by_size):
            return set(), {"injected_failure": True}

        namespace["census"].__globals__["core_relations"] = (
            broken_core_relations
        )
        namespace["census"](1)
        return namespace

    return original_run_path(path, *args, **kwargs)

with patch.object(runpy, "run_path", injected_run_path):
    runpy.run_path(script, run_name="__main__")
"""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                child_code,
                str(SCRIPT),
            ],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=SCRIPT.parent,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("audit failed at n=1", result.stderr)
        self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
