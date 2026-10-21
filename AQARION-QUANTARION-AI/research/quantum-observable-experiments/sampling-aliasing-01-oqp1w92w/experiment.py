from fractions import Fraction as F

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def cross(a, h):
    return (
        a[1]*h[2] - a[2]*h[1],
        a[2]*h[0] - a[0]*h[2],
        a[0]*h[1] - a[1]*h[0],
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
        pivot = rows[r][col]
        rows[r] = [x / pivot for x in rows[r]]
        for i in range(len(rows)):
            if i != r:
                q = rows[i][col]
                rows[i] = [
                    x - q*y for x, y in zip(rows[i], rows[r])
                ]
        r += 1
        if r == len(rows):
            break
    return r

h = (F(3,5), F(0), F(4,5))
ez = (F(0), F(0), F(1))
axes = [
    (F(1), F(0), F(0)),
    (F(0), F(1), F(0)),
    ez,
]
check(sum(x*x for x in h) == 1, "Axis normalization")

def rotation(v, c, s):
    dot = sum(a*b for a, b in zip(h, v))
    w = cross(v, h)
    return tuple(
        c*v[i] + (1-c)*h[i]*dot + s*w[i]
        for i in range(3)
    )

quarter = lambda v: rotation(v, F(0), F(1))
half = lambda v: rotation(v, F(-1), F(0))
full = lambda v: rotation(v, F(1), F(0))

for v in axes:
    check(
        quarter(quarter(v)) == half(v),
        "Quarter/half rotation mismatch",
    )
    check(
        half(half(v)) == v == full(v),
        "Rotation periodicity mismatch",
    )
    check(
        sum(x*x for x in quarter(v)) == 1,
        "Rotation norm mismatch",
    )

check(quarter(h) == h, "Axis must be fixed")
check(
    quarter(ez) == (F(12,25), F(3,5), F(16,25)),
    "Quarter-turn coefficients",
)
check(
    half(ez) == (F(24,25), F(0), F(7,25)),
    "Half-turn coefficients",
)

for name, operator, expected in [
    ("PI_OVER_2", quarter, 4),
    ("PI", half, 3),
    ("TWO_PI", full, 2),
]:
    orbit = [ez]
    for unused in range(3):
        orbit.append(operator(orbit[-1]))
    dimension = 1 + rank(orbit[:3])
    check(dimension == expected, "Sampled dimension mismatch")
    check(
        rank(orbit) == dimension - 1,
        "Next iterate escaped the sampled span",
    )
    print(
        "SAMPLE:", name,
        "DIMENSION_WITH_CONSTANT:", dimension,
    )

witness = (F(0), F(1), F(0))
check(sum(x*x for x in witness) == 1, "Witness purity")
check(
    ez[1] == half(ez)[1] == 0,
    "Bad-schedule witness disagreement",
)
check(
    quarter(ez)[1] == F(3,5),
    "Continuous-time witness separation",
)

print("BAD_SCHEDULE_ALL_INTEGER_TIMES=PROVED_BY_PERIOD_TWO")
print("WITNESS_STATES=(I+Y)/2_AND_(I-Y)/2")
print("Z_AT_PI_OVER_2:", ("3/5", "-3/5"))

for v in axes:
    z0 = v[2]
    z1 = sum(a*b for a, b in zip(quarter(ez), v))
    z2 = sum(a*b for a, b in zip(half(ez), v))
    recovered = (
        (25*z2 - 7*z0)/24,
        F(5,6)*(2*z1 - z2 - z0),
        z0,
    )
    check(recovered == v, "Reconstruction failure")

print("GOOD_SCHEDULE_RECONSTRUCTION=PASS")
print("ARITHMETIC=EXACT_FRACTION")
print(
    "SCOPE=UNCONDITIONAL_SINGLE_TIME_EXPECTATIONS_"
    "ON_SEPARATELY_PREPARED_COPIES"
)
print("SAMPLING_ALIASING_EXPERIMENT=PASS")
