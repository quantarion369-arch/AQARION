#!/usr/bin/env python3
import argparse
import hashlib
import itertools
import json
import math
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

EXPECTED = {
    "flat_census.json": "5e684e0152d240534632a9c0dc4916727c5b80e4baa5243727098a0710a1e161",
    "run_receipt.json": "745b853be897690264271064d05deb5bea3032c4ae0c85b033be542dc2c0fd12",
    "ten_point_circuit_search.json": "888290158e77937a706a9c5ca7e8f61dd5ae412df5a53417f27e444f128815f4",
}
N_FLATS = 11160
N_RANK7 = 2800
N_RANK8 = 8360
N_CIRCUITS = 22400
N_OUTSIDE = 56
N_PAIRS = math.comb(N_OUTSIDE, 2)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def feature(x):
    b = [(x >> i) & 1 for i in range(6)]
    return [1] + b + [b[i] * b[j] for i in range(6) for j in range(i + 1, 6)]


V = [feature(x) for x in range(64)]


def rref_q(matrix):
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return a, []
    m, n = len(a), len(a[0])
    pivots = []
    r = 0
    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        q = a[r][c]
        a[r] = [x / q for x in a[r]]
        for i in range(m):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [a[i][j] - q * a[r][j] for j in range(n)]
        pivots.append(c)
        r += 1
        if r == m:
            break
    return a, pivots


def nullspace(A):
    R, pivots = rref_q(A)
    n = len(A[0])
    pivot_set = set(pivots)
    basis = []
    for f in range(n):
        if f in pivot_set:
            continue
        w = [Fraction(0) for _ in range(n)]
        w[f] = Fraction(1)
        for i, p in enumerate(pivots):
            w[p] = -R[i][f]
        basis.append(w)
    return basis


def projective_key(q):
    first = next((x for x in q if x), None)
    if first is None:
        return None
    return tuple(x / first for x in q)


def bareiss_rank(matrix):
    if not matrix or not matrix[0]:
        return 0
    a = [list(map(int, row)) for row in matrix]
    m, n = len(a), len(a[0])
    r, previous = 0, 1
    for c in range(n):
        p = next((i for i in range(r, m) if a[i][c] != 0), None)
        if p is None:
            continue
        if p != r:
            a[r], a[p] = a[p], a[r]
        pivot = a[r][c]
        for i in range(r + 1, m):
            for j in range(c + 1, n):
                numerator = a[i][j] * pivot - a[i][c] * a[r][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss exact-division failure")
                a[i][j] = numerator // previous
            a[i][c] = 0
        previous = pivot
        r += 1
        if r == m:
            break
    return r


def support_key(points):
    p = tuple(sorted(map(int, points)))
    if len(p) != 10 or len(set(p)) != 10 or any(x < 0 or x >= 64 for x in p):
        raise ValueError("Invalid ten-point support: " + repr(p))
    return p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--allow-nonbaseline-hashes", action="store_true")
    args = ap.parse_args()

    D = Path(args.data_dir).expanduser().resolve()
    O = Path(args.output_dir).expanduser().resolve()
    paths = {name: D / name for name in EXPECTED}
    for p in paths.values():
        if not p.is_file():
            raise FileNotFoundError(p)

    before = {name: sha(p) for name, p in paths.items()}
    hash_match = {name: before[name] == EXPECTED[name] for name in EXPECTED}
    if not all(hash_match.values()) and not args.allow_nonbaseline_hashes:
        raise ValueError("Historical SHA-256 mismatch; audit stopped without processing.")

    if O.exists():
        if not O.is_dir() or any(O.iterdir()):
            raise FileExistsError("Output directory must be empty: " + str(O))
    else:
        O.mkdir(parents=True)

    census = json.loads(paths["flat_census.json"].read_text())
    search = json.loads(paths["ten_point_circuit_search.json"].read_text())

    flats = census.get("flats", [])
    records = search.get("circuits", [])

    if len(flats) != N_FLATS or census.get("flat_count") != N_FLATS:
        raise ValueError("Unexpected census size")
    if search.get("status") != "CIRCUITS_VERIFIED":
        raise ValueError("Historical search status mismatch")
    if search.get("rank_eight_flats_processed") != N_RANK8:
        raise ValueError("Historical rank-eight count mismatch")
    if search.get("verified_circuit_count") != N_CIRCUITS:
        raise ValueError("Historical verified circuit count mismatch")
    if search.get("census_sha256") != before["flat_census.json"]:
        raise ValueError("Search record refers to a different census hash")
    if len(records) != N_CIRCUITS:
        raise ValueError("Historical circuit record count mismatch")

    # Independent rank-engine sanity checks against exact rational elimination.
    tests = [
        ([], 0),
        ([[0, 0], [0, 0]], 0),
        ([[0, 1, 2], [0, 2, 4]], 1),
        ([[0, 1, 0], [1, 0, 1]], 2),
        ([[2, 4, 6], [1, 2, 3], [0, 1, 1]], 2),
        ([[1, 2], [3, 4], [5, 6]], 2),
    ]
    for M, expected in tests:
        got = bareiss_rank(M)
        exact = len(rref_q(M)[1])
        if got != expected or got != exact:
            raise AssertionError("Bareiss self-test failed")

    rank8 = [f for f in flats if int(f.get("rank_Q", -1)) == 8]
    rank7 = [f for f in flats if int(f.get("rank_Q", -1)) == 7]
    if len(rank8) != N_RANK8 or len(rank7) != N_RANK7:
        raise ValueError("Historical rank distribution mismatch")

    historical = Counter()
    for rec in records:
        if rec.get("circuit_verified") is not True:
            raise ValueError("Historical record not marked verified")
        historical[support_key(rec["points"])] += 1

    reconstructed = Counter()
    per_flat = []
    failures = []
    totals = Counter()
    minimality_checks = 0

    for index, flat in enumerate(rank8, 1):
        fid = int(flat["flat_id"])
        base = tuple(sorted(map(int, flat["points"])))
        if len(base) != 8 or len(set(base)) != 8:
            raise ValueError("Invalid base at flat " + str(fid))
        A = [V[x] for x in base]
        if bareiss_rank(A) != 8:
            raise ValueError("Independent base rank failure at flat " + str(fid))

        ns = nullspace(A)
        if len(ns) != 14:
            raise ValueError("Nullity is not 14 at flat " + str(fid))

        base_set = set(base)
        outside = [x for x in range(64) if x not in base_set]
        if len(outside) != N_OUTSIDE:
            raise AssertionError("Outside point count mismatch")

        groups = defaultdict(list)
        zeros = []
        for x in outside:
            q = tuple(
                sum((Fraction(V[x][j]) * ns[k][j] for j in range(22)), Fraction(0))
                for k in range(14)
            )
            key = projective_key(q)
            if key is None:
                zeros.append(x)
            else:
                groups[key].append(x)

        z = len(zeros)
        nz = N_OUTSIDE - z
        sizes = sorted((len(g) for g in groups.values()), reverse=True)
        zz = math.comb(z, 2)
        zn = z * nz
        prop = sum(math.comb(s, 2) for s in sizes)
        nonprop = sum(sizes[i] * sizes[j]
                      for i in range(len(sizes))
                      for j in range(i + 1, len(sizes)))
        accounted = zz + zn + prop + nonprop
        if accounted != N_PAIRS:
            raise AssertionError("Pair partition failed at flat " + str(fid))

        flat_failures = 0
        for group in groups.values():
            for x, y in itertools.combinations(sorted(group), 2):
                support = tuple(sorted(base + (x, y)))
                full = bareiss_rank([V[p] for p in support])
                deletions = [
                    bareiss_rank([V[p] for p in support if p != deleted])
                    for deleted in support
                ]
                minimality_checks += 1
                if full != 9 or any(r != 9 for r in deletions):
                    flat_failures += 1
                    failures.append({
                        "flat_id": fid,
                        "support": list(support),
                        "full_rank": full,
                        "deletion_ranks": deletions,
                    })
                else:
                    reconstructed[support] += 1

        totals.update({
            "incidences": N_PAIRS,
            "zero_zero": zz,
            "zero_nonzero": zn,
            "proportional_candidates": prop,
            "nonproportional": nonprop,
        })
        per_flat.append({
            "flat_id": fid,
            "base_points": list(base),
            "outside_points": N_OUTSIDE,
            "outside_pairs": N_PAIRS,
            "zero_quotient_points": z,
            "nonzero_projective_classes": len(groups),
            "class_sizes_descending": sizes,
            "zero_zero_pairs": zz,
            "zero_nonzero_pairs": zn,
            "proportional_candidate_pairs": prop,
            "nonproportional_pairs": nonprop,
            "accounted_pairs": accounted,
            "minimality_failures": flat_failures,
        })

        if index % 250 == 0:
            print(f"Processed {index}/{N_RANK8} bases", flush=True)

    missing = sorted(set(historical) - set(reconstructed))
    extra = sorted(set(reconstructed) - set(historical))
    dup_hist = [{"support": list(k), "count": v}
                for k, v in sorted(historical.items()) if v != 1]
    dup_recon = [{"support": list(k), "count": v}
                 for k, v in sorted(reconstructed.items()) if v != 1]

    after = {name: sha(p) for name, p in paths.items()}
    unchanged = before == after

    checks = {
        "input_hashes_match_baseline": all(hash_match.values()) or args.allow_nonbaseline_hashes,
        "all_8360_rank_eight_bases_processed": len(per_flat) == N_RANK8,
        "all_base_ranks_independently_verified": True,
        "all_nullspace_dimensions_are_14": True,
        "total_pair_incidences_are_12874400": totals["incidences"] == N_RANK8 * N_PAIRS,
        "all_per_flat_pair_partitions_complete": all(x["accounted_pairs"] == N_PAIRS for x in per_flat),
        "candidate_occurrences_are_22400": totals["proportional_candidates"] == N_CIRCUITS,
        "all_candidate_minimality_tests_pass": len(failures) == 0,
        "reconstructed_verified_occurrences_are_22400": sum(reconstructed.values()) == N_CIRCUITS,
        "historical_unique_supports_are_22400": len(historical) == N_CIRCUITS,
        "reconstructed_unique_supports_are_22400": len(reconstructed) == N_CIRCUITS,
        "no_missing_historical_supports": not missing,
        "no_extra_reconstructed_supports": not extra,
        "no_duplicate_historical_supports": not dup_hist,
        "no_duplicate_reconstructed_supports": not dup_recon,
        "historical_inputs_unchanged": unchanged,
    }
    status = "PASS" if all(checks.values()) else "FAIL"

    report = {
        "title": "Independent Rational-Nullspace Incidence Completeness Audit",
        "status": status,
        "scope": "Completeness relative to supplied historical flat census; does not regenerate the census or prove the global structural containment theorem.",
        "method": "Independent exact rational right-nullspace basis, projective quotient grouping, fraction-free Bareiss rank and deletion-rank checks.",
        "quotient": "For each rank-eight base B, use a Q-basis n_1,...,n_14 of ker(A_B); q_B(x)=(v(x)n_1,...,v(x)n_14).",
        "pair_partition": "1540 = C(z,2) + z(56-z) + sum C(s_i,2) + sum_{i<j} s_i*s_j",
        "expected": {
            "flats": N_FLATS,
            "rank_seven_flats": N_RANK7,
            "rank_eight_flats": N_RANK8,
            "outside_pairs_per_base": N_PAIRS,
            "total_incidences": N_RANK8 * N_PAIRS,
            "historical_circuits": N_CIRCUITS,
        },
        "observed": {
            "rank_eight_bases_processed": len(per_flat),
            "incidences": totals["incidences"],
            "zero_zero_pairs": totals["zero_zero"],
            "zero_nonzero_pairs": totals["zero_nonzero"],
            "proportional_candidate_occurrences": totals["proportional_candidates"],
            "nonproportional_pairs": totals["nonproportional"],
            "minimality_checks": minimality_checks,
            "verified_reconstructed_occurrences": sum(reconstructed.values()),
            "unique_reconstructed_supports": len(reconstructed),
            "unique_historical_supports": len(historical),
        },
        "input_sha256_before": before,
        "input_sha256_after": after,
        "baseline_hash_matches": hash_match,
        "checks": checks,
        "minimality_failure_count": len(failures),
        "missing_support_count": len(missing),
        "extra_support_count": len(extra),
        "duplicate_historical_support_count": len(dup_hist),
        "duplicate_reconstructed_support_count": len(dup_recon),
    }

    reconciliation = {
        "historical_occurrences": sum(historical.values()),
        "historical_unique_supports": len(historical),
        "reconstructed_verified_occurrences": sum(reconstructed.values()),
        "reconstructed_unique_supports": len(reconstructed),
        "missing_historical_supports": [list(x) for x in missing],
        "extra_reconstructed_supports": [list(x) for x in extra],
        "duplicate_historical_supports": dup_hist,
        "duplicate_reconstructed_supports": dup_recon,
        "minimality_failures": failures,
    }

    (O / "independent_incidence_completeness_report.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n")
    (O / "per_flat_incidence_accounting.json").write_text(
        json.dumps(per_flat, indent=2, sort_keys=True) + "\n")
    (O / "support_reconciliation.json").write_text(
        json.dumps(reconciliation, indent=2, sort_keys=True) + "\n")

    print(json.dumps({
        "status": status,
        "output_dir": str(O),
        "observed": report["observed"],
        "checks": checks,
        "input_hashes_before": before,
        "input_hashes_after": after,
    }, indent=2, sort_keys=True))
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"AUDIT_ABORTED: {type(e).__name__}: {e}", file=sys.stderr)
        raise
