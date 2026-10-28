from collections import Counter
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
import sys
import time

N = 16
MASK = (1 << N) - 1
PRIME = 2147483647

SUBSETS = [
    S
    for degree in range(1, 4)
    for S in combinations(range(N), degree)
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def primitive_representatives():
    a = [0] * N
    result = []

    def generate(length, period):
        if length == N:
            if period == N:
                result.append(int("".join(map(str, a)), 2))
            return

        a[length] = a[length - period]
        generate(length + 1, period)

        if a[length - period] == 0:
            a[length] = 1
            generate(length + 1, length + 1)

    generate(1, 1)
    return sorted(result)


def feature_columns(word):
    rotations = [
        ((word << shift) | (word >> (N - shift))) & MASK
        for shift in range(N)
    ]

    observations = [
        sum(
            ((rotation >> (N - 1 - coordinate)) & 1) << row
            for row, rotation in enumerate(rotations)
        )
        for coordinate in range(N)
    ]

    # A column is encoded by its sixteen Boolean evaluations.
    # Removing identical columns preserves rank.
    seen = {MASK}
    columns = [MASK]

    for S in SUBSETS:
        value = MASK
        for coordinate in S:
            value &= observations[coordinate]

        if value not in seen:
            seen.add(value)
            columns.append(value)

    return columns, rotations


def modular_rank(columns):
    basis = {}

    for bits in columns:
        vector = [(bits >> row) & 1 for row in range(N)]

        for pivot, existing in sorted(basis.items()):
            coefficient = vector[pivot]
            if coefficient:
                vector = [
                    (x - coefficient*y) % PRIME
                    for x, y in zip(vector, existing)
                ]

        pivot = next(
            (i for i, value in enumerate(vector) if value),
            None,
        )

        if pivot is not None:
            inverse = pow(vector[pivot], PRIME - 2, PRIME)
            basis[pivot] = [
                value * inverse % PRIME
                for value in vector
            ]

        if len(basis) == N:
            return N

    return len(basis)


def rational_rank(matrix):
    if not matrix:
        return 0

    A = [
        [Fraction(value) for value in row]
        for row in matrix
    ]
    rank = 0

    for column in range(len(A[0])):
        pivot = next(
            (r for r in range(rank, len(A)) if A[r][column]),
            None,
        )
        if pivot is None:
            continue

        A[rank], A[pivot] = A[pivot], A[rank]
        value = A[rank][column]
        A[rank] = [x / value for x in A[rank]]

        for r in range(rank + 1, len(A)):
            coefficient = A[r][column]
            if coefficient:
                A[r] = [
                    x - coefficient*y
                    for x, y in zip(A[r], A[rank])
                ]

        rank += 1
        if rank == len(A):
            break

    return rank


def exact_fallback(columns):
    # Row Gram matrix: sixteen by sixteen, never 697 by 697.
    gram = [
        [
            sum(
                ((bits >> i) & 1) * ((bits >> j) & 1)
                for bits in columns
            )
            for j in range(N)
        ]
        for i in range(N)
    ]
    return rational_rank(gram)


def direct_rational_rank(columns):
    matrix = [
        [(bits >> row) & 1 for bits in columns]
        for row in range(N)
    ]
    return rational_rank(matrix)


def main(output_directory):
    start = time.monotonic()
    representatives = primitive_representatives()

    require(
        len(representatives) == 4080,
        "Primitive-necklace count must be 4080",
    )
    require(
        len(set(representatives)) == 4080,
        "Duplicate representatives",
    )

    print("PRIMITIVE_NECKLACES=4080", flush=True)

    require(
        exact_fallback([0]) == 0,
        "Zero-matrix fallback test failed",
    )
    require(
        exact_fallback([1 << i for i in range(N)]) == N,
        "Identity fallback test failed",
    )
    require(
        exact_fallback(feature_columns(0)[0]) == 1,
        "Constant-observation fallback test failed",
    )

    sample_checks = []
    for index in (0, 100, len(representatives) - 1):
        word = representatives[index]
        columns, _ = feature_columns(word)
        modular = modular_rank(columns)
        exact = direct_rational_rank(columns)

        require(
            modular == exact == N,
            "Direct rational sample cross-check failed",
        )

        sample_checks.append({
            "word": format(word, "016b"),
            "modular_rank": modular,
            "direct_rational_rank": exact,
        })

    print("EXACT_FALLBACK_SELFTESTS=PASS", flush=True)
    print("DIRECT_RATIONAL_SAMPLE_CHECKS=3_PASS", flush=True)

    histogram = Counter()
    full_rank = 0
    deficient = 0
    prefix_good_total = 0
    deficient_prefix_good = []
    deficient_prefix_bad = []
    full_rank_prefix_bad = 0
    fallback_count = 0
    cases = []

    for index, word in enumerate(representatives, 1):
        columns, rotations = feature_columns(word)

        require(
            len(set(rotations)) == N,
            "Nonprimitive word entered the census",
        )
        require(
            min(rotations) == word,
            "Representative is not the minimum rotation",
        )

        modular = modular_rank(columns)

        if modular == N:
            exact = N
            method = "modular_full_rank_certificate"
        else:
            fallback_count += 1
            exact = exact_fallback(columns)
            method = "exact_rational_row_gram"

        prefix_good = len({
            rotation >> 12 for rotation in rotations
        }) == N

        histogram[exact] += 1
        prefix_good_total += int(prefix_good)

        item = {
            "word": format(word, "016b"),
            "modular_rank": modular,
            "rational_rank": exact,
            "four_prefix_separates": prefix_good,
            "rank_certificate_method": method,
        }
        cases.append(item)

        if exact == N:
            full_rank += 1
            if not prefix_good:
                full_rank_prefix_bad += 1
        else:
            deficient += 1
            if prefix_good:
                deficient_prefix_good.append(item)
            else:
                deficient_prefix_bad.append(item)

        if index % 250 == 0 or index == len(representatives):
            elapsed = time.monotonic() - start
            print(
                f"PROGRESS={index}/{len(representatives)} "
                f"SECONDS={elapsed:.2f} "
                f"EXACT_FALLBACKS={fallback_count}",
                flush=True,
            )

    require(
        full_rank + deficient == 4080,
        "Rank totals disagree",
    )
    require(
        prefix_good_total == 16,
        "Expected sixteen de Bruijn order-four cycles",
    )
    require(
        prefix_good_total
        + full_rank_prefix_bad
        + len(deficient_prefix_bad)
        == 4080,
        "Prefix totals disagree",
    )
    require(
        len(deficient_prefix_good)
        + len(deficient_prefix_bad)
        == deficient,
        "Deficient buckets disagree",
    )

    elapsed = time.monotonic() - start

    report = {
        "execution_status": "PASS",
        "scope": (
            "Primitive binary observations on one directed "
            "sixteen-state cycle, modulo rotation"
        ),
        "coefficient_field": "Q",
        "modulus": PRIME,
        "rank_method": (
            "Full modular rank certifies full rational rank; "
            "modular deficiency triggers exact rational rank "
            "of a sixteen-by-sixteen row Gram matrix"
        ),
        "primitive_necklaces": len(representatives),
        "full_rank_degree_3": full_rank,
        "deficient_degree_3": deficient,
        "rank_histogram": {
            str(rank): count
            for rank, count in sorted(histogram.items())
        },
        "prefix_good_total": prefix_good_total,
        "full_rank_and_prefix_bad": full_rank_prefix_bad,
        "deficient_and_prefix_good": deficient_prefix_good,
        "bridge_counterexamples": deficient_prefix_bad,
        "bridge_test_nonvacuous": deficient > 0,
        "exact_fallback_count": fallback_count,
        "direct_rational_sample_checks": sample_checks,
        "elapsed_seconds": elapsed,
        "cases": cases,
        "application_sources_modified": False,
        "stage_commit_push": "NONE",
    }

    path = output_directory / "results.json"
    path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    require(
        json.loads(path.read_text(encoding="utf-8")) == report,
        "Saved JSON read-back failed",
    )

    print("FULL_RANK_DEGREE_3=" + str(full_rank))
    print("DEFICIENT_DEGREE_3=" + str(deficient))
    print("PREFIX_GOOD_TOTAL=" + str(prefix_good_total))
    print("FULL_RANK_AND_PREFIX_BAD=" + str(full_rank_prefix_bad))
    print(
        "DEFICIENT_AND_PREFIX_GOOD="
        + str(len(deficient_prefix_good))
    )
    print(
        "BRIDGE_COUNTEREXAMPLES="
        + str(len(deficient_prefix_bad))
    )
    print(
        "BRIDGE_TEST_NONVACUOUS="
        + ("YES" if deficient else "NO")
    )
    print("EXACT_FALLBACKS=" + str(fallback_count))
    print("SAVED_JSON_READBACK=PASS")
    print("RUNTIME_SECONDS=" + format(elapsed, ".2f"))
    print("OVERALL_STATUS=PASS", flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
