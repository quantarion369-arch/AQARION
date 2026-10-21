from math import gcd, prod
from random import Random

SEED = 20261021
rng = Random(SEED)

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def rejected(call, message):
    try:
        call()
    except ValueError:
        return
    raise RuntimeError(message)

class Barrett:
    def __init__(self, q):
        if (
            type(q) is not int
            or q < 3
            or q & (q-1) == 0
        ):
            raise ValueError(
                "Require integer q >= 3, not a power of two"
            )
        self.q = q
        self.shift = 2*q.bit_length()
        self.mu = (1 << self.shift)//q

    def intermediate(self, T):
        if (
            type(T) is not int
            or not 0 <= T < self.q*self.q
        ):
            raise ValueError(
                "Unsigned Barrett input outside declared range"
            )
        estimate = (T*self.mu) >> self.shift
        return T-estimate*self.q, estimate

    def reduce(self, T):
        r, unused = self.intermediate(T)
        return r-self.q if r >= self.q else r

    def signed(self, T):
        if (
            type(T) is not int
            or not -self.q*self.q < T < self.q*self.q
        ):
            raise ValueError(
                "Signed wrapper input outside declared range"
            )
        r = self.reduce(abs(T))
        return self.q-r if T < 0 and r else r

barrett_total = 0
signed_total = 0

for q in (17, 3329, 8380417):
    reducer = Barrett(q)
    boundaries = [
        0, 1, q-1, q, q+1, 2*q-1, 2*q,
        (q-1)**2, q*q-2, q*q-1,
        q*(q-1), q*(q-1)-1,
    ]

    if q == 17:
        tests = list(range(q*q))
    else:
        tests = boundaries + [
            rng.randrange(q*q) for unused in range(2000)
        ]

    for T in tests:
        r, estimate = reducer.intermediate(T)
        check(0 <= r < 2*q, "Barrett intermediate range")
        check(
            T//q-1 <= estimate <= T//q,
            "Barrett quotient estimate",
        )
        out = reducer.reduce(T)
        check(
            out == T % q and 0 <= out < q,
            "Barrett oracle or canonical range",
        )

    if q == 17:
        signed_tests = list(range(-q*q+1, q*q))
    else:
        signed_tests = [
            -q*q+1, -q, -1, 0, 1, q, q*q-1,
        ] + [
            rng.randrange(-q*q+1, q*q)
            for unused in range(1000)
        ]

    for T in signed_tests:
        check(
            reducer.signed(T) == T % q,
            "Signed Barrett wrapper",
        )

    for bad in (-1, q*q, q*q+1):
        rejected(
            lambda bad=bad: reducer.reduce(bad),
            "Unsigned range not rejected",
        )

    for bad in (-q*q, q*q):
        rejected(
            lambda bad=bad: reducer.signed(bad),
            "Signed range not rejected",
        )

    check(
        reducer.intermediate(q)[0] == q
        and reducer.reduce(q) == 0,
        "Missing-final-subtraction mutant was not exposed",
    )

    barrett_total += len(tests)
    signed_total += len(signed_tests)
    print(
        "BARRETT q=", q,
        "UNSIGNED_CASES:", len(tests),
        "SIGNED_CASES:", len(signed_tests),
        "PASS",
    )

small = Barrett(17)
T = 17*17-1
ceil_mu = ((1 << small.shift)+16)//17
wrong = T-((T*ceil_mu) >> small.shift)*17
wrong = wrong-17 if wrong >= 17 else wrong
check(wrong != T % 17, "Ceiling reciprocal mutant survived")

wrong_shift_found = any(
    (
        lambda r: r-17 if r >= 17 else r
    )(T-((T*small.mu) >> (small.shift-1))*17)
    != T % 17
    for T in range(17*17)
)
check(wrong_shift_found, "Wrong-shift mutant survived")

def crt_unsigned(residues, moduli):
    if not moduli or len(residues) != len(moduli):
        raise ValueError("Empty CRT system or length mismatch")
    if any(type(m) is not int or m < 2 for m in moduli):
        raise ValueError("Invalid modulus")
    if any(type(r) is not int for r in residues):
        raise ValueError("Invalid residue")
    if any(
        gcd(moduli[i], moduli[j]) != 1
        for i in range(len(moduli))
        for j in range(i)
    ):
        raise ValueError("Noncoprime moduli")

    x = 0
    M = 1
    for r, m in zip(residues, moduli):
        t = ((r-x)*pow(M, -1, m)) % m
        x += M*t
        M *= m
    return x, M

def crt_signed(residues, moduli, C):
    if type(C) is not int or C < 0:
        raise ValueError("Invalid signed coefficient bound")
    x, M = crt_unsigned(residues, moduli)
    if M <= 2*C:
        raise ValueError(
            "Insufficient modulus product for uniform uniqueness"
        )
    if 2*x > M:
        x -= M
    if abs(x) > C:
        raise ValueError(
            "Residues incompatible with declared coefficient bound"
        )
    return x

crt_cases = 0
for mods in ((7,13), (5,7,11), (2,17)):
    M = prod(mods)
    C = (M-1)//2
    for c in range(-C, C+1):
        residues = [c % m for m in mods]
        x, Q = crt_unsigned(residues, mods)

        oracle = sum(
            r*(M//m)*pow(M//m, -1, m)
            for r, m in zip(residues, mods)
        ) % M

        check(
            Q == M and x == oracle and x == c % M,
            "Unsigned CRT oracle",
        )
        check(
            crt_signed(residues, mods, C) == c,
            "Signed CRT oracle",
        )

        noncanonical = [
            r+(i-1)*m
            for i, (r,m) in enumerate(zip(residues, mods))
        ]
        check(
            crt_signed(noncanonical, mods, C) == c,
            "CRT representative handling",
        )
        crt_cases += 1

check(
    [(-45) % m for m in (7,13)]
    == [46 % m for m in (7,13)],
    "Ambiguity witness",
)
rejected(
    lambda: crt_signed([46 % 7, 46 % 13], (7,13), 46),
    "Insufficient bound accepted",
)

check(
    [(-17) % m for m in (2,17)]
    == [17 % m for m in (2,17)],
    "Equality-bound witness",
)
rejected(
    lambda: crt_signed([1,0], (2,17), 17),
    "Q equals 2C was accepted",
)
rejected(
    lambda: crt_signed([42 % 7, 42 % 13], (7,13), 40),
    "Incompatible residue bound accepted",
)

for residues, moduli in [
    ([0,0], (6,9)),
    ([0,0], (7,7)),
    ([0], (1,)),
    ([], ()),
    ([0], (7,13)),
]:
    rejected(
        lambda residues=residues, moduli=moduli:
            crt_unsigned(residues, moduli),
        "Invalid CRT system accepted",
    )

check(
    crt_unsigned([6,12], (7,13))[0] == 90,
    "Unsigned representative witness",
)
check(
    crt_signed([6,12], (7,13), 45) == -1,
    "Centered representative witness",
)
check(
    crt_signed([6,5], (7,13), 45) != 19,
    "Residue ordering mutant survived",
)

def schoolbook(a, b):
    out = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out

def modular_product(a, b, m):
    return [
        sum(
            (a[i] % m)*(b[k-i] % m)
            for i in range(
                max(0, k-len(b)+1),
                min(len(a)-1, k)+1,
            )
        ) % m
        for k in range(len(a)+len(b)-1)
    ]

mods = (17,97,193)
fixtures = [
    ([0], [0]),
    ([-1], [1]),
    ([2,-3,4], [-5,0,6]),
    ([20]*12, [-20]*12),
]
for unused in range(200):
    a = [
        rng.randrange(-20,21)
        for unused in range(rng.randrange(1,13))
    ]
    b = [
        rng.randrange(-20,21)
        for unused in range(rng.randrange(1,13))
    ]
    fixtures.append((a,b))

coefficient_cases = 0
for a, b in fixtures:
    C = (
        min(len(a), len(b))
        * max(map(abs, a))
        * max(map(abs, b))
    )
    check(
        prod(mods) > 2*C,
        "Fixture has insufficient CRT modulus product",
    )

    expected = schoolbook(a, b)
    residues = [modular_product(a, b, m) for m in mods]
    recovered = [
        crt_signed([r[k] for r in residues], mods, C)
        for k in range(len(expected))
    ]

    check(
        recovered == expected,
        "Signed polynomial-product oracle",
    )
    check(
        all(abs(c) <= C for c in expected),
        "Coefficient bound violated",
    )
    coefficient_cases += len(expected)

print("TOTAL_BARRETT_UNSIGNED_CASES:", barrett_total)
print("TOTAL_SIGNED_WRAPPER_CASES:", signed_total)
print("TOTAL_CRT_INTEGER_CASES:", crt_cases)
print("SIGNED_POLYNOMIAL_PRODUCTS:", len(fixtures))
print("RECONSTRUCTED_PRODUCT_COEFFICIENTS:", coefficient_cases)
print("BARRETT_RANGE_INTERMEDIATE_AND_CANONICAL_ORACLES=PASS")
print("SIGNED_BARRETT_WRAPPER=PASS")
print("MISSING_FINAL_SUBTRACTION_MUTANT=REJECTED")
print("CEILING_RECIPROCAL_MUTANT=REJECTED")
print("WRONG_SHIFT_MUTANT=REJECTED")
print("SIGNED_CRT_PRODUCT_ORACLE=PASS")
print("INSUFFICIENT_CRT_BOUND=REJECTED")
print("Q_EQUALS_2C_BOUNDARY=REJECTED")
print("RESIDUES_INCOMPATIBLE_WITH_BOUND=REJECTED")
print("NONCOPRIME_AND_INVALID_CRT_SYSTEMS=REJECTED")
print("UNSIGNED_CENTERING_AND_ORDERING_MUTANTS=REJECTED")
print("AMBIGUITY_WITNESS: -45 AND 46 MODULO 91")
print("RANDOM_SEED:", SEED)
print("ARITHMETIC=EXACT_PYTHON_INTEGERS")
print("SCOPE=GENERIC_BARRETT_AND_SIGNED_LINEAR_CONVOLUTION_CRT")
print(
    "NO_NTT_INTEGRATION_NIST_CONFORMANCE_"
    "CONSTANT_TIME_OR_TIMING_CLAIM"
)
print("BARRETT_CRT_AUDIT=PASS")
