#!/usr/bin/env python3
"""AQARION finite Kaprekar audit. Standard library only."""

import argparse
import collections
import csv
import datetime
import hashlib
import itertools
import json
import math
import pathlib
import platform
import shutil
import sys
import time
from fractions import Fraction as Q

PAPER = "https://arxiv.org/abs/2608.22564v1"
START = time.time()
RESULTS = {}


def log(message):
    print(message, flush=True)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def encode(value):
    if isinstance(value, Q):
        return str(value)
    if isinstance(value, pathlib.Path):
        return str(value)
    raise TypeError(type(value).__name__)


def save(name, data):
    (OUT / name).write_text(
        json.dumps(data, indent=2, default=encode) + "\n"
    )


def csvsave(name, header, rows):
    with (OUT / name).open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def K(word):
    descending = int("".join(sorted(word, reverse=True)))
    ascending = int("".join(sorted(word)))
    return str(descending - ascending).zfill(len(word))


def H(word):
    digits = sorted(map(int, word), reverse=True)
    return (
        digits[0] - digits[-1],
        digits[1] - digits[2],
    )


def mat(A, B):
    columns = list(zip(*B))
    return [
        [
            sum(
                a * b
                for a, b in zip(row, column)
                if a and b
            )
            for column in columns
        ]
        for row in A
    ]


def eye(n):
    return [
        [int(i == j) for j in range(n)]
        for i in range(n)
    ]


def mpow(A, exponent):
    result = eye(len(A))
    while exponent:
        if exponent & 1:
            result = mat(result, A)
        exponent //= 2
        if exponent:
            A = mat(A, A)
    return result


def rref(A, nvars=None):
    A = [[Q(x) for x in row] for row in A]
    if not A:
        return A, []

    limit = len(A[0]) if nvars is None else nvars
    pivots = []
    i = 0

    for j in range(limit):
        k = next(
            (k for k in range(i, len(A)) if A[k][j]),
            None,
        )
        if k is None:
            continue

        A[i], A[k] = A[k], A[i]
        divisor = A[i][j]
        A[i] = [x / divisor for x in A[i]]

        for k in range(len(A)):
            if k != i and A[k][j]:
                coefficient = A[k][j]
                A[k] = [
                    a - coefficient * b
                    for a, b in zip(A[k], A[i])
                ]

        pivots.append(j)
        i += 1
        if i == len(A):
            break

    return A, pivots


def inverse(A):
    n = len(A)
    augmented = [
        list(row) + unit
        for row, unit in zip(A, eye(n))
    ]
    reduced, pivots = rref(augmented, n)
    require(len(pivots) == n, "Singular exact witness minor")
    return [row[n:] for row in reduced]


def rank(A):
    return len(rref(A)[1])


def determinant(A):
    A = [[Q(x) for x in row] for row in A]
    result = Q(1)
    n = len(A)

    for j in range(n):
        k = next(
            (k for k in range(j, n) if A[k][j]),
            None,
        )
        if k is None:
            return Q(0)

        if k != j:
            A[k], A[j] = A[j], A[k]
            result = -result

        pivot = A[j][j]
        result *= pivot

        for k in range(j + 1, n):
            if A[k][j]:
                coefficient = A[k][j] / pivot
                for t in range(j + 1, n):
                    A[k][t] -= coefficient * A[j][t]
                A[k][j] = 0

    return result


def pivot_columns(B, prime=1000003):
    """Modular discovery only; the chosen minor is checked over Q."""
    A = [[value % prime for value in row] for row in B]
    i = 0
    columns = []

    for j in range(len(A[0])):
        k = next(
            (k for k in range(i, len(A)) if A[k][j]),
            None,
        )
        if k is None:
            continue

        A[i], A[k] = A[k], A[i]
        reciprocal = pow(A[i][j], -1, prime)
        A[i] = [
            (value * reciprocal) % prime
            for value in A[i]
        ]

        for k in range(i + 1, len(A)):
            if A[k][j]:
                coefficient = A[k][j]
                A[k] = [
                    (a - coefficient * b) % prime
                    for a, b in zip(A[k], A[i])
                ]

        columns.append(j)
        i += 1

        if i == len(B):
            return columns

    raise AssertionError(
        "Modular pivot discovery failed; no certificate issued"
    )


def integer_row(row):
    denominator = math.lcm(
        *(Q(value).denominator for value in row)
    )
    terms = [
        (i, int(Q(value) * denominator))
        for i, value in enumerate(row)
        if value
    ]
    return denominator, terms


def check_function(row, B, target, message):
    denominator, terms = integer_row(row)

    for x, value in enumerate(target):
        lhs = sum(
            coefficient * B[k][x]
            for k, coefficient in terms
        )
        value = Q(value)
        require(
            lhs * value.denominator
            == denominator * value.numerator,
            message + " at state " + str(x),
        )


# ============================================================
# 1. PARAMETERIZED TWO-CYCLES AND OBSERVATIONAL COUNTEREXAMPLES
# ============================================================

def family_word(z, u, v):
    require(
        z > u + v > 0 and min(u, v) >= 0,
        "Invalid family parameters",
    )

    counts = {
        9: z,
        8: z - u - v,
        7: z + v,
        6: z - v,
        5: z,
        4: z,
        3: z - v,
        2: z + v,
        1: z - u - v,
    }

    return "".join(
        str(digit) * counts[digit]
        for digit in range(9, 0, -1)
    )


def family_cycle(z, u, v):
    require(u != v, "Fixed-point diagonal is not a two-cycle")

    a = family_word(z, u, v)
    b = family_word(z, v, u)
    c = K(b)
    d = K(a)

    require(
        "".join(sorted(c, reverse=True)) == a,
        "Family sorted C",
    )
    require(
        "".join(sorted(d, reverse=True)) == b,
        "Family sorted D",
    )
    require(
        c != d and K(c) == d and K(d) == c,
        "Family exact period two",
    )
    require(
        len(c) == 9 * z - 2 * (u + v),
        "Family digit length",
    )

    expected_h = (8, 1) if z == 2 else (8, 0)
    require(
        H(c) == H(d) == expected_h,
        "Dahl observation on family",
    )
    require(
        sum(map(int, c))
        == sum(map(int, d))
        == 9 * (5 * z - u - v),
        "Family digit sum",
    )

    return c, d


def audit_families(limit):
    log("\n[1/6] Parameterized families and observation counterexamples")

    rows = []
    count = 0

    for z in range(2, limit + 1):
        for u in range(z):
            for v in range(u):
                if 0 < u + v < z:
                    c, d = family_cycle(z, u, v)
                    count += 1
                    rows.append([
                        z, u, v, len(c), c, d,
                        *H(c), *H(d),
                    ])

    csvsave(
        "family3_cases.csv",
        [
            "z", "u", "v", "digits", "C", "D",
            "h1_C", "h2_C", "h1_D", "h2_D",
        ],
        rows,
    )

    # Family 2, using descending digit representatives.
    for x in range(2, 51):
        a = (
            "99"
            + "6" * (x + 1)
            + "55"
            + "44"
            + "3" * x
            + "21"
        )
        b = (
            "9"
            + "88"
            + "77"
            + "6" * x
            + "3" * x
            + "222"
            + "0"
        )
        c, d = K(b), K(a)

        require(
            "".join(sorted(c, reverse=True)) == a
            and "".join(sorted(d, reverse=True)) == b,
            "Family 2 sorted words",
        )
        require(
            c != d and K(c) == d and K(d) == c,
            "Family 2 exact period two",
        )

    first = family_cycle(4, 3, 0)
    second = family_cycle(4, 2, 1)

    require(
        set(first).isdisjoint(second),
        "30-digit cycles must be disjoint",
    )

    qvalues = []
    examples = []

    for orbit_index, orbit in enumerate((first, second)):
        for state in orbit:
            q = state.count("7")
            qvalues.append(q)

            require(H(state) == (8, 0), "Constant Dahl observation")
            require(
                K(state).count("7") == 11 - q,
                "Count-of-seven update",
            )
            require(
                Q((q - 5) * (q - 6), 2) == 1 - orbit_index,
                "Quadratic indicator on four-state subsystem",
            )

            examples.append([
                orbit_index,
                state,
                K(state),
                q,
                *H(state),
                str(Q((q - 5) * (q - 6), 2)),
            ])

    feature_matrix = [
        [q ** power for q in qvalues]
        for power in range(4)
    ]
    feature_ranks = [
        rank(feature_matrix[:r])
        for r in range(1, 5)
    ]
    require(
        feature_ranks == [1, 2, 3, 4],
        "Four-state feature ranks",
    )

    update = [
        [1, 0, 0],
        [11, -1, 0],
        [121, -22, 1],
    ]
    require(
        mat(update, update) == eye(3),
        "Quadratic feature update involution",
    )

    projector = [
        [
            Q(int(i == j) + update[i][j], 2)
            for j in range(3)
        ]
        for i in range(3)
    ]
    require(
        rank(projector) == 2
        and mat(projector, projector) == projector,
        "Restricted four-state projector",
    )

    csvsave(
        "30_digit_counterexample.csv",
        [
            "orbit", "state", "next", "count7",
            "h1", "h2", "chi_first_on_four_states",
        ],
        examples,
    )

    # Exact all-parameter affine coefficient identity.
    # A tuple means coefficients of [z,u,v,constant].
    def plus(a, b):
        return tuple(x + y for x, y in zip(a, b))

    zero = (0, 0, 0, 0)
    t = (1, -1, -1, 0)

    differences = {
        8: t,
        7: (0, 1, 1, 0),
        6: t,
        5: (0, 0, 1, 0),
        4: (1, 0, -1, 0),
        3: (0, 0, 1, 0),
        2: (1, 0, -1, 0),
    }

    output = {digit: zero for digit in range(10)}

    for delta, multiplicity in differences.items():
        output[delta] = plus(output[delta], multiplicity)
        output[9 - delta] = plus(
            output[9 - delta], multiplicity
        )

    # Outer delta=8 changes 1->2.
    # Inner delta=2 changes 2->1.
    # The corrections cancel in the total digit counts.
    output[9] = plus(output[9], (1, 0, 0, 0))

    expected = {
        0: zero,
        1: t,
        2: (1, 1, 0, 0),
        3: (1, -1, 0, 0),
        4: (1, 0, 0, 0),
        5: (1, 0, 0, 0),
        6: (1, -1, 0, 0),
        7: (1, 1, 0, 0),
        8: t,
        9: (1, 0, 0, 0),
    }
    require(
        output == expected,
        "All-parameter coefficient identity",
    )

    RESULTS["families"] = {
        "family3_cases": count,
        "family2_cases": 49,
        "max_z": limit,
        "all_parameter_coefficient_identity": True,
        "four_state_feature_ranks": feature_ranks,
        "restricted_update_matrix": update,
        "restricted_projector": projector,
        "first_30_digit_cycle": first,
        "second_30_digit_cycle": second,
        "scope": (
            "Family membership and restricted subsystem; "
            "not Section 6 classification necessity"
        ),
    }

    log("  PASS: Family 3 cases = " + str(count))
    log("  PASS: Family 2 cases = 49")
    log("  PASS: all-parameter coefficient identity")
    log("  PASS: two distinct 30-digit cycles have identical full traces")
    log("  PASS: feature ranks = [1, 2, 3, 4]")


# ============================================================
# 2. EXHAUSTIVE SORTED-PATTERN TWO-CYCLE CENSUS
# ============================================================

def audit_census(max_digits):
    log("\n[2/6] Exhaustive exact-period-two census")

    rows = []
    total = 0

    for n in range(2, max_digits + 1):
        weights = [
            10 ** i - 10 ** (n - 1 - i)
            for i in range(n)
        ]
        found = set()
        tested = 0

        for digits in itertools.combinations_with_replacement(
            range(10), n
        ):
            if digits[0] == digits[-1]:
                continue

            tested += 1

            d = sum(
                digit * weight
                for digit, weight in zip(digits, weights)
            )
            sorted_d = tuple(
                sorted(map(int, str(d).zfill(n)))
            )
            c = sum(
                digit * weight
                for digit, weight in zip(sorted_d, weights)
            )

            # Exclude fixed points explicitly.
            if c == d:
                continue

            if (
                tuple(sorted(map(int, str(c).zfill(n))))
                == digits
            ):
                found.add(tuple(sorted((
                    str(c).zfill(n),
                    str(d).zfill(n),
                ))))

        require(
            tested == math.comb(n + 9, 9) - 10,
            "Census state cardinality",
        )

        for c, d in found:
            require(
                K(c) == d and K(d) == c and c != d,
                "Census genuine two-cycle",
            )
            require(
                "9" in c and "9" in d,
                "Contains-nine bounded check",
            )

            a = sorted(map(int, c), reverse=True)
            b = sorted(map(int, d), reverse=True)

            ell_a = sum(
                a[i] > a[-1 - i]
                for i in range(n // 2)
            )
            ell_b = sum(
                b[i] > b[-1 - i]
                for i in range(n // 2)
            )

            exceptional = {c, d} == {"53955", "59994"}

            require(
                sum(a) == sum(b) or exceptional,
                "Equal-digit-sum bounded check",
            )
            require(
                ell_a == ell_b or exceptional,
                "Equal-ell bounded check",
            )

        expected = set()
        if n == 5:
            expected = {("53955", "59994")}
        if n == 13:
            expected = {
                ("8733209876622", "9665429654331")
            }

        require(
            found == expected,
            "Previously reported census differs at n=" + str(n),
        )

        total += tested
        rows.append([
            n, tested, len(found),
            json.dumps(sorted(found)),
        ])

        log(
            "  n=%d patterns=%d two_cycles=%d"
            % (n, tested, len(found))
        )

    csvsave(
        "two_cycle_census.csv",
        [
            "digits",
            "sorted_nonrepdigit_patterns",
            "cycle_count",
            "cycles",
        ],
        rows,
    )

    RESULTS["census"] = {
        "max_digits": max_digits,
        "patterns": total,
        "per_length": rows,
    }
    log("  PASS: total sorted patterns = " + str(total))


# ============================================================
# 3. EVEN-BASE FOUR-DIGIT DIFFERENCE-PAIR SWEEP
# ============================================================

def audit_even_bases(max_base):
    log("\n[3/6] Even-base four-digit sweep")

    rows = []
    total = 0
    unique = []

    for base in range(2, max_base + 1, 2):
        def step(pair):
            a, b = pair
            if b:
                raw = (
                    a,
                    b - 1,
                    base - b - 1,
                    base - a,
                )
            else:
                raw = (
                    a - 1,
                    base - 1,
                    base - 1,
                    base - a,
                )
            x, y, z, w = sorted(raw, reverse=True)
            return x - w, y - z

        states = [
            (a, b)
            for a in range(1, base)
            for b in range(a + 1)
        ]

        done = set()
        periods = []

        for state in states:
            if state in done:
                continue

            path = []
            seen = {}
            current = state

            while current not in done and current not in seen:
                seen[current] = len(path)
                path.append(current)
                current = step(current)

            if current in seen:
                periods.append(len(path) - seen[current])

            done.update(path)

        odd = base
        exponent = 0
        while odd % 2 == 0:
            odd //= 2
            exponent += 1

        predicted = (
            (odd in (3, 5) and exponent % 2 == 1)
            or (odd == 7 and exponent % 3 != 0)
        )

        require(
            (len(periods) == 1) == predicted,
            "Even-base uniqueness criterion at base "
            + str(base),
        )

        if predicted:
            expected_period = (
                3 * (exponent + 1)
                if odd == 3
                else (1 if odd == 5 else 3)
            )
            require(
                periods == [expected_period],
                "Even-base period at base " + str(base),
            )
            unique.append([base, expected_period])

        total += len(states)
        rows.append([
            base,
            len(states),
            len(periods),
            json.dumps(sorted(periods)),
            predicted,
        ])

    csvsave(
        "even_bases.csv",
        [
            "base", "difference_states",
            "cycles", "periods", "predicted_unique",
        ],
        rows,
    )

    RESULTS["even_bases"] = {
        "max_base": max_base,
        "bases_tested": max_base // 2,
        "states": total,
        "unique_cycle_bases": unique,
        "scope": (
            "Bounded numerical test, not Lean verification "
            "or an all-base proof"
        ),
    }

    log("  PASS: bases tested = " + str(max_base // 2))
    log("  PASS: difference states = " + str(total))
    log("  Unique-cycle bases and periods: " + str(unique))


# ============================================================
# 4. EXACT CONDITIONAL NO-NINE RECONSTRUCTION
# ============================================================

def affine_solution(equations, n):
    reduced, pivots = rref(equations, n)

    if any(
        not any(row[:n]) and row[n]
        for row in reduced
    ):
        return None

    free = [
        j for j in range(n)
        if j not in pivots
    ]
    expressions = [
        [Q(0)] * (len(free) + 1)
        for _ in range(n)
    ]

    for k, j in enumerate(free):
        expressions[j][k + 1] = 1

    for i, j in enumerate(pivots):
        expressions[j][0] = reduced[i][n]
        for k, free_column in enumerate(free):
            expressions[j][k + 1] = -reduced[i][free_column]

    return expressions, free


def feasible(inequalities, variables):
    """Exact Fourier-Motzkin over Q: coefficients . x <= bound."""
    for j in range(variables - 1, -1, -1):
        positive = []
        negative = []
        keep = []

        for coefficients, bound in inequalities:
            if coefficients[j] > 0:
                positive.append((coefficients, bound))
            elif coefficients[j] < 0:
                negative.append((coefficients, bound))
            else:
                keep.append((
                    coefficients[:j] + coefficients[j + 1:],
                    bound,
                ))

        for a, b in positive:
            for c, d in negative:
                keep.append((
                    [
                        (-c[j]) * x + a[j] * y
                        for h, (x, y) in enumerate(zip(a, c))
                        if h != j
                    ],
                    (-c[j]) * b + a[j] * d,
                ))

        if any(
            not any(coefficients) and bound < 0
            for coefficients, bound in keep
        ):
            return False

        inequalities = keep

    return all(
        bound >= 0
        for coefficients, bound in inequalities
    )


def audit_no9():
    log("\n[4/6] Exact conditional no-nine reconstruction")

    M = [[0] * 8 for _ in range(8)]
    N = [[0] * 8 for _ in range(8)]

    for a, b in [
        (0, 3), (0, 4),
        (2, 2), (2, 5),
        (4, 1), (4, 6),
        (6, 0), (6, 7),
    ]:
        M[a][b] = 1

    for a, b, coefficient in [
        (0, 3, -1),
        (1, 3, 1), (1, 5, 1),
        (2, 2, -1), (2, 5, -1),
        (3, 2, 1), (3, 6, 1),
        (4, 1, -1), (4, 6, -1),
        (5, 1, 1), (5, 7, 1),
        (6, 0, -1), (6, 7, -1),
        (7, 0, 1),
    ]:
        N[a][b] = coefficient

    MM = mat(M, M)
    MN = mat(M, N)
    C = [
        [
            int(i == j) - MM[i][j]
            for j in range(8)
        ]
        for i in range(8)
    ]

    choices = [
        pair
        for pair in itertools.combinations(
            (1, 2, 3, 4, 6, 7, 8), 2
        )
        if sum(pair) != 10
    ]

    stats = collections.Counter()
    survivors = []
    rows = []

    for pc in choices:
        p = [
            int(i in pc)
            for i in range(1, 9)
        ]
        np = [
            sum(a * b for a, b in zip(row, p))
            for row in N
        ]

        for qc in choices:
            q = [
                int(i in qc)
                for i in range(1, 9)
            ]

            rhs = [
                sum(a * b for a, b in zip(MN[i], p))
                + sum(a * b for a, b in zip(N[i], q))
                for i in range(8)
            ]
            equations = [
                C[i] + [rhs[i]]
                for i in range(8)
            ]

            for i in range(8):
                if not pc[0] <= i + 1 <= pc[1]:
                    equations.append(
                        [int(j == i) for j in range(8)]
                        + [0]
                    )

                if not qc[0] <= i + 1 <= qc[1]:
                    equations.append(M[i] + [-np[i]])

            solution = affine_solution(equations, 8)

            if solution is None:
                status = "linear_equalities_inconsistent"
            else:
                values, free = solution
                k = len(free)

                other = [
                    [
                        sum(
                            M[i][j] * values[j][c]
                            for j in range(8)
                        )
                        + (np[i] if c == 0 else 0)
                        for c in range(k + 1)
                    ]
                    for i in range(8)
                ]

                inequalities = []

                for expressions, bounds in (
                    (values, p),
                    (other, q),
                ):
                    for expression, lower in zip(
                        expressions, bounds
                    ):
                        inequalities.append((
                            [-x for x in expression[1:]],
                            expression[0] - lower,
                        ))

                if feasible(inequalities, k):
                    status = "rationally_feasible"
                    survivors.append({
                        "p": pc,
                        "q": qc,
                        "P_affine": values,
                        "free_original_indices": [
                            i + 1 for i in free
                        ],
                    })
                else:
                    status = "nonnegative_bounds_inconsistent"

            stats[status] += 1
            rows.append([str(pc), str(qc), status])

    require(
        dict(stats) == {
            "linear_equalities_inconsistent": 320,
            "nonnegative_bounds_inconsistent": 3,
            "rationally_feasible": 1,
        },
        "No-nine reconstruction outcome counts",
    )
    require(
        survivors[0]["p"]
        == survivors[0]["q"]
        == (2, 6),
        "No-nine survivor endpoints",
    )
    require(
        survivors[0]["P_affine"] == [
            [0, 0],
            [1, 0],
            [0, 1],
            [0, 0],
            [0, 0],
            [1, 0],
            [0, 0],
            [0, 0],
        ],
        "No-nine survivor difference multiplicities",
    )

    for q in range(101):
        fixed = "6" + "3" * q + "17" + "6" * q + "4"
        require(
            K(fixed) == fixed,
            "Residual family fixed-point check",
        )

    csvsave(
        "no9_endpoint_cases.csv",
        ["endpoint_C", "endpoint_D", "status"],
        rows,
    )

    RESULTS["no9_reconstruction"] = {
        "cases": len(rows),
        "stats": dict(stats),
        "survivors": survivors,
        "scope": (
            "Exact unbounded rational feasibility for necessary "
            "pair-count conditions, conditional on preceding "
            "paper lemmas; not full Section 6 proof"
        ),
    }

    log("  PASS: 324 endpoint cases")
    log("  320 inconsistent equalities")
    log("  3 inconsistent nonnegative-count bounds")
    log("  1 residual fixed-point family")


# ============================================================
# 5. D5/D6 EXACT OBSERVABILITY, CLOSURE, PROJECTORS AND BASINS
# ============================================================

def build_graph(n):
    states = [
        digits
        for digits in itertools.combinations_with_replacement(
            range(10), n
        )
        if digits[0] != digits[-1]
    ]

    strings = [
        "".join(map(str, digits))
        for digits in states
    ]
    index = {
        word: i
        for i, word in enumerate(strings)
    }
    successors = [K(word) for word in strings]

    F = [
        index["".join(sorted(word))]
        for word in successors
    ]
    observations = [
        (
            digits[-1] - digits[0],
            digits[-2] - digits[-3],
        )
        for digits in states
    ]

    labels = {}
    depth = {}
    cycles = {}

    for state in range(len(states)):
        if state in labels:
            continue

        path = []
        position = {}
        current = state

        while current not in labels and current not in position:
            position[current] = len(path)
            path.append(current)
            current = F[current]

        if current in position:
            cycle = path[position[current]:]
            label = min(
                int(successors[q])
                for q in cycle
            )
            cycles[label] = cycle

            for q in cycle:
                labels[q] = label
                depth[q] = 0

            path = path[:position[current]]

        for q in reversed(path):
            labels[q] = labels[F[q]]
            depth[q] = depth[F[q]] + 1

    weights = [
        math.factorial(n)
        // math.prod(
            math.factorial(count)
            for count in collections.Counter(digits).values()
        )
        for digits in states
    ]

    return (
        strings, F, observations, labels,
        depth, cycles, weights, successors,
    )


def audit_observables(n):
    log(
        "\n[5/6] D%d graph, trace quotient, closure and projector"
        % n
    )

    (
        strings, F, observations, labels,
        depth, cycles, weights, successors,
    ) = build_graph(n)

    number_states = len(strings)
    base = [
        list(column)
        for column in zip(*observations)
    ]
    max_time = 7 if n == 5 else 15

    iterates = [base]
    for _ in range(max_time + 1):
        iterates.append([
            [
                row[F[i]]
                for i in range(number_states)
            ]
            for row in iterates[-1]
        ])

    if n == 5:
        basis = [
            (t, j)
            for t in range(8)
            for j in range(2)
        ]
    else:
        basis = [
            (t, j)
            for t in range(15)
            for j in range(2)
        ] + [(15, 0)]

    B = [
        iterates[t][j]
        for t, j in basis
    ]
    next_B = [
        iterates[t + 1][j]
        for t, j in basis
    ]
    dimension = len(B)

    require(
        dimension == (16 if n == 5 else 31),
        "Declared basis size",
    )

    columns = pivot_columns(B)
    minor = [
        [row[x] for x in columns]
        for row in B
    ]
    minor_determinant = determinant(minor)

    require(
        minor_determinant != 0,
        "Exact rank lower bound",
    )

    minor_inverse = inverse(minor)
    M = mat(
        [
            [row[x] for x in columns]
            for row in next_B
        ],
        minor_inverse,
    )

    for row, target in zip(M, next_B):
        check_function(
            row, B, target,
            "Exact rational closure",
        )

    constant_coefficients = mat(
        [[1] * dimension],
        minor_inverse,
    )[0]
    denominator, terms = integer_row(constant_coefficients)

    constant_witness = next(
        (
            i for i in range(number_states)
            if sum(
                coefficient * B[k][i]
                for k, coefficient in terms
            ) != denominator
        ),
        None,
    )

    require(
        constant_witness is not None,
        "Constant unexpectedly belongs to original span",
    )

    partition = list(observations)
    history = [len(set(partition))]

    while True:
        keys = [
            (observations[i], partition[F[i]])
            for i in range(number_states)
        ]
        lookup = {
            key: j
            for j, key in enumerate(dict.fromkeys(keys))
        }
        new_partition = [
            lookup[key]
            for key in keys
        ]
        history.append(len(lookup))

        if history[-1] == history[-2]:
            partition = new_partition
            break

        partition = new_partition

    expected_history = (
        [54, 178, 179, 179]
        if n == 5
        else [54, 380, 532, 554, 554]
    )
    require(
        history == expected_history,
        "Trace-refinement history",
    )

    coordinate_classes = {}
    paired_classes = set()

    for i in range(number_states):
        key = tuple(row[i] for row in B)

        if key not in coordinate_classes:
            coordinate_classes[key] = len(coordinate_classes)

        paired_classes.add((
            coordinate_classes[key],
            partition[i],
        ))

    require(
        len(coordinate_classes)
        == len(set(partition))
        == len(paired_classes),
        "Coordinate partition equals complete trace partition",
    )

    basins = collections.Counter()
    for i, weight in enumerate(weights):
        basins[labels[i]] += weight

    expected_basins = (
        {
            53955: 3190,
            61974: 48480,
            62964: 48320,
        }
        if n == 5
        else {
            420876: 935520,
            549945: 1950,
            631764: 62520,
        }
    )

    require(
        dict(basins) == expected_basins,
        "Exact string-weighted basin populations",
    )
    require(
        sum(weights) == 10 ** n - 10,
        "Total nonrepdigit string weight",
    )

    mu = max(depth.values())
    period = math.lcm(
        *(len(cycle) for cycle in cycles.values())
    )

    require(
        (mu, period)
        == ((5, 4) if n == 5 else (12, 7)),
        "Graph preperiod and period bounds",
    )

    initial_power = mpow(M, mu)
    current_power = [
        row[:] for row in initial_power
    ]
    accumulated = [
        [Q(0) for _ in range(dimension)]
        for _ in range(dimension)
    ]

    for _ in range(period):
        accumulated = [
            [a + b for a, b in zip(x, y)]
            for x, y in zip(accumulated, current_power)
        ]
        current_power = mat(current_power, M)

    require(
        current_power == initial_power,
        "M^(mu+L) = M^mu",
    )

    projector = [
        [value / period for value in row]
        for row in accumulated
    ]

    require(
        mat(projector, projector) == projector,
        "Projector idempotence",
    )
    require(
        mat(M, projector) == projector,
        "M Pi = Pi",
    )
    require(
        mat(projector, M) == projector,
        "Pi M = Pi",
    )
    require(
        rank(projector) == 2,
        "Unaugmented projector rank",
    )

    means = {
        label: [
            sum(
                Q(base[j][i])
                for i in cycle
            ) / len(cycle)
            for j in range(2)
        ]
        for label, cycle in cycles.items()
    }

    for row, (_, observable_index) in zip(projector, basis):
        targets = [
            means[labels[i]][observable_index]
            for i in range(number_states)
        ]
        check_function(
            row, B, targets,
            "Projected feature equals exact cycle mean",
        )

    ordered_labels = sorted(cycles)
    cycle_mean_matrix = [
        [Q(1)] + means[label]
        for label in ordered_labels
    ]
    cycle_mean_inverse = inverse(cycle_mean_matrix)

    indicators = {}

    for j, label in enumerate(ordered_labels):
        coefficients = [
            cycle_mean_inverse[k][j]
            for k in range(3)
        ]
        indicators[label] = coefficients

        for i in range(number_states):
            value = (
                coefficients[0]
                + coefficients[1] * means[labels[i]][0]
                + coefficients[2] * means[labels[i]][1]
            )
            require(
                value == int(labels[i] == label),
                "Affine basin-indicator identity",
            )

    cycle_digit_sums = {
        label: sum(
            Q(sum(map(int, successors[i])))
            for i in cycle
        ) / len(cycle)
        for label, cycle in cycles.items()
    }

    digit_sum_coefficients = [
        sum(
            cycle_digit_sums[label] * indicators[label][k]
            for label in ordered_labels
        )
        for k in range(3)
    ]

    expected_digit_sum = (
        [Q(63, 2), Q(0), Q(-3)]
        if n == 5
        else [Q(549, 13), Q(-33, 13), Q(21, 13)]
    )

    require(
        digit_sum_coefficients == expected_digit_sum,
        "Asymptotic digit-sum formula",
    )

    prefix = "D%d_" % n

    save(
        prefix + "exact_matrices.json",
        {
            "orientation": "psi(Fx)=M psi(x)",
            "basis_function_convention": "U^t h_j",
            "basis": basis,
            "M": M,
            "projector": projector,
            "minor_columns": columns,
            "minor_states": [
                strings[i] for i in columns
            ],
            "minor_determinant": minor_determinant,
            "constant_nonmembership_witness":
                strings[constant_witness],
            "cycle_label_order": ordered_labels,
            "cycle_mean_rows": cycle_mean_matrix,
            "cycle_mean_determinant":
                determinant(cycle_mean_matrix),
            "basin_indicator_coefficients": indicators,
            "asymptotic_digit_sum_coefficients":
                digit_sum_coefficients,
        },
    )

    state_header = [
        "state_id",
        "sorted_ascending_digits",
        "F_state_id",
        "h1",
        "h2",
        "string_weight",
        "basin_minimum_actual_cycle_value",
        "depth_to_sorted_cycle",
        "trace_class",
    ] + [
        "U%d_h%d" % (t, j + 1)
        for t, j in basis
    ]

    state_rows = (
        [
            i,
            strings[i],
            F[i],
            *observations[i],
            weights[i],
            labels[i],
            depth[i],
            partition[i],
        ] + [
            row[i] for row in B
        ]
        for i in range(number_states)
    )

    csvsave(
        prefix + "states.csv",
        state_header,
        state_rows,
    )

    RESULTS["D%d" % n] = {
        "sorted_states": number_states,
        "trace_history_including_stability_check": history,
        "trace_states": history[-1],
        "linear_dimension": dimension,
        "with_constant_dimension": dimension + 1,
        "basis_minor_determinant": minor_determinant,
        "closure_verified_all_states": True,
        "coordinate_trace_partitions_equal": True,
        "basin_string_counts": dict(basins),
        "cycle_means": means,
        "mu": mu,
        "L": period,
        "projector_rank": 2,
        "with_constant_projector_rank": 3,
        "basin_indicator_coefficients_[1,a,b]": indicators,
        "digit_sum_coefficients_[1,a,b]":
            digit_sum_coefficients,
        "all_projector_and_indicator_identities_verified": True,
    }

    log(
        "  PASS: sorted=%d trace=%d linear=%d augmented=%d"
        % (
            number_states,
            history[-1],
            dimension,
            dimension + 1,
        )
    )
    log("  PASS: exact minor determinant = " + str(minor_determinant))
    log("  PASS: exact rational closure on EVERY state")
    log("  PASS: coordinate fibres equal complete trace blocks")
    log("  PASS: projector ranks = 2 without constant / 3 with constant")
    log("  PASS: basin indicators on EVERY state")
    log("  Basin weights: " + str(dict(sorted(basins.items()))))

    for label in ordered_labels:
        log(
            "  chi_%s coefficients [1,a,b] = %s"
            % (label, [str(x) for x in indicators[label]])
        )

    log(
        "  Mean digit-sum coefficients [1,a,b] = "
        + str([str(x) for x in digit_sum_coefficients])
    )


# ============================================================
# 6. SINGLE-ATTRACTOR ENTROPY NORMALIZATION BOUNDARY
# ============================================================

def audit_single_attractor_entropy():
    log("\n[6/6] Single-attractor entropy normalization boundary")

    details = {}

    for n in (3, 4):
        (
            strings, F, observations, labels,
            depth, cycles, weights, successors,
        ) = build_graph(n)

        require(
            len(cycles) == 1,
            "Single-attractor hypothesis",
        )

        details[n] = {
            "sorted_states": len(strings),
            "cycle_labels": sorted(cycles),
            "conditional_attractor_label_entropy_when_nonempty": 0,
            "H0_minus_Hinfinity": 0,
            "normalized_ratio": (
                "undefined: 0/0 unless an extra convention is specified"
            ),
        }

        log(
            "  D%d PASS: one attractor; normalized entropy denominator = 0"
            % n
        )

    RESULTS["single_attractor_entropy"] = details


NOTES = """# AQARION audit scope

This is an independent exact-arithmetic reproduction.
It is not a Lean build, peer review, or formal verification of Section 6.

Paper:
https://arxiv.org/abs/2608.22564v1

All computations use Python's standard library.

Modular arithmetic discovers pivot columns only. Exact Fraction inversion,
nonzero exact determinants, and all-state rational closure checks establish
the D5/D6 linear certificates.

D5/D6 domain:
Sorted decimal digit multisets excluding the ten repdigits.
Leading zeroes are retained.
Weights count all fixed-width decimal strings:
n! / product of digit-count factorials.

F sorts K's output.
h = (maximum-minus-minimum, second-largest-minus-third-largest).

The two-cycle census tests exact period two and excludes fixed points.

Family 3 is counted once per unordered off-diagonal parameter pair.
Its output-count identity is verified coefficientwise.
Family membership does not prove Section 6's converse.

The no-nine reconstruction is conditional on preceding paper lemmas and their
necessary pair-count equations. Exact Fourier-Motzkin checks rational
feasibility with unbounded multiplicities, not a digit-length bound.

The even-base sweep is bounded evidence, not an all-base theorem or an
independent Lean axiom audit.

The 30-digit quadratic indicator is restricted to the two exhibited orbits.
It is not asserted to label every 30-digit transient globally.
D5/D6 indicators are checked on every state of the declared domains.

The entropy test concerns the definition's zero denominator.
It does not inspect Dahl's implementation or plots.

Full default:
- census n=2..13
- even bases 2..256
- Family 3 z=2..30
- Family 2 x=2..50
- 324 exact no-nine endpoint cases
- complete D5/D6 closures, partitions, projectors and basin certificates

Quick mode lowers only census/base/family bounds.
D5/D6 checks remain complete.

Files include:
receipt.json
exact matrix JSON files
full state CSV files
minor witnesses
cycle and family tables
source
SHA256SUMS

A .tar.gz archive is created beside the output directory.
Existing output folders are refused.

Read CSV digit strings as TEXT to avoid spreadsheet precision loss.
"""


def main():
    global OUT

    if sys.version_info < (3, 9):
        raise SystemExit(
            "Python 3.9+ required. In Termux: pkg install python"
        )

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quick",
        action="store_true",
        help=(
            "Reduce census/base/family bounds; "
            "keep complete D5/D6 checks"
        ),
    )
    parser.add_argument(
        "--out",
        help="New output directory; must not already exist",
    )
    args = parser.parse_args()

    stamp = datetime.datetime.now(
        datetime.timezone.utc
    ).strftime("%Y%m%dT%H%M%S_%fZ")

    OUT = pathlib.Path(
        args.out or ("aqarion_results_" + stamp)
    ).resolve()
    OUT.mkdir(parents=True, exist_ok=False)

    source = pathlib.Path(__file__).read_bytes()
    (OUT / "audit_source.py").write_bytes(source)
    (OUT / "README.md").write_text(NOTES)

    log("=" * 68)
    log("AQARION FULL EXACT-ARITHMETIC KAPREKAR AUDIT")
    log("=" * 68)
    log("Output: " + str(OUT))
    log("Python: " + sys.version.split()[0])
    log("Mode: " + ("QUICK" if args.quick else "FULL"))
    log("No floating-point decisions are used for exact certificates.")

    try:
        audit_families(12 if args.quick else 30)
        audit_census(10 if args.quick else 13)
        audit_even_bases(64 if args.quick else 256)
        audit_no9()
        audit_observables(5)
        audit_observables(6)
        audit_single_attractor_entropy()

        receipt = {
            "status": "PASS",
            "mode": "quick" if args.quick else "full",
            "started_utc": stamp,
            "elapsed_seconds": round(time.time() - START, 3),
            "python": sys.version,
            "platform": platform.platform(),
            "source_sha256":
                hashlib.sha256(source).hexdigest(),
            "paper": PAPER,
            "results": RESULTS,
            "scope": (
                "Independent arithmetic audit; not formal verification "
                "or proof of all classification necessity statements"
            ),
        }
        save("receipt.json", receipt)

        checksum_lines = []

        for path in sorted(OUT.iterdir()):
            if path.is_file():
                checksum_lines.append(
                    hashlib.sha256(path.read_bytes()).hexdigest()
                    + "  "
                    + path.name
                )

        (OUT / "SHA256SUMS").write_text(
            "\n".join(checksum_lines) + "\n"
        )

        archive = shutil.make_archive(
            str(OUT),
            "gztar",
            root_dir=str(OUT.parent),
            base_dir=OUT.name,
        )

        log("\n" + "=" * 68)
        log("ALL ENABLED CHECKS PASSED")
        log("=" * 68)
        log(
            "Elapsed seconds: %.3f"
            % (time.time() - START)
        )
        log("Receipt: " + str(OUT / "receipt.json"))
        log("Checksums: " + str(OUT / "SHA256SUMS"))
        log("Archive: " + archive)
        log("")
        log("To verify the result files:")
        log('  cd "' + str(OUT) + '"')
        log("  sha256sum -c SHA256SUMS")
        log("")
        log(
            "This receipt records THIS run and platform. "
            "It is not a formal-verification claim."
        )

    except Exception as error:
        for name in ("receipt.json", "SHA256SUMS"):
            target = OUT / name
            if target.exists():
                target.unlink()

        save(
            "FAILURE.json",
            {
                "status": "FAIL",
                "error_type": type(error).__name__,
                "error": str(error),
                "elapsed_seconds": time.time() - START,
                "completed_results": RESULTS,
            },
        )
        log("\nFAIL: no passing receipt issued.")
        log("Failure report: " + str(OUT / "FAILURE.json"))
        raise


if __name__ == "__main__":
    main()
