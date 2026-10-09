#!/usr/bin/env python3
"""Refactor SM003 mutation coverage, add BRT regression tests, and report findings.

Run from a checkout of quantarion369-arch/AQARION:
    python3 aqarion_sm003_brt_refactor.py --repo . --apply

The script is pinned by default to commit
20e7447b93ae356fb8c3a937cce56573909b0a84. It refuses to modify a different
revision unless --allow-other-revision is explicitly supplied. It never pushes
or commits. A successful local test run is not a certification claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PINNED_COMMIT = "20e7447b93ae356fb8c3a937cce56573909b0a84"
SM = Path("AQARION-QUANTARION-AI/verification/SM/SM003")
BRT = Path("AQARION-QUANTARION-AI/verification/BRT")
MANIFEST = SM / "manifest.json"
README = SM / "README.md"
MUTATIONS = SM / "mutations.py"
BRT_MUTATION = BRT / "brt_mutation.py"
REPORT = SM / "SM003-BRT-REFRACTOR-AUDIT.md"

MUTATIONS_SOURCE = r'''#!/usr/bin/env python3
"""SM003 exact-rational defect-rank and alternative audit.

Default scope is exhaustive over all maps and partitions for n=1..4.
Use --max-n 5 for the larger census. The exact matrix arithmetic uses only
fractions.Fraction; no floating-point rank tolerance is used.

Mutation outcome vocabulary: DETECTED, NOT_DETECTED, NOT_RUN, INVALID_MUTANT.
A DETECTED result means the alternative's output differs from the baseline on
at least one enumerated case. It is not a proof about all finite systems.
"""
from __future__ import annotations

import argparse
import itertools
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Callable


def parts(n: int):
    """Yield all set partitions of range(n) as lists of nonempty blocks."""
    if n < 1:
        raise ValueError("n must be positive")
    labels = [0] * n
    def visit(i: int, maximum: int):
        if i == n:
            groups = [[] for _ in range(maximum + 1)]
            for x, label in enumerate(labels):
                groups[label].append(x)
            yield groups
            return
        for label in range(maximum + 2):
            labels[i] = label
            yield from visit(i + 1, max(maximum, label))
    labels[0] = 0
    yield from visit(1, 0)


def zeros(rows: int, cols: int):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n: int):
    a = zeros(n, n)
    for i in range(n):
        a[i][i] = F(1)
    return a


def transpose(a):
    return [list(row) for row in zip(*a)]


def matadd(a, b):
    return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matsub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def matmul(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("incompatible matrix dimensions")
    bt = transpose(b)
    return [[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt] for row in a]


def matrix_rank(a):
    """Exact rank over Q by Gauss-Jordan elimination."""
    if not a:
        return 0
    a = [list(map(F, row)) for row in a]
    if any(len(row) != len(a[0]) for row in a):
        raise ValueError("matrix is not rectangular")
    rows, cols, pivot_row = len(a), len(a[0]), 0
    for col in range(cols):
        pivot = next((r for r in range(pivot_row, rows) if a[r][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v / scale for v in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not a[r][col]:
                continue
            scale = a[r][col]
            a[r] = [x - scale * y for x, y in zip(a[r], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def koopman(t):
    n = len(t)
    k = zeros(n, n)
    for x, target in enumerate(t):
        if not 0 <= target < n:
            raise ValueError("transition target outside state space")
        k[x][target] = F(1)
    return k


def projector(blocks, n):
    p = zeros(n, n)
    flat = [x for block in blocks for x in block]
    if sorted(flat) != list(range(n)) or len(set(flat)) != n or any(not b for b in blocks):
        raise ValueError("blocks must be an exact partition of the state space")
    for block in blocks:
        weight = F(1, len(block))
        for x in block:
            for y in block:
                p[x][y] = weight
    return p


def component_count(k: int, groups, vertices=None):
    parent = list(range(k))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    for group in groups:
        group = sorted(set(group))
        for x in group[1:]:
            union(group[0], x)
    nodes = list(range(k)) if vertices is None else list(vertices)
    return len({find(x) for x in nodes})


def graph_data(t, blocks):
    n, k = len(t), len(blocks)
    block_of = {x: i for i, b in enumerate(blocks) for x in b}
    images = [sorted({block_of[t[x]] for x in b}) for b in blocks]
    touched = sorted(set().union(*(set(s) for s in images)))
    preimages = [[] for _ in range(k)]
    for source, targets in enumerate(images):
        for target in targets:
            preimages[target].append(source)
    return k, images, touched, [g for g in preimages if g]


def case_values(t, blocks):
    n = len(t)
    K, P, I = koopman(t), projector(blocks, n), eye(n)
    D = matmul(matsub(I, P), matmul(K, P))
    k, images, touched, preimage_groups = graph_data(t, blocks)
    c = component_count(k, images)
    baseline = matrix_rank(D)
    prediction = k - c
    return {
        "baseline_rank": baseline,
        "graph_prediction": prediction,
        "components": c,
        "block_count": k,
        "mutants": {
            # Six declared D-level alternatives, computed as actual matrices.
            "D:K^T": matrix_rank(transpose(K)),
            "D:[K,P]": matrix_rank(matsub(KP := matmul(K, P), matmul(P, K))),
            "D:(I-P)K": matrix_rank(matmul(matsub(I, P), K)),
            "D:PKP": matrix_rank(matmul(P, matmul(K, P))),
            "D:(I-P)K^T": matrix_rank(matmul(matsub(I, P), transpose(K))),
            "D:KP(I-P)": matrix_rank(matmul(matmul(K, P), matsub(I, P))),
            # Graph-level alternatives.
            "R:ignore-isolated": k - component_count(k, images, touched),
            "R:preimage": k - component_count(k, preimage_groups),
            "R:c": c,
            "R:k-c-1": k - c - 1,
            "R:first": k - component_count(k, [[g[0]] for g in images if g]),
            # This expression duplicates R:c and is not distinct coverage.
            "R:c-only-variant": c,
        },
        "graph_details": {"images": images, "touched": touched, "preimage_groups": preimage_groups},
    }


def run(max_n=4):
    if not 1 <= max_n <= 5:
        raise ValueError("max_n must be in 1..5")
    alias_of = {"R:c-only-variant": "R:c"}
    detection_counts = {}
    detection_sets = {}
    first_witness = {}
    per_n = {}
    total_cases = 0
    mismatch_count = 0
    for n in range(1, max_n + 1):
        cases_n = 0
        mismatch_n = 0
        for t in itertools.product(range(n), repeat=n):
            for blocks in parts(n):
                values = case_values(list(t), blocks)
                cases_n += 1
                total_cases += 1
                if values["baseline_rank"] != values["graph_prediction"]:
                    mismatch_n += 1
                    mismatch_count += 1
                for name, value in values["mutants"].items():
                    if name in alias_of:
                        continue
                    detected = value != values["baseline_rank"]
                    detection_counts[name] = detection_counts.get(name, 0) + int(detected)
                    if detected:
                        detection_sets.setdefault(name, set()).add((n, tuple(t), tuple(tuple(b) for b in blocks)))
                    if detected and name not in first_witness:
                        first_witness[name] = {
                            "n": n, "transition": list(t), "partition": blocks,
                            "baseline_rank": values["baseline_rank"],
                            "alternative_value": value,
                        }
        per_n[str(n)] = {
            "map_count": n ** n,
            "partition_map_pairs": cases_n,
            "expected_partition_map_pairs": n ** n * len(list(parts(n))),
            "theorem_mismatches": mismatch_n,
        }
    outcomes = {}
    for name in detection_counts:
        outcomes[name] = "DETECTED" if detection_counts[name] else "NOT_DETECTED"
    cluster_same_sets = detection_sets.get("R:ignore-isolated", set()) == detection_sets.get("R:preimage", set())
    if cluster_same_sets:
        outcomes["R:ignore+preimage_cluster"] = "DETECTED" if detection_counts.get("R:ignore-isolated", 0) else "NOT_DETECTED"
    else:
        outcomes["R:ignore+preimage_cluster"] = "INVALID_MUTANT"
    outcomes["R:c-only-variant"] = "INVALID_MUTANT"
    expected_total = sum(n ** n * len(list(parts(n))) for n in range(1, max_n + 1))
    if total_cases != expected_total:
        raise AssertionError(f"enumeration incomplete: {total_cases} != {expected_total}")
    return {
        "schema": "AQ-SM003-MUTATION-AUDIT/2",
        "status": "PASS" if mismatch_count == 0 else "FAIL",
        "scope": {"n_min": 1, "n_max": max_n, "cases": total_cases, "expected_cases": expected_total},
        "per_n": per_n,
        "theorem_mismatch_count": mismatch_count,
        "mutation_detection_counts": detection_counts,
        "mutation_outcomes": outcomes,
        "mutation_aliases": alias_of,
        "ignore_preimage_cluster": {
            "same_detection_sets_in_executed_scope": cluster_same_sets,
            "ignore_isolated_detection_cases": len(detection_sets.get("R:ignore-isolated", set())),
            "preimage_detection_cases": len(detection_sets.get("R:preimage", set())),
        },
        "first_detection_witnesses": first_witness,
        "environment": {"python": sys.version, "implementation": platform.python_implementation(), "platform": platform.platform()},
        "interpretation": "PASS checks the baseline matrix-rank identity on the declared finite scope only.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        report = run(args.max_n)
        text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        print(text, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(text, encoding="utf-8")
        return 0 if report["status"] == "PASS" else 1
    except Exception as exc:
        failure = {"schema": "AQ-SM003-MUTATION-AUDIT/2", "status": "FAIL", "error": str(exc)}
        text = json.dumps(failure, indent=2, sort_keys=True) + "\n"
        print(text, file=sys.stderr, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(text, encoding="utf-8")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''

SM_TESTS = r'''import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sm003_mutations", HERE / "mutations.py")
sm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sm)

class SM003RegressionTests(unittest.TestCase):
    def test_partition_counts(self):
        self.assertEqual([len(list(sm.parts(n))) for n in range(1, 5)], [1, 2, 5, 15])

    def test_rank_identity_edge_cases(self):
        cases = [
            ([0, 1], [[0], [1]]),
            ([0, 0], [[0], [1]]),
            ([1, 2, 0], [[0], [1], [2]]),
            ([1, 1, 2], [[0], [1], [2]]),
            ([0, 2, 2, 0], [[0, 1], [2, 3]]),
        ]
        for transition, blocks in cases:
            with self.subTest(transition=transition, blocks=blocks):
                values = sm.case_values(transition, blocks)
                self.assertEqual(values["baseline_rank"], values["graph_prediction"])

    def test_all_declared_alternatives_have_outcomes(self):
        report = sm.run(2)
        expected = {
            "D:K^T", "D:[K,P]", "D:(I-P)K", "D:PKP", "D:(I-P)K^T",
            "D:KP(I-P)", "R:ignore-isolated", "R:preimage", "R:ignore+preimage_cluster",
            "R:c", "R:k-c-1", "R:first", "R:c-only-variant",
        }
        self.assertEqual(set(report["mutation_outcomes"]), expected)
        self.assertEqual(report["mutation_outcomes"]["R:c-only-variant"], "INVALID_MUTANT")

    def test_partition_label_permutation_invariance(self):
        t = [1, 1, 2]
        a = sm.case_values(t, [[0], [1], [2]])
        b = sm.case_values(t, [[2], [0], [1]])
        self.assertEqual(a["baseline_rank"], b["baseline_rank"])
        self.assertEqual(a["graph_prediction"], b["graph_prediction"])

    def test_census_completion_counts(self):
        expected = {1: 1, 2: 8, 3: 135, 4: 3840}
        for n, count in expected.items():
            self.assertEqual(n ** n * len(list(sm.parts(n))), count)

if __name__ == "__main__":
    unittest.main()
'''

BRT_TESTS = r'''import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("brt_validation", HERE / "brt_validation.py")
brt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(brt)
mut_spec = importlib.util.spec_from_file_location("brt_mutation", HERE / "brt_mutation.py")
brt_mutation = importlib.util.module_from_spec(mut_spec)
mut_spec.loader.exec_module(brt_mutation)

class BRTRegressionTests(unittest.TestCase):
    def test_semantic_controls(self):
        controls = brt.semantic_controls()
        self.assertEqual(len(controls), 3)
        self.assertEqual(controls[0]["support_components"], 2)
        self.assertEqual(controls[2]["rank_D"], 3)

    def test_isolated_vertices_are_counted(self):
        result = brt.validate_case({"transition": [0, 1, 2], "partition": [0, 1, 2]})
        self.assertEqual(result["support_components"], 3)
        self.assertEqual(result["rank_D"], 0)

    def test_noninjective_map(self):
        result = brt.validate_case({"transition": [1, 1, 2], "partition": [0, 1, 2]})
        self.assertEqual(result["rank_D"], result["expected_rank_from_graph"])

    def test_partition_label_permutation(self):
        a = brt.validate_case({"transition": [2, 0, 1, 3], "partition": [0, 0, 1, 1]})
        b = brt.validate_case({"transition": [2, 0, 1, 3], "partition": [9, 9, 4, 4]})
        self.assertEqual(a["rank_D"], b["rank_D"])
        self.assertEqual(a["support_components"], b["support_components"])

    def test_invalid_transition_rejected(self):
        with self.assertRaises(AssertionError):
            brt.validate_case({"transition": [0, 3], "partition": [0, 1]})

    def test_case_corpus(self):
        data = json.loads((HERE / "brt_cases.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema"], brt.CASE_SCHEMA)
        self.assertEqual(len(data["cases"]), 10)
        for case in data["cases"]:
            brt.validate_case(case)

    def test_state_graph_alternative_is_detected_on_both_witnesses(self):
        first = brt_mutation.inspect_case("singleton-transposition", [1, 0], [0, 1], 2, 1)
        second = brt_mutation.inspect_case("constant-map-with-two-blocks", [0, 0, 0], [0, 0, 1], 2, 1)
        self.assertEqual(first["outcome"], "DETECTED")
        self.assertEqual(second["outcome"], "DETECTED")

if __name__ == "__main__":
    unittest.main()
'''

BRT_MUTATION_SOURCE = r'''#!/usr/bin/env python3
"""BRT semantic alternative audit using explicit detection outcomes."""
from __future__ import annotations
import json
from typing import Any

SCHEMA = "AQ-BRT-MUTATION/4"

def normalize_partition(labels: list[int]) -> list[list[int]]:
    if not labels:
        raise AssertionError("partition must not be empty")
    groups: dict[int, list[int]] = {}
    for state, label in enumerate(labels):
        groups.setdefault(int(label), []).append(state)
    return list(groups.values())

def validate_inputs(transition: list[int], labels: list[int]) -> None:
    n = len(transition)
    if n == 0:
        raise AssertionError("transition must not be empty")
    if len(labels) != n:
        raise AssertionError("partition label count must equal transition length")
    for target in transition:
        if not 0 <= target < n:
            raise AssertionError(f"transition target {target} leaves state space")

def component_count(n: int, edges) -> int:
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
    return len({find(i) for i in range(n)})

def correct_block_components(transition: list[int], labels: list[int]) -> int:
    validate_inputs(transition, labels)
    blocks = normalize_partition(labels)
    block_of = {state: j for j, block in enumerate(blocks) for state in block}
    edges = []
    for block in blocks:
        targets = sorted({block_of[transition[x]] for x in block})
        edges.extend((targets[0], target) for target in targets[1:])
    return component_count(len(blocks), edges)

def state_graph_components(transition: list[int]) -> int:
    if not transition:
        raise AssertionError("transition must not be empty")
    n = len(transition)
    for target in transition:
        if not 0 <= target < n:
            raise AssertionError("transition target outside state space")
    return component_count(n, list(enumerate(transition)))

def inspect_case(name: str, transition: list[int], labels: list[int], expected_block: int, expected_state: int) -> dict[str, Any]:
    validate_inputs(transition, labels)
    block_components = correct_block_components(transition, labels)
    state_components = state_graph_components(transition)
    if block_components != expected_block or state_components != expected_state:
        raise AssertionError(f"{name}: expectation mismatch: block={block_components}, state={state_components}")
    detected = block_components != state_components
    if not detected:
        raise AssertionError(f"{name}: alternative not detected by this witness")
    return {"name": name, "state_count": len(transition), "block_count": len(set(labels)),
            "correct_block_components": block_components, "alternative_state_components": state_components,
            "outcome": "DETECTED"}

def main() -> int:
    try:
        cases = [
            inspect_case("singleton-transposition", [1, 0], [0, 1], 2, 1),
            inspect_case("constant-map-with-two-blocks", [0, 0, 0], [0, 0, 1], 2, 1),
        ]
        report = {"schema": SCHEMA, "status": "PASS", "alternative_id": "BRT-ALT-STATE-GRAPH",
                  "alternative": "Individual state-transition graph substituted for partition-block co-occurrence graph.",
                  "comparison_contract": "component_count_only", "cases": cases,
                  "summary": {"cases": len(cases), "detected": sum(c["outcome"] == "DETECTED" for c in cases),
                              "not_detected": sum(c["outcome"] == "NOT_DETECTED" for c in cases)}}
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"schema": SCHEMA, "status": "FAIL", "error": str(exc)}, indent=2, sort_keys=True))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''

SM_README = r'''# SM003 — Exact Defect-Rank Verification

**Status:** SOURCE_AUDIT_REQUIRED until a clean checkout run and revision-bound receipt are recorded.

## Mathematical claim

For a finite map `T : X -> X`, a partition `Pi={B_1,...,B_k}`, Koopman matrix `K`, and block-average orthogonal projection `P`, define `D=(I-P)KP`. Construct `H_Pi` with one vertex per partition block and join every pair of target blocks reached from a common source block. Include isolated vertices. The claim is `rank(D)=k-c(H_Pi)`.

The kernel constraints force block coefficients to agree along each edge of `H_Pi`; the restricted kernel therefore has dimension `c(H_Pi)`. Since `D=DP`, `rank(D)=k-c(H_Pi)`. This is the paper-level argument; code execution is a separate evidence category.

## Executable audit

`mutations.py` now uses `fractions.Fraction` throughout and implements six D-level matrix alternatives plus the graph-level alternatives declared in `manifest.json`. It records `DETECTED`, `NOT_DETECTED`, `NOT_RUN`, or `INVALID_MUTANT` outcomes. `R:c-only-variant` is explicitly marked `INVALID_MUTANT` because its implemented expression is identical to `R:c`; it is not counted as distinct coverage.

Default scope is exhaustive over all maps and partitions for `n=1..4`, totaling 3,984 map–partition pairs. The historical `n=3,4` total is 3,975; historical `n=3,4,5` total is 166,475. The old `mutations.py` evaluated graph alternatives only, so those historical totals do not substantiate D-level mutation coverage.

Run from the repository root:

```bash
python3 AQARION-QUANTARION-AI/verification/SM/SM003/mutations.py --max-n 4 --report AQARION-QUANTARION-AI/verification/SM/SM003/sm003-mutation-report.json
python3 -m unittest discover -s AQARION-QUANTARION-AI/verification/SM/SM003 -p 'test_sm003.py' -v
