from collections import Counter
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
import json
import sys
import time

N = 16
D = 4
MASK = (1 << N) - 1


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def primitive_necklaces(n):
    """Generate one representative of each primitive binary necklace."""
    a = [0] * n
    result = []

    def generate(length, period):
        if length == n:
            if period == n:
                result.append(int("".join(map(str, a)), 2))
            return

        a[length] = a[length - period]
        generate(length + 1, period)

        if a[length - period] == 0:
            a[length] = 1
            generate(length + 1, length + 1)

    generate(1, 1)
    return sorted(result)


def rotations(word, n):
    mask = (1 << n) - 1
    return [
        ((word << shift) | (word >> (n - shift))) & mask
        for shift in range(n)
    ]


def point_rows(word, n):
    """Rows are rotations; coordinates are MSB first."""
    return [
        tuple((rotation >> (n - 1 - i)) & 1 for i in range(n))
        for rotation in rotations(word, n)
    ]


def exact_rank(matrix):
    """Exact rational row rank."""
    if not matrix:
        return 0

    A = [[Fraction(value) for value in row] for row in matrix]
    row_count = len(A)
    column_count = len(A[0])
    rank = 0

    for column in range(column_count):
        pivot = next(
            (r for r in range(rank, row_count) if A[r][column]),
            None,
        )
        if pivot is None:
            continue

        A[rank], A[pivot] = A[pivot], A[rank]
        pivot_value = A[rank][column]
        A[rank] = [value / pivot_value for value in A[rank]]

        for r in range(row_count):
            if r != rank and A[r][column]:
                factor = A[r][column]
                A[r] = [
                    A[r][j] - factor * A[rank][j]
                    for j in range(column_count)
                ]

        rank += 1
        if rank == row_count:
            break

    return rank


def degree_three_matrix(points):
    """Evaluation matrix of all squarefree monomials through degree 3."""
    n = len(points[0])
    monomials = [()]
    monomials.extend((i,) for i in range(n))
    monomials.extend(combinations(range(n), 2))
    monomials.extend(combinations(range(n), 3))

    matrix = []
    for point in points:
        matrix.append([
            1 if not S else int(all(point[i] for i in S))
            for S in monomials
        ])

    return matrix


def prefix_separates(points, width):
    return len({point[:width] for point in points}) == len(points)


def de_bruijn_cycle_count_binary(order):
    return 1 << ((1 << (order - 1)) - order)


def main(output_directory):
    start = time.monotonic()
    representatives = primitive_necklaces(N)

    expected_count = ((1 << N) - (1 << (N // 2))) // N
    # For N=16, primitive words are those not having any proper
    # divisor period. The exact necklace count is phi-based:
    # sum_{e|N} mu(N/e) 2^e / N. Here compute it directly by Mobius.
    def mobius(value):
        factors = 0
        p = 2
        x = value
        while p * p <= x:
            if x % p == 0:
                x //= p
                factors += 1
                if x % p == 0:
                    return 0
            p += 1
        if x > 1:
            factors += 1
        return -1 if factors % 2 else 1

    exact_expected = sum(
        mobius(N // divisor) * (1 << divisor)
        for divisor in range(1, N + 1)
        if N % divisor == 0
    ) // N

    require(
        len(representatives) == exact_expected,
        "Primitive-necklace count disagrees with Mobius formula",
    )
    require(
        len(representatives) == 4080,
        "Expected 4,080 primitive binary necklaces of length 16",
    )

    full_rank_count = 0
    deficient_count = 0
    deficient_prefix_good = []
    deficient_prefix_bad = []
    full_rank_prefix_bad = []
    prefix_good_total = 0
    rank_counts = Counter()
    examples = []

    for index, word in enumerate(representatives, 1):
        points = point_rows(word, N)
        require(
            len(set(points)) == N,
            "Primitive representative did not produce 16 distinct rotations",
        )

        rank = exact_rank(degree_three_matrix(points))
        prefix_good = prefix_separates(points, D)
        rank_counts[rank] += 1

        if rank == N:
            full_rank_count += 1
            if not prefix_good:
                full_rank_prefix_bad.append(word)
        else:
            deficient_count += 1
            item = {"word": format(word, f"0{N}b"), "rank": rank}
            if prefix_good:
                deficient_prefix_good.append(item)
            else:
                deficient_prefix_bad.append(item)

        if prefix_good:
            prefix_good_total += 1

        if len(examples) < 12 and (
            rank < N or not prefix_good
        ):
            examples.append({
                "word": format(word, f"0{N}b"),
                "degree_3_rank": rank,
                "four_prefix_separates": prefix_good,
            })

        if index % 500 == 0:
            print(
                f"PROGRESS={index}/{len(representatives)}",
                flush=True,
            )

    expected_de_bruijn = de_bruijn_cycle_count_binary(D)
    require(
        prefix_good_total == expected_de_bruijn,
        "Four-prefix-good count disagrees with de Bruijn count",
    )
    require(
        full_rank_count + deficient_count == len(representatives),
        "Rank totals do not sum to primitive-necklace count",
    )
    require(
        len(deficient_prefix_good)
        + len(deficient_prefix_bad)
        == deficient_count,
        "Deficient prefix buckets do not sum to deficient count",
    )
    require(
        len(full_rank_prefix_bad)
        <= full_rank_count,
        "Full-rank prefix-bad count exceeds full-rank count",
    )

    result = {
        "status": "PASS",
        "scope": (
            "All primitive binary observation necklaces of length 16 "
            "on a single 16-state directed cycle."
        ),
        "coefficient_field": "Q",
        "rank_method": "Exact Fraction Gaussian elimination",
        "rank_matrix": (
            "16 itinerary rows by 697 squarefree monomials "
            "of degree at most 3"
        ),
        "primitive_necklace_count": len(representatives),
        "full_rank_degree_3": full_rank_count,
        "deficient_degree_3": deficient_count,
        "degree_3_rank_histogram": {
            str(rank): count
            for rank, count in sorted(rank_counts.items())
        },
        "deficient_and_four_prefix_separates": len(
            deficient_prefix_good
        ),
        "deficient_and_four_prefix_fails": len(
            deficient_prefix_bad
        ),
        "full_rank_and_four_prefix_fails": len(
            full_rank_prefix_bad
        ),
        "four_prefix_separates_total": prefix_good_total,
        "expected_binary_de_bruijn_cycles_order_4": expected_de_bruijn,
        "bridge_counterexamples": deficient_prefix_bad,
        "deficient_prefix_good_examples": deficient_prefix_good,
        "full_rank_prefix_bad_examples": [
            format(word, f"0{N}b")
            for word in full_rank_prefix_bad[:100]
        ],
        "first_interesting_examples": examples,
        "repository_application_sources_modified": False,
        "git_stage_commit_push": "NONE",
    }

    output_path = output_directory / "results.json"
    output_path.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    print("PRIMITIVE_NECKLACES=", len(representatives))
    print("FULL_RANK_DEGREE_3=", full_rank_count)
    print("DEFICIENT_DEGREE_3=", deficient_count)
    print(
        "DEGREE_3_RANK_HISTOGRAM=",
        dict(sorted(rank_counts.items())),
    )
    print(
        "DEFICIENT_AND_PREFIX_GOOD=",
        len(deficient_prefix_good),
    )
    print(
        "DEFICIENT_AND_PREFIX_BAD=",
        len(deficient_prefix_bad),
    )
    print(
        "FULL_RANK_AND_PREFIX_BAD=",
        len(full_rank_prefix_bad),
    )
    print("PREFIX_GOOD_TOTAL=", prefix_good_total)
    print("EXPECTED_DE_BRUIJN_ORDER_4=", expected_de_bruijn)
    print("BRIDGE_COUNTEREXAMPLES=", deficient_prefix_bad)
    print("RUNTIME_SECONDS=", round(time.monotonic() - start, 2))
    print("RESULT_JSON=", output_path)
    print("OVERALL_STATUS=PASS")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
