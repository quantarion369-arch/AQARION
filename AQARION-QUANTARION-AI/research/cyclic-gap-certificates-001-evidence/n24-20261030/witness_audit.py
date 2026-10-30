from fractions import Fraction
from pathlib import Path
import hashlib
import json

# Coefficients are stored in ASCENDING degree order throughout.
WORDS = [
    "111100101101101001111000",
    "111000011010010010110000",
]

PHI = {
    4:  [1, 0, 1],
    12: [1, 0, -1, 0, 1],
    24: [1, 0, 0, 0, -1, 0, 0, 0, 1],
}

def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out

def div_exact(a, b):
    r = list(a)
    q = [0] * (len(a) - len(b) + 1)
    for k in range(len(q) - 1, -1, -1):
        c = r[k + len(b) - 1] // b[-1]
        q[k] = c
        for j, v in enumerate(b):
            r[k + j] -= c * v
    assert all(x == 0 for x in r), f"nonzero remainder: {r}"
    return q

def rank_q(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        v = a[r][c]
        a[r] = [x / v for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                v = a[i][c]
                a[i] = [x - v*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == m:
            break
    return r

def rotations(bits):
    n = len(bits)
    return [tuple(bits[(i+j) % n] for j in range(n)) for i in range(n)]

D = [1]
for d in (4, 12, 24):
    D = mul(D, PHI[d])

assert D == [1,0,0,0,-1,0,1,0,1,0,-1,0,0,0,1]

records = []
for word in WORDS:
    bits = [int(c) for c in word[::-1]]  # reverse display to ascending coefficients
    n = len(bits)
    rots = rotations(bits)
    p = len(set(rots))
    feature_matrix = [[1] + list(row) for row in rots]
    rank = rank_q(feature_matrix)
    gap = p - rank

    P = bits[:]
    quotient = div_exact(P, D)
    assert mul(D, quotient) == P
    assert p == n == 24
    assert gap == 14

    rec = {
        "display_word_descending": word,
        "coefficient_order": "ascending internally; displayed word is descending",
        "n": n,
        "weight": sum(bits),
        "distinct_rotations_p": p,
        "direct_feature_rank_over_Q": rank,
        "direct_gap": gap,
        "cyclotomic_signature_checked": [4, 12, 24],
        "D24_ascending": D,
        "quotient_ascending": quotient,
        "remainder_ascending": [0] * len(P),
    }
    records.append(rec)
    print(json.dumps(rec, sort_keys=True))

print("D24 degree:", len(D)-1)
print("D24 has only 0/1 coefficients:", all(x in (0,1) for x in D))
print("WITNESS_AUDIT_PASS")
