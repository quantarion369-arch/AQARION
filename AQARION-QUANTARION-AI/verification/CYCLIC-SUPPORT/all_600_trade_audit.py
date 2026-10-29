#!/usr/bin/env python3
"""Exact audit of deficient 10-subsets of the four-bit Boolean cube."""
from itertools import combinations
from fractions import Fraction
from math import gcd, lcm, prod
import hashlib
import json

P = 65521
N = 4
SIZE = 10

MONOMIALS = {
    d: list(combinations(range(N), d))
    for d in range(N + 1)
}
LOW_MONOMIALS = [
    c for d in range(3) for c in MONOMIALS[d]
]

def bits(h):
    return tuple((h >> (N - 1 - j)) & 1 for j in range(N))

def monomial_value(h, coords):
    x = bits(h)
    return prod(x[j] for j in coords)

def feature_row(h):
    return [monomial_value(h, c) for c in LOW_MONOMIALS]

def rref(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    m = len(a)
    n = len(a[0]) if m else 0
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

def rank_mod(matrix):
    a = [[int(v) % P for v in row] for row in matrix]
    m = len(a)
    n = len(a[0]) if m else 0
    r = 0

    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue

        a[r], a[p] = a[p], a[r]
        inv = pow(a[r][c], P - 2, P)
        a[r] = [(v * inv) % P for v in a[r]]

        for i in range(r + 1, m):
            if a[i][c]:
                q = a[i][c]
                a[i] = [
                    (u - q*v) % P
                    for u, v in zip(a[i], a[r])
                ]

        r += 1
        if r == m:
            break

    return r

def primitive_dependency(histories):
    # A c = 0, where rows of A are the degree <= 2 feature vectors.
    a = [feature_row(h) for h in histories]
    at = [[a[i][j] for i in range(len(a))]
          for j in range(len(a[0]))]
    reduced, pivots = rref(at)
    free = [j for j in range(len(histories)) if j not in pivots]

    if len(free) != 1:
        return None, len(pivots)

    f = free[0]
    v = [Fraction(0) for _ in histories]
    v[f] = Fraction(1)

    for row, pivot in enumerate(pivots):
        v[pivot] = -reduced[row][f]

    den = 1
    for z in v:
        den = lcm(den, z.denominator)

    ints = [int(z * den) for z in v]
    common = 0
    for z in ints:
        common = gcd(common, abs(z))

    ints = [z // common for z in ints]
    first = next(z for z in ints if z)
    if first < 0:
        ints = [-z for z in ints]

    return ints, len(pivots)

def moment_differences(histories, coeff, degree):
    return {
        "".join(f"x{j}" for j in coords) if coords else "1":
        sum(coeff[i] * monomial_value(h, coords)
            for i, h in enumerate(histories))
        for coords in MONOMIALS[degree]
    }

def support_mask(histories):
    return sum(1 << h for h in histories)

def cyclic_supports():
    # Every length-10 binary word, interpreted cyclically.
    found = set()
    for word_int in range(1 << SIZE):
        word = format(word_int, f"0{SIZE}b")
        cyclic = word + word[:N-1]
        histories = {
            int(cyclic[i:i+N], 2)
            for i in range(SIZE)
        }
        if len(histories) == SIZE:
            found.add(support_mask(sorted(histories)))
    return found

cyclic_masks = cyclic_supports()

def label(h):
    return format(h, "04b")

counts = {
    "rank_mod_full_screened": 0,
    "exact_deficient": 0,
    "rank_distribution": {},
    "first_separating_degree": {},
    "cubic_nonzero": 0,
    "quartic_nonzero": 0,
    "cyclic_realizable_deficient": 0,
    "cyclic_realizable_first_degree": {},
}
records = []
lower_rank_exceptions = []

for histories in combinations(range(16), SIZE):
    a = [feature_row(h) for h in histories]

    # Full rank modulo P certifies full rank over Q.
    if rank_mod(a) == SIZE:
        counts["rank_mod_full_screened"] += 1
        continue

    reduced, pivots = rref(a)
    rank_q = len(pivots)

    if rank_q == SIZE:
        # A modular rank drop can be caused by the chosen prime.
        continue

    counts["exact_deficient"] += 1
    counts["rank_distribution"][str(rank_q)] = (
        counts["rank_distribution"].get(str(rank_q), 0) + 1
    )

    if rank_q != SIZE - 1:
        lower_rank_exceptions.append({
            "support": [label(h) for h in histories],
            "rank": rank_q,
        })
        continue

    coeff, rank_check = primitive_dependency(histories)
    assert rank_check == rank_q
    assert coeff is not None

    low = {
        str(d): moment_differences(histories, coeff, d)
        for d in range(3)
    }
    assert all(v == 0 for family in low.values()
               for v in family.values())

    cubic = moment_differences(histories, coeff, 3)
    quartic = moment_differences(histories, coeff, 4)

    first = 3 if any(cubic.values()) else (
        4 if any(quartic.values()) else None
    )
    first_key = str(first) if first is not None else "none"
    counts["first_separating_degree"][first_key] = (
        counts["first_separating_degree"].get(first_key, 0) + 1
    )

    cubic_nz = any(cubic.values())
    quartic_nz = any(quartic.values())
    counts["cubic_nonzero"] += int(cubic_nz)
    counts["quartic_nonzero"] += int(quartic_nz)

    mask = support_mask(histories)
    is_cyclic = mask in cyclic_masks
    if is_cyclic:
        counts["cyclic_realizable_deficient"] += 1
        counts["cyclic_realizable_first_degree"][first_key] = (
            counts["cyclic_realizable_first_degree"].get(first_key, 0) + 1
        )

    records.append({
        "support": [label(h) for h in histories],
        "dependency": coeff,
        "positive_mass": sum(c for c in coeff if c > 0),
        "negative_mass": -sum(c for c in coeff if c < 0),
        "first_separating_degree": first_key,
        "cubic": cubic,
        "quartic": quartic,
        "cyclic_realizable": is_cyclic,
    })

records.sort(key=lambda r: r["support"])
summary = {
    "feature_definition": "all square-free Boolean monomials of degree <= 2",
    "cube_dimension": N,
    "support_size": SIZE,
    "modular_prime": P,
    "cyclic_support_masks_count": len(cyclic_masks),
    "counts": counts,
    "lower_rank_exceptions": lower_rank_exceptions,
    "records": records,
}
payload = json.dumps(
    summary, sort_keys=True, separators=(",", ":")
).encode()

print("AQARION ALL-600 TRADE AUDIT")
print("TOTAL SIZE-10 SUPPORTS:", 8008)
print("FULL-RANK MODULAR SCREEN:", counts["rank_mod_full_screened"])
print("EXACT DEFICIENT SUPPORTS:", counts["exact_deficient"])
print("EXACT RANK DISTRIBUTION:", counts["rank_distribution"])
print("FIRST SEPARATING DEGREE:", counts["first_separating_degree"])
print("NONZERO CUBIC MOMENT:", counts["cubic_nonzero"])
print("NONZERO QUARTIC MOMENT:", counts["quartic_nonzero"])
print("CYCLIC REALIZABLE SUPPORT MASKS:", len(cyclic_masks))
print("CYCLIC-REALIZABLE DEFICIENT SUPPORTS:",
      counts["cyclic_realizable_deficient"])
print("CYCLIC FIRST-DEGREE COUNTS:",
      counts["cyclic_realizable_first_degree"])
print("LOWER-RANK EXCEPTIONS:", len(lower_rank_exceptions))

exceptions = [
    r for r in records
    if r["first_separating_degree"] != "3"
]
print("NON-CUBIC-FIRST EXCEPTIONS:", len(exceptions))
for r in exceptions:
    print("  EXCEPTION:", " ".join(r["support"]),
          "degree=", r["first_separating_degree"],
          "cyclic=", r["cyclic_realizable"])

print("SUMMARY_SHA256:", hashlib.sha256(payload).hexdigest())

# These are prior-census cross-checks, not assumptions used in rank tests.
if counts["exact_deficient"] != 600:
    print("CENSUS CROSS-CHECK: FAIL (expected 600 deficient supports)")
elif lower_rank_exceptions:
    print("RANK CROSS-CHECK: FAIL (unexpected rank below 9)")
else:
    print("CENSUS CROSS-CHECK: PASS")
