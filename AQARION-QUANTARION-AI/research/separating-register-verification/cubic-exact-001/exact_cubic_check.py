#!/usr/bin/env python3

import json
import platform
import sys
from fractions import Fraction
from itertools import combinations
from math import gcd, prod
from pathlib import Path

CASES = [
    (
        (6, 1, 4, 0, 6, 4, 1, 0),
        (0, 1, 2, 3, 4, 5, 6, 7),
    ),
    (
        (1, 6, 4, 0, 6, 4, 1, 0),
        (84, 85, 86, 87, 168, 169, 170, 171),
    ),
    (
        (4, 0, 6, 1, 6, 4, 1, 0),
        (50, 51, 102, 103, 152, 153, 204, 205),
    ),
]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rref(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    if not a:
        return a, []

    rows = len(a)
    cols = len(a[0])
    pivot_row = 0
    pivots = []

    for col in range(cols):
        selected = next(
            (r for r in range(pivot_row, rows) if a[r][col]),
            None,
        )
        if selected is None:
            continue

        a[pivot_row], a[selected] = a[selected], a[pivot_row]

        pivot = a[pivot_row][col]
        a[pivot_row] = [v / pivot for v in a[pivot_row]]

        for r in range(rows):
            if r != pivot_row and a[r][col]:
                factor = a[r][col]
                a[r] = [
                    x - factor * y
                    for x, y in zip(a[r], a[pivot_row])
                ]

        pivots.append(col)
        pivot_row += 1

        if pivot_row == rows:
            break

    return a, pivots


def exact_rank(matrix):
    return len(rref(matrix)[1])


def itinerary_words(T, labels):
    n = len(T)
    words = []

    for initial in range(n):
        state = initial
        word = 0

        for t in range(n):
            word |= labels[state] << t
            state = T[state]

        words.append(word)

    return tuple(sorted(set(words)))


def feature_matrix(words, coordinate_count, degree):
    monomials = [
        S
        for d in range(degree + 1)
        for S in combinations(range(coordinate_count), d)
    ]

    matrix = [
        [
            prod((word >> t) & 1 for t in S)
            for S in monomials
        ]
        for word in words
    ]

    return matrix, monomials


def primitive_left_nullvector(matrix):
    transpose = [list(column) for column in zip(*matrix)]
    reduced, pivots = rref(transpose)
    width = len(matrix)
    free = [j for j in range(width) if j not in pivots]

    require(
        len(free) == 1,
        "Expected a one-dimensional quadratic left kernel.",
    )

    chosen = free[0]
    vector = [Fraction(0) for _ in range(width)]
    vector[chosen] = Fraction(1)

    for row, pivot in enumerate(pivots):
        vector[pivot] = -reduced[row][chosen]

    denominator = 1
    for value in vector:
        d = value.denominator
        denominator = denominator * d // gcd(denominator, d)

    integers = [int(value * denominator) for value in vector]

    common = 0
    for value in integers:
        common = gcd(common, abs(value))

    require(common > 0, "Null vector unexpectedly vanished.")
    integers = [value // common for value in integers]

    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]

    for column in transpose:
        require(
            sum(w * value for w, value in zip(integers, column)) == 0,
            "Quadratic annihilation failed.",
        )

    return integers


def check_case(T, expected_words):
    n = len(T)
    labels = (0, 0, 0, 0, 1, 1, 1, 1)

    require(n == 8, "This fixture requires eight states.")
    require(
        all(0 <= image < n for image in T),
        "Transition map is not a total self-map.",
    )

    words = itinerary_words(T, labels)
    require(words == expected_words, "Itinerary words differ.")

    matrices = [
        feature_matrix(words, n, degree)[0]
        for degree in range(4)
    ]

    profile = [exact_rank(matrix) for matrix in matrices]
    require(
        profile == [1, 4, 7, 8],
        "Unexpected exact interpolation profile.",
    )

    weights = primitive_left_nullvector(matrices[2])

    witness = None
    for S in combinations(range(n), 3):
        moment = sum(
            weight * prod((word >> t) & 1 for t in S)
            for weight, word in zip(weights, words)
        )

        if moment:
            witness = {
                "temporal_coordinates": list(S),
                "weighted_sum": moment,
            }
            break

    require(witness is not None, "No cubic witness found.")

    temporal_columns = {
        tuple((word >> t) & 1 for word in words)
        for t in range(n)
    }

    return {
        "T": list(T),
        "observation": list(labels),
        "T_image_size": len(set(T)),
        "distinct_itinerary_count": len(words),
        "itinerary_words": list(words),
        "distinct_temporal_columns": len(temporal_columns),
        "exact_ranks_degrees_0_to_3": profile,
        "quadratic_left_nullvector": weights,
        "cubic_witness": witness,
        "quadratic_annihilation": "PASS",
        "cubic_detection": "PASS",
    }


def main():
    destination = Path(sys.argv[1])
    results = [check_case(T, words) for T, words in CASES]

    report = {
        "status": "PASS",
        "scope": "Three supplied eight-state binary fixtures.",
        "arithmetic": "Exact rational arithmetic using fractions.Fraction.",
        "floating_point_rank_used": False,
        "external_python_packages_required": False,
        "full_census_rerun": False,
        "repository_operations": "NONE",
        "cases": results,
        "limitations": [
            "Does not certify the complete reported 4608-case census.",
            "Does not recreate the original verify10.py or verify13.py.",
            "Does not claim a Lean build, enrollment, or publication.",
        ],
    }

    environment = {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "arithmetic": "fractions.Fraction",
        "dependencies": "Python standard library only",
    }

    (destination / "results.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    (destination / "environment.json").write_text(
        json.dumps(environment, indent=2) + "\n",
        encoding="utf-8",
    )

    for number, result in enumerate(results, 1):
        print(f"CASE={number}")
        print(f"T={tuple(result['T'])}")
        print(f"T_IMAGE_SIZE={result['T_image_size']}")
        print(f"ITINERARY_WORDS={tuple(result['itinerary_words'])}")
        print(
            "EXACT_RANK_PROFILE="
            f"{result['exact_ranks_degrees_0_to_3']}"
        )
        print(
            "QUADRATIC_NULL_VECTOR="
            f"{result['quadratic_left_nullvector']}"
        )
        print(f"CUBIC_WITNESS={result['cubic_witness']}")
        print("CASE_STATUS=PASS")
        print()

    print("EXACT_CASES_CHECKED=3")
    print("QUADRATIC_ANNIHILATION=PASS")
    print("CUBIC_DETECTION=PASS")
    print("FLOATING_POINT_RANK_USED=NO")
    print("FULL_CENSUS_RERUN=NO")
    print("REPOSITORY_OPERATIONS=NONE")
    print("OVERALL_STATUS=PASS")


if __name__ == "__main__":
    main()
