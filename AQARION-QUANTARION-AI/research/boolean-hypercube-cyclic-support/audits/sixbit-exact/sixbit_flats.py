
#!/usr/bin/env python3
"""
AQARION six-bit exact affine 3-flat census.

Scope:
  - Enumerate all 3-dimensional linear subspaces of F_2^6.
  - Enumerate all affine cosets of each direction space.
  - Construct the 22-coordinate degree <= 2 evaluation matrix.
  - Compute exact rank over Q and rank over one verified prime field.
  - Preserve every flat and its rank data.

No outside-pair scan is performed.

Feature order:
  constant, six linear coordinates, fifteen quadratic products.

Bit convention:
  x_i = (x >> i) & 1, for i = 0,...,5.
"""

import hashlib
import itertools
import json
import math
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

N_BITS = 6
N_POINTS = 1 << N_BITS
FLAT_DIM = 3
FLAT_SIZE = 1 << FLAT_DIM
N_FEATURES = 1 + N_BITS + math.comb(N_BITS, 2)

PRIME = 2147483629

EXPECTED_DIRECTIONS = 1395
EXPECTED_FLATS = 11160
RANK_EIGHT_TARGET = 8360


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def is_prime_64(n):
    """Deterministic Miller-Rabin for unsigned 64-bit integers."""
    if n < 2:
        return False

    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    bases = (
        2, 325, 9375, 28178,
        450775, 9780504, 1795265022
    )

    for a in bases:
        if a % n == 0:
            continue

        x = pow(a, d, n)
        if x in (1, n - 1):
            continue

        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False

    return True


def gf2_rref(rows, width=N_BITS):
    """Return canonical RREF of a binary row space."""
    a = list(rows)
    pivot_row = 0

    for col in range(width):
        bit = 1 << col
        pivot = next(
            (i for i in range(pivot_row, len(a))
             if a[i] & bit),
            None
        )

        if pivot is None:
            continue

        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]

        for i in range(len(a)):
            if i != pivot_row and (a[i] & bit):
                a[i] ^= a[pivot_row]

        pivot_row += 1
        if pivot_row == len(a):
            break

    return tuple(a[:pivot_row])


def generate_directions():
    """
    Generate every 3-dimensional subspace exactly once.

    Every rank-three set of three vectors generates one row space.
    Canonical RREF keys remove basis duplication.
    """
    directions = set()

    for triple in itertools.combinations(range(N_POINTS), FLAT_DIM):
        rref = gf2_rref(triple)
        if len(rref) == FLAT_DIM:
            directions.add(rref)

    return sorted(directions)


def generate_span(basis):
    """Generate all 2^3 vectors in the direction space."""
    span = [0]

    for b in basis:
        span += [x ^ b for x in span]

    return tuple(sorted(span))


def generate_cosets(span):
    """Return canonical representatives and their affine cosets."""
    unseen = set(range(N_POINTS))
    result = []

    while unseen:
        representative = min(unseen)
        points = tuple(sorted(representative ^ v for v in span))

        if len(points) != FLAT_SIZE:
            raise RuntimeError("Incorrect affine coset size")

        if not set(points).issubset(unseen):
            raise RuntimeError("Affine cosets overlap")

        unseen.difference_update(points)
        result.append((representative, points))

    if unseen:
        raise RuntimeError("Affine coset coverage failure")

    return result


def feature_vector(x):
    """Integer evaluation row in the specified feature order."""
    bits = [(x >> i) & 1 for i in range(N_BITS)]

    row = [1]
    row.extend(bits)

    for i in range(N_BITS):
        for j in range(i + 1, N_BITS):
            row.append(bits[i] * bits[j])

    if len(row) != N_FEATURES:
        raise RuntimeError("Feature dimension mismatch")

    return row


def exact_rank_integer(matrix):
    """
    Exact rank over Q using integer-only elimination.

    At each pivot:
      row_i <- pivot * row_i - factor * pivot_row

    Dividing each resulting row by its gcd preserves its rational
    row space and limits integer growth.
    """
    a = [list(map(int, row)) for row in matrix]

    if not a:
        return 0

    nrows = len(a)
    ncols = len(a[0])

    if any(len(row) != ncols for row in a):
        raise ValueError("Ragged matrix")

    rank = 0

    for col in range(ncols):
        pivot = next(
            (i for i in range(rank, nrows) if a[i][col] != 0),
            None
        )

        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        g = 0
        for value in a[rank]:
            g = math.gcd(g, abs(value))

        if g > 1:
            a[rank] = [v // g for v in a[rank]]

        if a[rank][col] < 0:
            a[rank] = [-v for v in a[rank]]

        pivot_value = a[rank][col]
        pivot_row = a[rank][:]

        for i in range(rank + 1, nrows):
            factor = a[i][col]

            if factor == 0:
                continue

            a[i] = [
                pivot_value * a[i][j] - factor * pivot_row[j]
                for j in range(ncols)
            ]

            g = 0
            for value in a[i]:
                g = math.gcd(g, abs(value))

            if g > 1:
                a[i] = [v // g for v in a[i]]

        rank += 1

        if rank == nrows:
            break

    return rank


def rank_mod_prime(matrix, p):
    """Gaussian-elimination rank over F_p."""
    a = [[int(x) % p for x in row] for row in matrix]

    if not a:
        return 0

    nrows = len(a)
    ncols = len(a[0])
    rank = 0

    for col in range(ncols):
        pivot = next(
            (i for i in range(rank, nrows) if a[i][col] != 0),
            None
        )

        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        inv = pow(a[rank][col], p - 2, p)

        for j in range(col, ncols):
            a[rank][j] = a[rank][j] * inv % p

        for i in range(rank + 1, nrows):
            factor = a[i][col]

            if factor:
                for j in range(col, ncols):
                    a[i][j] = (
                        a[i][j] - factor * a[rank][j]
                    ) % p

        rank += 1

        if rank == nrows:
            break

    return rank


def build_census():
    if not is_prime_64(PRIME):
        raise RuntimeError("Configured modulus is not prime")

    directions = generate_directions()

    if len(directions) != EXPECTED_DIRECTIONS:
        raise RuntimeError(
            f"Direction count mismatch: {len(directions)}"
        )

    records = []
    rank_q_counts = Counter()
    rank_fp_counts = Counter()
    modular_rank_exceptions = []

    flat_id = 0

    for direction_id, basis in enumerate(directions):
        span = generate_span(basis)

        if len(span) != FLAT_SIZE:
            raise RuntimeError("Direction span has wrong size")

        cosets = generate_cosets(span)

        if len(cosets) != N_POINTS // FLAT_SIZE:
            raise RuntimeError("Wrong number of affine cosets")

        for representative, points in cosets:
            matrix = [feature_vector(x) for x in points]

            rank_q = exact_rank_integer(matrix)
            rank_fp = rank_mod_prime(matrix, PRIME)

            rank_q_counts[rank_q] += 1
            rank_fp_counts[rank_fp] += 1

            exception = (
                rank_q == FLAT_SIZE and rank_fp < FLAT_SIZE
            )

            record = {
                "flat_id": flat_id,
                "direction_id": direction_id,
                "direction_rref": list(basis),
                "coset_representative": representative,
                "points": list(points),
                "rank_Q": rank_q,
                "rank_Fp": rank_fp,
                "modular_rank_exception": exception,
            }

            records.append(record)

            if exception:
                modular_rank_exceptions.append(flat_id)

            flat_id += 1

    return {
        "directions": directions,
        "records": records,
        "rank_q_counts": rank_q_counts,
        "rank_fp_counts": rank_fp_counts,
        "modular_rank_exceptions": modular_rank_exceptions,
    }


def main():
    started = time.monotonic()
    started_utc = utc_now()

    output_dir = Path(__file__).resolve().parent
    output_dir.mkdir(parents=True, exist_ok=True)

    census_path = output_dir / "flat_census.json"
    receipt_path = output_dir / "run_receipt.json"

    result = build_census()

    records = result["records"]
    directions = result["directions"]

    rank_q = {
        str(k): result["rank_q_counts"][k]
        for k in sorted(result["rank_q_counts"])
    }

    rank_fp = {
        str(k): result["rank_fp_counts"][k]
        for k in sorted(result["rank_fp_counts"])
    }

    rank_eight = result["rank_q_counts"].get(8, 0)

    census = {
        "title": "AQARION six-bit affine 3-flat exact census",
        "dimension": N_BITS,
        "point_count": N_POINTS,
        "flat_dimension": FLAT_DIM,
        "flat_size": FLAT_SIZE,
        "feature_count": N_FEATURES,
        "feature_order": (
            "constant, linear coordinates x_0..x_5, "
            "quadratic products x_i*x_j for i<j"
        ),
        "bit_convention": "x_i = (x >> i) & 1",
        "field": "Q",
        "modular_field": f"F_{PRIME}",
        "direction_count": len(directions),
        "flat_count": len(records),
        "rank_Q_distribution": rank_q,
        "rank_Fp_distribution": rank_fp,
        "rank_eight_target": RANK_EIGHT_TARGET,
        "rank_eight_observed": rank_eight,
        "rank_eight_target_match": rank_eight == RANK_EIGHT_TARGET,
        "modular_rank_exception_count": len(
            result["modular_rank_exceptions"]
        ),
        "modular_rank_exception_flat_ids":
            result["modular_rank_exceptions"],
        "flats": records,
    }

    census_path.write_text(
        json.dumps(census, indent=2, sort_keys=True) + "\n"
    )

    finished_utc = utc_now()
    elapsed = time.monotonic() - started

    receipt = {
        "title": "AQARION six-bit flat census receipt",
        "status": "COMPUTATION_COMPLETE",
        "started_utc": started_utc,
        "finished_utc": finished_utc,
        "elapsed_seconds": round(elapsed, 6),
        "python_version": sys.version,
        "prime": PRIME,
        "prime_verified": is_prime_64(PRIME),
        "point_count": N_POINTS,
        "expected_direction_count": EXPECTED_DIRECTIONS,
        "observed_direction_count": len(directions),
        "expected_flat_count": EXPECTED_FLATS,
        "observed_flat_count": len(records),
        "rank_Q_distribution": rank_q,
        "rank_Fp_distribution": rank_fp,
        "rank_eight_target": RANK_EIGHT_TARGET,
        "rank_eight_observed": rank_eight,
        "rank_eight_target_match": rank_eight == RANK_EIGHT_TARGET,
        "modular_rank_exception_count": len(
            result["modular_rank_exceptions"]
        ),
        "flat_census_sha256": sha256_file(census_path),
        "script_sha256": sha256_file(Path(__file__).resolve()),
    }

    geometry_pass = (
        len(directions) == EXPECTED_DIRECTIONS
        and len(records) == EXPECTED_FLATS
    )

    receipt["geometry_gate"] = (
        "PASS" if geometry_pass else "FAIL"
    )

    receipt["rank_eight_gate"] = (
        "PASS" if rank_eight == RANK_EIGHT_TARGET else "FAIL"
    )

    receipt_path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    )

    print("===== SIX-BIT FLAT CENSUS =====")
    print("directions:", len(directions))
    print("affine flats:", len(records))
    print("rank_Q distribution:", rank_q)
    print("rank_Fp distribution:", rank_fp)
    print("rank-eight flats:", rank_eight)
    print("rank-eight target:", RANK_EIGHT_TARGET)
    print("modular rank exceptions:",
          len(result["modular_rank_exceptions"]))
    print("geometry gate:", receipt["geometry_gate"])
    print("rank-eight gate:", receipt["rank_eight_gate"])
    print("elapsed seconds:", round(elapsed, 3))
    print("census SHA256:", receipt["flat_census_sha256"])
    print("receipt:", receipt_path)

    if not geometry_pass:
        return 2

    if rank_eight != RANK_EIGHT_TARGET:
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

