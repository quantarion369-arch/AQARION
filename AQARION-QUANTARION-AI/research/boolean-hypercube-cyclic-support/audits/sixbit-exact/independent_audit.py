#!/usr/bin/env python3
"""Independent six-bit affine-flat census audit.

Uses:
- independent GF(2) RREF and span reconstruction
- direct affine-coset reconstruction
- Fraction-based Gaussian elimination over Q
- independent modular Gaussian elimination

Does not import or call sixbit_flats.py.
"""

import hashlib
import json
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CENSUS_PATH = ROOT / "flat_census.json"
RECEIPT_PATH = ROOT / "run_receipt.json"

N_BITS = 6
POINT_COUNT = 64
FLAT_SIZE = 8
FEATURE_COUNT = 22
PRIME = 2147483629

checks = {}
errors = []


def record(name, passed, detail=""):
    checks[name] = bool(passed)
    print(f"{'PASS' if passed else 'FAIL'} {name}" +
          (f": {detail}" if detail else ""))
    if not passed:
        errors.append(name)


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def gf2_rref(rows):
    """Canonical reduced row-echelon basis; bit i is coordinate i."""
    a = [int(x) for x in rows]
    pivot_row = 0

    for col in range(N_BITS):
        pivot = next(
            (r for r in range(pivot_row, len(a))
             if (a[r] >> col) & 1),
            None
        )
        if pivot is None:
            continue

        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]

        for r in range(len(a)):
            if r != pivot_row and ((a[r] >> col) & 1):
                a[r] ^= a[pivot_row]

        pivot_row += 1
        if pivot_row == len(a):
            break

    return [x for x in a if x != 0]


def span_of_basis(basis):
    span = {0}
    for b in basis:
        span |= {x ^ b for x in tuple(span)}
    return span


def feature_vector(x):
    """Constant, x_0..x_5, then x_i*x_j for i<j."""
    bits = [(x >> i) & 1 for i in range(N_BITS)]
    out = [1] + bits
    out.extend(
        bits[i] * bits[j]
        for i, j in combinations(range(N_BITS), 2)
    )
    return out


def rank_over_q(matrix):
    """Independent exact Gaussian elimination over Fraction."""
    a = [[Fraction(v) for v in row] for row in matrix]
    nrows = len(a)
    ncols = len(a[0]) if a else 0
    rank = 0

    for col in range(ncols):
        pivot = next(
            (r for r in range(rank, nrows) if a[r][col] != 0),
            None
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        pivot_value = a[rank][col]

        # Normalize pivot row.
        a[rank] = [v / pivot_value for v in a[rank]]

        # Eliminate below.
        for r in range(rank + 1, nrows):
            factor = a[r][col]
            if factor:
                a[r] = [
                    a[r][j] - factor * a[rank][j]
                    for j in range(ncols)
                ]

        rank += 1
        if rank == nrows:
            break

    return rank


def rank_mod_p(matrix, p):
    """Independent Gaussian elimination over F_p."""
    a = [[int(v) % p for v in row] for row in matrix]
    nrows = len(a)
    ncols = len(a[0]) if a else 0
    rank = 0

    for col in range(ncols):
        pivot = next(
            (r for r in range(rank, nrows) if a[r][col] != 0),
            None
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], p - 2, p)
        a[rank] = [(v * inv) % p for v in a[rank]]

        for r in range(rank + 1, nrows):
            factor = a[r][col]
            if factor:
                a[r] = [
                    (a[r][j] - factor * a[rank][j]) % p
                    for j in range(ncols)
                ]

        rank += 1
        if rank == nrows:
            break

    return rank


def main():
    census_hash = sha256(CENSUS_PATH)
    receipt = json.loads(RECEIPT_PATH.read_text())
    census = json.loads(CENSUS_PATH.read_text())

    record(
        "receipt_census_hash",
        receipt.get("flat_census_sha256") == census_hash,
        census_hash
    )

    record(
        "schema_constants",
        census.get("dimension") == 6
        and census.get("point_count") == 64
        and census.get("flat_dimension") == 3
        and census.get("flat_size") == 8
        and census.get("feature_count") == 22
        and census.get("field") == "Q"
        and census.get("bit_convention") == "x_i = (x >> i) & 1"
    )

    flats = census.get("flats")
    record(
        "flat_list_length",
        isinstance(flats, list) and len(flats) == 11160,
        f"observed {len(flats) if isinstance(flats, list) else 'invalid'}"
    )
    if not isinstance(flats, list):
        raise SystemExit("Cannot continue: flats is not a list")

    # Reconstruct every direction and group its flats.
    directions = {}
    direction_flats = defaultdict(list)
    flat_ids = []

    malformed = False
    for item in flats:
        try:
            did = int(item["direction_id"])
            basis = [int(x) for x in item["direction_rref"]]
            points = [int(x) for x in item["points"]]
            rep = int(item["coset_representative"])
            flat_id = int(item["flat_id"])
        except (KeyError, TypeError, ValueError):
            malformed = True
            continue

        flat_ids.append(flat_id)
        direction_flats[did].append(item)

        if did in directions and directions[did] != basis:
            malformed = True
        directions[did] = basis

        if len(points) != FLAT_SIZE or len(set(points)) != FLAT_SIZE:
            malformed = True
        if any(x < 0 or x >= POINT_COUNT for x in points):
            malformed = True
        if rep < 0 or rep >= POINT_COUNT:
            malformed = True

    record("flat_records_well_formed", not malformed)

    record(
        "flat_ids_unique_and_complete",
        sorted(flat_ids) == list(range(11160)),
        f"unique IDs = {len(set(flat_ids))}"
    )

    record(
        "direction_count",
        len(directions) == 1395,
        f"observed {len(directions)}"
    )

    # Check each stored direction is a canonical rank-three GF(2) basis.
    canonical_directions = set()
    direction_basis_ok = True
    direction_span_ok = True
    coset_partition_ok = True
    flat_geometry_ok = True

    for did, basis in directions.items():
        canonical = gf2_rref(basis)
        if len(basis) != 3 or canonical != basis:
            direction_basis_ok = False

        if len(canonical) != 3:
            direction_span_ok = False
            continue

        canonical_directions.add(tuple(canonical))
        span = span_of_basis(canonical)

        if len(span) != 8:
            direction_span_ok = False
            continue

        entries = direction_flats[did]
        if len(entries) != 8:
            coset_partition_ok = False
            continue

        covered = []
        coset_keys = set()

        for item in entries:
            rep = int(item["coset_representative"])
            expected = {rep ^ v for v in span}
            actual = set(int(x) for x in item["points"])

            if actual != expected:
                flat_geometry_ok = False

            coset_key = min(expected)
            coset_keys.add(coset_key)
            covered.extend(actual)

        if len(coset_keys) != 8:
            coset_partition_ok = False
        if len(covered) != 64 or set(covered) != set(range(64)):
            coset_partition_ok = False

    record(
        "direction_bases_are_canonical_rref",
        direction_basis_ok
    )
    record(
        "direction_spans_have_eight_points",
        direction_span_ok
    )
    record(
        "directions_are_distinct",
        len(canonical_directions) == 1395,
        f"distinct canonical bases = {len(canonical_directions)}"
    )
    record(
        "eight_cosets_partition_each_direction",
        coset_partition_ok
    )
    record(
        "stored_flats_match_reconstructed_cosets",
        flat_geometry_ok
    )

    # Check global uniqueness of all affine flats.
    flat_supports = []
    for item in flats:
        flat_supports.append(tuple(sorted(int(x) for x in item["points"])))

    record(
        "all_affine_flat_supports_unique",
        len(set(flat_supports)) == 11160,
        f"unique supports = {len(set(flat_supports))}"
    )

    # Independently reconstruct all 22-feature rows and exact ranks.
    q_counts = Counter()
    p_counts = Counter()
    q_mismatches = []
    p_mismatches = []
    feature_shape_ok = True

    for index, item in enumerate(flats):
        points = [int(x) for x in item["points"]]
        matrix = [feature_vector(x) for x in points]

        if any(len(row) != FEATURE_COUNT for row in matrix):
            feature_shape_ok = False
            continue

        rq = rank_over_q(matrix)
        rp = rank_mod_p(matrix, PRIME)

        q_counts[rq] += 1
        p_counts[rp] += 1

        if rq != int(item["rank_Q"]):
            q_mismatches.append((item["flat_id"], rq, item["rank_Q"]))

        if rp != int(item["rank_Fp"]):
            p_mismatches.append((item["flat_id"], rp, item["rank_Fp"]))

        if (index + 1) % 1000 == 0:
            print(f"rank audit progress: {index + 1}/{len(flats)}")

    record("feature_matrix_has_22_columns", feature_shape_ok)
    record(
        "all_exact_rational_ranks_match",
        not q_mismatches,
        f"mismatches = {len(q_mismatches)}"
    )
    record(
        "all_modular_ranks_match",
        not p_mismatches,
        f"mismatches = {len(p_mismatches)}"
    )

    expected_q = {"7": 2800, "8": 8360}
    expected_p = {"7": 2800, "8": 8360}

    q_distribution = {str(k): q_counts[k] for k in sorted(q_counts)}
    p_distribution = {str(k): p_counts[k] for k in sorted(p_counts)}

    record(
        "independent_rational_distribution",
        q_distribution == expected_q,
        str(q_distribution)
    )
    record(
        "independent_modular_distribution",
        p_distribution == expected_p,
        str(p_distribution)
    )

    record(
        "receipt_summary_matches_independent_results",
        receipt.get("rank_Q_distribution") == expected_q
        and receipt.get("rank_Fp_distribution") == expected_p
        and receipt.get("modular_rank_exception_count") == 0
    )

    report = {
        "audit": "independent six-bit affine-flat census audit",
        "method": "Fraction Gaussian elimination; independently reconstructed GF(2) directions and cosets",
        "census_sha256": census_hash,
        "flat_count": len(flats),
        "direction_count": len(directions),
        "rational_rank_distribution": q_distribution,
        "modular_rank_distribution": p_distribution,
        "rational_rank_mismatch_count": len(q_mismatches),
        "modular_rank_mismatch_count": len(p_mismatches),
        "checks": checks,
        "failed_checks": errors,
        "result": "PASS" if all(checks.values()) else "FAIL"
    }

    report_path = ROOT / "independent_audit_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    print("\n===== INDEPENDENT AUDIT SUMMARY =====")
    print("rational rank distribution:", q_distribution)
    print("modular rank distribution:", p_distribution)
    print("rational rank mismatches:", len(q_mismatches))
    print("modular rank mismatches:", len(p_mismatches))
    print("failed checks:", errors)
    print("result:", report["result"])
    print("report:", report_path)

    if errors:
        if q_mismatches:
            print("first rational mismatches:", q_mismatches[:10])
        if p_mismatches:
            print("first modular mismatches:", p_mismatches[:10])
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
