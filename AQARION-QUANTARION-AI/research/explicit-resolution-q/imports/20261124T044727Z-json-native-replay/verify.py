import ast
import datetime
import functools
import hashlib
import itertools
import json
import math
import pathlib
import platform
import sys
import time

import sympy as s

START = time.time()
OUT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

EXPECTED = {
    "complex": (
        "AQARION-complete-complex-20261114T163933580791Z.json",
        "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0",
    ),
    "replay": (
        "AQARION-algebra-replay-20261114T164651806439Z.json",
        "5581387035a1f5448f514adacc04fc47c1357c3f0cbb48496fae2b901c64d07d",
    ),
    "structural": (
        "AQARION-semigroup-certificate-20261114T164416695765Z.json",
        "291b40ac0b15a131b733ba96ae98752f5054ebf0a387c960efca39fb46c07f5b",
    ),
    "witness": (
        "AQARION-D4-rank13-witness-20261114T165438532744Z.json",
        "4a25bf580162f71d27d2a7dcc58ed4d6caa7a7c1792a425864997a6653e8e5f7",
    ),
}

NAMES = [
    "A", "E0", "E1", "E2", "E3",
    "B0", "B1", "B2", "B3", "C",
]
XS = s.symbols(" ".join(NAMES))
ENV = dict(zip(NAMES, XS))
WEIGHTS = (1,1,1,1,1,2,2,2,2,2)

SHIFTS = [
    [0],
    [3]*8 + [4]*6,
    [4]*3 + [5]*24 + [6]*8,
    [6]*8 + [7]*24 + [8]*3,
    [8]*6 + [9]*8,
    [12],
]

PRIME = 1000003
RESULTS = {}

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def log(message):
    print(message, flush=True)

def save(name, data):
    (OUT/name).write_text(
        json.dumps(data, indent=2, default=str) + "\n"
    )

def safe_expr(text, env):
    def walk(node):
        if isinstance(node, ast.Constant) and type(node.value) is int:
            return s.Integer(node.value)

        if isinstance(node, ast.Name) and node.id in env:
            return env[node.id]

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, (ast.USub, ast.UAdd)):
                value = walk(node.operand)
                return -value if isinstance(node.op, ast.USub) else value

        if isinstance(node, ast.BinOp):
            a, b = walk(node.left), walk(node.right)

            if isinstance(node.op, ast.Add):
                return a+b
            if isinstance(node.op, ast.Sub):
                return a-b
            if isinstance(node.op, ast.Mult):
                return a*b
            if isinstance(node.op, ast.Div) and b.is_Integer and b != 0:
                return a/b
            if isinstance(node.op, ast.Pow) and b.is_Integer and 0 <= b <= 32:
                return a**b

        raise ValueError("Unsupported expression syntax")

    tree = ast.parse(str(text), mode="eval")
    return s.expand(walk(tree.body))

@functools.lru_cache(None)
def expression(text):
    return safe_expr(text, ENV)

def matrix(data, shape):
    need(
        isinstance(data, list) and len(data) == shape[0],
        "Matrix row count",
    )
    need(
        all(
            isinstance(row, list) and len(row) == shape[1]
            for row in data
        ),
        "Matrix column count",
    )
    return s.Matrix([
        [expression(str(value)) for value in row]
        for row in data
    ])

@functools.lru_cache(None)
def monoms(degree, index=0):
    if degree < 0:
        return ()
    if index == 10:
        return ((),) if degree == 0 else ()

    return tuple(
        (exponent,) + tail
        for exponent in range(degree//WEIGHTS[index] + 1)
        for tail in monoms(
            degree-exponent*WEIGHTS[index],
            index+1,
        )
    )

def component_certificate(M, source, target, degree):
    row_ids = {}
    number_rows = 0

    for i, shift in enumerate(target):
        for exponent in monoms(degree-shift):
            row_ids[i, exponent] = number_rows
            number_rows += 1

    entries = {
        j: [
            (
                i,
                s.Poly(M[i,j], *XS, domain=s.QQ).terms(),
            )
            for i in range(M.rows)
            if M[i,j]
        ]
        for j in range(M.cols)
    }

    pivots = {}
    chosen_rows = []
    chosen_columns = []
    number_columns = 0

    for j, shift in enumerate(source):
        for multiplier in monoms(degree-shift):
            column_id = number_columns
            number_columns += 1
            column = {}

            for i, terms in entries[j]:
                for exponent, coefficient in terms:
                    coefficient = s.Rational(coefficient)

                    need(
                        coefficient.q % PRIME != 0,
                        "Denominator vanishes modulo prime",
                    )

                    value = (
                        int(coefficient.p)
                        * pow(int(coefficient.q), -1, PRIME)
                    ) % PRIME

                    row = row_ids[
                        i,
                        tuple(
                            a+b
                            for a,b in zip(exponent, multiplier)
                        ),
                    ]
                    column[row] = (
                        column.get(row, 0) + value
                    ) % PRIME

            column = {
                key: value
                for key, value in column.items()
                if value
            }

            while column:
                row = min(column)
                value = column[row]

                if row not in pivots:
                    reciprocal = pow(value, -1, PRIME)
                    pivots[row] = {
                        key: entry*reciprocal % PRIME
                        for key, entry in column.items()
                    }
                    chosen_rows.append(row)
                    chosen_columns.append(column_id)
                    break

                for key, entry in pivots[row].items():
                    new = (
                        column.get(key, 0) - value*entry
                    ) % PRIME

                    if new:
                        column[key] = new
                    else:
                        column.pop(key, None)

    return {
        "degree": degree,
        "rank_lower_bound": len(pivots),
        "rows": number_rows,
        "columns": number_columns,
        "prime": PRIME,
        "minor_row_indices": chosen_rows,
        "minor_column_indices": chosen_columns,
        "basis_order": (
            "module basis order; then weighted exponent tuples "
            "in recursive increasing-exponent order"
        ),
    }

def main():
    log("PROJECT 2 — JSON-NATIVE EXACT AUDIT")
    log("Read-only original inputs.")
    log("No Macaulay2, Lean, Git, or original audit scripts executed.")

    inputs = {}
    hashes = {}
    (OUT/"inputs").mkdir(exist_ok=False)

    for key, (name, expected) in EXPECTED.items():
        path = HOME/name
        data = path.read_bytes()
        actual = hashlib.sha256(data).hexdigest()

        need(
            actual == expected,
            "Frozen input hash mismatch: " + name,
        )

        (OUT/"inputs"/name).write_bytes(data)
        inputs[key] = json.loads(data)
        hashes[key] = {
            "path": str(path),
            "bytes": len(data),
            "sha256": actual,
        }

    log("[1] Four frozen input hashes: PASS")

    export = inputs["complex"]
    replay = inputs["replay"]
    structural = inputs["structural"]
    witness = inputs["witness"]

    need(
        replay["complex_sha256"]
        == structural["export_sha256"]
        == witness["complex_sha256"]
        == hashes["complex"]["sha256"],
        "Complex hash links",
    )
    need(
        replay["structural_certificate_sha256"]
        == hashes["structural"]["sha256"],
        "Structural hash link",
    )

    need(
        export["field"] == "QQ" and replay["field"] == "QQ",
        "Coefficient field",
    )
    need(
        export["variables"] == NAMES
        and tuple(export["weights"]) == WEIGHTS,
        "Variables and grading",
    )
    need(
        export["module_scalar_shifts"] == SHIFTS,
        "Scalar module shifts",
    )
    need(
        export["matrix_convention"]
        == "rows=target basis; columns=source basis",
        "Matrix orientation",
    )

    shapes = [
        (1,14), (14,35), (35,35), (35,14), (14,1)
    ]
    matrices = [
        matrix(export["matrices"]["D"+str(i+1)], shape)
        for i, shape in enumerate(shapes)
    ]

    RESULTS["inputs"] = hashes
    log("[2] JSON matrices parsed without original helpers: PASS")

    for i in range(4):
        need(
            all(
                s.expand(value) == 0
                for value in matrices[i]*matrices[i+1]
            ),
            "Nonzero differential composition",
        )

    log("[3] All four polynomial compositions: PASS")

    V = s.Matrix.hstack(
        s.Matrix([0,0,0,0,-1]),
        *[
            s.Matrix([int(i == j) for i in range(4)] + [0])
            for j in range(4)
        ],
        *[
            s.Matrix([int(i != j) for i in range(4)] + [1])
            for j in range(4)
        ],
        s.Matrix([1,1,1,1,2]),
    )

    need(
        export["variable_semigroup_degrees"]
        == [list(V[:,i]) for i in range(10)],
        "Semigroup degrees",
    )
    need(
        structural["generators"]
        == export["variable_semigroup_degrees"],
        "Structural generators",
    )
    need(V[:,:5].det() == -1, "Unimodular lattice basis")

    multishifts = export["module_semigroup_shifts"]
    need(len(multishifts) == 6, "Semigroup module count")

    for i, shifts in enumerate(multishifts):
        need(
            len(shifts) == len(SHIFTS[i]),
            "Semigroup basis size",
        )
        for shift, degree in zip(shifts, SHIFTS[i]):
            need(
                len(shift) == 5
                and sum(shift[:4])-shift[4] == degree,
                "Scalar/multigrading compatibility",
            )

    for i, M in enumerate(matrices):
        for row in range(M.rows):
            for col in range(M.cols):
                if not M[row,col]:
                    continue

                poly = s.Poly(M[row,col], *XS, domain=s.QQ)

                need(
                    poly.coeff_monomial((0,)*10) == 0,
                    "Nonzero constant differential entry",
                )

                target = (
                    s.Matrix(multishifts[i+1][col])
                    - s.Matrix(multishifts[i][row])
                )

                for exponent in poly.monoms():
                    need(
                        sum(
                            a*b
                            for a,b in zip(exponent, WEIGHTS)
                        )
                        == SHIFTS[i+1][col]-SHIFTS[i][row],
                        "Weighted homogeneity",
                    )
                    need(
                        V*s.Matrix(exponent) == target,
                        "Semigroup homogeneity",
                    )

    log("[4] Scalar/multigrading and zero constants: PASS")

    A = XS[0]
    E = list(XS[1:5])
    B = list(XS[5:9])
    C = XS[9]

    canonical = [
        E[i]*B[i]-A*C
        for i in range(4)
    ]
    canonical += [
        A*B[i]-s.prod(
            E[j] for j in range(4) if j != i
        )
        for i in range(4)
    ]
    canonical += [
        B[i]*B[j]-C*s.prod(
            E[k] for k in range(4) if k not in (i,j)
        )
        for i,j in itertools.combinations(range(4), 2)
    ]

    generators = list(matrices[0])
    G = s.groebner(
        generators, *XS, order="lex", domain=s.QQ
    )
    Gc = s.groebner(
        canonical, *XS, order="lex", domain=s.QQ
    )

    need(
        all(G.reduce(f)[1] == 0 for f in canonical),
        "Canonical relations contained in endpoint",
    )
    need(
        all(Gc.reduce(f)[1] == 0 for f in generators),
        "Endpoint contained in canonical presentation",
    )

    Z = s.Symbol("_saturation_auxiliary_")
    Gsat = s.groebner(
        generators + [Z*A-1],
        Z, *XS,
        order="lex",
        domain=s.QQ,
    )

    elimination = [
        poly.as_expr()
        for poly in Gsat.polys
        if not poly.as_expr().has(Z)
    ]

    need(
        all(G.reduce(f)[1] == 0 for f in elimination),
        "A-saturation",
    )

    localized = {
        B[i]: s.prod(
            E[j] for j in range(4) if j != i
        ) / A
        for i in range(4)
    }
    localized[C] = s.prod(E)/A**2

    need(
        all(
            s.cancel(f.xreplace(localized)) == 0
            for f in generators
        ),
        "Localized graph equations",
    )

    RESULTS["endpoint"] = {
        "canonical_presentation_matches": True,
        "A_saturated": True,
        "localized_graph_substitution": True,
        "groebner_basis_size": len(G.polys),
        "field": "QQ",
        "semigroup_model": (
            "a_i>=0, a_i+a_j-k>=0; "
            "extended symbolic Rees of the K4 cover ideal"
        ),
    }

    log("[5] Endpoint presentation, saturation and localization: PASS")

    facets = [
        list(s.eye(5).row(i))
        for i in range(4)
    ]

    pairs = list(itertools.combinations(range(4), 2))

    for i,j in pairs:
        facets.append(
            [int(k in (i,j)) for k in range(4)] + [-1]
        )

    F = s.Matrix(facets)
    kappa = s.Matrix([1,1,1,1,1])

    need(
        all(value >= 0 for value in F*V),
        "Generator cone inequalities",
    )
    need(
        F*kappa == s.ones(10,1),
        "Canonical translate facet values",
    )
    need(
        all(
            math.gcd(*map(abs, map(int, row))) == 1
            for row in facets
        ),
        "Primitive facets",
    )

    for i in range(10):
        if i < 4:
            point = [
                0 if j == i else 2
                for j in range(4)
            ] + [1]
        else:
            pair = pairs[i-4]
            point = [
                1 if j in pair else 2
                for j in range(4)
            ] + [2]

        values = F*s.Matrix(point)

        need(
            values[i] == 0
            and all(
                values[j] > 0
                for j in range(10)
                if j != i
            ),
            "Facet irredundancy witness",
        )

    need(
        sum(WEIGHTS)-3 == 12,
        "Canonical/final scalar shifts",
    )

    log("[6] Lattice/facet/translate certificates: PASS")

    t = s.Symbol("t")
    lattice = {(0,)*10: 1}

    for poly in G.polys:
        leading = poly.monoms()[0]
        changes = {}

        for monomial, coefficient in lattice.items():
            new = tuple(
                max(a,b)
                for a,b in zip(monomial, leading)
            )
            changes[new] = changes.get(new, 0)-coefficient

        for monomial, coefficient in changes.items():
            lattice[monomial] = (
                lattice.get(monomial, 0)+coefficient
            )
            if not lattice[monomial]:
                del lattice[monomial]

    N = s.expand(sum(
        coefficient*t**sum(
            a*b for a,b in zip(monomial, WEIGHTS)
        )
        for monomial, coefficient in lattice.items()
    ))

    expected_N = (
        1-8*t**3-3*t**4+24*t**5-24*t**7
        +3*t**8+8*t**9-t**12
    )

    need(
        s.expand(N-expected_N) == 0,
        "Independent Hilbert numerator",
    )
    need(
        s.expand(
            N-safe_expr(export["hilbert_numerator"], {"t":t})
        ) == 0,
        "Export numerator",
    )
    need(
        s.expand(
            N-safe_expr(replay["hilbert_numerator"], {"t":t})
        ) == 0,
        "Replay numerator",
    )
    need(
        s.expand(
            N-sum(
                (-1)**i*sum(t**degree for degree in shifts)
                for i, shifts in enumerate(SHIFTS)
            )
        ) == 0,
        "Complex Euler numerator",
    )

    RESULTS["hilbert"] = {
        "numerator": str(N),
        "factorization": str(s.factor(N)),
        "reduced_series": (
            "(1+2*t+6*t**2+2*t**3+t**4)"
            "/((1-t)**3*(1-t**2)**2)"
        ),
    }

    log("[7] Independent Groebner Hilbert numerator: PASS")

    def pdim(degree):
        return len(monoms(degree))

    def rdim(degree):
        return sum(
            int(s.Poly(N,t).nth(j))*pdim(degree-j)
            for j in range(13)
        )

    def fdim(index, degree):
        return sum(
            pdim(degree-shift)
            for shift in SHIFTS[index]
        )

    def k1(degree):
        return (
            fdim(1,degree)-pdim(degree)+rdim(degree)
        )

    def k2(degree):
        return fdim(2,degree)-k1(degree)

    def k3(degree):
        return fdim(3,degree)-k2(degree)

    minor = s.factor(
        matrices[1].extract(
            [2,3,4], [0,1,2]
        ).det()
    )
    need(
        minor == A**2*E[3],
        "Free degree-four syzygy minor",
    )

    components = []

    for index, degrees, target_dimension in [
        (2, [4,5,6], k1),
        (3, [6,7,8,9], k2),
        (4, [8,9], k3),
    ]:
        for degree in degrees:
            certificate = component_certificate(
                matrices[index-1],
                SHIFTS[index],
                SHIFTS[index-1],
                degree,
            )

            upper = target_dimension(degree)

            need(
                certificate["rank_lower_bound"] == upper,
                "Component rank/Hilbert bound mismatch",
            )

            certificate.update(
                map="D"+str(index),
                rational_upper_bound=upper,
                upper_bound_dependency=(
                    "Inductive kernel generation and structural "
                    "Gorenstein degree bounds; see proof notes"
                ),
            )
            components.append(certificate)

            log(
                "    D%d degree %d: rank >= %d mod %d; "
                "matching QQ upper bound %d"
                % (index, degree, upper, PRIME, upper)
            )

    RESULTS["components"] = components

    log(
        "[8] All nine component certificates: PASS "
        "(QQ conclusions use stated induction)"
    )

    point = {
        ENV[key]: s.Integer(value)
        for key, value in witness["point"].items()
    }

    rank4 = matrices[3].subs(point).rank()
    need(rank4 == 13, "Rank-13 specialization")

    d5 = matrices[4]

    need(
        d5.subs(point) == matrix(
            [[value] for value in witness["D5_value"]],
            (14,1),
        ),
        "Saved D5 values",
    )
    need(
        matrices[3].subs(point) == matrix(
            witness["D4_value"], (35,14)
        ),
        "Saved D4 values",
    )
    need(
        s.gcd_list(list(d5)) in (1,-1),
        "Primitive final column",
    )
    need(
        any(value != 0 for value in d5),
        "Nonzero final map",
    )

    RESULTS["tail"] = {
        "specialized_rank_D4": rank4,
        "D5_gcd": str(s.gcd_list(list(d5))),
        "D4_D5_zero": True,
        "conclusion": (
            "Kernel D4 equals P*D5 by fraction-field rank one "
            "and primitive-vector argument over the polynomial UFD"
        ),
    }

    log("[9] Saved specialization and primitive final column: PASS")

    charpath = HOME/"homology_check_charZ.m2"

    RESULTS["characteristic_source"] = {
        "path": str(charpath),
        "exists": charpath.is_file(),
        "bytes": (
            charpath.stat().st_size
            if charpath.is_file() else None
        ),
        "executed": False,
    }

    proof = """This is an arithmetic certificate with explicit
standard-theorem dependencies, not Lean verification.

1. Saturation plus the localized graph presentation identifies the
endpoint ideal with the semigroup kernel.

2. Semigroup equals cone lattice points:
k<=0 uses A,E.
k=1 subtracts a suitable B.
k>=2 subtracts C if all a_i>=1, otherwise B_i at a zero coordinate.
The step decreases k and preserves inequalities.
This is the mathematical induction, not a bounded enumeration.

3. The unimodular basis gives the full lattice.
The ten primitive facets have value one at kappa=(1,1,1,1,1).
Interior lattice points equal kappa+S.
Standard normal-semigroup Cohen-Macaulay and canonical-module theorems
give a codimension-five Gorenstein endpoint and final scalar shift 12.

4. Apply self-duality to an ABSTRACT minimal resolution, not to the
displayed complex.
K1 degree four has dimension three and is spanned by D2's first three
columns. Their nonzero minor A^2*E3 shows no polynomial relation among
them. No minimal third generator occurs below degree six.
Self-duality bounds minimal second generators above by degree six.
Component checks 4,5,6 prove full D2 generation.

5. D2 has no kernel in degrees four or five.
Its degree-six kernel has dimension eight, spanned by the eight
degree-six D3 columns. Zero constants ensure no redundant degree-six
D2 generator.
Thus D2 is minimal, with shifts 4^3,5^24,6^8.
Duality gives third shifts 6^8,7^24,8^3 and fourth shifts 8^6,9^8.
Corresponding component checks prove full D3 and D4 generation.
Degree nine for D3 is supplementary.

6. D4 has generic rank thirteen:
specialization gives a lower bound; nonzero D5 and composition zero
give an upper bound.
Its fraction-field kernel is generated by D5.
Gcd one implies every polynomial kernel vector has polynomial
multiplier. Nonzero D5 is injective.

7. Zero constant terms make the resulting graded resolution minimal.

Modular component calculations are NONZERO MINOR LOWER BOUNDS over QQ.
Matching upper bounds use the preceding induction.
They do not prove exactness over all finite fields.

No original-constructor recovery, Lean proof, Macaulay2 execution,
characteristic independence, or novelty is claimed.

Historical basis_bridge_T is not checked: it is not needed to verify
the standalone exported complex.
"""

    (OUT/"PROOF_DEPENDENCIES.txt").write_text(proof)

    receipt = {
        "status":
            "PASS_ARITHMETIC_WITH_EXPLICIT_THEOREM_DEPENDENCIES",
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "sympy": s.__version__,
        "platform": platform.platform(),
        "source_sha256": hashlib.sha256(
            pathlib.Path(__file__).read_bytes()
        ).hexdigest(),
        "elapsed_seconds": time.time()-START,
        "results": RESULTS,
        "scope": {
            "export": "Frozen ten-variable complex over QQ only",
            "minimal_resolution_conclusion": (
                "Requires standard theorems and induction recorded "
                "in PROOF_DEPENDENCIES.txt"
            ),
            "Lean": False,
            "Macaulay2_executed": False,
            "characteristic_independence": False,
            "original_constructor_recovered": False,
            "novelty_established": False,
            "basis_bridge_checked": False,
        },
    }

    save("RECEIPT.json", receipt)

    checks = []
    for path in sorted(OUT.rglob("*")):
        if (
            path.is_file()
            and path.name not in ("console.log", "SHA256SUMS")
        ):
            checks.append(
                hashlib.sha256(path.read_bytes()).hexdigest()
                + "  "
                + path.relative_to(OUT).as_posix()
            )

    (OUT/"SHA256SUMS").write_text(
        "\n".join(checks) + "\n"
    )

    log(
        "\nSTATUS="
        "PASS_ARITHMETIC_WITH_EXPLICIT_THEOREM_DEPENDENCIES"
    )
    log("FIELD=QQ")
    log("BETTI_TOTALS=1,14,35,35,14,1")
    log("CHARACTERISTIC_INDEPENDENCE=NOT_CLAIMED")
    log("MACAULAY2_HOMOLOGY_EXECUTION=NOT_PERFORMED")
    log(
        "CHARZ_SOURCE_BYTES="
        + str(RESULTS["characteristic_source"]["bytes"])
    )
    log("RESULTS="+str(OUT))

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        for name in ("RECEIPT.json", "SHA256SUMS"):
            path = OUT/name
            if path.exists():
                path.unlink()

        save(
            "FAILURE.json",
            {
                "status": "FAIL",
                "error_type": type(error).__name__,
                "message": str(error),
                "completed_results": RESULTS,
            },
        )
        raise
