#!/usr/bin/env python3
"""Exact rational audit of the proposed five-bit 10-circuit family."""

import hashlib
import itertools
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from sympy import Matrix

N = 5
P = 2147483629
ROOT = Path.cwd()
BASE = ROOT / "research/boolean-hypercube-cyclic-support/audits/fivebit-1200-exact"


def row_for(x):
    bits = [(x >> i) & 1 for i in range(N)]
    return [1] + bits + [
        bits[i] * bits[j]
        for i, j in itertools.combinations(range(N), 2)
    ]


ROWS = [row_for(x) for x in range(1 << N)]


def exact_rank(rows):
    return int(Matrix(rows).rank())


def binary_span(a, b, c):
    return frozenset(
        (i * a) ^ (j * b) ^ (k * c)
        for i, j, k in itertools.product((0, 1), repeat=3)
    )


def all_linear_3spaces():
    spaces = set()
    for a, b, c in itertools.combinations(range(1, 32), 3):
        s = binary_span(a, b, c)
        if len(s) == 8:
            spaces.add(s)
    return sorted(spaces, key=lambda s: tuple(sorted(s)))


def all_affine_flats():
    flats = set()
    for direction in all_linear_3spaces():
        unseen = set(range(32))
        while unseen:
            representative = min(unseen)
            coset = frozenset(representative ^ v for v in direction)
            flats.add((direction, coset))
            unseen.difference_update(coset)
    return sorted(
        flats,
        key=lambda item: (tuple(sorted(item[0])), tuple(sorted(item[1])))
    )


def add_mod_basis(basis, source):
    v = [x % P for x in source]
    for pivot, basis_row in basis:
        factor = v[pivot]
        if factor:
            v = [(x - factor * y) % P for x, y in zip(v, basis_row)]
    pivot = next((j for j, x in enumerate(v) if x), None)
    if pivot is None:
        return
    inv = pow(v[pivot], P - 2, P)
    v = [(x * inv) % P for x in v]
    basis.append((pivot, v))
    basis.sort(key=lambda item: item[0])


def reduce_mod_basis(basis, source):
    v = [x % P for x in source]
    for pivot, basis_row in basis:
        factor = v[pivot]
        if factor:
            v = [(x - factor * y) % P for x, y in zip(v, basis_row)]
    return v


def dependent_pair_mod(a, b):
    pivot = next((i for i, x in enumerate(a) if x), None)
    if pivot is None:
        return True
    ratio = b[pivot] * pow(a[pivot], P - 2, P) % P
    return all((b[i] - ratio * a[i]) % P == 0 for i in range(len(a)))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    commit = os.popen("git rev-parse HEAD").read().strip()
    branch = os.popen("git branch --show-current").read().strip()
    started = datetime.now(timezone.utc).isoformat()

    flats = all_affine_flats()
    flat_rank_counts = Counter()
    rank8_flats = []

    for direction, flat in flats:
        rank = exact_rank([ROWS[x] for x in sorted(flat)])
        flat_rank_counts[rank] += 1
        if rank == 8:
            rank8_flats.append((direction, flat))
        elif rank != 7:
            raise RuntimeError(f"Unexpected affine-flat rank: {rank}")

    if len(flats) != 620 or flat_rank_counts != Counter({7: 260, 8: 360}):
        raise RuntimeError(
            f"Unexpected flat census: total={len(flats)}, "
            f"rank_counts={dict(flat_rank_counts)}"
        )

    candidates = []
    candidates_by_flat = Counter()
    parallel_candidates = 0
    examined = 0

    for direction, flat in rank8_flats:
        flat_points = sorted(flat)
        outside = sorted(set(range(32)) - set(flat))

        basis = []
        for x in flat_points:
            add_mod_basis(basis, ROWS[x])

        if len(basis) != 8:
            raise RuntimeError(
                "Rank-eight rational flat lost rank modulo P; "
                "candidate filter cannot safely proceed."
            )

        residuals = {
            x: reduce_mod_basis(basis, ROWS[x])
            for x in outside
        }

        for a, b in itertools.combinations(outside, 2):
            examined += 1
            if dependent_pair_mod(residuals[a], residuals[b]):
                candidates.append((tuple(flat_points), a, b))
                candidates_by_flat[tuple(flat_points)] += 1
                if (a ^ b) in direction:
                    parallel_candidates += 1

    exact_rank_counts = Counter()
    circuit_count = 0
    deletion_failures = []
    exact_circuits = []
    parallel_exact_circuits = 0

    for flat_points, a, b in candidates:
        support = list(flat_points) + [a, b]
        matrix_rows = [ROWS[x] for x in support]
        rank = exact_rank(matrix_rows)
        exact_rank_counts[rank] += 1

        if rank != 9:
            continue

        failed = []
        for omitted in range(10):
            reduced = matrix_rows[:omitted] + matrix_rows[omitted + 1:]
            if exact_rank(reduced) != 9:
                failed.append(support[omitted])

        if failed:
            deletion_failures.append({
                "support": support,
                "rank": rank,
                "failed_deletions": failed,
            })
            continue

        circuit_count += 1
        exact_circuits.append({
            "flat": list(flat_points),
            "pair": [a, b],
            "support": support,
            "parallel_pair": ((a ^ b) in set(
                # Direction is recovered as all pairwise XORs in the flat.
                x ^ flat_points[0] for x in flat_points
            )),
        })
        if (a ^ b) in set(x ^ flat_points[0] for x in flat_points):
            parallel_exact_circuits += 1

    exact_circuits_per_flat = Counter(
        tuple(item["flat"]) for item in exact_circuits
    )
    flat_distribution = Counter(exact_circuits_per_flat.values())
    zero_circuit_flats = 360 - len(exact_circuits_per_flat)

    report = {
        "title": "Five-bit proposed ten-circuit family: exact rational audit",
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "git_branch": branch,
        "field_for_candidate_filter": P,
        "exact_field": "Q",
        "affine_3_flats": len(flats),
        "affine_flat_exact_rank_counts": dict(flat_rank_counts),
        "rank_8_flats": len(rank8_flats),
        "candidate_pairs_examined": examined,
        "modularly_deficient_candidates": len(candidates),
        "candidate_exact_rank_counts": dict(exact_rank_counts),
        "exact_rank_9_candidates": exact_rank_counts[9],
        "exact_ten_point_circuits": circuit_count,
        "deletion_failures": len(deletion_failures),
        "parallel_pair_exact_circuits": parallel_exact_circuits,
        "qualifying_flats": len(exact_circuits_per_flat),
        "qualifying_flats_by_circuit_count": dict(flat_distribution),
        "flats_with_zero_circuits": zero_circuit_flats,
        "candidate_count_per_flat_modular": dict(
            Counter(candidates_by_flat.values())
        ),
        "expected_checks": {
            "620_flats": len(flats) == 620,
            "260_rank_7_and_360_rank_8": (
                flat_rank_counts == Counter({7: 260, 8: 360})
            ),
            "99360_pairs_examined": examined == 99360,
            "1200_modular_candidates": len(candidates) == 1200,
            "1200_exact_rank_9": exact_rank_counts[9] == 1200,
            "1200_exact_circuits": circuit_count == 1200,
            "zero_deletion_failures": len(deletion_failures) == 0,
            "300_flats_with_four_circuits": (
                flat_distribution == Counter({4: 300})
            ),
            "60_flats_with_zero_circuits": zero_circuit_flats == 60,
        },
        "deletion_failure_examples": deletion_failures[:20],
        "exact_circuits": exact_circuits,
        "scope_warning": (
            "This audits the proposed rank-eight-flat-plus-pair family. "
            "It does not independently prove that every ten-point circuit "
            "in the full five-bit cube belongs to this family."
        ),
    }

    BASE.mkdir(parents=True, exist_ok=True)
    run_dir = BASE / ("run-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"))
    run_dir.mkdir()

    report_path = run_dir / "report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    candidate_path = run_dir / "exact_circuits.json"
    candidate_path.write_text(
        json.dumps(exact_circuits, indent=2, sort_keys=True) + "\n"
    )

    script_path = Path(__file__).resolve()
    sums_path = run_dir / "SHA256SUMS"
    sums_path.write_text(
        f"{sha256(script_path)}  {script_path}\n"
        f"{sha256(report_path)}  {report_path}\n"
        f"{sha256(candidate_path)}  {candidate_path}\n"
    )

    print(json.dumps({
        "git_commit": commit,
        "git_branch": branch,
        "affine_flats": len(flats),
        "flat_rank_counts": dict(flat_rank_counts),
        "pairs_examined": examined,
        "modular_candidates": len(candidates),
        "exact_rank_counts": dict(exact_rank_counts),
        "exact_circuits": circuit_count,
        "deletion_failures": len(deletion_failures),
        "parallel_exact_circuits": parallel_exact_circuits,
        "qualifying_flats": len(exact_circuits_per_flat),
        "qualifying_flat_distribution": dict(flat_distribution),
        "zero_circuit_flats": zero_circuit_flats,
        "expected_checks": report["expected_checks"],
        "run_directory": str(run_dir),
        "sha256sums": str(sums_path),
    }, indent=2))

    if not all(report["expected_checks"].values()):
        print("AUDIT COMPLETED: one or more expected checks did not match.")
        return 2

    print("AUDIT COMPLETED: all specified checks matched.")
    print("Scope remains limited to the proposed candidate family.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
