#!/usr/bin/env python3
"""Bounded exact Case B family test. Standard library only."""
from fractions import Fraction
from hashlib import sha256
from math import comb, factorial, isqrt
from pathlib import Path
import json

J_MAX = 6
P_MAX = 19

def prime(p):
    return p >= 2 and all(p % d for d in range(2, isqrt(p) + 1))

def vp(x, p):
    if x == 0:
        raise ValueError("valuation of zero is not used")
    x = abs(x)
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v

def vpf(n, p):
    v = 0
    while n:
        n //= p
        v += n
    return v

def stirling(n, m):
    row = [1] + [0] * m
    for total in range(1, n + 1):
        nxt = [0] * (m + 1)
        for k in range(1, min(total, m) + 1):
            nxt[k] = row[k - 1] + (total - 1) * row[k]
        row = nxt
    return row[m]

def partition_coin(n, m):
    deficit = n - m
    row = [1] + [0] * deficit
    for part in range(1, min(m, deficit) + 1):
        for d in range(part, deficit + 1):
            row[d] += row[d - part]
    return row[deficit]

def partition_recurrence(n, m):
    table = [[0] * (m + 1) for _ in range(n + 1)]
    table[0][0] = 1
    for total in range(1, n + 1):
        for k in range(1, min(total, m) + 1):
            table[total][k] = (
                table[total - 1][k - 1]
                + table[total - k][k]
            )
    return table[n][m]

def main():
    count = 0
    results = []
    endpoints = []

    def check(ok, label, j, p):
        nonlocal count
        count += 1
        if not ok:
            raise RuntimeError(
                f"FAIL: j={j}, p={p}, check={label}"
            )

    for j in range(1, J_MAX + 1):
        for p in range(2, P_MAX + 1):
            if not prime(p) or p <= 2 * j + 1:
                continue

            n = (2 * j + 1) * p
            m = j * p + j + 1
            c = stirling(n, m)
            residue = (-1) ** (j + 1) * comb(2 * j + 1, j)

            part = partition_coin(n, m)
            part2 = partition_recurrence(n, m)
            ratio = Fraction(
                factorial(m) * c,
                factorial(n) * part
            )
            actual = (
                vp(ratio.numerator, p)
                - vp(ratio.denominator, p)
            )
            predicted = -(j + 1) - vp(part, p)

            lo = Fraction(n - 1, m)
            hi = Fraction(n - 1, m - 1)
            integers = list(range(
                lo.numerator // lo.denominator + 1,
                hi.numerator // hi.denominator + 1
            ))

            tests = [
                (
                    j >= 1 and prime(p) and p > 2 * j + 1,
                    "domain"
                ),
                (
                    m == 2 * j + 1 + j * (p - 1),
                    "index mapping"
                ),
                (
                    c % p == residue % p,
                    "coefficient congruence"
                ),
                (
                    vp(c, p) == 0,
                    "Stirling unit"
                ),
                (
                    vp(factorial(m), p) == vpf(m, p) == j,
                    "m factorial valuation"
                ),
                (
                    vp(factorial(n), p) == vpf(n, p) == 2 * j + 1,
                    "n factorial valuation"
                ),
                (
                    part > 0 and part == part2,
                    "independent partition cross-check"
                ),
                (
                    actual == predicted and actual < 0,
                    "ratio valuation"
                ),
                (
                    ratio.denominator > 1 and ratio != 1,
                    "nonintegrality and equality exclusion"
                ),
                (
                    n - 2 * m == p - 2 * j - 2 and n > 2 * m,
                    "Case B"
                ),
                (
                    n - 1 - 2 * m == p - 2 * j - 3,
                    "lower endpoint arithmetic"
                ),
                (
                    3 * (m - 1) - (n - 1)
                    == (j - 1) * p + 3 * j + 1,
                    "upper endpoint arithmetic"
                ),
                (
                    2 <= lo < hi < 3,
                    "interval endpoints"
                ),
                (
                    not integers,
                    "no integer in strict-lower interval"
                ),
                (
                    not ((m - 1) * 2 <= n - 1 < m * 2),
                    "original criterion rejects prime power 2"
                ),
            ]

            for ok, label in tests:
                check(ok, label, j, p)

            if p == 2 * j + 3:
                check(
                    lo == 2 and n - 1 == 2 * m,
                    "strict endpoint equality",
                    j, p
                )
                endpoints.append([j, p, n, m])

            results.append({
                "j": j,
                "p": p,
                "n": n,
                "m": m,
                "vp_P": vp(part, p),
                "vp_R": actual,
            })

    check(len(results) == 24, "expected pair count", 0, 0)
    check(len(endpoints) == 4, "expected endpoint count", 0, 0)

    example = Fraction(
        factorial(7) * stirling(15, 7),
        factorial(15) * partition_coin(15, 7)
    )
    check(
        example > 1
        and vp(example.numerator, 5)
        - vp(example.denominator, 5) < 0,
        "negative valuation does not imply below one",
        1, 5
    )

    receipt = {
        "status": "PASS",
        "scope": "BOUNDED EXACT TEST; NOT FORMAL CERTIFICATION",
        "j_max": J_MAX,
        "p_max": P_MAX,
        "pairs": len(results),
        "checks": count,
        "endpoints": endpoints,
        "results": results,
        "source_sha256": sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "formal_certification": "OPEN",
        "global_classification": "OPEN",
        "real_order_classification": "NOT CLAIMED",
        "promotion": False,
        "git_operations": 0,
    }
    payload = json.dumps(
        receipt, sort_keys=True, separators=(",", ":")
    ).encode()
    receipt["receipt_payload_sha256"] = sha256(payload).hexdigest()

    print(json.dumps(receipt, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
