#!/usr/bin/env python3

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENSUS = ROOT / "flat_census.json"
SEARCH = ROOT / "ten_point_circuit_search.json"
OUTPUT = ROOT / "independent_circuit_audit_report.json"


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def feature_vector(x):
    bits = [(x >> i) & 1 for i in range(6)]
    return [1] + bits + [
        bits[i] * bits[j]
        for i, j in combinations(range(6), 2)
    ]


VECTORS = {x: feature_vector(x) for x in range(64)}


def bareiss_rank(matrix):
    """Exact integer rank using fraction-free Bareiss elimination."""
    if not matrix:
        return 0

    a = [list(map(int, row)) for row in matrix]
    m, n = len(a), len(a[0])
    previous_pivot = 1
    rank = 0

    for col in range(n):
        pivot_row = next(
            (i for i in range(rank, m) if a[i][col] != 0),
            None
        )
        if pivot_row is None:
            continue

        if pivot_row != rank:
            a[rank], a[pivot_row] = a[pivot_row], a[rank]

        pivot = a[rank][col]

        for i in range(rank + 1, m):
            factor = a[i][col]
            for j in range(col + 1, n):
                numerator = (
                    a[i][j] * pivot
                    - factor * a[rank][j]
                )
                if numerator % previous_pivot != 0:
                    raise ArithmeticError(
                        "Bareiss exact-division invariant failed"
                    )
                a[i][j] = numerator // previous_pivot
            a[i][col] = 0

        previous_pivot = pivot
        rank += 1

        if rank == m:
            break

    return rank


def matrix(points):
    return [VECTORS[x] for x in points]


def main():
    census = json.loads(CENSUS.read_text())
    search = json.loads(SEARCH.read_text())

    flats = {
        int(item["flat_id"]): item
        for item in census["flats"]
    }

    circuits = search["circuits"]

    geometry_errors = []
    rank_errors = []
    supports = []
    deletion_histogram = Counter()

    for index, circuit in enumerate(circuits, 1):
        points = tuple(circuit["points"])
        support = tuple(sorted(points))
        supports.append(support)

        if (
            len(points) != 10
            or len(set(points)) != 10
            or any(x not in VECTORS for x in points)
        ):
            geometry_errors.append((index, "invalid ten-point support"))
            continue

        flat_id = int(circuit["flat_id"])
        flat = flats.get(flat_id)

        if flat is None:
            geometry_errors.append((index, "unknown flat ID"))
            continue

        base = set(map(int, flat["points"]))
        support_set = set(points)

        if (
            len(base) != 8
            or not base.issubset(support_set)
            or len(support_set - base) != 2
            or int(flat["rank_Q"]) != 8
            or int(flat["direction_id"]) != int(circuit["direction_id"])
        ):
            geometry_errors.append((index, "flat containment mismatch"))
            continue

        full_rank = bareiss_rank(matrix(points))
        deletion_ranks = [
            bareiss_rank(matrix(points[:i] + points[i+1:]))
            for i in range(10)
        ]

        deletion_histogram[str(tuple(deletion_ranks))] += 1

        if full_rank != 9 or any(r != 9 for r in deletion_ranks):
            rank_errors.append({
                "index": index,
                "full_rank": full_rank,
                "deletion_ranks": deletion_ranks
            })

        if index % 1000 == 0:
            print(f"Independently checked {index}/{len(circuits)}")

    unique_supports = len(set(supports))

    report = {
        "title": "Independent exact ten-point circuit certificate audit",
        "method": "Fraction-free Bareiss integer elimination",
        "census_sha256": sha256(CENSUS),
        "search_result_sha256": sha256(SEARCH),
        "circuit_occurrences_checked": len(circuits),
        "unique_support_count": unique_supports,
        "geometry_error_count": len(geometry_errors),
        "rank_error_count": len(rank_errors),
        "deletion_rank_histogram": dict(deletion_histogram),
        "geometry_errors_first_20": geometry_errors[:20],
        "rank_errors_first_20": rank_errors[:20],
        "result": (
            "PASS"
            if (
                len(circuits) == 22400
                and unique_supports == 22400
                and not geometry_errors
                and not rank_errors
            )
            else "FAIL"
        )
    }

    OUTPUT.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n"
    )

    print("\n===== INDEPENDENT CIRCUIT AUDIT =====")
    print("Occurrences checked:", len(circuits))
    print("Unique supports:", unique_supports)
    print("Geometry errors:", len(geometry_errors))
    print("Rank errors:", len(rank_errors))
    print("Deletion rank histogram:", dict(deletion_histogram))
    print("RESULT:", report["result"])
    print("REPORT:", OUTPUT)


if __name__ == "__main__":
    main()
