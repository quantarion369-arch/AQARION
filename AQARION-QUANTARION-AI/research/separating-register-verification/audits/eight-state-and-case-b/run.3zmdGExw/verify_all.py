from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import combinations, permutations
from math import factorial, gcd, isqrt
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import time


EXPECTED_HASH = (
    "12a3ef626871915fa3c9a69a00a6701ff"
    "14c88e792e5f3f54db78c7ad1fb72af"
)

C_SOURCE = r"""
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint8_t cm[37];
    int nc = 0;

    cm[nc++] = 0;

    for (int i = 0; i < 8; i++)
        cm[nc++] = 1u << i;

    for (int i = 0; i < 8; i++)
        for (int j = i + 1; j < 8; j++)
            cm[nc++] = (1u << i) | (1u << j);

    unsigned separating_count = 0;
    unsigned deficient_count = 0;

    FILE *f = fopen("cand.txt", "w");

    if (!f) {
        perror("cand.txt");
        return 2;
    }

    for (uint32_t code = 0; code < 16777216u; code++) {
        if ((code & 1048575u) == 0) {
            printf("C_PROGRESS=%u/16777216\n", code);
            fflush(stdout);
        }

        uint32_t z = code;
        int T[8];

        for (int i = 0; i < 8; i++) {
            T[i] = z & 7u;
            z >>= 3;
        }

        uint8_t words[8];
        int separating = 1;

        for (int s = 0; s < 8; s++) {
            int x = s;
            uint8_t word = 0;

            for (int t = 0; t < 8; t++) {
                if (x >= 4)
                    word |= 1u << t;

                x = T[x];
            }

            words[s] = word;
        }

        for (int a = 0; a < 8 && separating; a++)
            for (int b = a + 1; b < 8; b++)
                if (words[a] == words[b]) {
                    separating = 0;
                    break;
                }

        if (!separating)
            continue;

        separating_count++;

        uint64_t basis[37] = {0};
        int rank = 0;

        for (int s = 0; s < 8; s++) {
            uint64_t vector = 0;

            for (int c = 0; c < 37; c++)
                if ((words[s] & cm[c]) == cm[c])
                    vector |= 1ULL << c;

            while (vector) {
                int pivot = 63 - __builtin_clzll(vector);

                if (basis[pivot]) {
                    vector ^= basis[pivot];
                } else {
                    basis[pivot] = vector;
                    rank++;
                    break;
                }
            }
        }

        if (rank < 8) {
            deficient_count++;

            if (fprintf(f, "%u\n", code) < 0) {
                fclose(f);
                return 3;
            }
        }
    }

    if (fclose(f))
        return 4;

    printf("MAPS_ENUMERATED=16777216\n");
    printf("SEPARATING_MAPS=%u\n", separating_count);
    printf("F2_DEGREE2_DEFICIENT=%u\n", deficient_count);

    return 0;
}
"""


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def integer_rank(matrix):
    """Exact rational rank using integer row elimination."""
    A = [row[:] for row in matrix]
    rank = 0

    for column in range(len(A[0]) if A else 0):
        pivot = next(
            (i for i in range(rank, len(A)) if A[i][column]),
            None,
        )

        if pivot is None:
            continue

        A[rank], A[pivot] = A[pivot], A[rank]

        for i in range(rank + 1, len(A)):
            a = A[i][column]

            if not a:
                continue

            b = A[rank][column]
            common_pivot = gcd(a, b)

            row = [
                (b // common_pivot) * x
                - (a // common_pivot) * y
                for x, y in zip(A[i], A[rank])
            ]

            common_row = reduce(gcd, row, 0)

            A[i] = (
                [x // common_row for x in row]
                if common_row > 1
                else row
            )

        rank += 1

        if rank == len(A):
            break

    return rank


def fraction_rank(matrix):
    """Separate exact elimination implementation using Fraction."""
    A = [
        [Fraction(value) for value in row]
        for row in matrix
    ]

    rank = 0

    for column in range(len(A[0]) if A else 0):
        pivot = next(
            (i for i in range(rank, len(A)) if A[i][column]),
            None,
        )

        if pivot is None:
            continue

        A[rank], A[pivot] = A[pivot], A[rank]

        value = A[rank][column]
        A[rank] = [x / value for x in A[rank]]

        for i in range(len(A)):
            if i != rank and A[i][column]:
                coefficient = A[i][column]
                A[i] = [
                    x - coefficient * y
                    for x, y in zip(A[i], A[rank])
                ]

        rank += 1

        if rank == len(A):
            break

    return rank


MASKS = (
    [0]
    + [1 << i for i in range(8)]
    + [
        (1 << i) | (1 << j)
        for i in range(8)
        for j in range(i + 1, 8)
    ]
)

LITERAL_MASKS = {
    0, 255, 15, 240, 51, 204, 85, 170
}


def words_of(T):
    words = []

    for x in range(8):
        word = 0

        for t in range(8):
            word |= int(x >= 4) << t
            x = T[x]

        words.append(word)

    return words


def matrix_of(words):
    return [
        [int((word & mask) == mask) for mask in MASKS]
        for word in words
    ]


def run_census(out):
    compiler = next(
        (
            shutil.which(name)
            for name in ("clang", "gcc", "cc")
            if shutil.which(name)
        ),
        None,
    )

    require(
        compiler is not None,
        "C compiler missing. In Termux install clang before running.",
    )

    source = out / "enumerate.c"
    executable = out / "enumerate"

    source.write_text(C_SOURCE, encoding="utf-8")

    command = [
        compiler,
        "-O3",
        "-std=c11",
        "-Wall",
        "-Wextra",
        str(source),
        "-o",
        str(executable),
    ]

    build = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    (out / "build.stdout.txt").write_text(
        build.stdout, encoding="utf-8"
    )
    (out / "build.stderr.txt").write_text(
        build.stderr, encoding="utf-8"
    )

    require(
        build.returncode == 0,
        "Compilation failed; inspect build.stderr.txt",
    )

    version = subprocess.run(
        [compiler, "--version"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    (out / "compiler.txt").write_text(
        version, encoding="utf-8"
    )

    c_start = time.monotonic()

    with (
        (out / "C_stdout.txt").open("w", encoding="utf-8") as log,
        (out / "C_stderr.txt").open("w", encoding="utf-8") as err,
    ):
        process = subprocess.Popen(
            [str(executable)],
            cwd=out,
            stdout=subprocess.PIPE,
            stderr=err,
            text=True,
            bufsize=1,
        )

        for line in process.stdout:
            print(line, end="", flush=True)
            log.write(line)
            log.flush()

        returncode = process.wait()

    (out / "C_exit.txt").write_text(
        str(returncode) + "\n", encoding="utf-8"
    )

    require(returncode == 0, "C enumerator failed")

    c_seconds = time.monotonic() - c_start
    fields = {}

    for line in (out / "C_stdout.txt").read_text().splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            if value.isdigit():
                fields[key] = int(value)

    require(
        fields.get("MAPS_ENUMERATED") == 16777216,
        "Enumeration count mismatch",
    )
    require(
        fields.get("SEPARATING_MAPS") == 1612800,
        "Separating count mismatch",
    )
    require(
        fields.get("F2_DEGREE2_DEFICIENT") == 9216,
        "F2 defect count mismatch",
    )

    codes = [
        int(line)
        for line in (out / "cand.txt").read_text().splitlines()
    ]

    require(
        len(codes) == 9216
        and codes == sorted(set(codes)),
        "Candidate list malformed",
    )

    rational_histogram = Counter()
    feedback_counts = Counter()
    rational_defects = []

    for index, code in enumerate(codes, 1):
        T = [(code >> (3 * i)) & 7 for i in range(8)]
        words = words_of(T)

        require(
            len(set(words)) == 8,
            "Nonseparating candidate",
        )

        A = matrix_of(words)
        rational_rank = integer_rank(A)

        require(
            rational_rank in (7, 8),
            "Unexpected rational rank",
        )

        rational_histogram[rational_rank] += 1

        prefix = [
            ((word & 1) << 2)
            | (((word >> 1) & 1) << 1)
            | ((word >> 2) & 1)
            for word in words
        ]

        require(
            len(set(prefix)) == 8,
            "Candidate prefix is not bijective",
        )

        feedback = [0] * 8

        for state in range(8):
            feedback[prefix[state]] = (words[state] >> 3) & 1

        feedback_mask = sum(
            value << u
            for u, value in enumerate(feedback)
        )

        require(
            all(
                prefix[T[state]]
                == (
                    ((prefix[state] << 1) & 7)
                    | feedback[prefix[state]]
                )
                for state in range(8)
            ),
            "Register shift identity failure",
        )

        feedback_counts[(feedback_mask, rational_rank)] += 1

        require(
            rational_rank
            == (7 if feedback_mask in LITERAL_MASKS else 8),
            "Feedback/rational-rank classification mismatch",
        )

        if rational_rank == 7:
            rational_defects.append(code)

            require(
                integer_rank([row[:9] for row in A]) == 4,
                "Linear rank mismatch",
            )

            parity = [
                (-1) ** u.bit_count()
                for u in prefix
            ]

            require(
                all(
                    sum(
                        parity[state] * A[state][column]
                        for state in range(8)
                    ) == 0
                    for column in range(37)
                ),
                "Parity obstruction failure",
            )

            require(
                sum(
                    parity[state]
                    * int((words[state] & 7) == 7)
                    for state in range(8)
                ) == -1,
                "Cubic witness failure",
            )

        if index % 1024 == 0 or index == len(codes):
            print(
                f"Q_PROGRESS={index}/{len(codes)}",
                flush=True,
            )

    require(
        dict(rational_histogram) == {7: 4608, 8: 4608},
        "Rational histogram mismatch",
    )

    affine_masks = {
        sum(
            (constant ^ ((coefficients & u).bit_count() & 1))
            << u
            for u in range(8)
        )
        for coefficients in range(8)
        for constant in (0, 1)
    }

    require(
        {
            feedback_mask
            for feedback_mask, rank in feedback_counts
        } == affine_masks,
        "F2 affine feedback set mismatch",
    )

    require(
        all(
            count == 576
            for count in feedback_counts.values()
        ),
        "Feedback multiplicity mismatch",
    )

    canonical_checks = []

    for feedback_mask in sorted(affine_masks):
        T = [
            ((u << 1) & 7) | ((feedback_mask >> u) & 1)
            for u in range(8)
        ]

        exact = fraction_rank(matrix_of(words_of(T)))

        require(
            exact
            == (7 if feedback_mask in LITERAL_MASKS else 8),
            "Independent Fraction rank disagreement",
        )

        canonical_checks.append({
            "feedback_mask": feedback_mask,
            "Fraction_rank": exact,
        })

    generated = set()

    for low in permutations(range(4)):
        for high in permutations(range(4, 8)):
            coordinate_map = list(low) + list(high)
            inverse = [0] * 8

            for state, u in enumerate(coordinate_map):
                inverse[u] = state

            for feedback_mask in LITERAL_MASKS:
                T = [
                    inverse[
                        ((u << 1) & 7)
                        | ((feedback_mask >> u) & 1)
                    ]
                    for u in coordinate_map
                ]

                generated.add(
                    sum(
                        value << (3 * state)
                        for state, value in enumerate(T)
                    )
                )

    require(
        generated == set(rational_defects),
        "Generated transition set differs from census",
    )

    payload = (
        b"\n".join(
            str(code).encode("ascii")
            for code in rational_defects
        )
        + b"\n"
    )

    fingerprint = hashlib.sha256(payload).hexdigest()

    require(
        fingerprint == EXPECTED_HASH,
        "Rational defect fingerprint mismatch",
    )

    (out / "rational_defect_codes.txt").write_bytes(payload)

    print("Q_RANK_7=4608")
    print("Q_RANK_8_WITHIN_F2_CANDIDATES=4608")
    print("GENERATED_SET_EQUALITY=PASS")
    print("PARITY_CERTIFICATES=4608_PASS")
    print("FRACTION_CANONICAL_CROSSCHECK=16_PASS")
    print("Q_DEFECT_SHA256=" + fingerprint)

    return {
        "maps": 16777216,
        "separating": 1612800,
        "F2_deficient": 9216,
        "Q_rank7": 4608,
        "Q_rank8_separating": 1608192,
        "canonical_Fraction_checks": canonical_checks,
        "feedback_counts": [
            {
                "mask": mask,
                "rank": rank,
                "count": count,
            }
            for (mask, rank), count
            in sorted(feedback_counts.items())
        ],
        "parity_certificates_checked": 4608,
        "generated_set_equals_census": True,
        "sha256": fingerprint,
        "C_scan_seconds": c_seconds,
        "compiler": compiler,
        "compile_command": command,
    }


def valuation_factorial(n, p):
    total = 0

    while n:
        n //= p
        total += n

    return total


def carries(a, b, p):
    """Count carries including incoming propagated carries."""
    require(
        0 <= b <= a and p >= 2,
        "Invalid carry-test inputs",
    )

    x = b
    y = a - b
    carry = 0
    total = 0

    while x or y or carry:
        carry = int(x % p + y % p + carry >= p)
        total += carry
        x //= p
        y //= p

    return total


def verify_case_b(out):
    N = 100

    stirling = [[0] * 4 for _ in range(N + 1)]
    stirling[0][0] = 1

    for n in range(1, N + 1):
        for m in range(1, min(n, 3) + 1):
            stirling[n][m] = (
                (n - 1) * stirling[n - 1][m]
                + stirling[n - 1][m - 1]
            )

    partitions = [[0] * (N + 1) for _ in range(4)]
    partitions[0][0] = 1

    for m in range(1, 4):
        for n in range(1, N + 1):
            partitions[m][n] = (
                partitions[m - 1][n - 1]
                + (
                    partitions[m][n - m]
                    if n >= m
                    else 0
                )
            )

    ratios = {
        n: Fraction(
            6 * stirling[n][3],
            factorial(n) * partitions[3][n],
        )
        for n in range(3, N + 1)
    }

    require(
        [ratios[n] for n in range(3, 9)]
        == [
            Fraction(1),
            Fraction(3, 2),
            Fraction(7, 8),
            Fraction(5, 8),
            Fraction(29, 60),
            Fraction(469, 1200),
        ],
        "Small ratio mismatch",
    )

    require(
        all(0 < ratios[n] < 1 for n in range(5, N + 1)),
        "Finite below-one check failed",
    )

    require(
        all(
            ratios[n].denominator != 1
            for n in range(4, N + 1)
        ),
        "Unexpected finite integral ratio",
    )

    def prime(p):
        return p >= 2 and all(
            p % divisor
            for divisor in range(2, isqrt(p) + 1)
        )

    uncovered = [
        n
        for n in range(7, 100)
        if not any(
            prime(p)
            for p in range(n // 3 + 1, (n - 1) // 2 + 1)
        )
    ]

    require(
        uncovered == [9, 10, 21, 22],
        "Prime witness coverage mismatch",
    )

    for a in range(31):
        for b in range(a + 1):
            for p in (2, 3, 5, 7):
                expected = (
                    valuation_factorial(a, p)
                    - valuation_factorial(b, p)
                    - valuation_factorial(a - b, p)
                )

                require(
                    carries(a, b, p) == expected,
                    "Corrected Kummer helper failed",
                )

    H = Fraction(0)
    H2 = Fraction(0)

    for n in range(2, N + 1):
        H += Fraction(1, n - 1)
        H2 += Fraction(1, (n - 1) ** 2)

        if n >= 3:
            require(
                stirling[n][3]
                == factorial(n - 1) * (H * H - H2) / 2,
                "Stirling harmonic identity failed",
            )

    report = {
        "finite_check_range": [3, N],
        "ratios": {
            str(n): str(value)
            for n, value in ratios.items()
        },
        "uncovered_prime_witnesses_7_to99": uncovered,
        "corrected_Kummer_checks": "PASS",
        "harmonic_identity_checks": "PASS",
        "general_m3_proof": (
            "Written in SCOPE_AND_PROOF.md; "
            "not machine formalized"
        ),
    }

    (out / "case_b_results.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    print("CASE_B_M3_FINITE_CHECKS=PASS")
    print("WITNESS_GAPS_7_TO99=[9,10,21,22]")
    print("CORRECTED_KUMMER_TESTS=PASS")
    print("STIRLING_HARMONIC_IDENTITY=PASS")

    return report


def verify_cancellation():
    rows = list(combinations(range(4), 1))
    columns = list(combinations(range(4), 2))

    U = {
        ell: [
            [
                int(len(set(a) & set(b)) == ell)
                for b in columns
            ]
            for a in rows
        ]
        for ell in (0, 1)
    }

    def combination(a, b):
        return [
            [
                a * x + b * y
                for x, y in zip(row0, row1)
            ]
            for row0, row1 in zip(U[0], U[1])
        ]

    for a in range(-3, 4):
        for b in range(-3, 4):
            require(
                fraction_rank(combination(a, b))
                == int(a + b != 0) + 3 * int(b - a != 0),
                "Small-family rank formula failed",
            )

    ranks = {
        label: fraction_rank(combination(a, b))
        for label, a, b in [
            ("U0", 1, 0),
            ("U1", 0, 1),
            ("U0+U1", 1, 1),
            ("U0-U1", 1, -1),
            ("2U0+U1", 2, 1),
        ]
    }

    require(
        ranks == {
            "U0": 4,
            "U1": 4,
            "U0+U1": 1,
            "U0-U1": 3,
            "2U0+U1": 4,
        },
        "Cancellation ranks mismatch",
    )

    print("TRADE_MATRIX_CANCELLATION_CHECK=PASS")

    return {
        "ranks": ranks,
        "coefficient_pairs_checked": 49,
        "scope": (
            "Explicit matrix family; not a verdict on "
            "other theorems or journal revisions"
        ),
    }


def main():
    out = Path(sys.argv[1]).resolve()
    start = time.monotonic()

    require(
        integer_rank([[1, 0], [0, 1]]) == 2,
        "Integer rank self-test failed",
    )

    require(
        fraction_rank([[1, 1], [1, 1]]) == 1,
        "Fraction rank self-test failed",
    )

    census = run_census(out)
    case_b = verify_case_b(out)
    trade = verify_cancellation()

    proof = """# Scope and elementary m=3 proof

The program reruns all 8^8 maps for fixed h=00001111.
Its C sieve uses F2; every deficient candidate receives exact Q rank.
Canonical Fraction elimination is a separate rank cross-check,
not SymPy. Generated-set equality and parity certificates are checked.

## Case B

Let R(n,3)=6*c(n,3)/(n!*p_3(n)).
Here c counts permutations with three cycles and p_3 counts
partitions into exactly three positive parts.

R(3,3)=1 and R(4,3)=3/2.

Direct exact checks give:
R(5..8,3)=7/8, 5/8, 29/60, 469/1200.

For n>=9, take the seven partitions of 9 into three parts:
(1,1,7), (1,2,6), (1,3,5), (1,4,4),
(2,2,5), (2,3,4), (3,3,3).

Adding n-9 to the largest part gives seven distinct partitions of n.
Thus p_3(n)>=7.

Since 0<c(n,3)<=n!, we have 0<R(n,3)<=6/7<1.

Consequently R(n,3) is integral exactly for n=3, among n>=3.
This written all-n proof is not machine formalized.

Finite ratio checks, a corrected Kummer helper, and the harmonic
Stirling identity are tested separately. No false harmonic/binomial
identity is used. This ratio lane is separate from the dynamics paper.

## Trade-matrix example

The program checks the explicit four-by-six matrices and 49 coefficient
pairs. It does not prove a general intersection-matrix rank theorem.

## Boundaries

No arbitrary-dimension dynamics theorem, novelty, publication,
or claim promotion is certified.

Application sources are not modified. No Git operation is performed.
"""

    (out / "SCOPE_AND_PROOF.md").write_text(
        proof, encoding="utf-8"
    )

    report = {
        "status": "PASS",
        "census": census,
        "case_b": case_b,
        "trade_example": trade,
        "elapsed_seconds": time.monotonic() - start,
        "application_sources_changed": False,
        "git_stage_commit_push": "NONE",
        "general_theorem_machine_checked": False,
    }

    result_path = out / "results.json"

    result_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    require(
        json.loads(result_path.read_text(encoding="utf-8"))
        == report,
        "JSON read-back failed",
    )

    print("SAVED_JSON_READBACK=PASS")
    print("APPLICATION_SOURCES_CHANGED=NO")
    print("STAGED_COMMITTED_PUSHED=NO")
    print(
        "TOTAL_SECONDS="
        + format(time.monotonic() - start, ".2f")
    )
    print("OVERALL_STATUS=PASS", flush=True)


if __name__ == "__main__":
    main()
