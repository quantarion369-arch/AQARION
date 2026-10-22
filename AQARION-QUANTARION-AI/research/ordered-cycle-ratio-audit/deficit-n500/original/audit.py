#!/usr/bin/env python3
"""Exact-integer cycle-ratio audit organized by deficit d=n-m."""

from pathlib import Path
from math import factorial
import hashlib
import json

N = 500
ROOT = Path.home() / "AQARION_AUDIT" / "cycle_ratio"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


# P[n][m] = number of partitions of n into exactly m parts.
P = [[0] * (N + 1) for _ in range(N + 1)]
P[0][0] = 1

for n in range(1, N + 1):
    for m in range(1, n + 1):
        P[n][m] = P[n - 1][m - 1] + P[n - m][m]


# C[n][m] = unsigned Stirling number of the first kind.
C = [[0] * (N + 1) for _ in range(N + 1)]
C[0][0] = 1

for n in range(1, N + 1):
    for m in range(1, n + 1):
        C[n][m] = (n - 1) * C[n - 1][m] + C[n - 1][m - 1]


# Independently construct unrestricted partition numbers p(k).
# Then construct p_{<=m}(d) by conjugating partitions:
# partitions of d into at most m parts equal partitions of d
# whose largest part is at most m.
#
# Q[d][m] = number of partitions of d with largest part <= m.
Q = [[0] * (N + 1) for _ in range(N + 1)]
Q[0] = [1] * (N + 1)

for part in range(1, N + 1):
    for total in range(part, N + 1):
        for limit in range(part, N + 1):
            Q[total][limit] += Q[total - part][limit]


pairs = 0
deficit_pairs = 0
bijection_checks = 0
zeros = []
positive = 0
negative = 0
min_abs_delta = None
min_abs_pair = None
closest_nonexceptional = None

for n in range(1, N + 1):
    for m in range(1, n + 1):
        d = n - m
        pairs += 1

        # Partition-deficit bijection:
        # p_{=m}(n) = p_{<=m}(d).
        require(
            P[n][m] == Q[d][m],
            f"Deficit partition identity failed at n={n}, m={m}"
        )
        bijection_checks += 1

        falling = factorial(n) // factorial(m)
        delta = C[n][m] - falling * P[n][m]

        if delta == 0:
            zeros.append([n, m, d])
        elif delta > 0:
            positive += 1
        else:
            negative += 1

        if d >= 3:
            deficit_pairs += 1
            if min_abs_delta is None or abs(delta) < min_abs_delta:
                min_abs_delta = abs(delta)
                min_abs_pair = [n, m, d, delta]

            # Record the exact integer difference, not a rounded ratio.
            if delta == 0:
                closest_nonexceptional = [n, m, d, delta]

expected = [[n, n, 0] for n in range(1, N + 1)]
expected.append([3, 2, 1])
expected.sort()

require(
    zeros == expected,
    f"Unexpected equality cases through N={N}: {zeros}"
)

source_hash = hashlib.sha256(
    Path(__file__).read_bytes()
).hexdigest()

receipt = {
    "audit": "exact_integer_deficit_difference",
    "status": "PASS",
    "maximum_n": N,
    "pairs_checked": pairs,
    "deficit_pairs_d_ge_3": deficit_pairs,
    "partition_deficit_bijection_checks": bijection_checks,
    "delta_positive_pairs": positive,
    "delta_negative_pairs": negative,
    "zero_difference_cases_n_m_d": zeros,
    "minimum_absolute_delta_for_d_ge_3": min_abs_delta,
    "minimum_absolute_delta_witness_n_m_d_delta": min_abs_pair,
    "unexpected_zero_for_d_ge_3": closest_nonexceptional,
    "script_sha256": source_hash,
    "scope": (
        "Exact recurrence-based integer audit through n <= 500. "
        "Finite evidence only; does not prove the global theorem."
    ),
    "global_theorem_proved": False,
    "promotion_authorized": False,
    "publication_authorized": False,
}

ROOT.mkdir(parents=True, exist_ok=True)
out = ROOT / "deficit_difference_receipt.json"
out.write_text(json.dumps(receipt, indent=2) + "\n")

print("EXACT DEFICIT-DIFFERENCE AUDIT")
print("Maximum n:", N)
print("Pairs checked:", pairs)
print("Pairs with d >= 3:", deficit_pairs)
print("Partition-deficit bijection checks:", bijection_checks)
print("Delta positive / negative:", positive, "/", negative)
print("Zero cases (n,m,d):", zeros)
print("Minimum |Delta| for d >= 3:", min_abs_delta)
print("Witness (n,m,d,Delta):", min_abs_pair)
print("Unexpected zero for d >= 3:", closest_nonexceptional)
print("Script SHA-256:", source_hash)
print("Receipt:", out)
print("GLOBAL THEOREM: NOT PROVED")
print("PUSH/PUBLICATION/PROMOTION: NOT AUTHORIZED")
