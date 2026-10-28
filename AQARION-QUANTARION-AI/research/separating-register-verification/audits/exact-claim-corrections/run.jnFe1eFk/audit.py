import json
from fractions import Fraction
from itertools import combinations
from math import comb, prod
from pathlib import Path
import sys


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def words_of(T, h, L):
    out = []
    for start in range(len(T)):
        x = start
        row = []
        for _ in range(L):
            row.append(h[x])
            x = T[x]
        out.append(tuple(row))
    return out


def rank_columns(columns, n):
    basis = {}

    for column in columns:
        vector = list(map(Fraction, column))

        for pivot, row in sorted(basis.items()):
            coefficient = vector[pivot]
            if coefficient:
                vector = [
                    x - coefficient*y
                    for x, y in zip(vector, row)
                ]

        pivot = next(
            (i for i, value in enumerate(vector) if value),
            None,
        )

        if pivot is not None:
            coefficient = vector[pivot]
            basis[pivot] = [
                value/coefficient for value in vector
            ]

        if len(basis) == n:
            break

    return len(basis)


def profile(points, maximum):
    points = sorted(set(points))
    n = len(points)

    # Identical Boolean observables can be deduplicated:
    # powers reduce by b*b=b.
    observations = list(dict.fromkeys(zip(*points)))
    result = []

    for k in range(maximum + 1):
        features = []

        for degree in range(min(k, len(observations)) + 1):
            for S in combinations(range(len(observations)), degree):
                features.append(tuple(
                    prod(observations[t][x] for t in S)
                    for x in range(n)
                ))

        result.append(
            rank_columns(dict.fromkeys(features), n)
        )

    return result


def determinant(matrix):
    A = [
        [Fraction(value) for value in row]
        for row in matrix
    ]
    n = len(A)
    answer = Fraction(1)

    for column in range(n):
        pivot = next(
            (r for r in range(column, n) if A[r][column]),
            None,
        )

        if pivot is None:
            return Fraction(0)

        if pivot != column:
            A[column], A[pivot] = A[pivot], A[column]
            answer = -answer

        value = A[column][column]
        answer *= value

        for r in range(column + 1, n):
            factor = A[r][column]/value
            for j in range(column, n):
                A[r][j] -= factor*A[column][j]

    return answer


def witness(points, monomials):
    points = sorted(set(points))
    matrix = [
        [
            prod(row[t] for t in S)
            for S in monomials
        ]
        for row in points
    ]
    return determinant(matrix)


def main(out):
    T = [1,2,3,4,5,6,7,0]
    h = [0,0,0,0,1,1,1,1]

    rows = words_of(T, h, 8)
    prefixes = [row[:3] for row in rows]

    full_profile = profile(rows, 3)
    prefix_profile = profile(prefixes, 3)

    require(
        full_profile == [1,5,8,8],
        "Full profile mismatch",
    )
    require(
        prefix_profile == [1,4,6,6],
        "Prefix profile mismatch",
    )

    full_columns = [
        (), (0,), (1,), (2,), (3,),
        (0,1), (0,2), (0,3),
    ]
    prefix_columns = [
        (), (0,), (1,), (2,), (0,1), (0,2),
    ]

    full_det = witness(rows, full_columns)
    prefix_det = witness(prefixes, prefix_columns)

    require(
        full_det == 1,
        "Expected full determinant +1",
    )
    require(
        prefix_det == -1,
        "Expected prefix determinant -1",
    )

    seen = {}
    collisions = []

    for x, prefix in enumerate(prefixes):
        if prefix in seen:
            collisions.append([
                seen[prefix], x, list(prefix)
            ])
        else:
            seen[prefix] = x

    require(
        collisions == [
            [0,1,[0,0,0]],
            [4,5,[1,1,1]],
        ],
        "Prefix collision mismatch",
    )

    and_results = []

    for d in range(2, 6):
        n = 1 << d

        # Application convention: MSB-first initial coordinates.
        transition = [
            ((x << 1) & (n - 1)) | int(x == n - 1)
            for x in range(n)
        ]
        labels = [
            x >> (d - 1) for x in range(n)
        ]

        actual = profile(
            words_of(transition, labels, n), d
        )

        expected = (
            [1]
            + [
                sum(comb(d, j) for j in range(k + 1)) + 1
                for k in range(1, d)
            ]
            + [n]
        )

        require(
            actual == expected,
            "Piecewise AND profile mismatch",
        )

        and_results.append({
            "d": d,
            "computed": actual,
            "expected": expected,
        })

        print(
            f"AND_d={d} PROFILE={actual} PASS",
            flush=True,
        )

    report = {
        "status": "PASS",
        "scope": (
            "Small exact claim-correction audit only. "
            "No register, necklace, or spectral-support census."
        ),
        "arithmetic": (
            "Python integers and fractions.Fraction. "
            "No NumPy, floating ranks, or Gram matrices."
        ),
        "full_itinerary_profile": full_profile,
        "prefix_profile": prefix_profile,
        "prefix_collisions": collisions,
        "full_witness_columns": [
            list(S) for S in full_columns
        ],
        "full_witness_determinant": str(full_det),
        "prefix_witness_columns": [
            list(S) for S in prefix_columns
        ],
        "prefix_witness_determinant": str(prefix_det),
        "row_order": (
            "Lexicographically sorted distinct itinerary tuples"
        ),
        "AND_profiles": and_results,
        "application_sources_modified": False,
        "git_stage_commit_push": "NONE",
    }

    result_path = out / "results.json"
    result_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    require(
        json.loads(result_path.read_text()) == report,
        "Saved JSON read-back mismatch",
    )

    print("FULL_PROFILE=" + str(full_profile))
    print("PREFIX_PROFILE=" + str(prefix_profile))
    print("FULL_WITNESS_DETERMINANT=" + str(full_det))
    print("PREFIX_WITNESS_DETERMINANT=" + str(prefix_det))
    print("CLAIM_DETERMINANT_8192=REJECTED_FOR_THIS_MATRIX")
    print("AND_DEGREE_ZERO=1")
    print("SAVED_JSON_READBACK=PASS")
    print("NUMPY_REQUIRED=NO")
    print("FULL_CENSUS_RERUN=NO")
    print("GIT_STAGE_COMMIT_PUSH=NONE")
    print("OVERALL_STATUS=PASS")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
