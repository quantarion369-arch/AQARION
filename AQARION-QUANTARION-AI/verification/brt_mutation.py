#!/usr/bin/env python3
"""
AQARION BRT semantic mutation suite.

Purpose:
    Verify that the BRT graph construction is sensitive to a
    deliberately wrong semantic substitution.

The mutant replaces the BRT block co-occurrence graph with the
individual state-transition graph.

Correct BRT graph:
    vertices = partition blocks
    each source block connects all target blocks appearing in
    that source block's transition row

Mutant graph:
    vertices = individual states
    edges = state -> T(state)

These graphs are not the same mathematical object.

The suite therefore requires explicit killing cases where the
resulting component counts, and hence rank predictions, differ.

Governance:
    MUTATION PASS means the declared mutant was killed.
    MUTATION PASS is not a mathematical proof.
    NO PROMOTION AUTHORITY.
"""

from __future__ import annotations

import json
from typing import Any


SCHEMA = "AQ-BRT-MUTATION/2"


def normalize_partition(
    labels: list[int],
) -> list[list[int]]:
    """Convert integer labels into canonical partition blocks."""
    if not labels:
        raise AssertionError("partition must not be empty")

    groups: dict[int, list[int]] = {}

    for state, label in enumerate(labels):
        groups.setdefault(int(label), []).append(state)

    return list(groups.values())


def validate_inputs(
    transition: list[int],
    labels: list[int],
) -> None:
    """Validate the finite transition and partition inputs."""
    n = len(transition)

    if n == 0:
        raise AssertionError("transition must not be empty")

    if len(labels) != n:
        raise AssertionError(
            "partition label count must equal transition length"
        )

    for target in transition:
        if not 0 <= target < n:
            raise AssertionError(
                f"transition target {target} leaves state space"
            )


def correct_block_components(
    transition: list[int],
    labels: list[int],
) -> int:
    """
    Count components of the correct BRT block co-occurrence graph.
    """
    validate_inputs(transition, labels)

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
        root_a = find(a)
        root_b = find(b)

        if root_a != root_b:
            parent[root_b] = root_a

    for block in blocks:
        targets = sorted({
            block_of[transition[state]]
            for state in block
        })

        if not targets:
            raise AssertionError(
                "source block has no transition targets"
            )

        first = targets[0]

        for target in targets[1:]:
            union(first, target)

    return len({
        find(index)
        for index in range(k)
    })


def mutant_state_transition_components(
    transition: list[int],
) -> int:
    """
    DELIBERATELY WRONG MUTANT.

    Computes connected components of the individual
    state-transition graph instead of the BRT block
    co-occurrence graph.
    """
    if not transition:
        raise AssertionError("transition must not be empty")

    n = len(transition)
    parent = list(range(n))

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

    for state, target in enumerate(transition):
        union(state, target)

    return len({
        find(index)
        for index in range(n)
    })


def run_mutation_case(
    *,
    name: str,
    transition: list[int],
    labels: list[int],
    expected_correct_components: int,
    expected_correct_rank: int,
    expected_mutant_components: int,
    expected_mutant_rank: int,
) -> dict[str, Any]:
    """
    Execute one mutation-killing case.

    Every expected value is checked explicitly so that a broken
    test expectation cannot silently convert into a PASS.
    """
    validate_inputs(transition, labels)

    blocks = normalize_partition(labels)
    k = len(blocks)

    correct_components = correct_block_components(
        transition,
        labels,
    )

    mutant_components = mutant_state_transition_components(
        transition,
    )

    correct_rank = k - correct_components
    mutant_rank = k - mutant_components

    if correct_components != expected_correct_components:
        raise AssertionError(
            f"{name}: incorrect correct-components expectation: "
            f"expected={expected_correct_components}, "
            f"actual={correct_components}"
        )

    if correct_rank != expected_correct_rank:
        raise AssertionError(
            f"{name}: incorrect correct-rank expectation: "
            f"expected={expected_correct_rank}, "
            f"actual={correct_rank}"
        )

    if mutant_components != expected_mutant_components:
        raise AssertionError(
            f"{name}: incorrect mutant-components expectation: "
            f"expected={expected_mutant_components}, "
            f"actual={mutant_components}"
        )

    if mutant_rank != expected_mutant_rank:
        raise AssertionError(
            f"{name}: incorrect mutant-rank expectation: "
            f"expected={expected_mutant_rank}, "
            f"actual={mutant_rank}"
        )

    if mutant_components == correct_components:
        raise AssertionError(
            f"{name}: mutant component count survived"
        )

    if mutant_rank == correct_rank:
        raise AssertionError(
            f"{name}: mutant rank prediction survived"
        )

    return {
        "name": name,
        "state_count": len(transition),
        "block_count": k,
        "correct_components": correct_components,
        "correct_rank": correct_rank,
        "mutant_state_components": mutant_components,
        "mutant_rank": mutant_rank,
        "killed": True,
    }


def main() -> int:
    try:
        results = []

        results.append(
            run_mutation_case(
                name="singleton-transposition-state-graph-mutant",
                transition=[1, 0],
                labels=[0, 1],
                expected_correct_components=2,
                expected_correct_rank=0,
                expected_mutant_components=1,
                expected_mutant_rank=1,
            )
        )

        results.append(
            run_mutation_case(
                name="constant-map-non-singleton-state-graph-mutant",
                transition=[0, 0, 0],
                labels=[0, 0, 1],
                expected_correct_components=2,
                expected_correct_rank=0,
                expected_mutant_components=1,
                expected_mutant_rank=1,
            )
        )

        report = {
            "schema": SCHEMA,
            "status": "PASS",
            "mutation": {
                "id": "BRT-MUT-STATE-GRAPH",
                "description": (
                    "Replace the partition-block co-occurrence "
                    "graph with the individual state-transition "
                    "graph."
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
            )
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
