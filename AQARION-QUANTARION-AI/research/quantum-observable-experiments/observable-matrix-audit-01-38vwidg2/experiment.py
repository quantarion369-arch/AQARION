from fractions import Fraction as F
from itertools import product
from collections import Counter

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def z(r=0, i=0):
    return (F(r), F(i))

def za(a, b):
    return (a[0]+b[0], a[1]+b[1])

def zm(a, b):
    return (
        a[0]*b[0]-a[1]*b[1],
        a[0]*b[1]+a[1]*b[0],
    )

def zs(a, q):
    return (a[0]*q, a[1]*q)

def scale(A, q):
    return [[zs(x, q) for x in row] for row in A]

def plus(A, B):
    return [
        [za(x, y) for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]

def mm(A, B):
    return [
        [
            za(
                zm(A[i][0], B[0][j]),
                zm(A[i][1], B[1][j]),
            )
            for j in range(2)
        ]
        for i in range(2)
    ]

def trace(A):
    return za(A[0][0], A[1][1])

def generator(H, O):
    commutator = plus(mm(H, O), scale(mm(O, H), -1))
    return [
        [zm(z(0, 1), x) for x in row]
        for row in commutator
    ]

I = [[z(1), z()], [z(), z(1)]]
X = [[z(), z(1)], [z(1), z()]]
Y = [[z(), z(0, -1)], [z(0, 1), z()]]
Z = [[z(1), z()], [z(), z(-1)]]
P = [I, X, Y, Z]
ZERO = scale(I, 0)

def coefficients(O):
    out = []
    for B in P:
        value = trace(mm(B, O))
        require(value[1] == 0, "Non-real Pauli coefficient")
        out.append(value[0]/2)
    rebuilt = ZERO
    for q, B in zip(out, P):
        rebuilt = plus(rebuilt, scale(B, q))
    require(rebuilt == O, "Pauli reconstruction failed")
    return tuple(out)

def cross(a, h):
    return (
        a[1]*h[2]-a[2]*h[1],
        a[2]*h[0]-a[0]*h[2],
        a[0]*h[1]-a[1]*h[0],
    )

def rank(vectors):
    rows = [list(v) for v in vectors]
    r = 0
    for col in range(4):
        pivot = next(
            (i for i in range(r, len(rows)) if rows[i][col]),
            None,
        )
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        q = rows[r][col]
        rows[r] = [x/q for x in rows[r]]
        for i in range(len(rows)):
            if i != r:
                q = rows[i][col]
                rows[i] = [
                    x-q*y for x, y in zip(rows[i], rows[r])
                ]
        r += 1
        if r == len(rows):
            break
    return r

counts = Counter()
sign_kills = scale_kills = images = 0

for axis in product(range(-2, 3), repeat=3):
    h = tuple(map(F, axis))
    H = ZERO
    for q, B in zip(h, P[1:]):
        H = plus(H, scale(B, q/2))

    sign_rejected = False
    scale_rejected = False
    require(generator(H, I) == ZERO, "Identity is not fixed")
    norm2 = sum(q*q for q in h)

    for index, O in enumerate(P):
        direct = coefficients(generator(H, O))
        a = tuple(
            F(int(index == j+1)) for j in range(3)
        )
        expected = (F(0),) + cross(a, h)
        require(
            direct == expected,
            "Matrix/vector generator mismatch",
        )

        sign_rejected |= (
            coefficients(scale(generator(H, O), -1))
            != expected
        )
        scale_rejected |= (
            coefficients(generator(scale(H, 2), O))
            != expected
        )

        O1 = generator(H, O)
        O3 = generator(H, generator(H, O1))
        require(
            O3 == scale(O1, -norm2),
            "Matrix generator cubic failed",
        )
        images += 1

    sign_kills += sign_rejected
    scale_kills += scale_rejected

    orbit = [I, Z]
    O = Z
    for unused in range(3):
        O = generator(H, O)
        orbit.append(O)

    vectors = [coefficients(O) for O in orbit]
    dimension = rank(vectors[:4])
    require(
        rank(vectors) == dimension,
        "Matrix Krylov invariance failed",
    )
    counts[dimension] += 1

require(
    dict(counts) == {2: 5, 3: 24, 4: 96},
    "Dimension count mismatch",
)
require(
    sign_kills == scale_kills == 124,
    "Mutant detection mismatch",
)

print("HAMILTONIANS_CHECKED: 125")
print("BASIS_GENERATOR_IMAGES_CHECKED:", images)
for dimension in sorted(counts):
    print(
        "DIMENSION_WITH_CONSTANT:", dimension,
        "COUNT:", counts[dimension],
    )
print("MATRIX_VECTOR_GENERATOR_MATCH=PASS")
print("PAULI_TRACE_RECONSTRUCTION=PASS")
print("MATRIX_KRYLOV_INVARIANCE=PASS")
print("MATRIX_GENERATOR_CUBIC=PASS")
print("SIGN_MUTANT_REJECTED_NONZERO_AXES:", sign_kills)
print("MISSING_HALF_MUTANT_REJECTED_NONZERO_AXES:", scale_kills)
print("ZERO_AXIS_MUTATION_INSENSITIVITY=EXPECTED")
print("ARITHMETIC=EXACT_GAUSSIAN_RATIONAL_PAIRS")
print(
    "SCOPE=IMPLEMENTATION_AUDIT_"
    "NOT_NEW_PHYSICS_OR_FORMAL_PROOF"
)
print("DIRECT_MATRIX_GENERATOR_AUDIT=PASS")
