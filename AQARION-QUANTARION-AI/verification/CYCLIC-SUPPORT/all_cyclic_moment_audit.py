#!/usr/bin/env python3
"""Exact moment-degree audit for all eight SC deficient size-10 supports."""
from fractions import Fraction
from itertools import combinations
from math import gcd, lcm
import hashlib
import json

SUPPORTS = [
    "0010 0011 0100 0101 0110 1001 1010 1011 1100 1101",
    "0001 0010 0011 0100 0101 0111 1000 1010 1100 1110",
    "0001 0010 0011 0101 0111 1000 1010 1011 1100 1110",
    "0001 0010 0100 0101 0111 1000 1010 1011 1101 1110",
    "0001 0011 0100 0101 0111 1000 1010 1100 1101 1110",
    "0001 0010 0011 0100 0111 1000 1011 1100 1101 1110",
    "0001 0011 0101 0111 1000 1010 1011 1100 1101 1110",
    "0000 0001 0011 0110 0111 1000 1001 1100 1110 1111",
]

def bits(word):
    return tuple(int(c) for c in word)

def monomials(max_degree):
    return [
        coords
        for degree in range(max_degree + 1)
        for coords in combinations(range(4), degree)
    ]

def phi(word, max_degree):
    x = bits(word)
    return [
        Fraction(1 if not coords else
                 __import__("math").prod(x[i] for i in coords))
        for coords in monomials(max_degree)
    ]

def rref(matrix):
    a = [row[:] for row in matrix]
    m = len(a)
    n = len(a[0]) if a else 0
    pivots = []
    r = 0

    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        q = a[r][c]
        a[r] = [v / q for v in a[r]]

        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [u - q*v for u, v in zip(a[i], a[r])]

        pivots.append(c)
        r += 1
        if r == m:
            break

    return a, pivots

def rank_q(matrix):
    return len(rref(matrix)[1])

def primitive_dependency(words):
    # Find c such that sum_x c_x * phi(x) = 0.
    # This is the nullspace of the transposed feature matrix.
    feature_rows = [phi(w, 2) for w in words]
    transposed = [
        [feature_rows[i][j] for i in range(len(words))]
        for j in range(len(feature_rows[0]))
    ]
    reduced, pivots = rref(transposed)
    free = [j for j in range(len(words)) if j not in pivots]
    assert len(free) == 1, (
        "Expected a one-dimensional dependency space",
        len(free), pivots
    )

    f = free[0]
    vec = [Fraction(0) for _ in words]
    vec[f] = Fraction(1)
    for row, pivot_col in enumerate(pivots):
        vec[pivot_col] = -reduced[row][f]

    denominator = 1
    for v in vec:
        denominator = lcm(denominator, v.denominator)
    ints = [int(v * denominator) for v in vec]
    common = 0
    for v in ints:
        common = gcd(common, abs(v))
    ints = [v // common for v in ints]

    first = next(v for v in ints if v)
    if first < 0:
        ints = [-v for v in ints]

    return ints

def moment_differences(words, coeff, degree):
    cols = monomials(degree)
    return {
        "".join(f"x{i}" for i in c) if c else "1":
        sum(
            coeff[k] * int(
                __import__("math").prod(bits(w)[i] for i in c)
            ) if c else coeff[k]
            for k, w in enumerate(words)
        )
        for c in cols
    }

records = []
for raw in SUPPORTS:
    words = sorted(raw.split())
    assert len(words) == 10 and len(set(words)) == 10

    rank2 = rank_q([phi(w, 2) for w in words])
    assert rank2 == 9

    coeff = primitive_dependency(words)
    assert any(c > 0 for c in coeff)
    assert any(c < 0 for c in coeff)

    degree_diffs = {
        d: moment_differences(words, coeff, d)
        for d in range(5)
    }
    assert all(v == 0 for v in degree_diffs[2].values())

    first_nonzero = None
    for d in range(5):
        if any(v != 0 for v in degree_diffs[d].values()):
            first_nonzero = d
            break

    # A nonzero dependency must be detected by some feature family.
    assert first_nonzero is not None

    records.append({
        "support": words,
        "dependency": coeff,
        "rank_degree2": rank2,
        "first_nonzero_degree": first_nonzero,
        "degree3_differences": degree_diffs[3],
        "degree4_differences": degree_diffs[4],
        "positive_mass": sum(v for v in coeff if v > 0),
        "negative_mass": -sum(v for v in coeff if v < 0),
    })

summary = {
    "supports_tested": len(records),
    "rank_degree2_counts": {
        str(r): sum(x["rank_degree2"] == r for x in records)
        for r in sorted(set(x["rank_degree2"] for x in records))
    },
    "first_nonzero_degree_counts": {
        str(d): sum(x["first_nonzero_degree"] == d for x in records)
        for d in range(5)
    },
    "records": records,
}
payload = json.dumps(summary, sort_keys=True, separators=(",", ":")).encode()

print("AQARION ALL-CYCLIC-SUPPORT MOMENT AUDIT")
print("SUPPORTS TESTED:", len(records))
print("DEGREE-2 RANK COUNTS:", summary["rank_degree2_counts"])
print("FIRST NONZERO MOMENT DEGREE COUNTS:",
      summary["first_nonzero_degree_counts"])
for i, r in enumerate(records, 1):
    print(f"\nSUPPORT {i}: {' '.join(r['support'])}")
    print("  primitive dependency:", r["dependency"])
    print("  positive/negative mass:",
          r["positive_mass"], r["negative_mass"])
    print("  first nonzero degree:", r["first_nonzero_degree"])
    print("  cubic differences:", r["degree3_differences"])
    print("  quartic differences:", r["degree4_differences"])

print("\nSUMMARY_SHA256:", hashlib.sha256(payload).hexdigest())
print("PASS: exact dependency and moment assertions completed")
