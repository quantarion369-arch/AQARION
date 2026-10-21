from fractions import Fraction as F
from itertools import product
from collections import Counter

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def cross(a, b):
    return (
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0],
    )

def rank(vectors):
    a = [[F(x) for x in v] for v in vectors]
    r = 0

    for column in range(3):
        pivot = next(
            (i for i in range(r, len(a)) if a[i][column]),
            None,
        )
        if pivot is None:
            continue

        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][column]
        a[r] = [x/value for x in a[r]]

        for i in range(r+1, len(a)):
            value = a[i][column]
            a[i] = [
                x-value*y for x, y in zip(a[i], a[r])
            ]

        r += 1

    return r

def determinant(a, b, c):
    bc = cross(b, c)
    return sum(x*y for x, y in zip(a, bc))

counts = Counter()
tested = 0
z = (F(0), F(0), F(1))

for h in product(range(-2, 3), repeat=3):
    hx, hy, hz = h
    transverse = hx*hx + hy*hy
    norm_squared = transverse + hz*hz

    v1 = cross(z, h)
    v2 = cross(v1, h)
    v3 = cross(v2, h)

    if transverse == 0:
        predicted = 2
    elif hz == 0:
        predicted = 3
    else:
        predicted = 4

    observed = rank([z, v1, v2]) + 1

    require(
        observed == predicted,
        "Classification failed at " + str(h),
    )
    require(
        rank([z, v1, v2, v3]) + 1 == observed,
        "Invariance failed at " + str(h),
    )
    require(
        determinant(z, v1, v2) == -hz*transverse,
        "Determinant identity failed at " + str(h),
    )
    require(
        v3 == tuple(-norm_squared*x for x in v1),
        "Generator recurrence failed at " + str(h),
    )

    counts[observed] += 1
    tested += 1

require(tested == 125, "Wrong test count")
require(
    dict(counts) == {2: 5, 3: 24, 4: 96},
    "Unexpected dimension counts",
)

print("HAMILTONIANS_CHECKED:", tested)
for dimension in (2, 3, 4):
    print(
        "DIMENSION_WITH_CONSTANT:",
        dimension,
        "COUNT:",
        counts[dimension],
    )

print("CLASSIFICATION_MATCH=PASS")
print("GENERATOR_INVARIANCE=PASS")
print("DETERMINANT_IDENTITY=PASS")
print("GENERATOR_CUBIC_RECURRENCE=PASS")
print("ZERO_HAMILTONIAN_INCLUDED=True")
print("ARITHMETIC=EXACT_FRACTION")
print("PROOF_SCOPE=ALL_REAL_TIME_INDEPENDENT_QUBIT_AXES")
print("REGRESSION_SCOPE=INTEGER_GRID_MINUS_2_TO_2")
print("GENERAL_GENERATOR_CLOSURE_EXPERIMENT=PASS")
