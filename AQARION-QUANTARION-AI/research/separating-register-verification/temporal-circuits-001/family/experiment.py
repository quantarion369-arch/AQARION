import hashlib
import itertools as it
import json
import math
import os
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

OUT = Path(os.environ["AQARION_FAMILY_RUN"])
START = time.monotonic()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rank_integer(columns, n):
    basis = {}

    for column in columns:
        v = list(column)

        for pivot, b in sorted(basis.items()):
            if v[pivot]:
                a = v[pivot]
                c = b[pivot]
                v = [c*x - a*y for x, y in zip(v, b)]
                g = math.gcd(*v)
                if g > 1:
                    v = [x // g for x in v]

        pivot = next(
            (i for i, x in enumerate(v) if x),
            None
        )
        if pivot is not None:
            basis[pivot] = v

        if len(basis) == n:
            break

    return len(basis)


def rank_fraction(columns):
    if not columns:
        return 0

    M = [list(map(Fraction, row)) for row in columns]
    rank = 0

    for c in range(len(M[0])):
        pivot = next(
            (r for r in range(rank, len(M)) if M[r][c]),
            None
        )
        if pivot is None:
            continue

        M[rank], M[pivot] = M[pivot], M[rank]
        a = M[rank][c]
        M[rank] = [x/a for x in M[rank]]

        for r in range(rank+1, len(M)):
            if M[r][c]:
                a = M[r][c]
                M[r] = [
                    x-a*y for x, y in zip(M[r], M[rank])
                ]

        rank += 1
        if rank == len(M):
            break

    return rank


def itineraries(T, h, length):
    result = []

    for state in range(len(T)):
        x = state
        word = []
        for _ in range(length):
            word.append(h[x])
            x = T[x]
        result.append(word)

    return result


def feature_columns(W, length, degree):
    return [
        [int(all(w[t] for t in S)) for w in W]
        for k in range(min(degree, length)+1)
        for S in it.combinations(range(length), k)
    ]


def predicted_rank(m, length, degree):
    if length == 0 or degree == 0:
        return 1
    if degree == 1:
        return 1 + min(length, m)
    if length == 1:
        return 2
    return min(length, m) + 2


cases = []
rank_checks = 0
deletion_checks = 0
fraction_checks = 0
mutation_checks = 0

for m in range(2, 21):
    n = m + 2

    # State 0: fixed zero.
    # State 1: fixed one.
    # States 2..m+1: an m-cycle.
    T = [0, 1] + [
        2 + (i+1) % m for i in range(m)
    ]
    h = [0, 1] + [
        int(i == 0) for i in range(m)
    ]

    weights = [m-1, 1] + [-1]*m
    W = itineraries(T, h, m+1)

    require(sum(weights) == 0, "Constant obstruction failed")
    require(math.gcd(*weights) == 1, "Nonprimitive weights")
    require(all(weights), "Zero circuit coefficient")

    # Every time-indexed linear observation must be annihilated.
    for t in range(m+1):
        require(
            sum(weights[s]*W[s][t] for s in range(n)) == 0,
            f"Linear obstruction failed: m={m}, t={t}"
        )

    horizon_rows = []

    for length in range(m+2):
        ranks = []

        for degree in range(3):
            columns = feature_columns(W, length, degree)
            actual = rank_integer(columns, n)
            expected = predicted_rank(m, length, degree)

            require(
                actual == expected,
                f"Rank mismatch: m={m}, L={length}, "
                f"degree={degree}, got={actual}, expected={expected}"
            )

            ranks.append(actual)
            rank_checks += 1

        horizon_rows.append({
            "L": length,
            "ranks_degree_0_to_2": ranks,
        })

    # Determine separation horizon directly from observation prefixes.
    least_separating = next(
        length
        for length in range(m+2)
        if len({tuple(w[:length]) for w in W}) == n
    )
    require(
        least_separating == m,
        f"Separating horizon mismatch: m={m}"
    )

    # Verify circuit minimality by deleting each point.
    for deleted in range(n):
        remaining = [
            W[s] for s in range(n) if s != deleted
        ]
        rank = rank_integer(
            feature_columns(remaining, m, 1),
            n-1
        )
        require(
            rank == n-1,
            f"Circuit deletion failed: m={m}, deleted={deleted}"
        )
        deletion_checks += 1

    # g=a_0*a_1 must be the fixed-one indicator.
    g = [w[0]*w[1] for w in W]
    require(
        g == [int(s == 1) for s in range(n)],
        f"Fixed-one indicator failed: m={m}"
    )

    cycle_indicator_states = []

    for t in range(m):
        indicator = [W[s][t]-g[s] for s in range(n)]
        require(
            all(x in (0, 1) for x in indicator),
            f"Nonbinary cycle indicator: m={m}, t={t}"
        )
        require(
            sum(indicator) == 1,
            f"Cycle indicator not singleton: m={m}, t={t}"
        )
        state = indicator.index(1)
        require(state >= 2, "Cycle indicator selected fixed state")
        cycle_indicator_states.append(state)

    require(
        set(cycle_indicator_states) == set(range(2, n)),
        f"Cycle indicators incomplete: m={m}"
    )

    fixed_zero_indicator = [
        1 - sum(W[s][:m]) + (m-1)*g[s]
        for s in range(n)
    ]
    require(
        fixed_zero_indicator == [int(s == 0) for s in range(n)],
        f"Fixed-zero indicator failed: m={m}"
    )

    # Independent exact-rank implementation for small representatives.
    if m <= 6:
        for degree in range(3):
            columns = feature_columns(W, m+1, degree)
            require(
                rank_fraction(columns)
                == rank_integer(columns, n),
                f"Fraction cross-check failed: m={m}, degree={degree}"
            )
            fraction_checks += 1

    # Negative controls: corruption must not be accepted.
    corrupted_weights = weights.copy()
    corrupted_weights[0] += 1
    require(
        sum(corrupted_weights) != 0,
        "Corrupted weights escaped constant check"
    )
    mutation_checks += 1

    corrupted_g = g.copy()
    corrupted_g[0] = 1
    require(
        corrupted_g != [int(s == 1) for s in range(n)],
        "Corrupted state indicator escaped comparison"
    )
    mutation_checks += 1

    case = {
        "cycle_length": m,
        "state_count": n,
        "state_order": "fixed_zero, fixed_one, cycle_0,...,cycle_(m-1)",
        "T": T,
        "h": h,
        "primitive_obstruction": weights,
        "least_separating_prefix_length": least_separating,
        "full_profile_degree_0_to_2":
            horizon_rows[-1]["ranks_degree_0_to_2"],
        "minimum_full_degree": 2,
        "maximum_absolute_obstruction_coefficient":
            max(map(abs, weights)),
        "horizon_profiles": horizon_rows,
        "cycle_indicator_state_for_each_time":
            cycle_indicator_states,
        "circuit_single_deletion_checks": n,
        "degree_two_state_indicators_verified": True,
    }
    cases.append(case)

    print(
        f"CASE_PASS m={m} states={n} "
        f"profile={case['full_profile_degree_0_to_2']} "
        f"Lsep={least_separating} "
        f"max_coefficient={max(map(abs, weights))}",
        flush=True
    )

require(len(cases) == 19, "Wrong family case count")
require(rank_checks == 741, "Wrong horizon-degree check count")
require(deletion_checks == 247, "Wrong deletion check count")
require(fraction_checks == 15, "Wrong Fraction cross-check count")
require(mutation_checks == 38, "Wrong negative-control count")

summary = {
    "scope": "two fixed points plus one-hot observed cycle",
    "cycle_lengths": {"minimum": 2, "maximum": 20},
    "family_cases": len(cases),
    "horizon_degree_rank_checks": rank_checks,
    "single_deletion_circuit_checks": deletion_checks,
    "fraction_rank_crosschecks": fraction_checks,
    "negative_controls": mutation_checks,
    "rank_formula_failures": 0,
    "obstruction_failures": 0,
    "state_indicator_failures": 0,
    "circuit_deletion_failures": 0,
    "coefficient_field": "Q",
    "arithmetic": "exact integer elimination and Fraction cross-checks",
    "python": sys.version,
    "platform": platform.platform(),
    "novelty": "not established",
    "general_proof_machine_checked": False,
    "scope_limit": (
        "A constructed family only; this experiment does not classify "
        "all temporal circuits or all finite systems."
    ),
    "old_censuses_rerun": False,
    "manuscript_changed": False,
    "repository_operations": "none",
    "elapsed_seconds": time.monotonic()-START,
    "status": "PASS",
}

for name, value in [
    ("cases.json", cases),
    ("summary.json", summary),
]:
    path = OUT / name
    path.write_text(
        json.dumps(value, indent=2) + "\n",
        encoding="utf-8"
    )
    require(
        json.loads(path.read_text(encoding="utf-8")) == value,
        "JSON readback failed: " + name
    )

print("\nSUMMARY_BEGIN", flush=True)
print(json.dumps(summary, indent=2), flush=True)
print("SUMMARY_END", flush=True)
print("SAVED_JSON_READBACK=PASS", flush=True)
print("NOVELTY=NOT_ESTABLISHED", flush=True)
print("GENERAL_PROOF_MACHINE_CHECKED=NO", flush=True)
print("OVERALL_STATUS=PASS", flush=True)
