#!/usr/bin/env python3
"""
AQARION BRT independent validation kernel.

BRT = block-transition / forward co-occurrence defect-rank verification.

Governance:
    COMPUTED != PROVED
    PASS = this executable contract passed
    PASS != formal certification
    NO PROMOTION AUTHORITY
    NO CLAIM OF UNIVERSAL PROOF FROM FINITE CASES

This verifier uses exact rational arithmetic only.

For a finite deterministic transition

    T : X -> X

and a partition

    P = {B_0, ..., B_{k-1}},

define the normalized block-transition matrix Q by

    Q[i,j] =
        |{x in B_i : T(x) in B_j}| / |B_i|.

The forward co-occurrence graph H has the partition blocks as
vertices. Two target blocks occurring in the same row of Q are
connected.

Let c(H) be the number of connected components.

The verified finite identity is

    rank(D) = k - c(H),

where

    D = (I - P) K P

and P is the block-average projection while K is the deterministic
Koopman matrix.

The implementation independently computes both sides.

Case-file schema:

{
  "schema": "AQ-BRT-CASES-002",
  "cases": [
    {
      "name": "...",
      "transition": [0, ...],
      "partition": [0, 1, 1, 2, ...],
      "expected": {
        "rank_D": 0,
        "support_components": 3
      }
    }
  ]
}

The partition is represented by integer block labels. Labels need not
be consecutive; the verifier canonicalizes them.
"""

from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


SCHEMA = "AQ-BRT-VALIDATION/2"
CASE_SCHEMA = "AQ-BRT-CASES-002"


def rank_frac(matrix: list[list[Fraction]]) -> int:
    """Return exact matrix rank over Q."""
    if not matrix:
        return 0

    width = len(matrix[0])

    if any(len(row) != width for row in matrix):
        raise AssertionError("matrix is not rectangular")

    a = [list(map(Fraction, row)) for row in matrix]

    rows = len(a)
    cols = width
    rank = 0

    for col in range(cols):
        pivot = None

        for row in range(rank, rows):
            if a[row][col] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        pivot_value = a[rank][col]

        a[rank] = [
            value / pivot_value
            for value in a[rank]
        ]

        for row in range(rows):
            if row == rank:
                continue

            value = a[row][col]

            if value == 0:
                continue

            a[row] = [
                left - value * pivot
                for left, pivot in zip(a[row], a[rank])
            ]

        rank += 1

        if rank == rows:
            break

    return rank


def matmul(
    a: list[list[Fraction]],
    b: list[list[Fraction]],
) -> list[list[Fraction]]:
    """Exact matrix multiplication over Q."""
    if not a or not b:
        return []

    if len(a[0]) != len(b):
        raise AssertionError(
            "matrix multiplication dimension mismatch"
        )

    return [
        [
            sum(
                a[i][t] * b[t][j]
                for t in range(len(b))
            )
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def normalize_partition_labels(
    labels: list[int],
    n: int,
) -> list[list[int]]:
    """Convert integer block labels into canonical block lists."""
    if len(labels) != n:
        raise AssertionError(
            "partition label count must equal transition length"
        )

    if not labels:
        raise AssertionError("partition must contain at least one state")

    groups: dict[int, list[int]] = {}

    for state, label in enumerate(labels):
        groups.setdefault(int(label), []).append(state)

    return list(groups.values())


def validate_partition(
    transition: list[int],
    blocks: list[list[int]],
) -> None:
    """Require an exact partition of states 0..n-1."""
    n = len(transition)

    if n == 0:
        raise AssertionError("transition must contain at least one state")

    if not blocks:
        raise AssertionError("partition must be nonempty")

    flat = [
        state
        for block in blocks
        for state in block
    ]

    if sorted(flat) != list(range(n)):
        raise AssertionError(
            "partition is not an exact cover of states 0..n-1"
        )

    if len(set(flat)) != n:
        raise AssertionError(
            "partition contains duplicate states"
        )

    for block in blocks:
        if not block:
            raise AssertionError(
                "partition contains an empty block"
            )

    for target in transition:
        if not 0 <= target < n:
            raise AssertionError(
                f"transition target {target} leaves state space"
            )


def build_projection(
    blocks: list[list[int]],
    n: int,
) -> list[list[Fraction]]:
    """Orthogonal block-average projection."""
    p = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for block in blocks:
        weight = Fraction(1, len(block))

        for x in block:
            for y in block:
                p[x][y] = weight

    return p


def build_koopman(
    transition: list[int],
    n: int,
) -> list[list[Fraction]]:
    """Deterministic Koopman matrix."""
    k = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    for x, target in enumerate(transition):
        k[x][target] = Fraction(1)

    return k


def build_normalized_block_transition(
    transition: list[int],
    blocks: list[list[int]],
) -> list[list[Fraction]]:
    """Build the normalized block-transition matrix Q."""
    block_of: dict[int, int] = {}

    for index, block in enumerate(blocks):
        for state in block:
            block_of[state] = index

    k = len(blocks)

    q = [
        [Fraction(0) for _ in range(k)]
        for _ in range(k)
    ]

    for source_index, block in enumerate(blocks):
        denominator = len(block)

        for state in block:
            target_block = block_of[transition[state]]

            q[source_index][target_block] += Fraction(
                1,
                denominator,
            )

    return q


def validate_q_normalization(
    q: list[list[Fraction]],
) -> None:
    """Every source block must distribute total mass exactly one."""
    for row_index, row in enumerate(q):
        if sum(row) != Fraction(1):
            raise AssertionError(
                f"Q row {row_index} does not normalize to 1"
            )


def graph_components_from_q(
    q: list[list[Fraction]],
) -> int:
    """
    Count connected components of the forward co-occurrence graph.

    Each partition block is a vertex.
    """
    k = len(q)

    if k == 0:
        raise AssertionError("co-occurrence graph has no vertices")

    parent = list(range(k))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]

        return x

    def union(a: int, b: int) -> None:
        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            parent[root_b] = root_a

    for row_index, row in enumerate(q):
        targets = [
            target
            for target, weight in enumerate(row)
            if weight != 0
        ]

        if not targets:
            raise AssertionError(
                f"Q row {row_index} has empty support"
            )

        first = targets[0]

        for target in targets[1:]:
            union(first, target)

    return len({
        find(vertex)
        for vertex in range(k)
    })


def exact_defect_matrix(
    transition: list[int],
    blocks: list[list[int]],
) -> list[list[Fraction]]:
    """Return D = (I-P) K P exactly over Q."""
    n = len(transition)

    p = build_projection(blocks, n)
    k = build_koopman(transition, n)

    identity_minus_p = [
        [
            Fraction(int(row == col)) - p[row][col]
            for col in range(n)
        ]
        for row in range(n)
    ]

    return matmul(
        matmul(identity_minus_p, k),
        p,
    )


def exact_defect_rank(
    transition: list[int],
    blocks: list[list[int]],
) -> int:
    """Return rank(D) exactly over Q."""
    return rank_frac(
        exact_defect_matrix(
            transition,
            blocks,
        )
    )


def validate_case(
    case: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(case, dict):
        raise AssertionError("case must be a JSON object")

    if "transition" not in case:
        raise AssertionError("case missing 'transition'")

    if "partition" not in case:
        raise AssertionError("case missing 'partition'")

    transition = [
        int(value)
        for value in case["transition"]
    ]

    labels = [
        int(value)
        for value in case["partition"]
    ]

    blocks = normalize_partition_labels(
        labels,
        len(transition),
    )

    validate_partition(
        transition,
        blocks,
    )

    q = build_normalized_block_transition(
        transition,
        blocks,
    )

    validate_q_normalization(q)

    support_components = graph_components_from_q(q)

    rank_d = exact_defect_rank(
        transition,
        blocks,
    )

    k = len(blocks)
    expected_rank_from_graph = k - support_components

    if rank_d != expected_rank_from_graph:
        raise AssertionError(
            "BRT rank identity failed: "
            f"rank(D)={rank_d}, "
            f"k-c(H)={expected_rank_from_graph}"
        )

    if rank_d > k - 1:
        raise AssertionError(
            "universal finite rank bound failed: "
            f"rank(D)={rank_d} > {k - 1}"
        )

    expected = case.get("expected")

    if expected is not None:
        if not isinstance(expected, dict):
            raise AssertionError(
                "'expected' must be an object when supplied"
            )

        if "rank_D" in expected:
            declared_rank = int(expected["rank_D"])

            if declared_rank != rank_d:
                raise AssertionError(
                    "declared rank does not match recomputation: "
                    f"declared={declared_rank}, actual={rank_d}"
                )

        if "support_components" in expected:
            declared_components = int(
                expected["support_components"]
            )

            if declared_components != support_components:
                raise AssertionError(
                    "declared component count does not match "
                    f"recomputation: "
                    f"declared={declared_components}, "
                    f"actual={support_components}"
                )

    return {
        "name": str(case.get("name", "unnamed")),
        "n": len(transition),
        "k": k,
        "rank_D": rank_d,
        "support_components": support_components,
        "expected_rank_from_graph": expected_rank_from_graph,
    }


def semantic_controls() -> list[dict[str, Any]]:
    """Regression controls for the mathematical interpretation of H."""
    controls: list[dict[str, Any]] = []

    trap = {
        "name": "singleton-permutation-trap",
        "transition": [1, 0],
        "partition": [0, 1],
    }

    result = validate_case(trap)

    if result["rank_D"] != 0:
        raise AssertionError(
            "singleton permutation trap must have rank(D)=0"
        )

    if result["support_components"] != 2:
        raise AssertionError(
            "singleton permutation trap must have two "
            "co-occurrence components"
        )

    controls.append(result)

    trap = {
        "name": "constant-map-trap",
        "transition": [0, 0],
        "partition": [0, 1],
    }

    result = validate_case(trap)

    if result["rank_D"] != 0:
        raise AssertionError(
            "constant-map trap must have rank(D)=0"
        )

    controls.append(result)

    blocks = [
        [0, 1],
        [2, 3],
        [4, 5],
        [6, 7],
    ]

    transition = [
        0, 2,
        2, 4,
        4, 6,
        6, 0,
    ]

    labels = [0, 0, 1, 1, 2, 2, 3, 3]

    result = validate_case({
        "name": "rank-bound-attainment",
        "transition": transition,
        "partition": labels,
        "expected": {
            "rank_D": 3,
            "support_components": 1,
        },
    })

    if result["rank_D"] != 3:
        raise AssertionError(
            "rank-bound attaining construction failed"
        )

    if result["support_components"] != 1:
        raise AssertionError(
            "rank-bound attaining construction must be connected"
        )

    controls.append(result)

    return controls


def load_cases(path: Path) -> list[dict[str, Any]]:
    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    if not isinstance(data, dict):
        raise AssertionError(
            "BRT case file must be a JSON object"
        )

    schema = data.get("schema")

    if schema != CASE_SCHEMA:
        raise AssertionError(
            f"unsupported BRT case schema: {schema!r}; "
            f"expected {CASE_SCHEMA!r}"
        )

    cases = data.get("cases")

    if not isinstance(cases, list):
        raise AssertionError(
            "BRT case file must contain a list named 'cases'"
        )

    if not cases:
        raise AssertionError(
            "BRT case corpus must not be empty"
        )

    return cases


def main() -> int:
    parser = argparse.ArgumentParser(
        description="AQARION exact BRT validation"
    )

    parser.add_argument(
        "--cases",
        type=Path,
        required=True,
        help="BRT case corpus",
    )

    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        help="optional JSON report path",
    )

    args = parser.parse_args()

    try:
        controls = semantic_controls()
        cases = load_cases(args.cases)

        repository_results = []

        for index, case in enumerate(cases):
            result = validate_case(case)
            result["index"] = index
            repository_results.append(result)

        report = {
            "schema": SCHEMA,
            "case_schema": CASE_SCHEMA,
            "status": "PASS",
            "semantic_controls": controls,
            "repository_cases": repository_results,
            "summary": {
                "case_count": len(repository_results),
                "semantic_control_count": len(controls),
                "failures": 0,
            },
        }

        encoded = json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )

        print(encoded)

        if args.report is not None:
            args.report.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            args.report.write_text(
                encoded + "\n",
                encoding="utf-8",
            )

        return 0

    except Exception as exc:
        failure = {
            "schema": SCHEMA,
            "status": "FAIL",
            "error": str(exc),
        }

        encoded = json.dumps(
            failure,
            indent=2,
            sort_keys=True,
        )

        print(
            encoded,
            file=sys.stderr,
        )

        if args.report is not None:
            args.report.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            args.report.write_text(
                encoded + "\n",
                encoding="utf-8",
            )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
