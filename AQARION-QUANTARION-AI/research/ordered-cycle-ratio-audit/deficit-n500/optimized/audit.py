#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import platform

N = 500
ROOT = Path(__file__).resolve().parent

P = [[0] * (N + 1) for _ in range(N + 1)]
P[0][0] = 1

for n in range(1, N + 1):
    for m in range(1, n + 1):
        P[n][m] = P[n - 1][m - 1]
        if n >= m:
            P[n][m] += P[n - m][m]

Q = [[0] * (N + 1) for _ in range(N + 1)]
Q[0] = [1] * (N + 1)

for m in range(1, N + 1):
    for d in range(1, N + 1):
        Q[d][m] = Q[d][m - 1]
        if d >= m:
            Q[d][m] += Q[d - m][m]

facts = [math.factorial(n) for n in range(N + 1)]
previous = [1] + [0] * N

pairs = positive = negative = zeros = 0
deep_pairs = deep_positive = deep_negative = 0
bijection_mismatches = []
unexpected_zeros = []
missing_expected_zeros = []
formula_mismatches = []
minimum = None
witness = None

for n in range(1, N + 1):
    current = [0] * (N + 1)

    for m in range(1, n + 1):
        current[m] = (
            (n - 1) * previous[m] + previous[m - 1]
        )
        d = n - m
        pairs += 1

        if P[n][m] != Q[d][m]:
            bijection_mismatches.append([n, m, d])

        falling = facts[n] // facts[m]
        denominator = falling * P[n][m]
        delta = current[m] - denominator

        expected_zero = m == n or (n, m) == (3, 2)

        if delta == 0:
            zeros += 1
            if not expected_zero:
                unexpected_zeros.append([n, m, d])
        elif delta > 0:
            positive += 1
        else:
            negative += 1

        if expected_zero and delta != 0:
            missing_expected_zeros.append([n, m, d])

        if d >= 3:
            deep_pairs += 1
            deep_positive += delta > 0
            deep_negative += delta < 0
            if minimum is None or abs(delta) < minimum:
                minimum = abs(delta)
                witness = [n, m, d, delta]

        expected_ratio = None

        if d == 0:
            expected_ratio = Fraction(1)
        elif d == 1:
            expected_ratio = Fraction(n - 1, 2)
        elif d == 2 and n >= 4:
            expected_ratio = Fraction((n - 2) * (3 * n - 1), 48)
        elif d == 3 and n >= 6:
            expected_ratio = Fraction(n * (n - 1) * (n - 3), 144)

        if expected_ratio is not None:
            if Fraction(current[m], denominator) != expected_ratio:
                formula_mismatches.append([n, m, d])

    previous = current

checks_pass = not (
    bijection_mismatches
    or unexpected_zeros
    or missing_expected_zeros
    or formula_mismatches
)

receipt = {
    "audit": "exact_integer_deficit_difference",
    "status": "PASS" if checks_pass else "COUNTEREXAMPLE_OR_MISMATCH",
    "maximum_n": N,
    "python": platform.python_version(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "pairs_checked": pairs,
    "partition_deficit_bijection_mismatches": bijection_mismatches,
    "delta_positive_pairs": positive,
    "delta_negative_pairs": negative,
    "zero_difference_count": zeros,
    "expected_zero_rule": "m=n, or (n,m)=(3,2)",
    "unexpected_zeros_n_m_d": unexpected_zeros,
    "missing_expected_zeros_n_m_d": missing_expected_zeros,
    "special_formula_mismatches_n_m_d": formula_mismatches,
    "d_ge_3_pairs": deep_pairs,
    "d_ge_3_positive": deep_positive,
    "d_ge_3_negative": deep_negative,
    "minimum_absolute_delta_d_ge_3": minimum,
    "minimum_witness_n_m_d_delta": witness,
    "scope": "Finite exact recurrence audit; not a global equality proof",
    "git_operations": 0
}

output = ROOT / "receipt.json"
with output.open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, indent=2)

print("STATUS=" + receipt["status"])
print("MAX_N=" + str(N))
print("PAIRS=" + str(pairs))
print("POSITIVE_NEGATIVE_ZERO=" + str([positive, negative, zeros]))
print("D_GE_3_PAIRS_POSITIVE_NEGATIVE=" + str(
    [deep_pairs, deep_positive, deep_negative]
))
print("UNEXPECTED_ZEROS=" + str(unexpected_zeros))
print("BIJECTION_MISMATCHES=" + str(len(bijection_mismatches)))
print("SPECIAL_FORMULA_MISMATCHES=" + str(len(formula_mismatches)))
print("MINIMUM_WITNESS=" + str(witness))
print("SOURCE_SHA256=" + receipt["script_sha256"])
print("RECEIPT_SHA256=" + hashlib.sha256(output.read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(ROOT))

if not checks_pass:
    raise SystemExit(1)
