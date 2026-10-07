#!/usr/bin/env python3
"""
FILE: AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/burnside_m3_recompute.py
TITLE: Burnside M3 Independent Recompute
PURPOSE: Independently recompute the recorded Burnside third moment and fail
         nonzero on any mismatch with burnside_m3.json.
REFERENCE: AQ-BURNSIDE-M3-001
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from functools import lru_cache
from itertools import permutations
from pathlib import Path


def integer_partitions(n, max_part=None):
    if n == 0:
        yield ()
        return

    max_part = min(n, max_part or n)

    for a in range(max_part, 0, -1):
        for rest in integer_partitions(n - a, a):
            yield (a,) + rest


def all_set_partitions(items):
    """
    Generate all set partitions of a finite tuple.

    Used only for the small-k independent control.
    It is NOT the production M3 engine.
    """
    items = tuple(items)

    if not items:
        yield ()
        return

    first, *rest = items

    for partition in all_set_partitions(rest):

        # first is its own block
        yield ((first,),) + partition

        # first joins each existing block
        for i in range(len(partition)):
            yield (
                partition[:i]
                + (tuple(sorted(partition[i] + (first,))),)
                + partition[i + 1:]
            )


def z_lambda(lam):
    """
    z_lambda = product_j j^(m_j) m_j!
    """
    counts = Counter(lam)

    z = 1

    for j, m in counts.items():
        z *= j ** m * math.factorial(m)

    return z


def representative_permutation(lam):
    """
    Construct a permutation having cycle type lam.
    """
    sigma = list(range(sum(lam)))

    start = 0

    for length in lam:
        for i in range(length):
            sigma[start + i] = start + ((i + 1) % length)

        start += length

    return tuple(sigma)


def invariant_partition(partition, sigma):
    """
    Test whether sigma maps the set partition to itself.
    """
    blocks = {
        frozenset(block)
        for block in partition
    }

    moved = {
        frozenset(sigma[x] for x in block)
        for block in partition
    }

    return moved == blocks


def direct_C(sigma):
    """
    Direct invariant-set-partition count.

    This is deliberately used only as a bounded independent control.
    """
    return sum(
        invariant_partition(partition, sigma)
        for partition in all_set_partitions(range(len(sigma)))
    )


@lru_cache(maxsize=None)
def recurrence_C(multiplicities):
    """
    Exact cycle-type recurrence for C(lambda).

    multiplicities[j-1] = number of cycles of length j.

    All arithmetic is integer arithmetic.
    """

    if not any(multiplicities):
        return 1

    # Choose one distinguished cycle.
    a = next(
        i + 1
        for i, m in enumerate(multiplicities)
        if m
    )

    remaining = list(multiplicities)

    remaining[a - 1] -= 1

    lengths = [
        i + 1
        for i, m in enumerate(remaining)
        if m
    ]

    total = 0

    def visit(pos, chosen, coefficient):
        nonlocal total

        if pos == len(lengths):

            occupied = [a] + [
                j
                for j, r in chosen.items()
                if r
            ]

            g = 0

            for j in occupied:
                g = math.gcd(g, j)

            block_size = 1 + sum(chosen.values())

            weight = sum(
                d ** (block_size - 1)
                for d in range(1, g + 1)
                if g % d == 0
            )

            remainder = tuple(
                remaining[j]
                - chosen.get(j + 1, 0)
                for j in range(len(remaining))
            )

            total += (
                coefficient
                * weight
                * recurrence_C(remainder)
            )

            return

        j = lengths[pos]

        available = remaining[j - 1]

        for r in range(available + 1):

            chosen[j] = r

            visit(
                pos + 1,
                chosen,
                coefficient * math.comb(available, r),
            )

        chosen.pop(j, None)

    visit(0, {}, 1)

    return total


def cycle_type_C(lam):
    """
    Compute C(lambda) from the exact cycle-type recurrence.
    """
    multiplicities = [0] * sum(lam)

    for j in lam:
        multiplicities[j - 1] += 1

    return recurrence_C(tuple(multiplicities))


def cycle_type_M3(k):
    """
    Exact Burnside third moment:

        M3(k)
          = sum_{lambda |- k}
            C(lambda)^3 / z_lambda

    Implemented using integer class multiplicities:

        number of permutations of type lambda
          = k! / z_lambda.

    Therefore the final division by k! is exact.
    """

    total = 0

    for lam in integer_partitions(k):

        total += (
            cycle_type_C(lam) ** 3
            * (math.factorial(k) // z_lambda(lam))
        )

    return total // math.factorial(k)


def direct_M3(k):
    """
    Direct permutation-level M3.

    Used only for small-k independent controls.
    """

    total = sum(
        direct_C(permutation) ** 3
        for permutation in permutations(range(k))
    )

    return total // math.factorial(k)


def fail(message):
    raise SystemExit(
        "VALIDATION_FAILURE: " + message
    )


def main():

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "record",
        nargs="?",
        default=str(
            Path(__file__).with_name("burnside_m3.json")
        ),
    )

    record_path = Path(
        parser.parse_args().record
    )

    record = json.loads(
        record_path.read_text(
            encoding="utf-8"
        )
    )

    if record["claim_id"] != "AQ-BURNSIDE-M3-001":
        fail("unexpected claim_id")

    if record["schema_version"] != "AQ-BURNSIDE-M3-001.v1":
        fail("unexpected schema_version")

    expected = record["results"]["M3"]

    if set(expected) != {
        str(k)
        for k in range(1, 32)
    }:
        fail(
            "recorded M3 domain is not exactly k=1..31"
        )

    # ------------------------------------------------------------
    # CONTROL A
    # Direct permutation-level M3.
    # ------------------------------------------------------------

    for k, expected_value in {
        1: 1,
        2: 8,
        3: 37,
        4: 285,
        5: 2150,
    }.items():

        got = direct_M3(k)

        if (
            got != expected_value
            or got != int(expected[str(k)])
        ):
            fail(
                f"direct M3 mismatch at k={k}: "
                f"got {got}, expected {expected_value}"
            )

    # ------------------------------------------------------------
    # CONTROL B
    # Direct invariant-partition C(lambda) versus
    # cycle-type recurrence for every lambda through k=6.
    # ------------------------------------------------------------

    for k in range(1, 7):

        for lam in integer_partitions(k):

            got_direct = direct_C(
                representative_permutation(lam)
            )

            got_recurrence = cycle_type_C(lam)

            if got_direct != got_recurrence:

                fail(
                    f"C(lambda) mismatch at lambda={lam}: "
                    f"direct={got_direct}, "
                    f"recurrence={got_recurrence}"
                )

    # ------------------------------------------------------------
    # PRIMARY CHECK
    # Independent cycle-type M3 recomputation through k=31.
    # ------------------------------------------------------------

    for k in range(1, 32):

        got = cycle_type_M3(k)

        if got != int(expected[str(k)]):

            fail(
                f"M3 mismatch at k={k}: "
                f"got {got}, "
                f"expected {expected[str(k)]}"
            )

    print("AQ-BURNSIDE-M3-001")
    print("JSON_INTEGRITY=PASS")
    print("DIRECT_PERMUTATION_M3_K1_5=PASS")
    print("DIRECT_CYCLE_TYPE_C_K1_6=PASS")
    print("CYCLE_TYPE_M3_K1_31=PASS")
    print("EXACT_INTEGER_ARITHMETIC=PASS")
    print("MISMATCHES=0")
    print("FORMALIZATION=OPEN")
    print("PROMOTION=BLOCKED")


if __name__ == "__main__":
    main()
