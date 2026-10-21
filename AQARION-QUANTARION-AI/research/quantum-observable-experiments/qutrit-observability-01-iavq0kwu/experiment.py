from fractions import Fraction as F
from collections import deque

def check(ok, message):
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

def total(values):
    out = z()
    for value in values:
        out = za(out, value)
    return out

def real(rows):
    return [[z(x) for x in row] for row in rows]

def diag(values):
    return real([
        [values[i] if i == j else 0 for j in range(3)]
        for i in range(3)
    ])

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
            total(zm(A[i][k], B[k][j]) for k in range(3))
            for j in range(3)
        ]
        for i in range(3)
    ]

def trace(A):
    return total(A[i][i] for i in range(3))

def pairing(A, B):
    return trace(mm(A, B))

def generator(energies, O):
    return [
        [
            zm(z(0, energies[i]-energies[j]), O[i][j])
            for j in range(3)
        ]
        for i in range(3)
    ]

def coordinates(O):
    for i in range(3):
        for j in range(3):
            check(
                O[i][j] == (O[j][i][0], -O[j][i][1]),
                "Not Hermitian",
            )
    return (
        [O[i][i][0] for i in range(3)]
        + [
            value
            for i, j in [(0,1), (0,2), (1,2)]
            for value in O[i][j]
        ]
    )

def rank(vectors):
    rows = [list(v) for v in vectors]
    r = 0
    for col in range(9):
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

def closure(energies, seeds):
    basis = []
    vectors = []
    queue = deque()

    def add(O):
        v = coordinates(O)
        if rank(vectors+[v]) > len(vectors):
            vectors.append(v)
            basis.append(O)
            queue.append(O)

    for O in seeds:
        add(O)
    while queue:
        add(generator(energies, queue.popleft()))

    for O in basis:
        candidate = coordinates(generator(energies, O))
        check(
            rank(vectors+[candidate]) == len(basis),
            "Invariance failed",
        )
    return basis

I = diag([1,1,1])
Q = diag([0,1,-1])
u = [1,2,2]
P = real([
    [F(u[i]*u[j], 9) for j in range(3)]
    for i in range(3)
])
check(
    mm(P,P) == P and trace(P) == z(1),
    "Measurement is not a rank-one projector",
)

generic = (-1,0,2)
resonant = (-1,0,1)
bases = {}

for name, H, seeds, expected in [
    ("GENERIC_ONE_PROJECTOR", generic, [I,P], 8),
    ("GENERIC_PLUS_Q", generic, [I,P,Q], 9),
    ("REPEATED_GAPS_ONE_PROJECTOR", resonant, [I,P], 6),
    ("REPEATED_GAPS_PLUS_Q", resonant, [I,P,Q], 7),
]:
    B = closure(H, seeds)
    check(len(B) == expected, "Dimension mismatch")
    bases[name] = B
    print(
        "CASE:", name,
        "OBSERVABLE_DIMENSION:", len(B),
    )

rho2 = diag([0,1,0])
rho3 = diag([0,0,1])
for rho in (rho2, rho3):
    check(
        mm(rho,rho) == rho and trace(rho) == z(1),
        "Invalid pure-state witness",
    )
    check(
        generator(generic, rho) == diag([0,0,0]),
        "Witness is not stationary",
    )
    check(
        pairing(P,rho) == z(F(4,9)),
        "Stationary witness output",
    )

check(
    all(
        pairing(Q,O) == z()
        for O in bases["GENERIC_ONE_PROJECTOR"]
    ),
    "Q not invisible",
)
check(
    pairing(Q,rho2) == z(1)
    and pairing(Q,rho3) == z(-1),
    "Q fails to distinguish states",
)
print("STATIONARY_WITNESS_P_OUTPUTS:", ("4/9","4/9"))
print("REPAIR_Q_WITNESS_OUTPUTS:", ("1","-1"))
print("STATIONARY_WITNESS_ALL_TIMES=PASS")

B = bases["GENERIC_ONE_PROJECTOR"]
jordan = [
    scale(plus(mm(A,D), mm(D,A)), F(1,2))
    for A in B for D in B
]
check(
    rank([coordinates(O) for O in B+jordan]) == 9,
    "Jordan extension mismatch",
)
print("LINEAR_CLOSURE_DIMENSION: 8")
print("JORDAN_EXTENSION_DIMENSION: 9")
print("LINEAR_SPACE_IS_MULTIPLICATION_ALGEBRA=False")

C = real([[0,2,0], [2,0,-1], [0,-1,0]])
check(
    all(
        pairing(C,O) == z()
        for O in bases["REPEATED_GAPS_PLUS_Q"]
    ),
    "Gap witness not invisible",
)

def leading_minors(M):
    check(
        all(v[1] == 0 for row in M for v in row),
        "State is not real",
    )
    a = [[v[0] for v in row] for row in M]
    det = (
        a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
        - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
        + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
    )
    return (
        a[0][0],
        a[0][0]*a[1][1]-a[0][1]*a[1][0],
        det,
    )

second = []
for sign in (1,-1):
    rho = plus(scale(I,F(1,3)), scale(C,F(sign,12)))
    coordinates(rho)
    check(
        trace(rho) == z(1)
        and all(v > 0 for v in leading_minors(rho)),
        "State positivity failed",
    )
    check(
        pairing(P,rho) == z(F(1,3)),
        "Gap witness initial output",
    )
    check(
        pairing(generator(generic,P),rho) == z(),
        "Gap witness first derivative",
    )
    value = pairing(
        generator(generic,generator(generic,P)),
        rho,
    )
    check(
        value == z(F(sign*2,9)),
        "Gap witness second derivative",
    )
    second.append(str(value[0]))

print("GAP_WITNESS_POSITIVITY=PASS_BY_EXACT_SYLVESTER_MINORS")
print(
    "REPEATED_GAP_WITNESS_ALL_TIMES="
    "PROVED_BY_INVARIANT_SPACE"
)
print("GENERIC_GAP_SECOND_DERIVATIVES:", tuple(second))
print("GENERATOR_INVARIANCE=PASS")
print("ARITHMETIC=EXACT_GAUSSIAN_RATIONAL_PAIRS")
print(
    "SCOPE=THREE_LEVEL_FIXED_HAMILTONIAN_EXPECTATIONS_"
    "NOT_NEUTRINO_SIMULATION"
)
print("QUTRIT_OBSERVABILITY_EXPERIMENT=PASS")
