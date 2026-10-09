#!/usr/bin/env python3
"""SM003 exact-rational defect-rank and mutation audit.

The true defect is D = (I-P) K P.

D-level mutants are Boolean zero-tests: a mutant is killed when its
zero/nonzero verdict disagrees with the independent closure oracle.

Graph-level mutants are candidate rank formulas: a mutant is killed
when its predicted rank differs from the exact matrix rank of D.

All matrix arithmetic and ranks use fractions.Fraction.
No NumPy or floating-point tolerances are used.

Evidence boundary:
  PASS means the baseline rank identity passed on the enumerated scope.
  It does not mean that every mutant was killed or that the theorem has
  been formally verified.
"""
from __future__ import annotations

import argparse
import itertools
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path


D_MUTANTS = (
    "D:K^T",
    "D:[K,P]",
    "D:(I-P)K",
    "D:PKP",
    "D:(I-P)K^T",
    "D:KP(I-P)",
)

R_MUTANTS = (
    "R:ignore-isolated",
    "R:preimage",
    "R:c",
    "R:k-c-1",
    "R:first",
)

INVALID_MUTANTS = {
    "R:c-only-variant": "Duplicates R:c; not a distinct mutant."
}


def parts(n: int):
    """Yield every set partition of range(n), in canonical label order."""
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
    result = zeros(n, n)
    for i in range(n):
        result[i][i] = F(1)
    return result


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    if len(a) != len(b) or any(
        len(x) != len(y) for x, y in zip(a, b)
    ):
        raise ValueError("incompatible matrix dimensions")
    return [[x + y for x, y in zip(rx, ry)]
            for rx, ry in zip(a, b)]


def sub(a, b):
    if len(a) != len(b) or any(
        len(x) != len(y) for x, y in zip(a, b)
    ):
        raise ValueError("incompatible matrix dimensions")
    return [[x - y for x, y in zip(rx, ry)]
            for rx, ry in zip(a, b)]


def mul(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError("incompatible matrix dimensions")
    bt = transpose(b)
    return [
        [
            sum((x * y for x, y in zip(row, col)), F(0))
            for col in bt
        ]
        for row in a
    ]


def iszero(a):
    return all(value == 0 for row in a for value in row)


def matrix_rank(a):
    """Exact rank over Q using Gauss-Jordan elimination."""
    if not a:
        return 0
    a = [list(map(F, row)) for row in a]
    if any(len(row) != len(a[0]) for row in a):
        raise ValueError("matrix is not rectangular")

    rows, cols = len(a), len(a[0])
    pivot_row = 0

    for col in range(cols):
        pivot = next(
            (r for r in range(pivot_row, rows) if a[r][col] != 0),
            None,
        )
        if pivot is None:
            continue

        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v / scale for v in a[pivot_row]]

        for r in range(rows):
            if r == pivot_row or a[r][col] == 0:
                continue
            scale = a[r][col]
            a[r] = [
                x - scale * y
                for x, y in zip(a[r], a[pivot_row])
            ]

        pivot_row += 1
        if pivot_row == rows:
            break

    return pivot_row


def validate_instance(t, blocks):
    """Validate a total self-map and an exact partition."""
    n = len(t)
    if n < 1:
        raise ValueError("state space must be nonempty")
    if any(not isinstance(y, int) or not 0 <= y < n for y in t):
        raise ValueError("transition target outside state space")
    flat = [x for block in blocks for x in block]
    if (
        not blocks
        or any(not block for block in blocks)
        or sorted(flat) != list(range(n))
        or len(set(flat)) != n
    ):
        raise ValueError("blocks must be an exact partition")


def koopman(t):
    """K[x,y] = 1 iff T(x)=y; row-vector convention."""
    n = len(t)
    k = zeros(n, n)
    for x, target in enumerate(t):
        k[x][target] = F(1)
    return k


def projector(blocks, n):
    """Orthogonal block-average projector."""
    p = zeros(n, n)
    for block in blocks:
        weight = F(1, len(block))
        for x in block:
            for y in block:
                p[x][y] = weight
    return p


def closed_oracle(t, blocks):
    """Independent combinatorial closure oracle; uses no matrices."""
    block_of = {
        x: i for i, block in enumerate(blocks) for x in block
    }
    return all(
        len({block_of[t[x]] for x in block}) == 1
        for block in blocks
    )


def component_count(k, groups, vertices=None):
    """Count components, optionally on an induced vertex subset."""
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
    """Build target-block co-occurrence and preimage data."""
    k = len(blocks)
    block_of = {
        x: i for i, block in enumerate(blocks) for x in block
    }
    images = [
        sorted({block_of[t[x]] for x in block})
        for block in blocks
    ]
    touched = sorted(set().union(*(set(group) for group in images)))
    preimages = [[] for _ in range(k)]

    for source, targets in enumerate(images):
        for target in targets:
            preimages[target].append(source)

    return k, images, touched, [g for g in preimages if g]


def case_values(t, blocks):
    """Evaluate the true defect and all canonical mutant alternatives."""
    validate_instance(t, blocks)

    n = len(t)
    K = koopman(t)
    P = projector(blocks, n)
    I = eye(n)
    Q = sub(I, P)

    # Canonical defect: D = (I-P) K P.
    D = mul(Q, mul(K, P))
    baseline_rank = matrix_rank(D)
    truth = closed_oracle(t, blocks)

    k, images, touched, preimage_groups = graph_data(t, blocks)
    components = component_count(k, images)
    graph_rank = k - components

    # D-level alternatives are predicates, not rank-valued mutants.
    d_tests = {
        "D:K^T": iszero(mul(Q, mul(transpose(K), P))),
        "D:[K,P]": iszero(sub(mul(K, P), mul(P, K))),
        "D:(I-P)K": iszero(mul(Q, K)),
        "D:PKP": iszero(mul(P, mul(K, P))),
        "D:(I-P)K^T": iszero(mul(Q, transpose(K))),
        "D:KP(I-P)": iszero(mul(mul(K, P), Q)),
    }

    # Graph-level alternatives are rank predictions, compared to rank(D).
    r_values = {
        "R:ignore-isolated":
            k - component_count(k, images, touched),
        "R:preimage":
            k - component_count(k, preimage_groups),
        "R:c": components,
        "R:k-c-1": k - components - 1,
        "R:first": k - component_count(
            k, [[group[0]] for group in images if group]
        ),
    }

    detected = set()
    for mutant, verdict in d_tests.items():
        if verdict != truth:
            detected.add(mutant)

    for mutant, predicted_rank in r_values.items():
        if predicted_rank != baseline_rank:
            detected.add(mutant)

    return {
        "baseline_rank": baseline_rank,
        "graph_prediction": graph_rank,
        "components": components,
        "block_count": k,
        "closure_truth": truth,
        "d_test_verdicts": d_tests,
        "graph_rank_predictions": r_values,
        "detected": sorted(detected),
        "graph_details": {
            "images": images,
            "touched": touched,
            "preimage_groups": preimage_groups,
        },
    }


def witness_instance(witness):
    """Read the repository manifest's witness object."""
    return (
        tuple(witness["f"]),
        [tuple(block) for block in witness["partition"]],
    )


def witness_detection_sets(manifest):
    """Recompute every witness kill set without trusting declarations."""
    result = {}
    for witness in manifest["witness_suite"]["instances"]:
        wid = witness["w"]
        t, blocks = witness_instance(witness)
        values = case_values(t, blocks)
        result[wid] = values["detected"]
    return result


def run(max_n=4):
    if not 1 <= max_n <= 5:
        raise ValueError("--max-n must be in 1..5")

    counts = {name: 0 for name in (*D_MUTANTS, *R_MUTANTS)}
    detection_counts = {name: 0 for name in (*D_MUTANTS, *R_MUTANTS)}
    first_witness = {}
    per_n = {}
    total_cases = 0
    mismatch_count = 0

    for n in range(1, max_n + 1):
        cases_n = 0
        mismatch_n = 0

        for t in itertools.product(range(n), repeat=n):
            for blocks in parts(n):
                values = case_values(t, blocks)
                cases_n += 1
                total_cases += 1

                if values["baseline_rank"] != values["graph_prediction"]:
                    mismatch_n += 1
                    mismatch_count += 1

                for mutant in (*D_MUTANTS, *R_MUTANTS):
                    counts[mutant] += 1
                    if mutant in values["detected"]:
                        detection_counts[mutant] += 1
                        first_witness.setdefault(
                            mutant,
                            {
                                "n": n,
                                "transition": list(t),
                                "partition": blocks,
                            },
                        )

        per_n[str(n)] = {
            "map_count": n ** n,
            "partition_map_pairs": cases_n,
            "expected_partition_map_pairs":
                n ** n * len(list(parts(n))),
            "theorem_mismatches": mismatch_n,
        }

    expected_total = sum(
        n ** n * len(list(parts(n))) for n in range(1, max_n + 1)
    )
    if total_cases != expected_total:
        raise AssertionError(
            f"enumeration incomplete: {total_cases} != {expected_total}"
        )

    outcomes = {
        name: ("DETECTED" if detection_counts[name] else "NOT_DETECTED")
        for name in detection_counts
    }
    outcomes.update({
        name: "INVALID_MUTANT" for name in INVALID_MUTANTS
    })

    return {
        "schema": "AQ-SM003-MUTATION-AUDIT/3",
        "status": "PASS" if mismatch_count == 0 else "FAIL",
        "scope": {
            "n_min": 1,
            "n_max": max_n,
            "cases": total_cases,
            "expected_cases": expected_total,
        },
        "per_n": per_n,
        "theorem_mismatch_count": mismatch_count,
        "mutation_detection_counts": detection_counts,
        "mutation_outcomes": outcomes,
        "mutation_semantics": {
            "D-level": "Kill iff zero-test verdict differs from closure truth.",
            "R-level": "Kill iff predicted rank differs from exact rank(D).",
            "invalid": INVALID_MUTANTS,
        },
        "first_detection_witnesses": first_witness,
        "environment": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "interpretation": (
            "PASS certifies only agreement between exact matrix rank and "
            "the graph prediction over this finite scope. It does not "
            "certify all mutation claims, a Lean proof, or a release."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=4)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    try:
        report = run(args.max_n)
        output = json.dumps(report, indent=2, sort_keys=True) + "\n"
        print(output, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(output, encoding="utf-8")
        return 0 if report["status"] == "PASS" else 1
    except Exception as exc:
        failure = {
            "schema": "AQ-SM003-MUTATION-AUDIT/3",
            "status": "FAIL",
            "error": str(exc),
        }
        output = json.dumps(failure, indent=2, sort_keys=True) + "\n"
        print(output, file=sys.stderr, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(output, encoding="utf-8")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
