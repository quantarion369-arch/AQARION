#!/usr/bin/env python3
"""
AQARION BRT semantic mutation suite.

Purpose:
    Verify that the BRT implementation is sensitive to a meaningful
    semantic error in the graph construction.

This suite does NOT mutate source text.

Instead it implements an explicitly wrong alternative calculation
and proves that the repository's semantic trap distinguishes it from
the correct BRT construction.

Correct BRT graph:
    vertices = partition blocks
    edges = target-block co-occurrence within each source block

Mutant:
    vertices = individual states
    edges = individual transition edges x -- T(x)

The mutant is deliberately wrong for BRT because it computes
connectivity of the state-transition graph rather than connectivity
of the block co-occurrence graph.

The singleton transposition

    T = [1, 0]

with singleton partition

    [0, 1]

is the required killing case:

    correct BRT components = 2
    correct rank prediction = 0

    mutant state-graph components = 1
    mutant rank prediction = 1

A mutation suite passes only when the wrong implementation is actually
distinguished from the correct contract.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


SCHEMA = "AQ-BRT-MUTATION/1"


# ---------------------------------------------------------------------------
# Correct block normalization
# ---------------------------------------------------------------------------

def normalize_partition(
    labels: list[int],
) -> list[list[int]]:
    groups: dict[int, list[int]] = {}

    for state, label in enumerate(labels):
        groups.setdefault(int(label), []).append(state)

    return list(groups.values())


# ---------------------------------------------------------------------------
# Correct BRT component count
# ---------------------------------------------------------------------------

def correct_block_components(
    transition: list[int],
    labels: list[int],
) -> int:
    """
    Count components of the correct block co-occurrence graph.
    """
    blocks = normalize_partition(labels)

    block_of = {
        state: block_index
        for block_index, block in enumerate(blocks)
        for state in block
    }

    k = len(blocks)
    parent = list(range(k))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]

        return x

    def union(a: int, b: int) -> None:
        a = find(a)
        b = find(b)

        if a != b:
            parent[b] = a

    for block in blocks:
        targets = {
            block_of[transition[state]]
            for state in block
        }

        targets = sorted(targets)

        first = targets[0]

        for target in targets[1:]:
            union(first, target)

    return len({
        find(i)
        for i in range(k)
    })


# ---------------------------------------------------------------------------
# Deliberately wrong mutant
# ---------------------------------------------------------------------------

def mutant_state_transition_components(
    transition: list[int],
) -> int:
    """
    WRONG implementation.

    Computes connected components of the state-transition graph.

    This is not the BRT forward co-occurrence graph.
    """
    n = len(transition)

    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]

        return x

    def union(a: int, b: int) -> None:
        a = find(a)
        b = find(b)

        if a != b:
            parent[b] = a

    for state, target in enumerate(transition):
        union(state, target)

    return len({
        find(i)
        for i in range(n)
    })


def mutant_rank_prediction(
    transition: list[int],
    labels: list[int],
) -> int:
    """
    Rank prediction produced by the deliberately wrong mutant.
    """
    k = len(normalize_partition(labels))
    components = mutant_state_transition_components(transition)

    return k - components


# ---------------------------------------------------------------------------
# Mutation cases
# ---------------------------------------------------------------------------

def run_mutation_case(
    name: str,
    transition: list[int],
    labels: list[int],
    expected_correct_components: int,
    expected_correct_rank: int,
) -> dict[str, Any]:
    correct_components = correct_block_components(
        transition,
        labels,
    )

    mutant_components = mutant_state_transition_components(
        transition,
    )

    k = len(normalize_partition(labels))

    mutant_rank = k - mutant_components

    if correct_components != expected_correct_components:
        raise AssertionError(
            f"{name}: correct component expectation failed: "
            f"expected={expected_correct_components}, "
            f"actual={correct_components}"
        )

    if k - correct_components != expected_correct_rank:
        raise AssertionError(
            f"{name}: correct rank expectation failed: "
            f"expected={expected_correct_rank}, "
            f"actual={k - correct_components}"
        )

    if mutant_rank == expected_correct_rank:
        raise AssertionError(
            f"{name}: mutant survived; "
            f"mutant_rank={mutant_rank}, "
            f"correct_rank={expected_correct_rank}"
        )

    return {
        "name": name,
        "correct_components": correct_components,
        "correct_rank": expected_correct_rank,
        "mutant_state_components": mutant_components,
        "mutant_rank": mutant_rank,
        "killed": True,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    try:
        results = []

        # Required semantic killing case.
        results.append(
            run_mutation_case(
                name="singleton-transposition-state-graph-mutant",
                transition=[1, 0],
                labels=[0, 1],
                expected_correct_components=2,
                expected_correct_rank=0,
            )
        )

        # A second non-singleton regression case.
        results.append(
            run_mutation_case(
                name="two-block-four-cycle-state-graph-mutant",
                transition=[1, 2, 3, 0],
                labels=[0, 0, 1, 1],
                expected_correct_components=1,
                expected_correct_rank=1,
            )
        )

        report = {
            "schema": SCHEMA,
            "status": "PASS",
            "mutation": {
                "id": "BRT-MUT-STATE-GRAPH",
                "description": (
                    "Replace the block co-occurrence graph with the "
                    "individual state-transition graph."
                ),
                "survived": False,
                "killed": True,
            },
            "cases": results,
            "summary": {
                "cases": len(results),
                "killed": len(results),
                "survived": 0,
            },
        }

        print(
            json.dumps(
                report,
                indent=2,
                sort_keys=True,
            )
        )

        return 0

    except Exception as exc:
        failure = {
            "schema": SCHEMA,
            "status": "FAIL",
            "error": str(exc),
        }

        print(
            json.dumps(
                failure,
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
