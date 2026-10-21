from random import Random


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


class Montgomery:
    def __init__(self, q, R):
        if q <= 1 or q % 2 == 0:
            raise ValueError("q must be odd and greater than one")
        if R <= q or R & (R - 1):
            raise ValueError(
                "R must be a power of two greater than q"
            )

        self.q = q
        self.R = R
        self.mask = R - 1
        self.shift = R.bit_length() - 1
        self.qprime = (-pow(q, -1, R)) & self.mask
        self.R2 = R * R % q

    def redc(self, T):
        q, R = self.q, self.R

        if not 0 <= T < q * R:
            raise ValueError("REDC requires 0 <= T < q*R")

        m = (T * self.qprime) & self.mask
        numerator = T + m * q

        require(
            numerator & self.mask == 0,
            "Divisibility failed",
        )

        u = numerator >> self.shift

        require(
            0 <= u < 2 * q,
            "Intermediate range failed",
        )

        result = u - q if u >= q else u

        require(
            0 <= result < q,
            "Canonical output failed",
        )

        return result

    def encode(self, a):
        return self.redc((a % self.q) * self.R2)

    def decode(self, encoded):
        self.canonical(encoded)
        return self.redc(encoded)

    def multiply(self, encoded_a, encoded_b):
        self.canonical(encoded_a)
        self.canonical(encoded_b)
        return self.redc(encoded_a * encoded_b)

    def canonical(self, value):
        if not 0 <= value < self.q:
            raise ValueError(
                "Encoded operand must be in [0,q)"
            )


def rejects(function):
    try:
        function()
    except ValueError:
        return True
    return False


rng = Random(20261021)

configs = [
    (17, 32),
    (3329, 65536),
    (8380417, 4294967296),
]

total_redc = 0
total_products = 0
total_conversions = 0

for q, R in configs:
    M = Montgomery(q, R)
    inverse_R = pow(R, -1, q)

    require(
        (q * M.qprime + 1) % R == 0,
        "qprime identity failed",
    )

    if q == 17:
        redc_inputs = set(range(q * R))
    else:
        redc_inputs = {
            0, 1, q-1, q, q+1,
            R-1, R, R+1,
            (q-1)**2,
            q*R-q, q*R-2, q*R-1,
        }
        redc_inputs.update(
            rng.randrange(q * R)
            for unused in range(2000)
        )

    for T in sorted(redc_inputs):
        require(
            M.redc(T) == T * inverse_R % q,
            "REDC oracle mismatch",
        )

    total_redc += len(redc_inputs)

    if q == 17:
        conversion_inputs = list(range(-2*q, 2*q+1))
    else:
        conversion_inputs = [
            -q*q-1, -q-1, -q, -1,
            0, 1, q-1, q, q+1, q*q+1,
        ]

    for a in conversion_inputs:
        encoded = M.encode(a)

        require(
            encoded == a*R % q,
            "Encode oracle mismatch",
        )
        require(
            M.decode(encoded) == a % q,
            "Conversion round trip failed",
        )

    total_conversions += len(conversion_inputs)

    if q == 17:
        pairs = [
            (a, b)
            for a in range(q)
            for b in range(q)
        ]
    else:
        edges = [0, 1, 2, q//2, q-2, q-1]

        pairs = [
            (a, b)
            for a in edges
            for b in edges
        ]

        pairs += [
            (rng.randrange(q), rng.randrange(q))
            for unused in range(1000)
        ]

    for a, b in pairs:
        encoded_product = M.multiply(
            M.encode(a),
            M.encode(b),
        )

        require(
            encoded_product == a*b*R % q,
            "Encoded product mismatch",
        )
        require(
            M.decode(encoded_product) == a*b % q,
            "Product oracle mismatch",
        )

    total_products += len(pairs)

    require(
        rejects(lambda: M.redc(-1)),
        "Negative REDC input accepted",
    )
    require(
        rejects(lambda: M.redc(q*R)),
        "Upper REDC bound accepted",
    )
    require(
        rejects(lambda: M.decode(-1)),
        "Negative encoded input accepted",
    )
    require(
        rejects(lambda: M.decode(q)),
        "Noncanonical encoded input accepted",
    )
    require(
        rejects(lambda: M.multiply(q, 0)),
        "Noncanonical product input accepted",
    )

    print(
        "CASE q=%d R=%d REDC=%d CONVERSIONS=%d PRODUCTS=%d PASS"
        % (
            q, R,
            len(redc_inputs),
            len(conversion_inputs),
            len(pairs),
        )
    )


for q, R in [
    (0, 32),
    (16, 32),
    (17, 16),
    (17, 31),
]:
    require(
        rejects(lambda q=q, R=R: Montgomery(q, R)),
        "Invalid configuration accepted",
    )


M = Montgomery(17, 32)
a, b = 7, 9
aR, bR = M.encode(a), M.encode(b)
productR = M.multiply(aR, bR)

require(
    (aR, bR, productR, M.decode(productR))
    == (3, 16, 10, 12),
    "Witness failed",
)

T = M.q
m = (T * M.qprime) & M.mask
uncorrected = (T + m * M.q) >> M.shift

require(
    uncorrected == M.q and M.redc(T) == 0,
    "Final subtraction mutant survived",
)

require(
    M.redc(a*b) != a*b % M.q,
    "Mixed representation mutant survived",
)

wrong_m = pow(M.q, -1, M.R) & M.mask

require(
    (1 + wrong_m * M.q) % M.R != 0,
    "Inverse sign mutant survived",
)

require(
    M.redc(1) != 1,
    "Missing Montgomery conversion mutant survived",
)

weak = Montgomery(17, 256)

require(
    all(weak.encode(a) == a for a in range(17)),
    "Weak-radix control failed",
)

print("WITNESS_ENCODED_A_B_PRODUCT_DECODED: 3 16 10 12")
print("BARRETT_AND_CRT=NOT_INCLUDED")
print("REDC_ORACLE=PASS")
print("SIGNED_INPUT_ENCODING=PASS")
print("MONTGOMERY_ENCODE_MULTIPLY_DECODE=PASS")
print("INPUT_RANGE_REJECTION=PASS")
print("MISSING_FINAL_SUBTRACTION_MUTANT=REJECTED")
print("MIXED_REPRESENTATION_MUTANT=REJECTED")
print("WRONG_INVERSE_SIGN_MUTANT=REJECTED")
print("MISSING_CONVERSION_MUTANT=REJECTED")
print("RADIX_CONGRUENT_ONE_WEAK_CONTROL=DETECTED")
print("TOTAL_REDC_CASES:", total_redc)
print("TOTAL_CONVERSION_CASES:", total_conversions)
print("TOTAL_PRODUCT_CASES:", total_products)
print("RANDOM_SEED=20261021")
print("ARITHMETIC=EXACT_PYTHON_INTEGERS")
print(
    "SCOPE=GENERIC_REDUCTION_NOT_NIST_CONFORMANCE_"
    "CONSTANT_TIME_OR_TIMING"
)
print("MONTGOMERY_REDUCTION_AUDIT=PASS")
