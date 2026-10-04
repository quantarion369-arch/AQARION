#!/usr/bin/env python3
"""
PB-CORE-005 — Cycle-Orbit Classification Verifier

FILE:
    PB-CORE/verify_cycle_classification.py

PURPOSE:
    Exact finite verification of:

    1. PB-CORE-005:
       The closed cycle-length/phase formula for invariant
       equivalence relations of finite permutations.

    2. PB-CORE-004:
       The restriction/extension bijection between pullback-fixed
       equivalences of a finite map and invariant equivalences on
       its eventual permutation core.

NO floating point arithmetic is used.

DEFAULT:
    Runs both verification suites for n <= 6.

IMPORTANT:
    A successful run is [V] evidence only.
    It does not constitute a formal Lean proof or repository CI
    certification.
"""

from __future__ import annotations

from itertools import permutations, product
from math import gcd
from functools import reduce
import sys


MAX_N = 6


# ---------------------------------------------------------------------------
# Set partitions
# ---------------------------------------------------------------------------

def set_partitions(n: int):
    """
    Generate all set partitions of {0,...,n-1} as restricted-growth
    label tuples.

    Example for n=3:
        (0,0,0)
        (0,0,1)
        (0,1,0)
        (0,1,1)
        (0,1,2)
    """
    if n == 0:
        yield ()
        return

    labels = [0] * n

    def rec(i: int, current_max: int):
        if i == n:
            yield tuple(labels)
            return

        for value in range(current_max + 2):
            labels[i] = value
            yield from rec(i + 1, max(current_max, value))

    labels[0] = 0
    yield from rec(1, 0)


def partition_count(n: int) -> int:
    return sum(1 for _ in set_partitions(n))


# ---------------------------------------------------------------------------
# Permutations and cycles
# ---------------------------------------------------------------------------

def cycle_lengths(perm):
    """Return the cycle lengths of a permutation."""
    n = len(perm)
    seen = [False] * n
    lengths = []

    for start in range(n):
        if seen[start]:
            continue

        x = start
        length = 0

        while not seen[x]:
            seen[x] = True
            x = perm[x]
            length += 1

        lengths.append(length)

    lengths.sort()
    return tuple(lengths)


def divisors(n: int):
    """Return all positive divisors of n."""
    out = []
    for d in range(1, n + 1):
        if n % d == 0:
            out.append(d)
    return out


def gcd_many(values):
    return reduce(gcd, values)


# ---------------------------------------------------------------------------
# Formula
# ---------------------------------------------------------------------------

def component_weight(component, lengths):
    """
    For a connected component S of cycle indices:

        sum_{d | gcd(m_i : i in S)} d^(|S|-1)
    """
    component_lengths = [lengths[i] for i in component]
    g = gcd_many(component_lengths)
    k = len(component)

    return sum(d ** (k - 1) for d in divisors(g))


def cycle_formula(lengths):
    """
    Exact PB-CORE-005 formula:

        sum_{set partitions S of cycle indices}
            product_{component S}
                sum_{d | gcd(m_i : i in S)} d^(|S|-1)
    """
    r = len(lengths)

    total = 0

    for labels in set_partitions(r):
        components = {}

        for i, label in enumerate(labels):
            components.setdefault(label, []).append(i)

        value = 1

        for component in components.values():
            value *= component_weight(component, lengths)

        total += value

    return total


# ---------------------------------------------------------------------------
# Partition invariance
# ---------------------------------------------------------------------------

def partition_is_invariant_under_map(labels, mapping):
    """
    Check the forward congruence condition:

        x E y => T(x) E T(y)

    where labels encode E.
    """
    n = len(mapping)

    for x in range(n):
        for y in range(x + 1, n):
            if labels[x] == labels[y]:
                if labels[mapping[x]] != labels[mapping[y]]:
                    return False

    return True


def partition_is_pullback_fixed(labels, mapping):
    """
    Check exact equality T*E = E.

    E:
        labels[x] == labels[y]

    T*E:
        labels[T(x)] == labels[T(y)]
    """
    n = len(mapping)

    for x in range(n):
        for y in range(x + 1, n):
            left = labels[x] == labels[y]
            right = labels[mapping[x]] == labels[mapping[y]]

            if left != right:
                return False

    return True


# ---------------------------------------------------------------------------
# Test A: every permutation n <= 6
# ---------------------------------------------------------------------------

def verify_permutations(max_n=MAX_N):
    total_permutations = 0
    total_mismatches = 0

    print("=" * 72)
    print("PB-CORE-005 TEST A — PERMUTATION FORMULA")
    print("=" * 72)

    for n in range(1, max_n + 1):
        partitions = list(set_partitions(n))
        checked = 0
        mismatches = 0

        for perm in permutations(range(n)):
            checked += 1
            total_permutations += 1

            brute_count = sum(
                1
                for labels in partitions
                if partition_is_invariant_under_map(labels, perm)
            )

            lengths = cycle_lengths(perm)
            formula_count = cycle_formula(lengths)

            if brute_count != formula_count:
                mismatches += 1
                total_mismatches += 1

                print(
                    "MISMATCH:",
                    "n=", n,
                    "perm=", perm,
                    "cycles=", lengths,
                    "brute=", brute_count,
                    "formula=", formula_count,
                )

        print(
            f"n={n}: permutations={checked}, "
            f"mismatches={mismatches}"
        )

    print()
    print("TOTAL PERMUTATIONS:", total_permutations)
    print("TOTAL MISMATCHES:", total_mismatches)

    return total_mismatches == 0


# ---------------------------------------------------------------------------
# Finite maps and eventual core
# ---------------------------------------------------------------------------

def image_of_map(mapping):
    return frozenset(mapping)


def image_iterate(mapping, subset):
    return frozenset(mapping[x] for x in subset)


def periodic_core(mapping):
    """
    Compute the eventual image/core P.

    Starting with X, repeatedly apply T to the whole current set
    until the image stabilizes.
    """
    current = frozenset(range(len(mapping)))

    while True:
        nxt = image_iterate(mapping, current)

        if nxt == current:
            return nxt

        current = nxt


def iterate_point(mapping, x, h):
    for _ in range(h):
        x = mapping[x]
    return x


def core_height(mapping, core):
    """
    Find the least h for which T^h(X)=core.
    """
    current = frozenset(range(len(mapping)))
    h = 0

    while current != core:
        current = image_iterate(mapping, current)
        h += 1

    return h


def relabel_partition(labels, points):
    """
    Restrict a partition encoded on X to an ordered point list.

    Returns canonical restricted labels.
    """
    first_label_to_new = {}
    result = []

    for x in points:
        old = labels[x]

        if old not in first_label_to_new:
            first_label_to_new[old] = len(first_label_to_new)

        result.append(first_label_to_new[old])

    return tuple(result)


def core_partition_is_invariant(core_labels, core_points, mapping):
    """
    Check invariance of a partition of the periodic core.
    """
    index = {x: i for i, x in enumerate(core_points)}

    core_mapping = tuple(
        index[mapping[x]]
        for x in core_points
    )

    return partition_is_invariant_under_map(core_labels, core_mapping)


def extend_core_partition(core_labels, core_points, mapping, h):
    """
    Extend a core equivalence to X by:

        x E y iff T^h(x) F T^h(y).
    """
    index = {x: i for i, x in enumerate(core_points)}

    def core_label(x):
        return core_labels[index[x]]

    return tuple(
        core_label(iterate_point(mapping, x, h))
        for x in range(len(mapping))
    )


def canonical_labels(labels):
    """
    Canonicalize arbitrary class labels into restricted-growth labels.
    """
    translation = {}
    result = []

    for value in labels:
        if value not in translation:
            translation[value] = len(translation)

        result.append(translation[value])

    return tuple(result)


def stable_partition_count(mapping):
    return sum(
        1
        for labels in set_partitions(len(mapping))
        if partition_is_pullback_fixed(labels, mapping)
    )


# ---------------------------------------------------------------------------
# Test B: every finite map n <= 6
# ---------------------------------------------------------------------------

def verify_core_restriction_extension(max_n=MAX_N):
    total_maps = 0
    restriction_failures = 0
    extension_failures = 0
    surjectivity_failures = 0

    aggregate_counts = {}

    print()
    print("=" * 72)
    print("PB-CORE-004 TEST B — FINITE-MAP CORE BIJECTION")
    print("=" * 72)

    for n in range(1, max_n + 1):
        partitions = list(set_partitions(n))

        checked_maps = 0
        n_restriction_failures = 0
        n_extension_failures = 0
        n_surjectivity_failures = 0
        aggregate = 0

        for mapping in product(range(n), repeat=n):
            checked_maps += 1
            total_maps += 1

            core = periodic_core(mapping)
            core_points = tuple(sorted(core))
            h = core_height(mapping, core)

            stable_labels = []

            for labels in partitions:
                if partition_is_pullback_fixed(labels, mapping):
                    stable_labels.append(labels)

            aggregate += len(stable_labels)

            # Every stable E must equal the extension of E|P.
            for labels in stable_labels:
                restricted = relabel_partition(labels, core_points)

                extended = extend_core_partition(
                    restricted,
                    core_points,
                    mapping,
                    h,
                )

                if canonical_labels(extended) != canonical_labels(labels):
                    restriction_failures += 1
                    n_restriction_failures += 1

            # Every invariant core partition must extend to a stable
            # partition on X.
            core_size = len(core_points)

            for core_labels in set_partitions(core_size):
                if not core_partition_is_invariant(
                    core_labels,
                    core_points,
                    mapping,
                ):
                    continue

                extended = extend_core_partition(
                    core_labels,
                    core_points,
                    mapping,
                    h,
                )

                if not partition_is_pullback_fixed(
                    extended,
                    mapping,
                ):
                    extension_failures += 1
                    n_extension_failures += 1

                # Verify that the extension restricts back to the
                # original core partition.
                restricted_back = relabel_partition(
                    extended,
                    core_points,
                )

                if restricted_back != canonical_labels(core_labels):
                    surjectivity_failures += 1
                    n_surjectivity_failures += 1

        aggregate_counts[n] = aggregate

        print(
            f"n={n}: maps={checked_maps}, "
            f"restriction_failures={n_restriction_failures}, "
            f"extension_failures={n_extension_failures}, "
            f"surjectivity_failures={n_surjectivity_failures}, "
            f"aggregate_stable_equivalences={aggregate}"
        )

    print()
    print("TOTAL MAPS:", total_maps)
    print("RESTRICTION FAILURES:", restriction_failures)
    print("EXTENSION FAILURES:", extension_failures)
    print("SURJECTIVITY FAILURES:", surjectivity_failures)
    print("AGGREGATE COUNTS:", aggregate_counts)

    expected_maps = sum(n ** n for n in range(1, max_n + 1))

    if total_maps != expected_maps:
        print(
            "INTERNAL ERROR: map census mismatch:",
            total_maps,
            expected_maps,
        )
        return False

    return (
        restriction_failures == 0
        and extension_failures == 0
        and surjectivity_failures == 0
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ok_perm = verify_permutations(MAX_N)
    ok_maps = verify_core_restriction_extension(MAX_N)

    print()
    print("=" * 72)
    print("FINAL RESULT")
    print("=" * 72)

    print("Permutation formula:", "PASS" if ok_perm else "FAIL")
    print("Finite-map core bijection:", "PASS" if ok_maps else "FAIL")

    if ok_perm and ok_maps:
        print()
        print("[V] Exact finite verification completed with zero failures.")
        print(
            "This is verification evidence only; Lean and repository "
            "certification remain separate."
        )
        return 0

    print()
    print("[V] FAILURE: at least one verification suite failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
