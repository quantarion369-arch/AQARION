#!/usr/bin/env python3

"""
AQARION — SIXBIT independent direction census

Enumerates every 3-dimensional linear subspace of F_2^6.
Computes exact rank over Q of the 22-feature evaluation matrix:
    Phi(x) = (1, x_1,...,x_6, x_i*x_j for i<j)

Then:
  - checks the rank distribution;
  - reconstructs root-swap orbits on rank-8 directions;
  - compares orbit representatives with six canonical bases;
  - computes affine-flat orbit sizes and stabilizer orders.

Standard library only.
No external packages.
"""

from fractions import Fraction
from itertools import combinations
from math import factorial
from hashlib import sha256
from pathlib import Path
import json
import sys
import time
import traceback


ROOT = Path(__file__).resolve().parent
REPORT = ROOT / "SIXBIT_DIRECTION_CENSUS_REPORT.json"

N = 6
FEATURE_COUNT = 22
GROUP_ORDER = 64 * factorial(7)

EXPECTED_RANK_DISTRIBUTION = {
    7: 350,
    8: 1045,
}

CANONICAL_BASES = [
    (0, 7, 25, 30, 42, 45, 51, 52),
    (0, 3, 5, 6, 9, 10, 12, 15),
    (0, 1, 6, 7, 10, 11, 12, 13),
    (0, 3, 5, 6, 24, 27, 29, 30),
    (0, 1, 6, 7, 26, 27, 28, 29),
    (0, 3, 12, 15, 21, 22, 25, 26),
]

EXPECTED_ORBIT_SIZES = [30, 35, 140, 210, 315, 315]

EXPECTED_AFFINE_ORBIT_SIZES = [
    240, 280, 1120, 1680, 2520, 2520
]

EXPECTED_STABILIZER_ORDERS = [
    1344, 1152, 288, 192, 128, 128
]


def feature_row(x):
    """Return the 22 integer-valued degree <= 2 features."""
    bits = [(x >> i) & 1 for i in range(6)]

    row = [1]
    row.extend(bits)

    for i, j in combinations(range(6), 2):
        row.append(bits[i] * bits[j])

    assert len(row) == FEATURE_COUNT
    return row


def exact_rational_rank(matrix):
    """
    Exact Gaussian elimination over Q.
    No floating-point arithmetic is used.
    """
    if not matrix:
        return 0

    A = [
        [Fraction(v) for v in row]
        for row in matrix
    ]

    rows = len(A)
    cols = len(A[0])
    pivot_row = 0

    for col in range(cols):
        pivot = None

        for r in range(pivot_row, rows):
            if A[r][col] != 0:
                pivot = r
                break

        if pivot is None:
            continue

        A[pivot_row], A[pivot] = A[pivot], A[pivot_row]

        p = A[pivot_row][col]

        for j in range(col, cols):
            A[pivot_row][j] /= p

        for r in range(rows):
            if r == pivot_row:
                continue

            q = A[r][col]

            if q == 0:
                continue

            for j in range(col, cols):
                A[r][j] -= q * A[pivot_row][j]

        pivot_row += 1

        if pivot_row == rows:
            break

    return pivot_row


def rref_binary_subspaces():
    """
    Enumerate all 3-dimensional subspaces of F_2^6
    using unique reduced row-echelon basis matrices.

    A binary RREF matrix is determined by:
      - its three pivot columns;
      - its free entries to the right of each pivot,
        excluding the other pivot columns.
    """
    subspaces = set()

    for pivots in combinations(range(6), 3):
        pivot_set = set(pivots)

        free_positions = []

        for i, p in enumerate(pivots):
            for j in range(p + 1, 6):
                if j not in pivot_set:
                    free_positions.append((i, j))

        for mask in range(1 << len(free_positions)):
            rows = [0, 0, 0]

            # Install pivot entries.
            for i, p in enumerate(pivots):
                rows[i] |= 1 << p

            # Install free binary entries.
            for k, (i, j) in enumerate(free_positions):
                if (mask >> k) & 1:
                    rows[i] |= 1 << j

            # Enumerate the eight vectors in the row span.
            points = set()

            for coeff in range(8):
                x = 0

                for i in range(3):
                    if (coeff >> i) & 1:
                        x ^= rows[i]

                points.add(x)

            assert len(points) == 8

            key = tuple(sorted(points))
            subspaces.add(key)

    return sorted(subspaces)


def root_swap(x, j):
    """
    Exact root-swap generator used in the reconciliation source.

    j ranges from 1 through 6.
    """
    bits = [0] + [
        (x >> i) & 1
        for i in range(6)
    ]

    bits[0], bits[j] = bits[j], bits[0]

    y = 0

    for i in range(1, 7):
        y |= (bits[i] ^ bits[0]) << (i - 1)

    return y


def apply_generator(subspace, j):
    return tuple(sorted(
        root_swap(x, j)
        for x in subspace
    ))


def compute_orbits(subspaces):
    """
    Partition the supplied subspaces into orbits under
    the six root swaps.
    """
    universe = set(subspaces)
    unseen = set(subspaces)
    orbits = []

    while unseen:
        seed = min(unseen)
        orbit = {seed}
        stack = [seed]

        while stack:
            current = stack.pop()

            for j in range(1, 7):
                image = apply_generator(current, j)

                if image not in universe:
                    raise AssertionError(
                        "Root-swap action left the subspace universe"
                    )

                if image not in orbit:
                    orbit.add(image)
                    stack.append(image)

        unseen.difference_update(orbit)
        orbits.append(orbit)

    return orbits


def main():
    started = time.time()

    print("=" * 68)
    print("AQARION — SIXBIT INDEPENDENT DIRECTION CENSUS")
    print("=" * 68)
    print("Arithmetic: exact rational")
    print("Dependencies: Python standard library only")
    print()

    # ------------------------------------------------------------
    # Enumerate all linear 3-flats.
    # ------------------------------------------------------------

    print("[1/6] Enumerating all 3-dimensional subspaces of F_2^6 ...")

    all_subspaces = rref_binary_subspaces()

    print("      Enumerated:", len(all_subspaces))

    assert len(all_subspaces) == 1395, (
        "Unexpected subspace count"
    )

    # ------------------------------------------------------------
    # Exact rational feature rank.
    # ------------------------------------------------------------

    print("[2/6] Computing exact rational feature ranks ...")

    rank_by_subspace = {}
    rank_distribution = {}

    for index, subspace in enumerate(all_subspaces, start=1):
        matrix = [
            feature_row(x)
            for x in subspace
        ]

        rank = exact_rational_rank(matrix)

        rank_by_subspace[subspace] = rank
        rank_distribution[rank] = (
            rank_distribution.get(rank, 0) + 1
        )

        if index % 250 == 0:
            print(
                "      Processed:",
                index,
                "/",
                len(all_subspaces)
            )

    rank_distribution = dict(sorted(rank_distribution.items()))

    print("      Rank distribution:", rank_distribution)

    assert rank_distribution == EXPECTED_RANK_DISTRIBUTION, (
        "Rank distribution differs from expected census"
    )

    rank7 = {
        s for s, r in rank_by_subspace.items()
        if r == 7
    }

    rank8 = {
        s for s, r in rank_by_subspace.items()
        if r == 8
    }

    assert len(rank7) == 350
    assert len(rank8) == 1045

    # ------------------------------------------------------------
    # Reconstruct root-swap orbits.
    # ------------------------------------------------------------

    print("[3/6] Reconstructing root-swap orbits ...")

    orbits = compute_orbits(rank8)
    orbits.sort(key=lambda o: (len(o), min(o)))

    orbit_sizes = sorted(len(o) for o in orbits)

    print("      Number of rank-8 orbits:", len(orbits))
    print("      Orbit sizes:", orbit_sizes)

    assert len(orbits) == 6
    assert orbit_sizes == EXPECTED_ORBIT_SIZES

    assert sum(orbit_sizes) == 1045

    # ------------------------------------------------------------
    # Compare the six canonical bases.
    # ------------------------------------------------------------

    print("[4/6] Checking six canonical representatives ...")

    canonical_orbit_sizes = []
    canonical_results = []

    for number, base in enumerate(CANONICAL_BASES, start=1):
        base = tuple(sorted(base))

        assert len(base) == 8
        assert len(set(base)) == 8
        assert all(0 <= x < 64 for x in base)

        matches = [
            orbit for orbit in orbits
            if base in orbit
        ]

        assert len(matches) == 1, (
            "Canonical base does not belong to exactly one orbit: "
            + str(base)
        )

        orbit = matches[0]
        orbit_size = len(orbit)

        canonical_orbit_sizes.append(orbit_size)

        canonical_results.append({
            "canonical_index": number,
            "base": list(base),
            "direction_orbit_size": orbit_size,
            "canonical_base_rank": rank_by_subspace[base],
        })

        print(
            "      Base",
            number,
            "rank =",
            rank_by_subspace[base],
            "orbit size =",
            orbit_size
        )

        assert rank_by_subspace[base] == 8

    assert sorted(canonical_orbit_sizes) == EXPECTED_ORBIT_SIZES

    # ------------------------------------------------------------
    # Affine flats and stabilizer orders.
    # ------------------------------------------------------------

    print("[5/6] Computing affine orbit and stabilizer data ...")

    affine_orbit_sizes = [
        8 * len(orbit)
        for orbit in orbits
    ]

    affine_orbit_sizes.sort()

    stabilizer_orders = sorted(
        GROUP_ORDER // size
        for size in affine_orbit_sizes
    )

    expected_affine = sorted(EXPECTED_AFFINE_ORBIT_SIZES)
    expected_stabilizers = sorted(EXPECTED_STABILIZER_ORDERS)

    print("      Group order:", GROUP_ORDER)
    print("      Affine orbit sizes:", affine_orbit_sizes)
    print("      Stabilizer orders:", stabilizer_orders)

    assert affine_orbit_sizes == expected_affine
    assert stabilizer_orders == expected_stabilizers

    eligible_affine_flats = 8 * len(rank8)
    excluded_affine_flats = 8 * len(rank7)

    assert eligible_affine_flats == 8360
    assert excluded_affine_flats == 2800

    assert sum(affine_orbit_sizes) == eligible_affine_flats

    # ------------------------------------------------------------
    # Final report.
    # ------------------------------------------------------------

    print("[6/6] Writing machine-readable report ...")

    report = {
        "project": "AQARION",
        "audit": "SIXBIT_INDEPENDENT_DIRECTION_CENSUS",
        "arithmetic": "exact rational Gaussian elimination",
        "dependencies": "Python standard library only",
        "dimension": 6,
        "subspace_dimension": 3,
        "feature_dimension": FEATURE_COUNT,
        "total_linear_3_flats": len(all_subspaces),
        "rank_distribution": {
            str(k): v
            for k, v in rank_distribution.items()
        },
        "rank_7_directions": len(rank7),
        "rank_8_directions": len(rank8),
        "root_swap_orbit_count": len(orbits),
        "root_swap_orbit_sizes": orbit_sizes,
        "canonical_bases": canonical_results,
        "affine_group_order": GROUP_ORDER,
        "eligible_affine_3_flats": eligible_affine_flats,
        "excluded_rank_7_affine_flats": excluded_affine_flats,
        "affine_orbit_sizes": affine_orbit_sizes,
        "stabilizer_orders": stabilizer_orders,
        "elapsed_seconds": round(time.time() - started, 6),
        "status": "PASS",
        "scope_limit": (
            "This census does not prove completeness of the six "
            "local 12-point circuit replay generators."
        ),
    }

    encoded = json.dumps(
        report,
        indent=2,
        sort_keys=True
    ) + "\n"

    REPORT.write_text(encoded, encoding="utf-8")

    digest = sha256(
        REPORT.read_bytes()
    ).hexdigest()

    print()
    print("=" * 68)
    print("RESULT")
    print("=" * 68)
    print("All 3-flats:", len(all_subspaces))
    print("Rank distribution:", rank_distribution)
    print("Rank-eight orbits:", orbit_sizes)
    print("Rank-eight directions:", len(rank8))
    print("Eligible affine flats:", eligible_affine_flats)
    print("Excluded rank-seven affine flats:", excluded_affine_flats)
    print("Affine orbit sizes:", affine_orbit_sizes)
    print("Stabilizer orders:", stabilizer_orders)
    print()
    print("REPORT:", REPORT)
    print("REPORT_SHA256:", digest)
    print("ELAPSED_SECONDS:", round(time.time() - started, 3))
    print()
    print("STATUS: PASS")
    print(
        "PROMOTION: NOT AUTHORIZED — local circuit enumeration "
        "completeness remains a separate obligation."
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print()
        print("STATUS: FAIL")
        traceback.print_exc()
        sys.exit(1)
