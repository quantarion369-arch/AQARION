from fractions import Fraction as F
from collections import deque

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

def closure(generators):
    basis = [(F(0), F(0), F(1))]
    queue = deque(basis)
    while queue:
        v = queue.popleft()
        for h in generators:
            w = cross(v, h)
            if rank(basis+[w]) > len(basis):
                basis.append(w)
                queue.append(w)
    for v in basis:
        for h in generators:
            check(
                rank(basis+[cross(v, h)]) == len(basis),
                "Closure failure",
            )
    return basis

ex = (F(1), F(0), F(0))
ey = (F(0), F(1), F(0))
ez = (F(0), F(0), F(1))
axes = {"X": ex, "Y": ey}

for name, generators, expected in [
    ("X_ONLY", [ex], 3),
    ("Y_ONLY", [ey], 3),
    ("COMMON_X_Y", [ex, ey], 4),
]:
    B = closure(generators)
    check(
        1+len(B) == expected,
        "Closure dimension mismatch",
    )
    print(
        "CASE:", name,
        "DIMENSION_WITH_CONSTANT:", 1+len(B),
    )

# The +/-X witness difference is orthogonal to the
# entire fixed-X observable space, proving invisibility
# for every fixed-X evolution time.
check(
    all(
        sum(a*b for a, b in zip(v, ex)) == 0
        for v in closure([ex])
    ),
    "Fixed-X witness not invisible",
)

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

def dagger(A):
    return [
        [
            (A[j][i][0], -A[j][i][1])
            for j in range(2)
        ]
        for i in range(2)
    ]

def trace(A):
    return za(A[0][0], A[1][1])

I = [[z(1), z()], [z(), z(1)]]
X = [[z(), z(1)], [z(1), z()]]
Y = [[z(), z(0, -1)], [z(0, 1), z()]]
Z = [[z(1), z()], [z(), z(-1)]]
P = [X, Y, Z]

# Each pulse lasts pi/2.
# V = sqrt(2)*U = I - i*P.
# The channel uses V*rho*V_dagger/2, so all arithmetic
# remains rational despite the square root in U.
V = {}
for name, M in [("X", X), ("Y", Y)]:
    minus_i_M = [
        [zm(z(0, -1), x) for x in row]
        for row in M
    ]
    V[name] = plus(I, minus_i_M)
    check(
        mm(dagger(V[name]), V[name]) == scale(I, 2),
        "Pulse normalization",
    )

def state_pulse(rho, name):
    return scale(
        mm(mm(V[name], rho), dagger(V[name])),
        F(1, 2),
    )

def observable_pulse(a, name):
    h = axes[name]
    dot = sum(x*y for x, y in zip(h, a))
    w = cross(a, h)
    return tuple(h[i]*dot+w[i] for i in range(3))

protocols = [
    ("X_THEN_Y", ("X", "Y")),
    ("Y_THEN_X", ("Y", "X")),
]
comparisons = 0
wrong_order_rejected = 0
outputs = {}

for label, protocol in protocols:
    a = ez
    for name in reversed(protocol):
        a = observable_pulse(a, name)

    wrong = ez
    for name in protocol:
        wrong = observable_pulse(wrong, name)

    for j, M in enumerate(P):
        for sign in (1, -1):
            rho = scale(
                plus(I, scale(M, sign)),
                F(1, 2),
            )
            evolved = rho
            for name in protocol:
                evolved = state_pulse(evolved, name)

            value = trace(mm(Z, evolved))
            expected = sign*a[j]
            check(
                value == z(expected),
                "Schrodinger/Heisenberg pulse mismatch",
            )
            check(
                trace(evolved) == z(1)
                and dagger(evolved) == evolved,
                "Invalid evolved state",
            )
            det = za(
                zm(evolved[0][0], evolved[1][1]),
                zs(zm(evolved[0][1], evolved[1][0]), -1),
            )
            check(
                det == z(),
                "Pure-state determinant changed",
            )

            wrong_order_rejected += (
                sign*wrong[j] != expected
            )
            comparisons += 1
            if j == 0:
                outputs[(label, sign)] = str(expected)

check(
    comparisons == 12 and wrong_order_rejected == 8,
    "Protocol regression counts",
)
check(
    [outputs[("X_THEN_Y", s)] for s in (1, -1)]
    == ["-1", "1"],
    "Switched witness mismatch",
)
check(
    [outputs[("Y_THEN_X", s)] for s in (1, -1)]
    == ["0", "0"],
    "Reverse-protocol witness mismatch",
)

print("FIXED_X_WITNESS_ALL_TIMES=PROVED_BY_INVARIANT_PLANE")
print("WITNESS_STATES=(I+X)/2_AND_(I-X)/2")
for label, unused in protocols:
    print(
        "PROTOCOL:", label,
        "Z_OUTPUTS:",
        tuple(outputs[(label, s)] for s in (1, -1)),
    )
print("SCHRODINGER_HEISENBERG_COMPARISONS:", comparisons)
print(
    "WRONG_OBSERVABLE_COMPOSITION_ORDER_REJECTED:",
    wrong_order_rejected,
)
print("PHYSICAL_STATE_CHECKS=PASS")
print("COMMON_GENERATOR_INVARIANCE=PASS")
print("ARITHMETIC=EXACT_GAUSSIAN_RATIONAL_PAIRS")
print("SCOPE=KNOWN_PIECEWISE_HAMILTONIANS_FINAL_TIME_EXPECTATIONS")
print("NO_INTERMEDIATE_MEASUREMENT_NO_NEUTRINO_SIMULATION")
print("SWITCHED_GENERATOR_CLOSURE_EXPERIMENT=PASS")
