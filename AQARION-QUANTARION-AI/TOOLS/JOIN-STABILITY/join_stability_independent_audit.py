#!/usr/bin/env python3
"""Independent finite census for JOIN-STABILITY.

For each n, enumerate all maps T : {0,...,n-1} -> {0,...,n-1}
and all equivalence relations on that set.

Count ordered pairs (E,F) for which both relations are pullback-stable,
then count cases where their join is not pullback-stable.

This is a finite computational check, not a proof for arbitrary finite
sets and not a Lean verification.
"""

from __future__ import annotations

import itertools
import json
import sys
from typing import Iterable

EXPECTED = {
    1: (1, 0),
    2: (10, 0),
    3: (117, 0),
    4: (1960, 0),
    5: (40385, 0),
    6: (1016496, 0),
}


def partitions(n: int) -> list[tuple[int, ...]]:
    """Return all set partitions as canonical restricted-growth labels."""
    if n < 1:
        raise ValueError("n must be at least 1")

    result: list[tuple[int, ...]] = []

    def visit(labels: list[int], largest: int) -> None:
        if len(labels) == n:
            result.append(tuple(labels))
            return

        for label in range(largest + 2):
            labels.append(label)
            visit(labels, max(largest, label))
            labels.pop()

    visit([0], 0)
    return result


def is_stable(t: tuple[int, ...], p: tuple[int, ...]) -> bool:
    """Check T^{-1}(E) subseteq E for partition E encoded by p."""
    n = len(t)
    for x in range(n):
        for y in range(x + 1, n):
            if p[t[x]] == p[t[y]] and p[x] != p[y]:
                return False
    return True


def join_partition(
    p: tuple[int, ...], q: tuple[int, ...]
) -> tuple[int, ...]:
    """Compute the equivalence-relation join E_p join E_q."""
    n = len(p)
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[ry] = rx

    for labels in (p, q):
        first: dict[int, int] = {}
        for x, label in enumerate(labels):
            if label in first:
                union(x, first[label])
            else:
                first[label] = x

    roots = [find(x) for x in range(n)]
    renumber: dict[int, int] = {}
    canonical: list[int] = []
    for root in roots:
        if root not in renumber:
            renumber[root] = len(renumber)
        canonical.append(renumber[root])
    return tuple(canonical)


def audit_n(n: int) -> tuple[int, int]:
    """Return (ordered stable-pair count, join-failure count)."""
    ps = partitions(n)

    # Cache joins for every ordered partition pair, independent of T.
    joins = [
        [join_partition(p, q) for q in ps]
        for p in ps
    ]

    stable_pair_count = 0
    join_failure_count = 0

    for t in itertools.product(range(n), repeat=n):
        stable_indices = [
            i for i, p in enumerate(ps) if is_stable(t, p)
        ]

        stable_pair_count += len(stable_indices) ** 2

        for i in stable_indices:
            for j in stable_indices:
                joined = joins[i][j]
                if not is_stable(t, joined):
                    join_failure_count += 1

    return stable_pair_count, join_failure_count


def main() -> int:
    all_ok = True

    for n, expected in EXPECTED.items():
        observed = audit_n(n)
        passed = observed == expected
        all_ok = all_ok and passed

        print(json.dumps({
            "n": n,
            "ordered_stable_relation_pairs": observed[0],
            "join_stability_failures": observed[1],
            "expected": {
                "ordered_stable_relation_pairs": expected[0],
                "join_stability_failures": expected[1],
            },
            "match": passed,
        }, sort_keys=True))

        if not passed:
            print(
                f"AUDIT_MISMATCH n={n}: "
                f"observed={observed}, expected={expected}",
                file=sys.stderr,
            )

    print("AUDIT_RESULT=" + ("PASS" if all_ok else "FAIL"))
    print("AUDIT_SCOPE=FINITE_ENUMERATION_ONLY")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
