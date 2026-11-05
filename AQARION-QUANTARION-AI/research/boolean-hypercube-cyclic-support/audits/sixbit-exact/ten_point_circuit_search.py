#!/usr/bin/env python3

import hashlib
import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENSUS = ROOT / "flat_census.json"
RECEIPT = ROOT / "run_receipt.json"
GENERATOR = ROOT / "sixbit_flats.py"
OUTPUT = ROOT / "ten_point_circuit_search.json"

P = 2147483629
N_BITS = 6
N_FEATURES = 22
POINTS = range(64)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def feature_vector(x):
    bits = [(x >> i) & 1 for i in range(N_BITS)]
    return [1] + bits + [
        bits[i] * bits[j]
        for i, j in combinations(range(N_BITS), 2)
    ]


VECTORS = {x: feature_vector(x) for x in POINTS}


def rref_q(matrix):
    a = [[Fraction(v) for v in row] for row in matrix]
    if not a:
        return [], []

    rows = len(a)
    cols = len(a[0])
    pivots = []
    r = 0

    for c in range(cols):
        pivot = next(
            (i for i in range(r, rows) if a[i][c] != 0),
            None
        )
        if pivot is None:
            continue

        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][c]
        a[r] = [v / value for v in a[r]]

        for i in range(rows):
            if i == r:
                continue
            factor = a[i][c]
            if factor:
                a[i] = [
                    a[i][j] - factor * a[r][j]
                    for j in range(cols)
                ]

        pivots.append(c)
        r += 1

        if r == rows:
            break

    return a[:r], pivots


def rank_q(matrix):
    return len(rref_q(matrix)[1])


def quotient_signature(vector, basis, pivots):
    """
    Reduce a row vector modulo the row space of an RREF basis.
    Return a canonical projective representative over Q.
    """
    v = [Fraction(x) for x in vector]

    for row, pivot in zip(basis, pivots):
        factor = v[pivot]
        if factor:
            v = [
                v[j] - factor * row[j]
                for j in range(N_FEATURES)
            ]

    residual = tuple(
        v[j] for j in range(N_FEATURES)
        if j not in pivots
    )

    first = next((x for x in residual if x != 0), None)
    if first is None:
        return None

    return tuple(x / first for x in residual)


def rank_certificate(points):
    return rank_q([VECTORS[x] for x in points])


def main():
    census_hash = sha256(CENSUS)
    receipt = json.loads(RECEIPT.read_text())
    census = json.loads(CENSUS.read_text())

    assert receipt["flat_census_sha256"] == census_hash
    assert receipt["status"] == "COMPUTATION_COMPLETE"
    assert census["flat_count"] == 11160
    assert census["rank_Q_distribution"] == {
        "7": 2800, "8": 8360
    }

    generator_hash = sha256(GENERATOR)
    generator_hash_matches = (
        generator_hash == receipt["script_sha256"]
    )

    flats = [
        item for item in census["flats"]
        if int(item["rank_Q"]) == 8
    ]

    assert len(flats) == 8360

    candidate_count = 0
    circuit_count = 0
    failed_deletion_count = 0
    circuits = []
    deletion_failure_histogram = {}

    for flat_index, item in enumerate(flats, 1):
        base = tuple(sorted(int(x) for x in item["points"]))
        base_set = set(base)

        rows = [VECTORS[x] for x in base]
        basis, pivots = rref_q(rows)

        if len(basis) != 8:
            raise RuntimeError(
                f"Unexpected base rank: flat {item['flat_id']}"
            )

        groups = defaultdict(list)

        for x in POINTS:
            if x in base_set:
                continue

            signature = quotient_signature(
                VECTORS[x], basis, pivots
            )

            if signature is not None:
                groups[signature].append(x)

        for group in groups.values():
            if len(group) < 2:
                continue

            for x, y in combinations(sorted(group), 2):
                candidate_count += 1
                ten = tuple(sorted(base + (x, y)))

                full_rank = rank_certificate(ten)

                deletion_ranks = [
                    rank_certificate(ten[:i] + ten[i+1:])
                    for i in range(10)
                ]

                passed = (
                    full_rank == 9
                    and all(r == 9 for r in deletion_ranks)
                )

                if passed:
                    circuit_count += 1
                    circuits.append({
                        "flat_id": int(item["flat_id"]),
                        "direction_id": int(item["direction_id"]),
                        "points": list(ten),
                        "full_rank_Q": full_rank,
                        "deletion_ranks_Q": deletion_ranks,
                        "circuit_verified": True
                    })
                else:
                    failed_deletion_count += 1
                    key = str(tuple(deletion_ranks))
                    deletion_failure_histogram[key] = (
                        deletion_failure_histogram.get(key, 0) + 1
                    )

        if flat_index % 500 == 0:
            print(
                f"Processed {flat_index}/{len(flats)} "
                f"rank-eight flats; "
                f"candidates={candidate_count}; "
                f"circuits={circuit_count}"
            )

    result = {
        "title": "AQARION exact ten-point circuit search",
        "method": "Exact rational quotient signatures and deletion-rank certification",
        "census_sha256": census_hash,
        "receipt_generator_sha256": receipt["script_sha256"],
        "actual_generator_sha256": generator_hash,
        "generator_hash_matches_receipt": generator_hash_matches,
        "rank_eight_flats_processed": len(flats),
        "candidate_pair_count": candidate_count,
        "failed_candidate_count": failed_deletion_count,
        "verified_circuit_count": circuit_count,
        "deletion_failure_histogram": deletion_failure_histogram,
        "circuit_criterion": {
            "full_ten_point_rank": 9,
            "all_ten_deletion_ranks": 9
        },
        "circuits": circuits,
        "status": (
            "CIRCUITS_VERIFIED" if circuit_count else
            "NO_CIRCUIT_FOUND"
        )
    }

    OUTPUT.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    print("\n===== EXACT CIRCUIT SEARCH SUMMARY =====")
    print("Generator hash matches receipt:", generator_hash_matches)
    print("Rank-eight flats:", len(flats))
    print("Candidate pairs:", candidate_count)
    print("Failed candidates:", failed_deletion_count)
    print("Verified circuits:", circuit_count)
    print("Result:", result["status"])
    print("Output:", OUTPUT)


if __name__ == "__main__":
    main()
