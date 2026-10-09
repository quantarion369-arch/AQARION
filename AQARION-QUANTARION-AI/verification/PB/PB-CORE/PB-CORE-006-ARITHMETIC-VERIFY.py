#!/usr/bin/env python3
"""Exact arithmetic verifier for the PB-CORE-006 candidate formula.

Uses Python's standard library only.
This verifies the arithmetic of the displayed formula; it does not
prove the combinatorial identity represented by that formula.
"""

import json
import math
import sys


REPORTED = {
    1: 1,
    2: 6,
    3: 51,
    4: 592,
    5: 8565,
    6: 148896,
    7: 3018127,
    8: 69844608,
    9: 1816084233,
    10: 52399129600,
    11: 1660832066091,
    12: 57351480413184,
}


def partition_numbers(limit):
    """Return p(0),...,p(limit) using the coin-change recurrence."""
    p = [0] * (limit + 1)
    p[0] = 1

    for part in range(1, limit + 1):
        for total in range(part, limit + 1):
            p[total] += p[total - part]

    return p


def aggregate_formula(n, p):
    if n < 1:
        raise ValueError("n must be >= 1")

    factorial_n = math.factorial(n)
    terms = []
    total = factorial_n * p[n]

    for k in range(1, n):
        denominator = math.factorial(n - k)
        numerator = factorial_n
        quotient, remainder = divmod(numerator, denominator)

        if remainder:
            raise ArithmeticError(
                f"Non-exact factorial ratio for n={n}, k={k}"
            )

        term = quotient * k * p[k] * n ** (n - k - 1)
        terms.append({
            "k": k,
            "factorial_ratio": quotient,
            "partition_count": p[k],
            "power": n ** (n - k - 1),
            "term": term,
        })
        total += term

    return total, terms


def main(limit=12):
    if limit < 1:
        raise ValueError("limit must be positive")

    p = partition_numbers(limit)
    results = {}
    all_match = True

    for n in range(1, limit + 1):
        value, terms = aggregate_formula(n, p)
        expected = REPORTED.get(n)
        matches = expected is None or value == expected
        all_match = all_match and matches

        results[str(n)] = {
            "computed": value,
            "reported_reference": expected,
            "matches_reference": matches,
            "partition_number": p[n],
            "terms": terms,
        }
        print(
            f"n={n}: computed={value}, "
            f"reference={expected}, match={matches}",
            flush=True,
        )

    output = {
        "artifact_id": "PB-CORE-006-ARITHMETIC-VERIFY",
        "formula_arithmetic": "PASS" if all_match else "FAIL",
        "combinatorial_identity_proved": False,
        "lean_verified": False,
        "limit": limit,
        "partition_numbers": p,
        "results": results,
        "interpretation": (
            "PASS means the displayed formula was evaluated with exact "
            "integer arithmetic and matched every supplied reference "
            "value in range. It does not establish the general formula."
        ),
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    if not all_match:
        return 1
    return 0


if __name__ == "__main__":
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    raise SystemExit(main(bound))
