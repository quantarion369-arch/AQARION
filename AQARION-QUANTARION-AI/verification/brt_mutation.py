#!/usr/bin/env python3
"""
AQARION BRT semantic mutation suite.

Purpose:
    Verify that the BRT graph construction is sensitive to a deliberately
    wrong semantic substitution.

Correct BRT graph:
    vertices = partition blocks
    each source block connects all target blocks appearing in that source
    block's transition row.

Mutant graph:
    vertices = individual states
    edges = state -> T(state)

These are different mathematical objects. The mutation contract therefore
compares COMPONENT COUNTS ONLY.

The mutant is deliberately NOT assigned the BRT rank formula

    k - c(H)

because that formula is meaningful for the block co-occurrence graph,
where k is the number of partition-block vertices. The mutant graph has
n individual-state vertices, so reusing k for the mutant rank was
semantically invalid.

Mutation status:
    PASS means the declared mutant was killed.
    PASS is an executable mutation result, not a mathematical proof.
    NO PROMOTION AUTHORITY.
"""

from __future__ import annotations

import json
from typing import Any


SCHEMA = "AQ-BRT-MUTATION/3"


def normalize_partition(labels: list[int]) -> list[list[int]]:
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
    """Validate finite transition and partition inputs."""
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
    Count connected components of the correct BRT block graph.

    Vertices:
        partition blocks.

    Edges:
        target blocks that occur in the same source-block transition row.
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
        targets = sorted(
            {
                block_of[transition[state]]
                for state in block
            }
        )

        if not targets:
            raise AssertionError(
                "source block has no transition targets"
            )

        first = targets[0]

        for target in targets[1:]:
            union(first, target)

    return len({find(index) for index in range(k)})


def mutant_state_transition_components(
    transition: list[int],
) -> int:
    """
    Count connected components of the deliberately wrong state graph.

    Vertices:
        individual states.

    Edges:
        state -> T(state).

    This function intentionally computes ONLY the component count.
    It does not apply the BRT block-rank formula to this mutant graph.
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

    return len({find(index) for index in range(n)})


def run_mutation_case(
    *,
    name: str,
    transition: list[int],
    labels: list[int],
    expected_correct_components: int,
    expected_mutant_components: int,
) -> dict[str, Any]:
    """
    Execute one mutation-killing case under the component-only contract.
    """
    validate_inputs(transition, labels)

    blocks = normalize_partition(labels)
    block_count = len(blocks)

    correct_components = correct_block_components(
        transition,
        labels,
    )

    mutant_components = mutant_state_transition_components(
        transition,
    )

    if correct_components != expected_correct_components:
        raise AssertionError(
            f"{name}: incorrect correct-components expectation: "
            f"expected={expected_correct_components}, "
            f"actual={correct_components}"
        )

    if mutant_components != expected_mutant_components:
        raise AssertionError(
            f"{name}: incorrect mutant-components expectation: "
            f"expected={expected_mutant_components}, "
            f"actual={mutant_components}"
        )

    killed = mutant_components != correct_components

    if not killed:
        raise AssertionError(
            f"{name}: mutant component count survived"
        )

    return {
        "name": name,
        "state_count": len(transition),
        "block_count": block_count,
        "correct_components": correct_components,
        "mutant_state_components": mutant_components,
        "killed": True,
    }


def main() -> int:
    try:
        results = [
            run_mutation_case(
                name="singleton-transposition-state-graph-mutant",
                transition=[1, 0],
                labels=[0, 1],
                expected_correct_components=2,
                expected_mutant_components=1,
            ),
            run_mutation_case(
                name="constant-map-non-singleton-state-graph-mutant",
                transition=[0, 0, 0],
                labels=[0, 0, 1],
                expected_correct_components=2,
                expected_mutant_components=1,
            ),
        ]

        report = {
            "schema": SCHEMA,
            "status": "PASS",
            "mutation": {
                "id": "BRT-MUT-STATE-GRAPH",
                "description": (
                    "Replace the partition-block co-occurrence graph "
                    "with the individual state-transition graph."
                ),
                "contract": "component_count_only",
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
