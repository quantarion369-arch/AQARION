#!/usr/bin/env python3
"""Exact iterated Koopman closure-profile auditor.

This module computes the closure sequence

    W_{j+1} = W_j + K(W_j)

for a finite deterministic map T and an arbitrary initial observable
basis. It uses exact rational arithmetic only.

The Koopman convention is the pullback convention:

    (K f)(x) = f(T(x)).

The stage-wise defect operator is

    D_j = (I - P_j) K P_j,

where P_j is the orthogonal projection onto W_j. Its rank equals the
dimension increment

    delta_j = dim(W_{j+1}) - dim(W_j).

The total unrestricted linear repair cost is

    dim(W_infinity) - dim(W_0) = sum_j delta_j.
"""

from fractions import Fraction


def validate_transition(T):
    """Validate that T is a total map on {0,...,n-1}."""
    T = list(T)
    n = len(T)

    if n == 0:
        raise ValueError("state space must be nonempty")

    for target in T:
        if not isinstance(target, int) or target < 0 or target >= n:
            raise ValueError(
                "T must map {0,...,n-1} into itself"
            )

    return T


def validate_basis(T, initial_basis):
    """Validate an initial observable basis given as column vectors."""
    n = len(T)

    if not initial_basis:
        raise ValueError("initial_basis must be nonempty")

    columns = []
    for column in initial_basis:
        if len(column) != n:
            raise ValueError(
                "each observable column must have length n"
            )
        columns.append([Fraction(value) for value in column])

    return columns


def koopman_matrix(T):
    """Construct the pullback Koopman matrix for T."""
    n = len(T)
    return [
        [
            Fraction(int(T[x] == y))
            for y in range(n)
        ]
        for x in range(n)
    ]


def koopman_apply_column(T, column):
    """Apply the pullback Koopman operator to one observable column."""
    return [column[T[x]] for x in range(len(T))]


def columns_to_matrix(columns):
    """Convert a list of column vectors into a row-major matrix."""
    if not columns:
        return []

    n = len(columns[0])

    if any(len(column) != n for column in columns):
        raise ValueError("all observable columns must have equal length")

    return [
        [column[x] for column in columns]
        for x in range(n)
    ]


def matmul(A, B):
    """Exact matrix multiplication."""
    return [
        [
            sum(A[i][r] * B[r][j] for r in range(len(B)))
            for j in range(len(B[0]))
        ]
        for i in range(len(A))
    ]


def rank_q(matrix):
    """Exact rank over Q by Gauss-Jordan elimination."""
    A = [
        [Fraction(value) for value in row]
        for row in matrix
    ]

    if not A:
        return 0

    rows = len(A)
    cols = len(A[0])
    pivot_row = 0

    for col in range(cols):
        pivot = None

        for row in range(pivot_row, rows):
            if A[row][col] != 0:
                pivot = row
                break

        if pivot is None:
            continue

        A[pivot_row], A[pivot] = A[pivot], A[pivot_row]

        pivot_value = A[pivot_row][col]
        A[pivot_row] = [
            value / pivot_value
            for value in A[pivot_row]
        ]

        for row in range(rows):
            if row == pivot_row or A[row][col] == 0:
                continue

            factor = A[row][col]
            A[row] = [
                value - factor * pivot_value2
                for value, pivot_value2 in zip(
                    A[row],
                    A[pivot_row],
                )
            ]

        pivot_row += 1

        if pivot_row == rows:
            break

    return pivot_row


def orthogonal_projection_from_columns(columns):
    """Exact orthogonal projection onto the span of column vectors."""
    n = len(columns[0])

    projection = [
        [Fraction(0) for _ in range(n)]
        for _ in range(n)
    ]

    orthogonal_basis = []

    for vector in columns:
        vector = [Fraction(value) for value in vector]

        for basis_vector in orthogonal_basis:
            dot_product = sum(
                left * right
                for left, right in zip(vector, basis_vector)
            )
            vector = [
                left - dot_product * right
                for left, right in zip(vector, basis_vector)
            ]

        norm_squared = sum(
            value * value
            for value in vector
        )

        if norm_squared == 0:
            continue

        orthogonal_basis.append(vector)

        for x in range(n):
            for y in range(n):
                projection[x][y] += (
                    vector[x] * vector[y] / norm_squared
                )

    return projection


def closure_profile(T, initial_basis):
    """Compute the exact iterated Koopman closure profile.

    Parameters
    ----------
    T : sequence of int
        Total map on {0,...,n-1}.
    initial_basis : sequence of sequences
        Initial observable basis, supplied as column vectors.

    Returns
    -------
    dict
        Exact closure profile, defect ranks, checks, and total cost.
    """
    T = validate_transition(T)
    columns = validate_basis(T, initial_basis)

    K = koopman_matrix(T)

    dimensions = [rank_q(columns_to_matrix(columns))]
    increments = []
    defect_ranks = []

    for stage in range(len(T) + 1):
        projection = orthogonal_projection_from_columns(columns)

        identity_minus_projection = [
            [
                Fraction(int(x == y)) - projection[x][y]
                for y in range(len(T))
            ]
            for x in range(len(T))
        ]

        defect = matmul(
            identity_minus_projection,
            matmul(K, projection),
        )

        defect_ranks.append(rank_q(defect))

        image_columns = [
            koopman_apply_column(T, column)
            for column in columns
        ]

        enlarged_columns = columns + image_columns
        enlarged_dimension = rank_q(
            columns_to_matrix(enlarged_columns)
        )

        increment = enlarged_dimension - dimensions[-1]

        increments.append(increment)
        dimensions.append(enlarged_dimension)

        if increment == 0:
            break

        columns = enlarged_columns

    stabilization_stage = len(increments) - 1
    total_linear_repair_cost = dimensions[-1] - dimensions[0]

    checks = {
        "increment_identity": all(
            defect_ranks[index] == increments[index]
            for index in range(len(increments))
        ),
        "monotonicity": all(
            increments[index + 1] <= increments[index]
            for index in range(len(increments) - 1)
        ),
        "telescoping_sum": (
            total_linear_repair_cost == sum(increments)
        ),
    }

    return {
        "schema": "AQ-DEFECT-CLOSURE-PROFILE/1",
        "state_count": len(T),
        "initial_dimension": dimensions[0],
        "final_dimension": dimensions[-1],
        "profile": increments,
        "defect_ranks": defect_ranks,
        "stabilization_stage": stabilization_stage,
        "total_linear_repair_cost": total_linear_repair_cost,
        "checks": checks,
        "result": (
            "PASS"
            if all(checks.values())
            else "FAIL"
        ),
    }


def main():
    """Minimal demonstration using the four-state leakage fixture."""
    T = [1, 2, 3, 3]
    initial_basis = [
        [1, 1, 1, 1],
        [0, 0, 0, 1],
    ]

    result = closure_profile(T, initial_basis)

    import json

    print(json.dumps(result, indent=2, sort_keys=True))

    if result["result"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
