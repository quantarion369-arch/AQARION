from fractions import Fraction as F

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def cross(a, b):
    return [
        a[1]*b[2]-a[2]*b[1],
        a[2]*b[0]-a[0]*b[2],
        a[0]*b[1]-a[1]*b[0],
    ]

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

# O = a_x X + a_y Y + a_z Z.
# For H = (h_x X + h_y Y + h_z Z)/2:
# i[H,O] has coefficient vector a cross h.
z = [F(0), F(0), F(1)]

cases = [
    ("Z_AXIS", (0, 0, 1), 1),
    ("X_AXIS", (1, 0, 0), 2),
    ("TILTED_AXIS", (1, 0, 1), 3),
]

for name, h, expected_dimension in cases:
    vector = z[:]
    orbit = []
    growth = []

    for step in range(3):
        orbit.append(vector)
        growth.append(rank(orbit))
        vector = cross(vector, h)

    dimension = rank(orbit)

    require(
        dimension == expected_dimension,
        "Unexpected observable dimension: " + name,
    )

    # Also check that the next generator image adds no dimension.
    require(
        rank(orbit + [vector]) == dimension,
        "Generated space did not close: " + name,
    )

    print("CASE:", name)
    print("SPIN_SPAN_GROWTH:", growth)
    print("DIMENSION_WITH_CONSTANT:", dimension+1)
    print("GENERATOR_INVARIANCE=PASS")
    print()

# Tilted model: two valid pure states with Bloch vectors +/-X.
h = (1, 0, 1)
rho_plus = [F(1), F(0), F(0)]
rho_minus = [F(-1), F(0), F(0)]

for state in (rho_plus, rho_minus):
    require(dot(state, state) == 1, "Invalid pure-state vector")

y = [F(0), F(1), F(0)]
Lz = cross(z, h)
L2z = cross(Lz, h)

require(Lz == y, "First generator identity failed")
require(
    L2z == [F(1), F(0), F(-1)],
    "Second generator identity failed",
)

summary_plus = (dot(rho_plus, y), dot(rho_plus, z))
summary_minus = (dot(rho_minus, y), dot(rho_minus, z))

first = (dot(rho_plus, Lz), dot(rho_minus, Lz))
second = (dot(rho_plus, L2z), dot(rho_minus, L2z))

require(
    summary_plus == summary_minus == (F(0), F(0)),
    "Retained summaries do not match",
)
require(first == (F(0), F(0)), "First derivatives differ")
require(second == (F(1), F(-1)), "Second-derivative witness failed")

print("SAME_RETAINED_Y_Z:", tuple(map(str, summary_plus)))
print("Z_FIRST_DERIVATIVES:", tuple(map(str, first)))
print("Z_SECOND_DERIVATIVES:", tuple(map(str, second)))
print("UNIVERSAL_THREE_DIMENSIONAL_REPAIR=REFUTED")
print("HAMILTONIAN_SPECIFIC_CLOSURE=PASS")
print("ARITHMETIC=EXACT_FRACTION")
print("SCOPE=TWO_LEVEL_GENERATOR_TEST_NOT_NEUTRINO_SIMULATION")
print("GENERATOR_CLOSURE_EXPERIMENT=PASS")
