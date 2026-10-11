"""AQ-FPR-006 adversarial tests.

The local weight W(B) and global invariant-partition count N(lambda)
are distinct quantities. This file tests them independently.

The brute-force partition oracle lives in fpr_enumerator.py; this
module's global_count uses a separate subset recurrence.

A passing mutation gate only establishes detection of the listed
mutations on at least one declared anchor. It does not establish
detection of every possible implementation error.
"""

from math import gcd, lcm


def divisors(n):
    """Return the positive divisors of positive integer n."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    return [d for d in range(1, n + 1) if n % d == 0]


def _gcd_of_lengths(cycle_lengths):
    """Return the gcd of a nonempty sequence of positive cycle lengths."""
    if not cycle_lengths:
        raise ValueError("cycle_lengths must be nonempty")

    g = 0
    for c in cycle_lengths:
        if not isinstance(c, int) or isinstance(c, bool) or c < 1:
            raise ValueError("cycle lengths must be positive integers")
        g = gcd(g, c)

    return g


def weighted_block(cycle_lengths):
    """Correct local weight W(B) = sum_{d | gcd(B)} d^(|B|-1)."""
    g = _gcd_of_lengths(cycle_lengths)
    k = len(cycle_lengths)
    return sum(d ** (k - 1) for d in divisors(g))


def weighted_block_lcm_mutation(cycle_lengths):
    """Deliberately incorrect mutation: use lcm instead of gcd."""
    if not cycle_lengths:
        raise ValueError("cycle_lengths must be nonempty")

    g = 1
    for c in cycle_lengths:
        if not isinstance(c, int) or isinstance(c, bool) or c < 1:
            raise ValueError("cycle lengths must be positive integers")
        g = lcm(g, c)

    k = len(cycle_lengths)
    return sum(d ** (k - 1) for d in divisors(g))


def weighted_block_exponent_mutation(cycle_lengths):
    """Deliberately incorrect mutation: use exponent |B|."""
    g = _gcd_of_lengths(cycle_lengths)
    k = len(cycle_lengths)
    return sum(d ** k for d in divisors(g))


def weighted_block_no_phase_mutation(cycle_lengths):
    """Deliberately incorrect mutation: omit the phase multiplicity."""
    g = _gcd_of_lengths(cycle_lengths)
    return len(divisors(g))


def global_count(cycle_type, local_weight=weighted_block):
    """Evaluate the global formula by a subset recurrence.

    For each nonempty set of cycle indices, choose the block containing
    its least index. This counts each set partition exactly once.

    This is a formula-side aggregation, not a brute-force enumeration
    of equivalence relations on the underlying points.
    """
    if not cycle_type:
        return 1

    for c in cycle_type:
        if not isinstance(c, int) or isinstance(c, bool) or c < 1:
            raise ValueError("cycle lengths must be positive integers")

    r = len(cycle_type)
    memo = {0: 1}

    def rec(mask):
        if mask in memo:
            return memo[mask]

        first = mask & -mask
        rest = mask ^ first
        total = 0
        sub = rest

        while True:
            block = sub | first
            lengths = tuple(
                cycle_type[i]
                for i in range(r)
                if block & (1 << i)
            )

            total += local_weight(lengths) * rec(mask ^ block)

            if sub == 0:
                break

            sub = (sub - 1) & rest

        memo[mask] = total
        return total

    return rec((1 << r) - 1)


def assert_local_anchors():
    """Check local W(B) values against local, not global, anchors."""
    local_anchors = {
        (2,): 2,
        (3,): 2,
        (2, 2): 3,
        (3, 3): 4,
        (2, 4): 3,
        (2, 2, 2): 5,
        (2, 2, 2, 2): 9,
    }

    for cycle_type, expected in local_anchors.items():
        actual = weighted_block(cycle_type)
        assert actual == expected, {
            "scope": "local",
            "cycle_type": cycle_type,
            "expected": expected,
            "actual": actual,
        }


def assert_global_anchors():
    """Check global N(lambda) values after set-partition aggregation."""
    global_anchors = {
        (2, 2): 7,
        (3, 3): 8,
        (2, 4): 9,
        (2, 2, 2): 31,
        (2, 2, 2, 2): 164,
    }

    for cycle_type, expected in global_anchors.items():
        actual = global_count(cycle_type)
        assert actual == expected, {
            "scope": "global",
            "cycle_type": cycle_type,
            "expected": expected,
            "actual": actual,
        }


def assert_mutation_gate():
    """Require every listed mutation to fail at least one proper anchor."""
    assert_local_anchors()
    assert_global_anchors()

    local_anchors = {
        (2,): 2,
        (3,): 2,
        (2, 2): 3,
        (3, 3): 4,
        (2, 4): 3,
        (2, 2, 2): 5,
        (2, 2, 2, 2): 9,
    }

    local_mutations = {
        "lcm": weighted_block_lcm_mutation,
        "exponent": weighted_block_exponent_mutation,
        "no_phase": weighted_block_no_phase_mutation,
    }

    for name, mutant in local_mutations.items():
        caught = any(
            mutant(cycle_type) != expected
            for cycle_type, expected in local_anchors.items()
        )
        assert caught, f"local mutation escaped all local anchors: {name}"

    global_anchors = {
        (2, 2): 7,
        (3, 3): 8,
        (2, 4): 9,
        (2, 2, 2): 31,
        (2, 2, 2, 2): 164,
    }

    global_mutations = {
        "lcm": lambda ct: global_count(
            ct, weighted_block_lcm_mutation
        ),
        "exponent": lambda ct: global_count(
            ct, weighted_block_exponent_mutation
        ),
        "no_phase": lambda ct: global_count(
            ct, weighted_block_no_phase_mutation
        ),
    }

    for name, mutant in global_mutations.items():
        caught = any(
            mutant(cycle_type) != expected
            for cycle_type, expected in global_anchors.items()
        )
        assert caught, f"global mutation escaped all global anchors: {name}"


def pb003_counterexample():
    """Retain the counterexample to the old quotient-bound statement.

    The old statement used q = |X/E| to define L = lcm(1,...,q)
    and asserted that T^L is a retraction. For the universal relation
    q = 1, but the example below has T(T(0)) != T(0).
    """
    transition = {
        0: 1,
        1: 2,
        2: 2,
    }

    q = 1
    period_bound = 1

    assert q == 1
    assert period_bound == 1
    assert transition[transition[0]] == 2
    assert transition[0] == 1
    assert transition[transition[0]] != transition[0]


def corrected_pb003_bound():
    """Check the state-space LCM bound for the declared finite test range.

    For N = |X|, L = lcm(1,...,N) is divisible by every possible
    cycle length in a map on N states and is at least N-1.
    This is a finite arithmetic check, not a proof about arbitrary N.
    """
    for n in range(1, 11):
        period_bound = 1

        for k in range(1, n + 1):
            period_bound = lcm(period_bound, k)

        assert period_bound >= n - 1

        for cycle_length in range(1, n + 1):
            assert period_bound % cycle_length == 0


def run_all():
    assert_local_anchors()
    assert_global_anchors()
    assert_mutation_gate()
    pb003_counterexample()
    corrected_pb003_bound()


if __name__ == "__main__":
    run_all()
    print("FPR-006 LOCAL WEIGHTS: PASS")
    print("FPR-006 GLOBAL COUNTS: PASS")
    print("FPR-006 MUTATION GATES: PASS")
    print("PB-003 OLD QUOTIENT-BOUND: REFUTED")
    print("PB-003 CORRECTED STATE-SPACE-BOUND: VERIFIED FOR n<=10")
    print("C4: BLOCKED")
    print("PROMOTION: FALSE")
