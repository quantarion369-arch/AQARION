from math import prod, gcd
from random import Random
from collections import Counter

class AuditFailure(Exception):
    pass

def need(ok, message):
    if not ok:
        raise AuditFailure(message)

MODS = (97,193,257)
ROOT32 = {97:19,193:8,257:15}
SEED = 20261021
stats = Counter()

def compatible(moduli, required_order):
    for q in moduli:
        if (q-1) % required_order:
            raise ValueError(
                "Required scalar root order unavailable"
            )

class Arithmetic:
    def __init__(self, q):
        self.q = q
        self.R = 1 << q.bit_length()
        self.R2 = self.R*self.R % q
        self.qprime = -pow(q,-1,self.R) % self.R
        self.Rinv = pow(self.R,-1,q)
        self.shift = 2*q.bit_length()
        self.mu = (1 << self.shift)//q

    def canonical(self, x):
        q = self.q
        need(abs(x) < q*q, "Barrett input range")
        T = abs(x)
        r = T-((T*self.mu) >> self.shift)*q
        need(0 <= r < 2*q, "Barrett intermediate range")
        if r >= q:
            r -= q
        if x < 0 and r:
            r = q-r
        need(
            0 <= r < q and r == x % q,
            "Barrett oracle",
        )
        stats["barrett_calls"] += 1
        return r

    def redc(self, T):
        q, R = self.q, self.R
        need(0 <= T < q*R, "REDC input range")
        m = (T*self.qprime) % R
        numerator = T+m*q
        need(numerator % R == 0, "REDC exact division")
        r = numerator//R
        need(0 <= r < 2*q, "REDC intermediate range")
        if r >= q:
            r -= q
        need(
            0 <= r < q and r == (T*self.Rinv) % q,
            "REDC oracle",
        )
        stats["redc_calls"] += 1
        return r

    def encode(self, x):
        a = self.canonical(x)
        out = self.redc(a*self.R2)
        need(
            out == a*self.R % self.q,
            "Montgomery encoding",
        )
        return out

    def multiply(self, a, b):
        need(
            0 <= a < self.q and 0 <= b < self.q,
            "Montgomery operand range",
        )
        return self.redc(a*b)

    def ntt(self, values, omega,
            inverse=False, normalize=True):
        a = list(values)
        n = len(a)
        j = 0
        need(
            n > 0 and n & (n-1) == 0,
            "Transform length",
        )
        need(
            pow(omega,n,self.q) == 1
            and pow(omega,n//2,self.q) == self.q-1,
            "Root order",
        )

        for i in range(1,n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i],a[j] = a[j],a[i]

        if inverse:
            omega = pow(omega,-1,self.q)

        length = 2
        while length <= n:
            step = self.encode(
                pow(omega,n//length,self.q)
            )
            for start in range(0,n,length):
                w = self.encode(1)
                for k in range(start,start+length//2):
                    u = a[k]
                    t = self.multiply(
                        w,a[k+length//2]
                    )
                    a[k] = self.canonical(u+t)
                    a[k+length//2] = self.canonical(u-t)
                    w = self.multiply(w,step)
            length *= 2

        if inverse and normalize:
            f = self.encode(pow(n,-1,self.q))
            a = [self.multiply(x,f) for x in a]
        return a

def crt_signed(residues, C):
    M = prod(MODS)
    if M <= 2*C:
        raise ValueError("CRT uniqueness bound failed")
    need(
        all(
            gcd(MODS[i],MODS[j]) == 1
            for i in range(3) for j in range(i)
        ),
        "CRT moduli",
    )
    x = 0
    current = 1
    for r,q in zip(residues,MODS):
        x += current*((r-x)*pow(current,-1,q) % q)
        current *= q
    if 2*x > M:
        x -= M
    if abs(x) > C:
        raise ValueError(
            "CRT result outside coefficient bound"
        )
    need(
        all(
            x % q == r % q
            for r,q in zip(residues,MODS)
        ),
        "CRT residue verification",
    )
    return x

def oracle(a, b, mode):
    raw = [0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            raw[i+j] += x*y
    n = 32 if mode == "linear" else 16
    if mode == "linear":
        return raw+[0]*(n-len(raw))
    out = [0]*n
    for k,c in enumerate(raw):
        out[k % n] += c if (k//n) % 2 == 0 else -c
    return out

def pipeline(a, b, mode,
             fault=None, forced_C=None):
    need(
        mode in ("linear","negacyclic"),
        "Unknown ring",
    )
    n = 32 if mode == "linear" else 16
    compatible(
        MODS,n if mode == "linear" else 2*n
    )

    if not a or not b or max(len(a),len(b)) > n:
        raise ValueError("Invalid operand length")
    if mode == "linear" and len(a)+len(b)-1 > n:
        raise ValueError("Insufficient zero padding")

    C = (
        min(len(a),len(b))
        * max(map(abs,a))
        * max(map(abs,b))
    )
    if forced_C is not None:
        C = forced_C
    if prod(MODS) <= 2*C:
        raise ValueError("CRT uniqueness bound failed")

    channels = []
    for q in MODS:
        core = Arithmetic(q)
        psi = ROOT32[q]
        omega = psi if mode == "linear" else psi*psi % q
        transformed = []

        for values in (a,b):
            plain = values+[0]*(n-len(values))
            encoded = [core.encode(x) for x in plain]

            if mode == "negacyclic" and fault != "cyclic_sign":
                encoded = [
                    core.multiply(
                        x,core.encode(pow(psi,i,q))
                    )
                    for i,x in enumerate(encoded)
                ]

            out = core.ntt(encoded,omega)
            decoded = [core.redc(x) for x in out]

            direct = [
                sum(
                    x*pow(
                        psi,
                        (k if mode == "linear" else 2*k+1)*i,
                        q,
                    )
                    for i,x in enumerate(plain)
                ) % q
                for k in range(n)
            ]
            need(
                decoded == direct,
                "Direct transform evaluation mismatch",
            )
            stats["forward_oracles"] += 1
            transformed.append(out)

        fa,fb = transformed
        if fault == "ordering":
            fa = fa[::-1]

        if fault == "ordinary_multiply":
            pointwise = [
                core.canonical(x*y)
                for x,y in zip(fa,fb)
            ]
        else:
            pointwise = [
                core.multiply(x,y)
                for x,y in zip(fa,fb)
            ]

        back = core.ntt(
            pointwise,omega,inverse=True,
            normalize=fault != "normalization",
        )

        if mode == "negacyclic" and fault != "cyclic_sign":
            back = [
                core.multiply(
                    x,core.encode(pow(psi,-i,q))
                )
                for i,x in enumerate(back)
            ]

        channels.append(
            back if fault == "decode"
            else [core.redc(x) for x in back]
        )

    recovered = [
        crt_signed([r[k] for r in channels],C)
        for k in range(n)
    ]
    need(
        recovered == oracle(a,b,mode),
        "Integer product oracle mismatch",
    )
    return recovered

rng = Random(SEED)
fixtures = [
    ([1],[1]),
    ([-1],[1]),
    ([0],[0]),
    ([20]*16,[20]*16),
    ([20]*16,[-20]*16),
    ([0]*15+[1],[0,1]),
]
for unused in range(26):
    fixtures.append((
        [
            rng.randint(-20,20)
            for unused in range(rng.randint(1,16))
        ],
        [
            rng.randint(-20,20)
            for unused in range(rng.randint(1,16))
        ],
    ))

for mode in ("linear","negacyclic"):
    for a,b in fixtures:
        pipeline(a,b,mode)
    print(
        "RING:",mode,
        "PRODUCT_CASES:",len(fixtures),"PASS",
    )

normal_stats = dict(stats)

def expect_bad(label, action):
    try:
        action()
    except (AuditFailure,ValueError) as exc:
        print(label+"=REJECTED",str(exc))
        return
    raise AuditFailure(label+" survived")

expect_bad(
    "UNSUPPORTED_SCALAR_ROOT",
    lambda: compatible((17,97,193),32),
)
expect_bad(
    "MISSING_MONTGOMERY_DECODE",
    lambda: pipeline([1],[1],"linear","decode"),
)
expect_bad(
    "ORDINARY_PRODUCT_OF_MONTGOMERY_VALUES",
    lambda: pipeline(
        [1],[1],"linear","ordinary_multiply"
    ),
)
expect_bad(
    "MISSING_INVERSE_NORMALIZATION",
    lambda: pipeline(
        [1],[1],"linear","normalization"
    ),
)
expect_bad(
    "WRONG_TRANSFORM_ORDERING",
    lambda: pipeline(
        [2,-3,4],[-5,0,6],"linear","ordering"
    ),
)
expect_bad(
    "CYCLIC_NEGACYCLIC_SIGN_MUTANT",
    lambda: pipeline(
        [0]*15+[1],[0,1],"negacyclic","cyclic_sign"
    ),
)
expect_bad(
    "INSUFFICIENT_LINEAR_PADDING",
    lambda: pipeline([1]*17,[1]*17,"linear"),
)
expect_bad(
    "INSUFFICIENT_CRT_BOUND",
    lambda: pipeline(
        [1],[1],"linear",
        forced_C=prod(MODS)//2+1,
    ),
)

# Explicit unsigned-word-wrap models, not C signed-overflow models.
for q,bits in [(3329,32),(8380417,64)]:
    T = q*q-1
    shift = 2*q.bit_length()
    mu = (1 << shift)//q
    quotient = (
        (T*mu) & ((1 << bits)-1)
    ) >> shift
    out = T-quotient*q
    if out >= q:
        out -= q
    need(
        out % q == T % q,
        "Unsigned-wrap control congruence",
    )
    need(
        out != T % q and not 0 <= out < q,
        "Unsigned-wrap mutant survived",
    )

print("UNSIGNED_WORD_WRAP_MUTANTS=REJECTED_BY_CANONICAL_RANGE")
print("TOTAL_INTEGRATED_PRODUCTS:",2*len(fixtures))
print(
    "DIRECT_FORWARD_ORACLES:",
    normal_stats["forward_oracles"],
)
print(
    "NORMAL_PIPELINE_REDC_CALLS:",
    normal_stats["redc_calls"],
)
print(
    "NORMAL_PIPELINE_BARRETT_CALLS:",
    normal_stats["barrett_calls"],
)
print("MODULI:",MODS,"CRT_PRODUCT:",prod(MODS))
print("ROOTS_ORDER_32:",ROOT32)
print(
    "RADICES:",
    {q:1 << q.bit_length() for q in MODS},
)
print("RANDOM_SEED:",SEED)
print("ARITHMETIC=EXACT_PYTHON_INTEGERS")
print(
    "SCOPE=SELF_CONTAINED_REFERENCE_INTEGRATION_"
    "NOT_EXECUTION_OF_HISTORICAL_SCRIPTS"
)
print(
    "NO_MLKEM_QUADRATIC_INTEGRATION_FIXED_WIDTH_"
    "SAFETY_NIST_OR_TIMING_CLAIM"
)
print("WHOLE_PIPELINE_REFERENCE_INTEGRATION=PASS")
