from fractions import Fraction as F

# Gaussian rational numbers: (real part, imaginary part).
def c(r=0, i=0):
    return (F(r), F(i))

def add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def neg(a):
    return (-a[0], -a[1])

def times(a, b):
    return (
        a[0]*b[0]-a[1]*b[1],
        a[0]*b[1]+a[1]*b[0],
    )

def conj(a):
    return (a[0], -a[1])

def scale(A, s):
    return [[times(s, x) for x in row] for row in A]

def plus(A, B):
    return [
        [add(x, y) for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]

def mm(A, B):
    return [
        [
            add(
                times(A[i][0], B[0][j]),
                times(A[i][1], B[1][j]),
            )
            for j in range(2)
        ]
        for i in range(2)
    ]

def dag(A):
    return [
        [conj(A[j][i]) for j in range(2)]
        for i in range(2)
    ]

def tr(A):
    return add(A[0][0], A[1][1])

def mean(rho, O):
    value = tr(mm(rho, O))
    if value[1]:
        raise RuntimeError("Non-real expectation")
    return value[0]

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

I = [[c(1), c()], [c(), c(1)]]
X = [[c(), c(1)], [c(1), c()]]
Y = [[c(), c(0, -1)], [c(0, 1), c()]]
Z = [[c(1), c()], [c(), c(-1)]]

P0 = [[c(1), c()], [c(), c()]]
P1 = [[c(), c()], [c(), c(1)]]
basis = [I, X, Y, Z]

# U = B/sqrt(2); channels use B and an exact factor 1/2.
B = [[c(1), c(0, -1)], [c(0, -1), c(1)]]
require(
    mm(dag(B), B) == scale(I, c(2)),
    "Unitary normalization failed",
)

def evolve(rho):
    return scale(
        mm(mm(B, rho), dag(B)),
        c(F(1, 2)),
    )

def heisenberg(O):
    return scale(
        mm(mm(dag(B), O), B),
        c(F(1, 2)),
    )

def populations(rho):
    return (mean(rho, P0), mean(rho, P1))

def dephase(rho):
    return [[rho[0][0], c()], [c(), rho[1][1]]]

def coords(O):
    return tuple(mean(P, O)/2 for P in basis)

def generator(O):
    commutator = plus(
        mm(X, O),
        scale(mm(O, X), c(-1)),
    )
    return scale(commutator, c(0, F(1, 2)))

# Six physical states: the +/- eigenstates of X, Y, Z.
states = [
    scale(
        plus(I, scale(O, c(sign))),
        c(F(1, 2)),
    )
    for O in (X, Y, Z)
    for sign in (1, -1)
]

checks = 0

for rho in states:
    state = rho
    evolved_observables = basis[:]

    for step in range(9):
        require(
            state == dag(state) and tr(state) == c(1),
            "Invalid state symmetry or trace",
        )

        determinant = add(
            times(state[0][0], state[1][1]),
            neg(times(state[0][1], state[1][0])),
        )

        require(
            state[0][0][0] >= 0
            and state[1][1][0] >= 0
            and determinant[1] == 0
            and determinant[0] >= 0,
            "State positivity failed",
        )

        for O, Ot in zip(basis, evolved_observables):
            require(
                mean(state, O) == mean(rho, Ot),
                "State/observable picture mismatch",
            )
            checks += 1

        state = evolve(state)
        evolved_observables = [
            heisenberg(O) for O in evolved_observables
        ]

print("PICTURE_PAIRING_CHECKS:", checks)
print("SCHRODINGER_HEISENBERG_DICTIONARY=PASS")

# Same populations, opposite coherence.
rp = scale(plus(I, Y), c(F(1, 2)))
rm = scale(
    plus(I, scale(Y, c(-1))),
    c(F(1, 2)),
)

require(
    populations(rp) == populations(rm) == (F(1, 2), F(1, 2)),
    "Initial populations differ",
)
require(
    populations(evolve(rp)) == (F(1), F(0)),
    "Unexpected plus-state evolution",
)
require(
    populations(evolve(rm)) == (F(0), F(1)),
    "Unexpected minus-state evolution",
)

print("SAME_INITIAL_POPULATIONS:",
      tuple(map(str, populations(rp))))
print("NEXT_POPULATIONS_PLUS:",
      tuple(map(str, populations(evolve(rp)))))
print("NEXT_POPULATIONS_MINUS:",
      tuple(map(str, populations(evolve(rm)))))
print("POPULATION_ONLY_CLOSURE=REFUTED")

# Continuous-time generator closure, not just sampled agreement.
require(
    generator(Z) == Y
    and generator(Y) == scale(Z, c(-1)),
    "Generator identities failed",
)

for O in (I, Y, Z):
    require(
        coords(generator(O))[1] == 0,
        "Augmented space is not invariant",
    )

require(
    mm(Y, Z) == scale(X, c(0, 1)),
    "Observable product identity failed",
)

print("GENERATOR_Z=Y; GENERATOR_Y=-Z")
print("AUGMENTED_LINEAR_CLOSURE=PASS")
print("AUGMENTED_SPACE_IS_MULTIPLICATION_ALGEBRA=False")

# Uninterrupted evolution versus intermediate dephasing.
coherent = evolve(evolve(P0))
interrupted = evolve(dephase(evolve(P0)))

require(
    populations(coherent) == (F(0), F(1)),
    "Coherent two-step result failed",
)
require(
    populations(interrupted) == (F(1, 2), F(1, 2)),
    "Dephased two-step result failed",
)

print("TWO_STEP_COHERENT:",
      tuple(map(str, populations(coherent))))
print("TWO_STEP_WITH_INTERMEDIATE_DEPHASING:",
      tuple(map(str, populations(interrupted))))
print("INTERMEDIATE_COHERENCE_LOSS=DETECTED")
print("ARITHMETIC=EXACT_RATIONAL_COMPLEX_PAIRS")
print("SCOPE=TWO_LEVEL_TOY_MODEL_NOT_A_NEUTRINO_SIMULATION")
print("QUANTUM_OBSERVABLE_PILOT=PASS")
