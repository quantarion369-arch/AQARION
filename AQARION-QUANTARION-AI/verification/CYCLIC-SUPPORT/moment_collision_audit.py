#!/usr/bin/env python3
"""Exact higher-order moment audit of the AQARION cyclic witness."""
from itertools import combinations
from math import prod
import hashlib
import json

WORD = "0001011101"
COEFF = (-1, 1, -1, 2, -1, 1, -2, 1, -1, 1)

def windows(word):
    doubled = word + word[:3]
    return sorted({
        int(doubled[i:i+4], 2)
        for i in range(len(word))
    })

def bits(h):
    return tuple((h >> (3-j)) & 1 for j in range(4))

support = windows(WORD)
assert len(support) == 10
assert len(COEFF) == len(support)

# Verify the support and coefficients match the known exact witness.
assert [format(h, "04b") for h in support] == [
    "0001", "0010", "0100", "0101", "0111",
    "1000", "1010", "1011", "1101", "1110"
]

X = [bits(h) for h in support]
positive = [(format(h, "04b"), c) for h, c in zip(support, COEFF) if c > 0]
negative = [(format(h, "04b"), -c) for h, c in zip(support, COEFF) if c < 0]

assert sum(w for _, w in positive) == 6
assert sum(w for _, w in negative) == 6

records = []
by_degree = {}

for degree in range(5):
    degree_rows = []
    for coords in combinations(range(4), degree):
        delta = sum(
            c * prod(X[i][j] for j in coords)
            for i, c in enumerate(COEFF)
        )
        degree_rows.append({
            "coordinates": list(coords),
            "monomial": "1" if not coords else "*".join(f"x{j}" for j in coords),
            "signed_moment_difference": delta,
        })
    by_degree[degree] = degree_rows
    records.extend(degree_rows)

assert all(r["signed_moment_difference"] == 0
           for d in range(3) for r in by_degree[d])
assert [r["signed_moment_difference"] for r in by_degree[3]] == [1, -1, 1, -1]
assert by_degree[4][0]["signed_moment_difference"] == 0

# Positive and negative measures are normalized by their common mass 6.
result = {
    "word": WORD,
    "sorted_support": [format(h, "04b") for h in support],
    "positive_measure": positive,
    "negative_measure": negative,
    "common_total_mass": 6,
    "normalized_moment_differences": {
        str(d): [
            {
                "monomial": r["monomial"],
                "difference": f'{r["signed_moment_difference"]}/6'
            }
            for r in by_degree[d]
        ]
        for d in range(5)
    },
    "first_separating_degree": 3,
    "interpretation": "Exact for this witness and these four Boolean coordinates only",
}

payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
print("AQARION HIGHER-ORDER MOMENT COLLISION AUDIT")
print("WORD:", WORD)
print("POSITIVE WEIGHTS:", positive)
print("NEGATIVE WEIGHTS:", negative)
print("COMMON MASS:", 6)
print()
for degree in range(5):
    print(f"DEGREE {degree}:")
    for row in by_degree[degree]:
        print(f'  {row["monomial"]:10s} delta={row["signed_moment_difference"]}')
print()
print("FIRST SEPARATING DEGREE:", 3)
print("NORMALIZED CUBIC DIFFERENCES:", ["1/6", "-1/6", "1/6", "-1/6"])
print("EXACT INTEGER ASSERTIONS: PASS")
print("SUMMARY_SHA256:", hashlib.sha256(payload).hexdigest())
