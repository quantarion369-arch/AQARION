#!/usr/bin/env python3
"""Exact eight-point circuit structure on the pinned six-bit flats."""

import hashlib
import itertools
import json
import math
import sys
import time
import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

SOURCE = Path(__file__).resolve()
BASE = SOURCE.parent.parent.parent

PINS = {
    "flat_census.json":
        "5e684e0152d240534632a9c0dc4916727c5b80e4baa5243727098a0710a1e161",
    "run_receipt.json":
        "745b853be897690264271064d05deb5bea3032c4ae0c85b033be542dc2c0fd12",
    "sixbit_flats.py":
        "700d2b036c8cf3617f26f4e97bcdc52fa00ad648514426598b948d38aea6d5b5",
}

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def features(x):
    b = [(x >> i) & 1 for i in range(6)]
    return (
        [1] + b
        + [b[i]*b[j] for i in range(6) for j in range(i+1,6)]
    )

def exact_rank(rows):
    """Integer row operations preserving rank over Q."""
    a = [list(row) for row in rows]
    rank = 0

    for col in range(len(a[0])):
        pivot = next(
            (i for i in range(rank,len(a)) if a[i][col]),
            None,
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]

        for i in range(rank+1,len(a)):
            q = a[i][col]
            if not q:
                continue

            p = a[rank][col]
            divisor = math.gcd(abs(p),abs(q))
            u, v = p//divisor, q//divisor

            a[i] = [
                u*x-v*y for x,y in zip(a[i],a[rank])
            ]

            divisor = math.gcd(*(abs(x) for x in a[i]))
            if divisor > 1:
                a[i] = [x//divisor for x in a[i]]

        rank += 1
        if rank == len(a):
            break

    return rank

def parameter_points(basis, representative):
    return [
        representative
        ^ (basis[0] if u & 1 else 0)
        ^ (basis[1] if u & 2 else 0)
        ^ (basis[2] if u & 4 else 0)
        for u in range(8)
    ]

def character_indices(basis):
    signatures = [
        sum(((v >> i)&1) << j for j,v in enumerate(basis))
        for i in range(6)
    ]
    return (
        {0}
        | set(signatures)
        | {
            signatures[i] ^ signatures[j]
            for i in range(6)
            for j in range(i+1,6)
        }
    )

def audit(report):
    for name,digest in PINS.items():
        path = BASE/name
        need(path.is_file(), "Missing input: "+name)
        need(sha(path) == digest, "Input hash mismatch: "+name)

    census = json.loads((BASE/"flat_census.json").read_text())
    records = census["flats"]
    need(len(records) == 11160, "Wrong flat count")

    # Arithmetic controls.
    need(exact_rank([[1,0],[0,1]]) == 2,
         "Independent-rank control")
    need(exact_rank([[1,1],[2,2]]) == 1,
         "Dependent-rank control")

    rank_hist = Counter()
    direction_ranks = defaultdict(set)
    direction_flats = Counter()
    direction_bases = {}
    seen_points = set()
    seen_ids = set()
    examples = []
    kernel_digest = hashlib.sha256()
    kernels_checked = 0
    rank7_directions = set()

    for number,rec in enumerate(records,1):
        basis = rec["direction_rref"]
        representative = rec["coset_representative"]
        flat_id = rec["flat_id"]
        direction_id = rec["direction_id"]

        need(
            len(basis) == 3
            and all(type(x) is int and 0 < x < 64 for x in basis),
            "Invalid direction basis",
        )
        need(type(representative) is int
             and 0 <= representative < 64,
             "Invalid representative")

        points = parameter_points(basis,representative)
        key = tuple(sorted(points))

        need(len(set(points)) == 8, "Dependent binary basis")
        need(key == tuple(rec["points"]), "Point reconstruction")
        need(key not in seen_points, "Repeated affine flat")
        need(flat_id not in seen_ids, "Repeated flat ID")

        seen_points.add(key)
        seen_ids.add(flat_id)

        if direction_id in direction_bases:
            need(direction_bases[direction_id] == tuple(basis),
                 "Direction ID changes basis")
        else:
            direction_bases[direction_id] = tuple(basis)

        rows = [features(x) for x in points]
        rank = exact_rank(rows)
        characters = character_indices(basis)

        need(rank in (7,8), "Unexpected exact rank")
        need(rank == len(characters), "Character-rank disagreement")
        need(rec["rank_Q"] == rank, "Stored rational rank mismatch")

        rank_hist[rank] += 1
        direction_ranks[direction_id].add(rank)
        direction_flats[direction_id] += 1

        if rank == 7:
            need(set(range(8))-characters == {7},
                 "Missing character is not 111")

            need(all(
                (basis[i] & basis[j]) == 0
                for i,j in itertools.combinations(range(3),2)
            ), "Rank-seven basis blocks overlap")

            z = [
                1 if u.bit_count()%2 == 0 else -1
                for u in range(8)
            ]

            need(all(
                sum(z[u]*rows[u][j] for u in range(8)) == 0
                for j in range(22)
            ), "Alternating dependency failed")

            # One-dimensional kernel and no zero coefficient:
            # every seven-point deletion is independent.
            need(8-rank == 1 and all(z),
                 "Circuit-minimality criterion failed")

            bad = z[:]
            bad[0] += 1
            need(any(
                sum(bad[u]*rows[u][j] for u in range(8))
                for j in range(22)
            ), "Corrupted-kernel rejection control failed")

            witness = {
                "flat_id": flat_id,
                "direction_id": direction_id,
                "direction_rref": basis,
                "representative": representative,
                "points_parameter_order": points,
                "primitive_kernel": z,
                "walsh_character": 7,
            }

            kernel_digest.update(
                (json.dumps(witness,sort_keys=True,
                            separators=(",",":"))+"\n").encode()
            )

            if len(examples) < 5:
                examples.append(witness)

            kernels_checked += 1
            rank7_directions.add(direction_id)

        if number % 1000 == 0:
            print("EXACT FLATS CHECKED:", number, flush=True)

    need(rank_hist == Counter({7:2800,8:8360}),
         "Rank distribution mismatch")
    need(len(direction_bases) == 1395, "Direction count")
    need(len(set(direction_bases.values())) == 1395,
         "Different direction IDs share a basis")
    need(all(v == 8 for v in direction_flats.values()),
         "Wrong coset count per direction")
    need(all(len(v) == 1 for v in direction_ranks.values()),
         "Mixed ranks within a direction")
    need(kernels_checked == 2800, "Kernel certificate count")
    need(len(rank7_directions) == 350, "Rank-seven direction count")

    for name,digest in PINS.items():
        need(sha(BASE/name) == digest, "Input changed: "+name)

    report.update({
        "input_sha256": PINS,
        "point_reconstruction_checks": 11160,
        "exact_rational_rank_checks": 11160,
        "rank_distribution": dict(sorted(rank_hist.items())),
        "directions_checked": 1395,
        "rank_seven_directions": 350,
        "rank_eight_directions": 1045,
        "mixed_rank_directions": 0,
        "full_support_primitive_kernels_checked": 2800,
        "eight_point_circuits_certified_in_flat_census": 2800,
        "missing_character_111_checks": 2800,
        "disjoint_variable_block_checks": 2800,
        "kernel_certificate_stream_sha256": kernel_digest.hexdigest(),
        "first_five_kernel_witnesses": examples,
        "circuit_minimality_method":
            "Exact rank seven plus nonzero eight-entry kernel",
        "all_deletion_ranks_individually_computed": False,
        "inputs_unchanged": True,
    })

def main():
    started = time.monotonic()
    output = Path(sys.argv[1]).resolve()
    original = SOURCE.read_bytes()

    report = {
        "gate": "SIXBIT-CIRCUIT-003",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": hashlib.sha256(original).hexdigest(),
        "python_version": sys.version,
        "scope":
            "Exact structural certification of the pinned affine-flat "
            "census: rational ranks, parameter reconstruction and "
            "rank-seven alternating kernels. Not a new ten/twelve-point "
            "circuit census, formal proof, or novelty claim.",
    }

    try:
        audit(report)
        need(SOURCE.read_bytes() == original, "Source changed")
        report["source_unchanged"] = True
        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = type(exc).__name__+": "+str(exc)
        (output/"traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic()-started,6)

    (output/"REPORT.json").write_text(
        json.dumps(report,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(report,indent=2,sort_keys=True),flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
