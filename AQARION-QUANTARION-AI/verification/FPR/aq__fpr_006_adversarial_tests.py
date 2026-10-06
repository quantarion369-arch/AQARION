

from math import gcd, lcm


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def weighted_block(cycle_lengths):
    g = 0
    for c in cycle_lengths:
        g = gcd(g, c)

    k = len(cycle_lengths)
    return sum(d ** (k - 1) for d in divisors(g))


def weighted_block_lcm_mutation(cycle_lengths):
    g = 1
    for c in cycle_lengths:
        g = lcm(g, c)

    k = len(cycle_lengths)
    return sum(d ** (k - 1) for d in divisors(g))


def weighted_block_exponent_mutation(cycle_lengths):
    g = 0
    for c in cycle_lengths:
        g = gcd(g, c)

    k = len(cycle_lengths)
    return sum(d ** k for d in divisors(g))


def weighted_block_no_phase_mutation(cycle_lengths):
    g = 0
    for c in cycle_lengths:
        g = gcd(g, c)

    return len(divisors(g))


def assert_mutation_gate():
    anchors = {
        (2, 2): 7,
        (3, 3): 8,
        (2, 4): 9,
        (2, 2, 2): 31,
        (2, 2, 2, 2): 164,
    }

    for cycle_type, expected in anchors.items():
        assert weighted_block(cycle_type) == expected

        if len(cycle_type) > 1:
            assert weighted_block_lcm_mutation(cycle_type) != expected
            assert weighted_block_no_phase_mutation(cycle_type) != expected

        assert weighted_block_exponent_mutation(cycle_type) != expected


def pb003_counterexample():
    """
    Counterexample to the OLD incorrect statement:

        q = |X/E|
        L = lcm(1,...,q)
        r = T^L

    need not be a retraction.
    """
    T = {
        0: 1,
        1: 2,
        2: 2,
    }

    # Universal E has one equivalence class, hence q = 1.
    q = 1
    L = 1

    assert q == 1
    assert T[T[0]] == 2
    assert T[0] == 1

    # Therefore T^2 != T.
    assert T[T[0]] != T[0]


def corrected_pb003_bound():
    """
    Correct bound:

        N = |X|
        L = lcm(1,...,N)

    This is large enough both to clear every transient tail
    and to be divisible by every possible cycle length.
    """
    for n in range(1, 11):
        L = 1
        for k in range(1, n + 1):
            L = lcm(L, k)

        assert L >= n - 1
        for cycle_length in range(1, n + 1):
            assert L % cycle_length == 0


if __name__ == "__main__":
    assert_mutation_gate()
    pb003_counterexample()
    corrected_pb003_bound()
    print("PB-006 ADVERSARIAL TESTS: PASS")
    print("PB-003 OLD QUOTIENT-BOUND: REFUTED")
    print("PB-003 CORRECTED STATE-SPACE-BOUND: VERIFIED FOR n<=10")
    print("C4: BLOCKED")
    print("PROMOTION: FALSE")
