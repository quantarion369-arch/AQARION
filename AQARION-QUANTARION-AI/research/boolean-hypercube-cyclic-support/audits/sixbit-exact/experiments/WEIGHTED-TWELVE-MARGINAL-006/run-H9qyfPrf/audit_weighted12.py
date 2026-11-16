#!/usr/bin/env python3
"""Published weighted seed, independent margins, and exact extensions."""

import hashlib
import itertools as it
import json
import math
import subprocess
import sys
import time
import traceback
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

SOURCE = Path(__file__).resolve()
ROOT = Path.home() / "AQARION"

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def index_fingerprint():
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--stage", "-z"],
        capture_output=True,
    )
    need(result.returncode == 0, "Cannot read Git index")
    return sha(result.stdout)

def rank_q(rows):
    a = [[Fraction(v) for v in row] for row in rows]
    rank = 0

    for col in range(len(a[0])):
        pivot = next(
            (i for i in range(rank,len(a)) if a[i][col]),
            None,
        )
        if pivot is None:
            continue

        a[rank],a[pivot] = a[pivot],a[rank]
        value = a[rank][col]
        a[rank] = [x/value for x in a[rank]]

        for i in range(rank+1,len(a)):
            value = a[i][col]
            if value:
                a[i] = [
                    x-value*y
                    for x,y in zip(a[i],a[rank])
                ]

        rank += 1
        if rank == len(a):
            break

    return rank

def monomials(x,n):
    bits = [(x >> i)&1 for i in range(n)]
    return (
        [1] + bits
        + [bits[i]*bits[j] for i,j in it.combinations(range(n),2)]
    )

def margins(x,n):
    # Constructed directly as categorical indicators.
    return [
        int(((x >> i)&1) == a and ((x >> j)&1) == b)
        for i,j in it.combinations(range(n),2)
        for a,b in it.product((0,1),repeat=2)
    ]

def identity(rows, coefficients):
    return all(
        sum(c*row[j] for c,row in zip(coefficients,rows)) == 0
        for j in range(len(rows[0]))
    )

def certify(points, coefficients, n):
    need(len(points) == len(set(points)) == 12,
         "Invalid twelve-point support")
    need(all(coefficients), "Zero kernel coefficient")
    need(math.gcd(*coefficients) == 1, "Nonprimitive kernel")

    result = {}
    for name,feature in (
        ("monomial",monomials),
        ("marginal",margins),
    ):
        rows = [feature(x,n) for x in points]

        need(identity(rows,coefficients),
             name+": feature identity")
        need(rank_q(rows) == 11,
             name+": support rank")

        deletions = [
            rank_q(rows[:i]+rows[i+1:])
            for i in range(12)
        ]
        need(deletions == [11]*12,
             name+": deletion rank")

        bad = list(coefficients)
        bad[0] += 1
        bad[1] -= 1
        need(not identity(rows,bad),
             name+": corrupted-kernel control")

        result[name] = {
            "rank": 11,
            "deletion_ranks": deletions,
            "exact_identity": True,
            "corrupted_kernel_rejected": True,
        }

    return result

def check_representation_identity(n):
    checks = 0

    for x in range(1 << n):
        bits = [(x >> i)&1 for i in range(n)]
        direct = margins(x,n)
        reconstructed = []

        for i,j in it.combinations(range(n),2):
            u,v = bits[i],bits[j]
            reconstructed.extend([
                1-u-v+u*v,
                v-u*v,
                u-u*v,
                u*v,
            ])

        need(direct == reconstructed,
             "Indicator/monomial identity mismatch")
        checks += len(direct)

    return checks

def orbit(points):
    result = set()

    for perm in it.permutations(range(6)):
        transformed = [
            sum(((x >> perm[i])&1) << i for i in range(6))
            for x in points
        ]
        for shift in range(64):
            result.add(tuple(sorted(
                x ^ shift for x in transformed
            )))

    return result

def digest_supports(supports):
    h = hashlib.sha256()
    for points in sorted(supports):
        h.update(bytes(points))
    return h.hexdigest()

def audit(report):
    report["representation_scalar_checks"] = {
        "five_bits": check_representation_identity(5),
        "six_bits": check_representation_identity(6),
    }

    seed = [
        x for x in range(32)
        if x.bit_count() in (0,1,4,5)
    ]
    coefficients = [
        3 if x == 0
        else -3 if x == 31
        else -1 if x.bit_count() == 1
        else 1
        for x in seed
    ]

    report["seed"] = {
        "points": seed,
        "primitive_kernel": coefficients,
        "trade_volume": sum(
            x for x in coefficients if x > 0
        ),
        "certification": certify(seed,coefficients,5),
    }
    print("PASS: seed in monomial and marginal representations",
          flush=True)

    accepted = []

    for g in it.product((0,1),repeat=12):
        valid = all(
            sum(
                coefficients[k] * int(
                    ((seed[k] >> i)&1) == a and g[k] == b
                )
                for k in range(12)
            ) == 0
            for i in range(5)
            for a,b in it.product((0,1),repeat=2)
        )
        if valid:
            accepted.append(g)

    expected = {(0,)*12,(1,)*12}
    for i in range(5):
        g = tuple((x >> i)&1 for x in seed)
        expected.add(g)
        expected.add(tuple(1-a for a in g))

    need(set(accepted) == expected,
         "Unexpected or missing coordinate extensions")
    need(len(accepted) == 12, "Accepted-extension count")

    print("PASS: all 4096 extensions; exactly 12 accepted",
          flush=True)

    union = set()
    orbit_records = []

    for g in accepted:
        unsorted_points = [
            x | (g[k] << 5)
            for k,x in enumerate(seed)
        ]
        points = tuple(sorted(unsorted_points))

        if points in union:
            continue

        coefficient_map = {
            point: coefficients[k]
            for k,point in enumerate(unsorted_points)
        }
        lifted_coefficients = [
            coefficient_map[x] for x in points
        ]

        certification = certify(
            points,lifted_coefficients,6
        )
        current = orbit(points)

        need(not (current & union), "Orbit overlap")
        union.update(current)

        orbit_records.append({
            "representative": points,
            "primitive_kernel": lifted_coefficients,
            "orbit_size": len(current),
            "stabilizer_order": 46080 // len(current),
            "support_set_sha256": digest_supports(current),
            "certification": certification,
        })

        print("PASS: six-bit orbit size",len(current),
              flush=True)

    sizes = sorted(r["orbit_size"] for r in orbit_records)
    need(sizes == [192,480], "Unexpected orbit partition")
    need(len(union) == 672, "Distinct-union count")

    report.update({
        "assignments_tested": 4096,
        "accepted_assignments": len(accepted),
        "allowed_coordinate_functions":
            "constants, five coordinate copies, five complements",
        "orbits": orbit_records,
        "orbit_sizes": sizes,
        "distinct_six_bit_supports": len(union),
        "support_set_sha256": digest_supports(union),
        "all_672_ranks_individually_recomputed": False,
        "circuit_transfer_method":
            "Exact orbit-representative certification plus "
            "coordinate permutations and bit complements",
        "arbitrary_binary_affine_maps_used": False,
        "source_of_seed":
            "Develin-Sullivant, Markov Bases of Binary Graph Models, "
            "displayed K5 degree-eight move / Proposition 2.7",
        "scope":
            "Complete one-coordinate extension and cube-orbit closure "
            "of one published five-bit weighted circuit. "
            "Not all weighted twelve-point circuits, not a complete "
            "six-bit circuit census, and no novelty claim.",
    })

def main():
    output = Path(sys.argv[1]).resolve()
    started = time.monotonic()
    original = SOURCE.read_bytes()
    original_index = index_fingerprint()

    report = {
        "experiment": "WEIGHTED-TWELVE-MARGINAL-006",
        "status": "RUNNING",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha(original),
        "git_index_before": original_index,
        "python_version": sys.version,
    }

    try:
        audit(report)
        need(SOURCE.read_bytes() == original, "Source changed")
        need(index_fingerprint() == original_index,
             "Git index changed during experiment")
        report["source_unchanged"] = True
        report["git_index_unchanged"] = True
        report["status"] = "PASS"

    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = type(exc).__name__+": "+str(exc)
        (output/"traceback.txt").write_text(
            traceback.format_exc()
        )

    report["finished_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"] = round(time.monotonic()-started,6)

    (output/"REPORT.json").write_text(
        json.dumps(report,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(report,indent=2,sort_keys=True),flush=True)
    return 0 if report["status"] == "PASS" else 2

if __name__ == "__main__":
    raise SystemExit(main())
