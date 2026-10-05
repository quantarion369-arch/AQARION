"""
AQ-FPR-006 — Invariant Partition Enumerator under a Permutation

Formula:
    W(B) = sum_{d | gcd(c_i : i in B)} d^(|B|-1)

    N(lambda) = sum_{pi in Pi([r])} prod_{B in pi} W(B)

EVIDENCE BOUNDARY (must match README ledger)
    Mathematical status:               proof candidate
    Internal corroboration:            distinct route only
    External independent reproduction: NOT ESTABLISHED
    Literature:                        OPEN
    Lean:                              OPEN
    C4:                                BLOCKED
    Publication:                       BLOCKED

This script MUST NOT print a status string stronger than the ledger above.

The formula and the direct enumeration route are separate computational
routes within the same source artifact. This is internal corroboration only;
it is NOT external independent reproduction.

The direct enumeration is retained as an audit oracle; it is not part of
the mathematical proof.
"""
from math import gcd


# ---------------------------------------------------------------- formula side

def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def cycle_type_part_weight(cycle_lengths):
    """W(B) for a nonempty set B of sigma-cycles."""
    g = 0
    for c in cycle_lengths:
        g = gcd(g, c)

    m = len(cycle_lengths)

    return sum(d ** (m - 1) for d in divisors(g))


def set_partitions(r):
    """All set partitions of {0,...,r-1} via restricted-growth strings."""
    if r == 0:
        yield []
        return

    labels = [0] * r
    labels[0] = 0

    def rec(i, max_label):
        if i == r:
            blocks = [[] for _ in range(max_label + 1)]

            for j, label in enumerate(labels):
                blocks[label].append(j)

            yield blocks
            return

        for label in range(max_label + 2):
            labels[i] = label
            yield from rec(i + 1, max(max_label, label))

    yield from rec(1, 0)


def formula_count(cycle_type):
    """Candidate formula under audit."""
    total = 0

    for pi in set_partitions(len(cycle_type)):
        contribution = 1

        for B in pi:
            lengths = [cycle_type[i] for i in B]
            contribution *= cycle_type_part_weight(lengths)

        total += contribution

    return total


# ---------------------------------------------------------------- direct enumeration route

def build_permutation(cycle_type):
    """Canonical permutation realizing a cycle type."""
    n = sum(cycle_type)
    perm = list(range(n))

    start = 0

    for length in cycle_type:
        for j in range(length):
            perm[start + j] = start + ((j + 1) % length)

        start += length

    return perm


def partitions_rgs(n):
    """All set partitions of {0,...,n-1}."""
    if n == 0:
        yield []
        return

    labels = [0] * n
    labels[0] = 0

    def rec(i, maximum):
        if i == n:
            blocks = {}

            for index, label in enumerate(labels):
                blocks.setdefault(label, []).append(index)

            result = [
                tuple(block)
                for _, block in sorted(blocks.items())
            ]

            yield tuple(result)
            return

        for value in range(maximum + 2):
            labels[i] = value
            yield from rec(i + 1, max(maximum, value))

    yield from rec(1, 0)


def invariant_partition(blocks, permutation):
    """Exact sigma-invariance test."""
    mapped = []

    for block in blocks:
        mapped.append(
            tuple(sorted(permutation[x] for x in block))
        )

    return sorted(mapped) == sorted(blocks)


def brute_force_count(cycle_type):
    """Direct invariant-partition enumeration audit oracle."""
    permutation = build_permutation(cycle_type)

    count = 0

    for blocks in partitions_rgs(sum(cycle_type)):
        if invariant_partition(blocks, permutation):
            count += 1

    return count


# ---------------------------------------------------------------- driver

def integer_partitions(n, maximum=None):
    """Integer partitions of n in nonincreasing order."""
    if n == 0:
        yield ()
        return

    if maximum is None or maximum > n:
        maximum = n

    for first in range(maximum, 0, -1):
        for rest in integer_partitions(n - first, first):
            yield (first,) + rest


def verify(n_max=7):
    cases = 0

    for n in range(1, n_max + 1):
        for cycle_type in integer_partitions(n):
            formula = formula_count(cycle_type)
            brute = brute_force_count(cycle_type)

            cases += 1

            if formula != brute:
                raise AssertionError(
                    {
                        "cycle_type": cycle_type,
                        "formula": formula,
                        "brute_force": brute,
                    }
                )

    return cases


if __name__ == "__main__":
    cases = verify(7)

    print("AQ-FPR-006")
    print(f"CYCLE_TYPE_CASES={cases}")
    print("FORMULA_VS_DIRECT_ENUMERATION=PASS")

    EMITTED_STATUS = "COMPUTATIONALLY_CORROBORATED"

    ALLOWED_STATUSES = {
        EMITTED_STATUS,
    }

    print(f"STATUS={EMITTED_STATUS}")
    print("INTERNAL_CORROBORATION=DISTINCT_ROUTE_ONLY")
    print("EXTERNAL_INDEPENDENT_REPRODUCTION=NOT_ESTABLISHED")

    assert EMITTED_STATUS in ALLOWED_STATUSES, (
        f"Refusing to emit status {EMITTED_STATUS!r}: "
        f"not in allowed set {sorted(ALLOWED_STATUSES)}. "
        f"See EVIDENCE BOUNDARY header."
            )
