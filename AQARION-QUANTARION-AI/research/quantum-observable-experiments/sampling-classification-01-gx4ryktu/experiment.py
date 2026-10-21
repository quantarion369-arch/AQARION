from fractions import Fraction as F
from itertools import product
from collections import Counter

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def cross(a, b):
    return (
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0],
    )

def rank(vectors):
    rows = [[F(x) for x in v] for v in vectors]
    r = 0
    for col in range(3):
        p = next(
            (i for i in range(r, len(rows)) if rows[i][col]),
            None,
        )
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
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

def determinant(rows):
    return sum(
        a*b for a, b in zip(
            rows[0], cross(rows[1], rows[2])
        )
    )

def rotate(v, u, c, s):
    dot = sum(a*b for a, b in zip(u, v))
    w = cross(v, u)
    return tuple(
        c*v[i] + (1-c)*u[i]*dot + s*w[i]
        for i in range(3)
    )

def predicted(u, c, s):
    transverse = 1-u[2]*u[2]
    if not transverse or c == 1:
        return 2
    if not s:
        return 2 if u[2] == 0 else 3
    return 3 if u[2] == 0 else 4

axes = set()
for p, q in product(range(-2, 3), repeat=2):
    d = 1+p*p+q*q
    axes.add((
        F(2*p, d),
        F(2*q, d),
        F(1-p*p-q*q, d),
    ))
axes.add((F(0), F(0), F(-1)))

angles = set()
for t in range(-2, 3):
    angles.add((
        F(1-t*t, 1+t*t),
        F(2*t, 1+t*t),
    ))
angles.add((F(-1), F(0)))

ez = (F(0), F(0), F(1))
basis = [
    (F(1), F(0), F(0)),
    (F(0), F(1), F(0)),
    ez,
]
counts = Counter()

for u in sorted(axes):
    check(sum(x*x for x in u) == 1, "Non-unit axis")
    for c, s in sorted(angles):
        check(c*c+s*s == 1, "Invalid sine/cosine pair")

        orbit = [ez]
        for unused in range(3):
            orbit.append(rotate(orbit[-1], u, c, s))

        dimension = 1+rank(orbit[:3])
        check(
            dimension == predicted(u, c, s),
            "Classification mismatch",
        )
        check(
            rank(orbit) == dimension-1,
            "Sampled closure failed",
        )

        expected = -2*u[2]*(1-u[2]*u[2])*s*(1-c)
        check(
            determinant(orbit[:3]) == expected,
            "Determinant identity failed",
        )

        for v in basis:
            v1 = rotate(v, u, c, s)
            v2 = rotate(v1, u, c, s)
            v3 = rotate(v2, u, c, s)
            residual = tuple(
                v3[i]-(1+2*c)*v2[i]+(1+2*c)*v1[i]-v[i]
                for i in range(3)
            )
            check(
                residual == (0, 0, 0),
                "Rotation cubic failed",
            )

        counts[dimension] += 1

check(
    dict(counts) == {2: 40, 3: 36, 4: 80},
    "Regression count mismatch",
)

# Zero Hamiltonian: identity propagator at every interval.
check(
    1+rank([ez, ez, ez]) == 2,
    "Zero-Hamiltonian case failed",
)

print("UNIT_AXES_CHECKED:", len(axes))
print("EXACT_ROTATIONS_PER_AXIS:", len(angles))
print(
    "AXIS_ROTATION_PAIRS_CHECKED:",
    len(axes)*len(angles),
)
for dimension in sorted(counts):
    print(
        "DIMENSION_WITH_CONSTANT:", dimension,
        "COUNT:", counts[dimension],
    )
print("ZERO_HAMILTONIAN_DIMENSION: 2")
print("CLASSIFICATION_MATCH=PASS")
print("DETERMINANT_IDENTITY=PASS")
print("SAMPLED_INVARIANCE=PASS")
print("ROTATION_CUBIC_RECURRENCE=PASS")
print("ARITHMETIC=EXACT_FRACTION_NO_TRIG_ROUNDING")
print(
    "THEOREM_SCOPE=ALL_REAL_FIXED_QUBIT_AXES_"
    "AND_UNIFORM_SAMPLING_INTERVALS"
)
print(
    "REGRESSION_SCOPE=26_RATIONAL_AXES_"
    "TIMES_6_EXACT_ROTATIONS"
)
print(
    "SCOPE=SEPARATELY_PREPARED_COPIES_"
    "NOT_SEQUENTIAL_MEASUREMENT"
)
print("GENERAL_SAMPLING_CLASSIFICATION_EXPERIMENT=PASS")
