#!/usr/bin/env python3
import hashlib
import itertools as it
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path
import sys

P = 2147483629
PIN = {
    "flat_census.json":
        "5e684e0152d240534632a9c0dc4916727c5b80e4baa5243727098a0710a1e161",
    "ten_point_circuit_search.json":
        "888290158e77937a706a9c5ca7e8f61dd5ae412df5a53417f27e444f128815f4",
    "run_receipt.json":
        "745b853be897690264271064d05deb5bea3032c4ae0c85b033be542dc2c0fd12",
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def integer(x):
    return type(x) is int

def load_json(b):
    def unique(pairs):
        out = {}
        for k, v in pairs:
            need(k not in out, "Duplicate JSON key: " + k)
            out[k] = v
        return out
    def bad_constant(x):
        raise ValueError("Invalid JSON constant: " + x)
    return json.loads(
        b, object_pairs_hook=unique, parse_constant=bad_constant
    )

def valid_points(xs, size):
    need(type(xs) is list and len(xs) == size, "Point-list size")
    need(all(integer(x) and 0 <= x < 64 for x in xs), "Invalid point")
    need(len(set(xs)) == size, "Repeated point")
    return tuple(sorted(xs))

def span(b):
    out = {0}
    for v in b:
        out |= {x ^ v for x in tuple(out)}
    return tuple(sorted(out))

def rref2(b):
    a = list(b)
    r = 0
    for col in range(6):
        p = next(
            (i for i in range(r, len(a)) if (a[i] >> col) & 1),
            None
        )
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        for i in range(len(a)):
            if i != r and ((a[i] >> col) & 1):
                a[i] ^= a[r]
        r += 1
    return tuple(a[:r])

def cosets(U):
    left = set(range(64))
    while left:
        c = min(left)
        F = tuple(sorted(c ^ u for u in U))
        need(set(F) <= left, "Overlapping cosets")
        left.difference_update(F)
        yield c, F

def feature(x):
    b = [(x >> i) & 1 for i in range(6)]
    return tuple(
        [1] + b + [b[i] * b[j] for i, j in it.combinations(range(6), 2)]
    )

V = tuple(feature(x) for x in range(64))

def character_rank(b):
    signatures = {
        sum(((v >> i) & 1) << j for j, v in enumerate(b))
        for i in range(6)
    }
    return len(
        {0} | signatures |
        {u ^ v for u in signatures for v in signatures}
    )

def augmented_rref(U):
    rows = [
        list(map(Q, V[u])) + [Q(i == j) for j in range(8)]
        for i, u in enumerate(U)
    ]
    pivots = []
    r = 0
    for col in range(22):
        p = next((i for i in range(r, 8) if rows[i][col]), None)
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        t = rows[r][col]
        rows[r] = [v / t for v in rows[r]]
        for i in range(8):
            if i != r and rows[i][col]:
                t = rows[i][col]
                rows[i] = [
                    x - t * y for x, y in zip(rows[i], rows[r])
                ]
        pivots.append(col)
        r += 1
        if r == 8:
            break
    need(r == 8, "Independent rational base-rank failure")
    return rows, pivots

def reduce_point(x, rows, pivots):
    residual = list(map(Q, V[x]))
    coeff = [Q(0)] * 8
    for row, pivot in zip(rows, pivots):
        t = residual[pivot]
        if t:
            residual = [
                a - t * b for a, b in zip(residual, row[:22])
            ]
            coeff = [
                a + t * b for a, b in zip(coeff, row[22:])
            ]
    scale = next((v for v in residual if v), None)
    key = tuple(v / scale for v in residual) if scale else None
    return key, scale, coeff

def run(data_dir, output_dir):
    started = datetime.now(timezone.utc).isoformat()
    source_hash = sha(Path(__file__).read_bytes())
    blobs = {n: (data_dir / n).read_bytes() for n in PIN}
    before = {n: sha(b) for n, b in blobs.items()}
    need(before == PIN, "Pinned input hash mismatch")
    data = {n: load_json(b) for n, b in blobs.items()}
    census = data["flat_census.json"]
    history = data["ten_point_circuit_search.json"]
    receipt = data["run_receipt.json"]

    need(all(P % d for d in range(2, math.isqrt(P) + 1)), "Prime test")
    need(P > 4096, "Rank-preservation determinant bound")
    distribution = {"7": 2800, "8": 8360}

    for key, value in {
        "dimension": 6,
        "point_count": 64,
        "feature_count": 22,
        "direction_count": 1395,
        "flat_count": 11160,
        "modular_field": "F_2147483629",
        "rank_Q_distribution": distribution,
        "rank_Fp_distribution": distribution,
        "modular_rank_exception_count": 0,
    }.items():
        need(census.get(key) == value, "Census metadata: " + key)

    for key, value in {
        "status": "COMPUTATION_COMPLETE",
        "prime": P,
        "expected_direction_count": 1395,
        "observed_direction_count": 1395,
        "expected_flat_count": 11160,
        "observed_flat_count": 11160,
        "geometry_gate": "PASS",
        "rank_eight_gate": "PASS",
        "rank_Q_distribution": distribution,
        "rank_Fp_distribution": distribution,
        "modular_rank_exception_count": 0,
        "flat_census_sha256": PIN["flat_census.json"],
    }.items():
        need(receipt.get(key) == value, "Receipt field: " + key)
    need(receipt.get("prime_verified") is True, "Receipt prime flag")
    generator = data_dir / "sixbit_flats.py"
    need(generator.is_file(), "Missing historical generator")
    generator_hash = sha(generator.read_bytes())
    need(generator_hash == receipt.get("script_sha256"),
         "Historical generator hash mismatch")
    print("PASS: pinned inputs, receipt semantics, prime and generator binding",
          flush=True)

    dirs = {}
    for b in it.combinations(range(1, 64), 3):
        U = span(b)
        if len(U) == 8:
            dirs.setdefault(U, rref2(b))
    need(len(dirs) == 1395, "Independent direction count")
    expected = {F for U in dirs for c, F in cosets(U)}
    need(len(expected) == 11160, "Independent flat count")

    records = census.get("flats")
    need(type(records) is list and len(records) == 11160, "Flat records")
    index = {}
    ids = set()
    did_to_U = {}
    U_to_did = {}
    ranks = Counter()

    for f in records:
        F = valid_points(f["points"], 8)
        need(F in expected and F not in index, "Flat coverage/duplication")
        fid, did = f["flat_id"], f["direction_id"]
        need(integer(fid) and fid >= 0 and fid not in ids, "Flat ID")
        need(integer(did) and did >= 0, "Direction ID")
        b = f["direction_rref"]
        need(type(b) is list and len(b) == 3, "Basis size")
        need(all(integer(v) and 0 < v < 64 for v in b), "Basis vector")
        U = span(b)
        need(U in dirs and tuple(b) == dirs[U], "Canonical basis")
        need(tuple(sorted(p ^ F[0] for p in F)) == U, "Flat geometry")
        need(integer(f["coset_representative"]) and
             f["coset_representative"] == F[0], "Coset representative")
        need(did not in did_to_U or did_to_U[did] == U, "Direction ID reuse")
        need(U not in U_to_did or U_to_did[U] == did, "Direction relabelling")
        rank = character_rank(b)
        for name in ("rank_Q", "rank_Fp"):
            need(integer(f[name]) and f[name] == rank, "Incorrect " + name)
        need(f.get("modular_rank_exception") is False, "Modular exception")
        ids.add(fid)
        did_to_U[did] = U
        U_to_did[U] = did
        index[F] = (fid, did, U)
        ranks[rank] += 1

    need(set(index) == expected, "Incomplete flat coverage")
    need(ids == set(range(11160)), "Incomplete flat IDs")
    need(set(did_to_U) == set(range(1395)), "Incomplete direction IDs")
    need(ranks == Counter({7: 2800, 8: 8360}), "Independent rank distribution")
    print("PASS: all 1395 directions and 11160 flats independently reconciled",
          flush=True)

    need(history.get("status") == "CIRCUITS_VERIFIED", "Historical status")
    need(history.get("census_sha256") == PIN["flat_census.json"],
         "Historical census binding")
    need(history.get("rank_eight_flats_processed") == 8360,
         "Historical flat count")
    need(history.get("verified_circuit_count") == 22400,
         "Historical circuit count")
    need(history.get("candidate_pair_count") == 22400,
         "Historical candidate count")
    need(history.get("failed_candidate_count") == 0,
         "Historical candidate failures")
    need(history.get("actual_generator_sha256") == generator_hash,
         "Search generator binding")
    need(history.get("receipt_generator_sha256") == generator_hash,
         "Search receipt-generator binding")
    need(history.get("generator_hash_matches_receipt") is True,
         "Search generator-match flag")

    byid = {fid: (F, did, U) for F, (fid, did, U) in index.items()}
    historical = Counter()
    ledger = history.get("circuits")
    need(type(ledger) is list and len(ledger) == 22400, "Ledger length")
    for rec in ledger:
        S = valid_points(rec["points"], 10)
        fid, did = rec["flat_id"], rec["direction_id"]
        need(integer(fid) and fid in byid and integer(did), "Ledger IDs")
        F, expected_did, U = byid[fid]
        need(did == expected_did and character_rank(dirs[U]) == 8,
             "Ledger base binding")
        need(set(F) <= set(S), "Ledger base missing")
        need(rec.get("circuit_verified") is True, "Ledger verification flag")
        need(integer(rec.get("full_rank_Q")) and rec["full_rank_Q"] == 9,
             "Ledger rank claim")
        dr = rec.get("deletion_ranks_Q")
        need(type(dr) is list and len(dr) == 10 and
             all(integer(v) and v == 9 for v in dr), "Ledger deletion claims")
        historical[(fid, did, S)] += 1
    need(len(historical) == 22400 and
         all(v == 1 for v in historical.values()), "Ledger duplicates")
    need(len({k[2] for k in historical}) == 22400, "Ledger support duplicates")

    reconstructed = Counter()
    directions_checked = 0
    direct_kernels = 0
    affine_instances = 0
    for U, b in sorted(dirs.items()):
        if character_rank(b) != 8:
            continue
        rows, pivots = augmented_rref(U)
        groups = defaultdict(list)
        for x in range(64):
            if x in U:
                continue
            key, scale, coeff = reduce_point(x, rows, pivots)
            need(key is not None, "Zero quotient point")
            groups[key].append((x, scale, coeff))

        for group in groups.values():
            for (x, sx, cx), (y, sy, cy) in it.combinations(group, 2):
                need((x ^ y) in U, "Displacement counterexample")
                t = sx / sy
                kernel = [-(a - t * b) for a, b in zip(cx, cy)]
                kernel += [Q(1), -t]
                support = U + (x, y)
                need(all(kernel), "Kernel has zero coefficient")
                need(all(
                    sum(k * V[p][j] for p, k in zip(support, kernel)) == 0
                    for j in range(22)
                ), "Kernel identity failure")
                direct_kernels += 1

                for c, F in cosets(U):
                    xx, yy = x ^ c, y ^ c
                    need((xx ^ yy) in U, "Translated displacement")
                    S = tuple(sorted(F + (xx, yy)))
                    fid, did, unused = index[F]
                    reconstructed[(fid, did, S)] += 1
                    affine_instances += 1

        directions_checked += 1
        if directions_checked % 100 == 0:
            print("Rank-eight directions processed:", directions_checked,
                  "affine instances:", affine_instances, flush=True)

    need(directions_checked == 1045, "Rank-eight direction coverage")
    need(direct_kernels == 2800, "Direct kernel count")
    need(affine_instances == 22400, "Affine certificate count")
    need(len(reconstructed) == 22400 and
         all(v == 1 for v in reconstructed.values()), "Reconstruction duplicates")
    need(len({k[2] for k in reconstructed}) == 22400,
         "Multiple flat representations")
    need(reconstructed == historical, "Historical incidence-counter mismatch")

    after = {n: sha((data_dir / n).read_bytes()) for n in PIN}
    need(after == before, "Pinned input changed during execution")
    need(sha(generator.read_bytes()) == generator_hash, "Generator changed")
    need(sha(Path(__file__).read_bytes()) == source_hash, "Verifier changed")
    payload = json.dumps(
        [[a, b, list(c), v] for (a, b, c), v in sorted(reconstructed.items())],
        separators=(",", ":")
    ).encode()

    report = {
        "status": "PASS",
        "gate": "SIXBIT-VERIFY-002",
        "started_utc": started,
        "finished_utc": datetime.now(timezone.utc).isoformat(),
        "python_version": sys.version,
        "source_sha256": source_hash,
        "input_sha256": before,
        "historical_generator_sha256": generator_hash,
        "receipt_semantics_verified": True,
        "prime": P,
        "modular_rank_method":
            "Rational character rank plus prime and Hadamard minor bound",
        "directions_verified": len(dirs),
        "flats_verified": len(index),
        "rank_distribution": dict(ranks),
        "rank_eight_directions_checked": directions_checked,
        "direct_kernel_checks": direct_kernels,
        "affine_circuit_instances_certified": affine_instances,
        "covered_outside_pair_universe_size": 8360 * 1540,
        "pair_universe_individually_enumerated": False,
        "incidence_counter_sha256": sha(payload),
        "historical_incidence_equality": True,
        "inputs_unchanged": True,
        "scope":
            "Finite rank-eight-affine-flat-containing circuit family, "
            "displacement and historical incidence equality. "
            "Not global ten-point circuit completeness. "
            "Mutation suite not run by this verifier."
    }
    with (output_dir / "PASS.json").open("x") as f:
        json.dump(report, f, indent=2, sort_keys=True)
        print(file=f)
    print(json.dumps(report, indent=2, sort_keys=True))

if __name__ == "__main__":
    output = Path(__file__).resolve().parent
    try:
        need(len(sys.argv) == 2, "Usage: verify.py DATA_DIRECTORY")
        run(Path(sys.argv[1]).expanduser().resolve(), output)
    except Exception as exc:
        failure = {
            "status": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "source_sha256": sha(Path(__file__).read_bytes()),
        }
        target = output / "FAIL.json"
        if not target.exists():
            with target.open("x") as f:
                json.dump(failure, f, indent=2, sort_keys=True)
                print(file=f)
        print("FAIL:", type(exc).__name__ + ":", str(exc), file=sys.stderr)
        sys.exit(2)
