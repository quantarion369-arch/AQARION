#!/usr/bin/env python3
"""Exact arithmetic verifier for the PB-CORE-006 candidate formula.

Uses Python's standard library only.

This verifies the arithmetic of the displayed formula against supplied
reference values. It does not prove the combinatorial identity represented
by that formula.

A value with no stored reference is reported as UNREFERENCED. It is never
counted as a successful reference comparison.
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
    """Evaluate the PB-CORE-006 aggregate formula using exact integers."""
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

    matched = 0
    mismatched = 0
    unreferenced = 0

    for n in range(1, limit + 1):
        value, terms = aggregate_formula(n, p)
        expected = REPORTED.get(n)

        if expected is None:
            status = "UNREFERENCED"
            matches_reference = False
            unreferenced += 1
        elif value == expected:
            status = "REFERENCE_MATCH"
            matches_reference = True
            matched += 1
        else:
            status = "REFERENCE_MISMATCH"
            matches_reference = False
            mismatched += 1

        results[str(n)] = {
            "computed": value,
            "reported_reference": expected,
            "matches_reference": matches_reference,
            "status": status,
            "partition_number": p[n],
            "terms": terms,
        }

        print(
            f"n={n}: computed={value}, "
            f"reference={expected}, status={status}",
            flush=True,
        )

    if mismatched > 0:
        reference_status = "FAIL_REFERENCE_COMPARISON"
        exit_code = 1
    elif matched > 0:
        reference_status = "PASS_REFERENCE_COMPARISON"
        exit_code = 0
    else:
        reference_status = "INCONCLUSIVE_NO_REFERENCES"
        exit_code = 1

    output = {
        "artifact_id": "PB-CORE-006-ARITHMETIC-VERIFY",
        "reference_comparison": reference_status,
        "formula_evaluation": "COMPLETED",
        "reference_matched": matched,
        "reference_mismatched": mismatched,
        "unreferenced_values": unreferenced,
        "combinatorial_identity_proved": False,
        "lean_verified": False,
        "limit": limit,
        "partition_numbers": p,
        "results": results,
        "interpretation": (
            "PASS_REFERENCE_COMPARISON means every supplied reference value "
            "in range matched the exact integer evaluation of the displayed "
            "formula. Values marked UNREFERENCED were computed but were not "
            "independently checked against a stored reference. This script "
            "does not establish the general combinatorial identity."
        ),
    }

    print(json.dumps(output, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    bound = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    raise SystemExit(main(bound))
