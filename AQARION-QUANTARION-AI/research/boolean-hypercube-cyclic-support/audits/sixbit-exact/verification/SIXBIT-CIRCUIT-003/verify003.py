#!/usr/bin/env python3
"""SIXBIT-CIRCUIT-003
Independent reconstruction and exact audit of rank-seven affine 3-flats.

Scope:
- Reconstruct all 3-dimensional directions in F_2^6.
- Reconstruct all affine cosets.
- Audit all 11,160 quadratic-feature evaluation matrices.
- Prove rank-seven cases have an exact rational, full-support kernel relation.
- Check all single-point deletions modulo a pinned prime.
- Classify rank-seven directions under coordinate permutations S_6.

This is not a search for, or classification of, every possible circuit.
Standard library only.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PRIME = 2147483629

PINS = {
    "flat_census.json":
        "5e684e0152d240534632a9c0dc4916727c5b80e4baa5243727098a0710a1e161",
    "run_receipt.json":
        "745b853be897690264271064d05deb5bea3032c4ae0c85b033be542dc2c0fd12",
    "sixbit_flats.py":
        "700d2b036c8cf3617f26f4e97bcdc52fa00ad648514426598b948d38aea6d5b5",
}

def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def parity(x: int) -> int:
    return x.bit_count() & 1

def rref_binary(vectors: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    """Canonical RREF basis; bit i represents coordinate x_i."""
    rows = [int(v) & 63 for v in vectors if int(v) & 63]
    pivot_row = 0
    for col in range(6):
        pivot = next(
            (r for r in range(pivot_row, len(rows))
             if (rows[r] >> col) & 1),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        for r in range(len(rows)):
            if r != pivot_row and ((rows[r] >> col) & 1):
                rows[r] ^= rows[pivot_row]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return tuple(rows[:pivot_row])

def enumerate_directions() -> list[tuple[int, ...]]:
    """Every 3-space, generated from independent triples and deduplicated."""
    found = set()
    for triple in combinations(range(1, 64), 3):
        basis = rref_binary(triple)
        if len(basis) == 3:
            found.add(basis)
    result = sorted(found)
    require(len(result) == 1395,
            f"direction count mismatch: {len(result)}")
    return result

def subspace_points(basis: tuple[int, ...]) -> tuple[int, ...]:
    points = []
    for t in range(8):
        x = 0
        for j in range(3):
            if (t >> j) & 1:
                x ^= basis[j]
        points.append(x)
    require(len(set(points)) == 8, "subspace does not contain 8 points")
    return tuple(points)

def coset_representatives(
    subspace: tuple[int, ...],
) -> tuple[int, ...]:
    reps = []
    seen = set()
    for x in range(64):
        rep = min(x ^ v for v in subspace)
        if rep not in seen:
            seen.add(rep)
            reps.append(rep)
    reps = tuple(sorted(reps))
    require(len(reps) == 8,
            f"coset count mismatch: {len(reps)}")
    return reps

def feature_vector(x: int) -> list[int]:
    bits = [(x >> i) & 1 for i in range(6)]
    out = [1] + bits
    out.extend(bits[i] * bits[j]
               for i in range(6) for j in range(i + 1, 6))
    require(len(out) == 22, "feature dimension mismatch")
    return out

def matrix_for_flat(
    rep: int, basis: tuple[int, ...]
) -> tuple[list[int], list[list[int]]]:
    params = list(range(8))
    points = []
    for t in params:
        x = rep
        for j in range(3):
            if (t >> j) & 1:
                x ^= basis[j]
        points.append(x)
    require(len(set(points)) == 8, "affine flat has duplicate points")
    return points, [feature_vector(x) for x in points]

def is_prime_trial_division(n: int) -> bool:
    """Deterministic primality test by trial division."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 2
    return True


def rank_mod(matrix: list[list[int]], p: int = PRIME) -> int:
    """Gaussian rank over F_p."""
    if not matrix:
        return 0
    a = [[int(v) % p for v in row] for row in matrix]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [(a[i][j] - q * a[r][j]) % p
                        for j in range(n)]
        r += 1
        if r == m:
            break
    return r

def rank_exact(matrix: list[list[int]]) -> int:
    """Exact Gaussian elimination over Q using Fraction arithmetic."""
    if not matrix:
        return 0
    a = [[Fraction(v) for v in row] for row in matrix]
    m, n = len(a), len(a[0])
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r, m) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        pv = a[r][c]
        a[r] = [v / pv for v in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [a[i][j] - q * a[r][j] for j in range(n)]
        r += 1
        if r == m:
            break
    return r

def walsh_missing_character(
    matrix: list[list[int]],
) -> int | None:
    """Return the unique zero Walsh row, if exactly one exists."""
    zero_rows = []
    for character in range(8):
        row = []
        for col in range(22):
            total = sum(
                (-1 if parity(character & t) else 1) * matrix[t][col]
                for t in range(8)
            )
            row.append(total)
        if all(v == 0 for v in row):
            zero_rows.append(character)
    return zero_rows[0] if len(zero_rows) == 1 else None

def coordinate_permute(
    basis: tuple[int, ...], perm: tuple[int, ...]
) -> tuple[int, ...]:
    """Coordinate i is sent to coordinate perm[i]."""
    mapped = []
    for v in basis:
        w = 0
        for i in range(6):
            if (v >> i) & 1:
                w |= 1 << perm[i]
        mapped.append(w)
    return rref_binary(mapped)

def classify_s6_orbits(
    directions: list[tuple[int, ...]],
) -> list[dict]:
    direction_set = set(directions)
    all_perms = list(permutations(range(6)))
    unvisited = set(direction_set)
    orbit_sizes = []
    representatives = []

    while unvisited:
        seed = min(unvisited)
        orbit = {
            coordinate_permute(seed, p)
            for p in all_perms
        }
        require(orbit <= direction_set,
                "coordinate permutation left the direction census")
        require(seed in orbit, "orbit does not contain its seed")
        unvisited.difference_update(orbit)
        orbit_sizes.append(len(orbit))
        representatives.append(list(seed))

    require(sum(orbit_sizes) == len(direction_set),
            "S6 orbit sizes do not cover all rank-seven directions")
    return [
        {"representative_rref": rep, "orbit_size": size}
        for rep, size in sorted(
            zip(representatives, orbit_sizes),
            key=lambda item: (item[1], item[0]),
        )
    ]

def main() -> None:
    require(is_prime_trial_division(PRIME),
            f'pinned modulus is not prime: {PRIME}')
    # 1. Verify immutable input pins.
    input_hashes = {}
    for name, expected in PINS.items():
        path = BASE / name
        require(path.is_file(), f"missing pinned input: {path}")
        actual = digest(path)
        require(actual == expected,
                f"SHA256 mismatch for {name}: {actual}")
        input_hashes[name] = actual

    # Parse pinned JSON inputs to reject malformed files.
    for name in ("flat_census.json", "run_receipt.json"):
        with (BASE / name).open("r", encoding="utf-8") as f:
            json.load(f)

    # 2. Independently reconstruct all directions and affine flats.
    directions = enumerate_directions()
    total_flats = 0
    rank_hist = Counter()
    rank7_directions = set()
    rank7_supports = 0
    exact_rank_checks = 0
    deletion_checks = 0
    kernel_identity_checks = 0
    missing_character_hist = Counter()
    per_direction_rank7 = Counter()

    for basis in directions:
        subspace = subspace_points(basis)
        reps = coset_representatives(subspace)
        direction_rank7 = 0

        for rep in reps:
            points, matrix = matrix_for_flat(rep, basis)
            total_flats += 1

            rm = rank_mod(matrix)
            require(rm in (7, 8),
                    f"unexpected modular rank {rm}, basis={basis}, rep={rep}")
            rank_hist[rm] += 1

            if rm == 8:
                continue

            # Rank over Q is at least modular rank and at most 8.
            # An exact rank-7 check is required for every rank-7 candidate.
            rq = rank_exact(matrix)
            exact_rank_checks += 1
            require(rq == 7,
                    f"exact rank mismatch: modular=7, rational={rq}")

            missing = walsh_missing_character(matrix)
            require(missing is not None,
                    f"no unique missing Walsh character: {basis}, {rep}")
            missing_character_hist[missing] += 1

            # Coefficients (-1)^<missing,t> form a rational kernel vector.
            coeffs = [
                -1 if parity(missing & t) else 1
                for t in range(8)
            ]
            require(all(c != 0 for c in coeffs),
                    "kernel relation contains a zero coefficient")

            for col in range(22):
                value = sum(coeffs[t] * matrix[t][col] for t in range(8))
                require(value == 0,
                        f"kernel identity failed at feature column {col}")
                kernel_identity_checks += 1

            # Check all eight deletions modulo p. Since rational rank is 7,
            # modular rank 7 proves each deletion has rational rank 7 too.
            # Each deletion has at most 7 rows, so rank cannot exceed 7.
            for deleted in range(8):
                reduced = [
                    matrix[i] for i in range(8) if i != deleted
                ]
                rd = rank_mod(reduced)
                require(rd == 7,
                        f"deletion rank failure: deleted={deleted}, rank={rd}")
                deletion_checks += 1

            rank7_supports += 1
            direction_rank7 += 1

        per_direction_rank7[direction_rank7] += 1
        if direction_rank7:
            require(direction_rank7 == 8,
                    "rank-seven status is not constant across all 8 cosets")
            rank7_directions.add(basis)

    # 3. Exhaustive census assertions.
    require(total_flats == 11160,
            f"affine flat count mismatch: {total_flats}")
    require(rank_hist[7] == 2800,
            f"rank-seven count mismatch: {rank_hist[7]}")
    require(rank_hist[8] == 8360,
            f"rank-eight count mismatch: {rank_hist[8]}")
    require(rank7_supports == 2800,
            f"rank-seven support count mismatch: {rank7_supports}")
    require(len(rank7_directions) == 350,
            f"rank-seven direction count mismatch: {len(rank7_directions)}")
    require(exact_rank_checks == 2800,
            f"exact rank check count mismatch: {exact_rank_checks}")
    require(deletion_checks == 22400,
            f"deletion check count mismatch: {deletion_checks}")
    require(kernel_identity_checks == 61600,
            f"kernel identity count mismatch: {kernel_identity_checks}")

    # 4. Coordinate-permutation orbit classification.
    orbit_records = classify_s6_orbits(sorted(rank7_directions))
    require(len(orbit_records) == 7,
            f"expected 7 S6 orbits, observed {len(orbit_records)}")
    require(sum(r["orbit_size"] for r in orbit_records) == 350,
            "S6 orbit sizes do not sum to 350 directions")

    affine_orbit_sizes = [8 * r["orbit_size"] for r in orbit_records]
    require(sum(affine_orbit_sizes) == 2800,
            "affine orbit sizes do not sum to 2,800 supports")

    # 5. Emit certificate only after every assertion has passed.
    script_hash = digest(Path(__file__))
    certificate = {
        "audit": "SIXBIT-CIRCUIT-003",
        "status": "PASS",
        "scope": (
            "All affine 3-flats in F_2^6 under the pinned quadratic "
            "22-feature evaluation map; rank-seven circuit minimality "
            "and S6 coordinate-permutation orbits."
        ),
        "exclusions": [
            "No claim that all possible circuits in the full system "
            "have been classified.",
            "No circuit-search completeness claim.",
            "No formal Lean proof is claimed.",
        ],
        "input_sha256": input_hashes,
        "script_sha256": script_hash,
        "field": "Q for exact rank and identities; F_p for independent "
                 "modular rank checks",
        "prime": PRIME,
        "prime_verification": "deterministic trial division through floor(sqrt(prime))",
        "bit_convention": "x_i=(x>>i)&1",
        "feature_dimension": 22,
        "cube_points": 64,
        "directions": len(directions),
        "cosets_per_direction": 8,
        "affine_flats": total_flats,
        "rank_distribution": {
            "7": rank_hist[7],
            "8": rank_hist[8],
        },
        "rank_seven_directions": len(rank7_directions),
        "exact_rational_rank_checks": exact_rank_checks,
        "kernel_identity_checks": kernel_identity_checks,
        "single_point_deletion_checks_mod_p": deletion_checks,
        "missing_walsh_character_histogram": {
            str(k): v for k, v in sorted(missing_character_hist.items())
        },
        "S6_direction_orbits": orbit_records,
        "affine_support_counts_by_direction_orbit": affine_orbit_sizes,
        "group_order_S6": 720,
        "hypercube_affine_group_order": 46080,
    }

    target = OUT / "PASS.json"
    tmp = OUT / "PASS.json.tmp"
    tmp.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(target)

    print("SIXBIT-CIRCUIT-003: PASS")
    print(f"directions: {len(directions)}")
    print(f"affine flats: {total_flats}")
    print(f"rank 7: {rank_hist[7]}")
    print(f"rank 8: {rank_hist[8]}")
    print(f"rank-seven directions: {len(rank7_directions)}")
    print(f"exact rational rank checks: {exact_rank_checks}")
    print(f"kernel identities: {kernel_identity_checks}")
    print(f"single-point deletion checks: {deletion_checks}")
    print(f"S6 direction orbits: {len(orbit_records)}")
    print("orbit sizes:", [r["orbit_size"] for r in orbit_records])
    print("affine orbit sizes:", affine_orbit_sizes)
    print(f"script SHA256: {script_hash}")
    print(f"certificate: {target}")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"SIXBIT-CIRCUIT-003: FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
