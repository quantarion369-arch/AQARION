#!/usr/bin/env python3
"""SM003 exact-rational defect-rank and alternative audit.

Default scope is exhaustive over all maps and partitions for n = 1..4.
Use --max-n 5 for the larger census. The exact matrix arithmetic uses only
fractions.Fraction; no floating-point rank tolerance is used.

Mutation outcome vocabulary:
    DETECTED, NOT_DETECTED, NOT_RUN, INVALID_MUTANT.

A DETECTED result means the alternative's output differs from the baseline
on at least one enumerated case. It is not a proof about all finite systems.
"""
from __future__ import annotations

import argparse
import itertools
import json
import platform
import sys
from fractions import Fraction as F
from pathlib import Path


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
    return [
        [sum((x * y for x, y in zip(row, col)), F(0)) for col in bt]
        for row in a
    ]


def matrix_rank(a):
    """Exact rank over Q by Gauss-Jordan elimination."""
    if not a:
        return 0
    a = [list(map(F, row)) for row in a]
    if any(len(row) != len(a[0]) for row in a):
        raise ValueError("matrix is not rectangular")
    rows, cols, pivot_row = len(a), len(a[0]), 0
    for col in range(cols):
        pivot = next(
            (r for r in range(pivot_row, rows) if a[r][col]), None
        )
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        scale = a[pivot_row][col]
        a[pivot_row] = [v / scale for v in a[pivot_row]]
        for r in range(rows):
            if r == pivot_row or not a[r][col]:
                continue
            scale = a[r][col]
            a[r] = [
                x - scale * y for x, y in zip(a[r], a[pivot_row])
            ]
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
    if (
        sorted(flat) != list(range(n))
        or len(set(flat)) != n
        or any(not b for b in blocks)
    ):
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
    KP = matmul(K, P)
    return {
        "baseline_rank": baseline,
        "graph_prediction": prediction,
        "components": c,
        "block_count": k,
        "mutants": {
            "D:K^T": matrix_rank(transpose(K)),
            "D:[K,P]": matrix_rank(matsub(KP, matmul(P, K))),
            "D:(I-P)K": matrix_rank(matmul(matsub(I, P), K)),
            "D:PKP": matrix_rank(matmul(P, KP)),
            "D:(I-P)K^T": matrix_rank(matmul(matsub(I, P), transpose(K))),
            "D:KP(I-P)": matrix_rank(matmul(KP, matsub(I, P))),
            "R:ignore-isolated": k - component_count(k, images, touched),
            "R:preimage": k - component_count(k, preimage_groups),
            "R:c": c,
            "R:k-c-1": k - c - 1,
            "R:first": k - component_count(
                k, [[g[0]] for g in images if g]
            ),
            "R:c-only-variant": c,
        },
        "graph_details": {
            "images": images,
            "touched": touched,
            "preimage_groups": preimage_groups,
        },
    }


def run(max_n=4):
    if not 1 <= max_n <= 5:
        raise ValueError("max_n must be in 1..5")
    alias_of = {"R:c-only-variant": "R:c"}
    detection_counts: dict[str, int] = {}
    detection_sets: dict[str, set] = {}
    first_witness: dict[str, dict] = {}
    per_n: dict[str, dict] = {}
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
                    detection_counts[name] = (
                        detection_counts.get(name, 0) + int(detected)
                    )
                    if detected:
                        detection_sets.setdefault(name, set()).add(
                            (
                                n,
                                tuple(t),
                                tuple(tuple(b) for b in blocks),
                            )
                        )
                    if detected and name not in first_witness:
                        first_witness[name] = {
                            "n": n,
                            "transition": list(t),
                            "partition": blocks,
                            "baseline_rank": values["baseline_rank"],
                            "alternative_value": value,
                        }
        per_n[str(n)] = {
            "map_count": n ** n,
            "partition_map_pairs": cases_n,
            "expected_partition_map_pairs": n ** n * len(list(parts(n))),
            "theorem_mismatches": mismatch_n,
        }
    outcomes = {
        name: ("DETECTED" if count else "NOT_DETECTED")
        for name, count in detection_counts.items()
    }
    cluster_same_sets = (
        detection_sets.get("R:ignore-isolated", set())
        == detection_sets.get("R:preimage", set())
    )
    outcomes["R:ignore+preimage_cluster"] = (
        "DETECTED"
        if cluster_same_sets
        and detection_counts.get("R:ignore-isolated", 0)
        else "INVALID_MUTANT"
    )
    outcomes["R:c-only-variant"] = "INVALID_MUTANT"
    expected_total = sum(
        n ** n * len(list(parts(n))) for n in range(1, max_n + 1)
    )
    if total_cases != expected_total:
        raise AssertionError(
            f"enumeration incomplete: {total_cases} != {expected_total}"
        )
    return {
        "schema": "AQ-SM003-MUTATION-AUDIT/2",
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
        "mutation_aliases": alias_of,
        "ignore_preimage_cluster": {
            "same_detection_sets_in_executed_scope": cluster_same_sets,
            "ignore_isolated_detection_cases": len(
                detection_sets.get("R:ignore-isolated", set())
            ),
            "preimage_detection_cases": len(
                detection_sets.get("R:preimage", set())
            ),
        },
        "first_detection_witnesses": first_witness,
        "environment": {
            "python": sys.version,
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "interpretation": (
            "PASS checks the baseline matrix-rank identity on the "
            "declared finite scope only."
        ),
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
        failure = {
            "schema": "AQ-SM003-MUTATION-AUDIT/2",
            "status": "FAIL",
            "error": str(exc),
        }
        text = json.dumps(failure, indent=2, sort_keys=True) + "\n"
        print(text, file=sys.stderr, end="")
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(text, encoding="utf-8")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
