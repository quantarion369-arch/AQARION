#!/usr/bin/env python3
"""SIXBIT-NOVELTY-001: independent balanced-support novelty experiment."""
import argparse
import hashlib
import itertools
import json
import random
from datetime import datetime, timezone
from pathlib import Path

def vertex_permute(x, p):
    y = 0
    for i, j in enumerate(p):
        if (x >> i) & 1:
            y |= 1 << j
    return y

def support_mask(points):
    m = 0
    for x in points:
        m |= 1 << x
    return m

def decode_support(m):
    return [x for x in range(64) if (m >> x) & 1]

def balance_check(pos, neg):
    if len(pos) != 6 or len(neg) != 6:
        return False
    if len(set(pos)) != 6 or len(set(neg)) != 6:
        return False
    if set(pos) & set(neg):
        return False
    if sum(pos) < 0:  # harmless type guard
        return False
    for j in range(6):
        if sum((x >> j) & 1 for x in pos) != \
           sum((x >> j) & 1 for x in neg):
            return False
    return True

def make_candidate(rng):
    # A: six independent random six-bit vertices.
    pos = [rng.randrange(64) for _ in range(6)]
    if len(set(pos)) != 6:
        return None

    # B: each column is a random permutation of A's same column.
    neg = [0] * 6
    for j in range(6):
        col = [(x >> j) & 1 for x in pos]
        rng.shuffle(col)
        for i, bit in enumerate(col):
            neg[i] |= bit << j

    if not balance_check(pos, neg):
        return None

    return sorted(pos), sorted(neg)

def build_permutation_maps():
    perms = list(itertools.permutations(range(6)))
    maps = [
        [vertex_permute(x, p) for x in range(64)]
        for p in perms
    ]
    return perms, maps

def transform_support(points, pmap, flip):
    m = 0
    for x in points:
        m |= 1 << (pmap[x] ^ flip)
    return m

def canonical_orbit(points, maps):
    best = None
    for pmap in maps:
        base = [pmap[x] for x in points]
        for flip in range(64):
            m = 0
            for x in base:
                m |= 1 << (x ^ flip)
            if best is None or m < best:
                best = m
    return best

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("catalog", type=Path)
    ap.add_argument("output", type=Path)
    ap.add_argument("--attempts", type=int, default=50000)
    ap.add_argument("--max-orbits", type=int, default=25)
    ap.add_argument("--seed", type=int, default=377001)
    args = ap.parse_args()

    data = json.loads(args.catalog.read_text())
    reps = data["six_bit_simple_orbits"]
    if len(reps) != 32:
        raise SystemExit(f"FAIL: expected 32 representatives; got {len(reps)}")

    rng = random.Random(args.seed)
    perms, maps = build_permutation_maps()

    # Expand catalog orbits exactly under coordinate permutations + bit flips.
    known = set()
    for rec in reps:
        support = rec["support"]
        if len(support) != 12 or len(set(support)) != 12:
            raise SystemExit("FAIL: malformed catalog support")
        for pmap in maps:
            base = [pmap[x] for x in support]
            for flip in range(64):
                known.add(support_mask(x ^ flip for x in base))

    if len(known) != 206304:
        raise SystemExit(
            f"FAIL: catalog orbit union={len(known)}, expected 206304"
        )

    found = {}
    counters = {
        "attempts": 0,
        "invalid": 0,
        "known_orbit_hits": 0,
        "novel_supports": 0,
        "novel_orbits": 0,
    }

    for trial in range(args.attempts):
        counters["attempts"] += 1
        candidate = make_candidate(rng)
        if candidate is None:
            counters["invalid"] += 1
            continue

        pos, neg = candidate
        points = sorted(pos + neg)
        sm = support_mask(points)

        if sm in known:
            counters["known_orbit_hits"] += 1
            continue

        counters["novel_supports"] += 1
        canon = canonical_orbit(points, maps)

        if canon in found:
            found[canon]["encounters"] += 1
            continue

        found[canon] = {
            "canonical_support_mask_hex": hex(canon),
            "support": points,
            "positive_vertices": pos,
            "negative_vertices": neg,
            "kernel": [1 if x in set(pos) else -1 for x in points],
            "coordinate_balance": [0] * 6,
            "constant_balance": 0,
            "encounters": 1,
            "support_sha256": hashlib.sha256(
                json.dumps(points, separators=(",", ":")).encode()
            ).hexdigest(),
            "status": "NOVEL_BALANCED_SUPPORT_CANDIDATE",
            "rank_Q": "NOT_TESTED",
            "circuit_minimality": "NOT_TESTED",
        }

        counters["novel_orbits"] = len(found)
        if len(found) >= args.max_orbits:
            break

    args.output.mkdir(parents=True, exist_ok=True)
    ledger = {
        "experiment": "SIXBIT-NOVELTY-001",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "seed": args.seed,
        "generator": "independent_column_permutations",
        "group": "Q6 = coordinate permutations × coordinate flips",
        "group_order": 46080,
        "catalog_representatives": 32,
        "catalog_orbit_union": len(known),
        "scope": {
            "balance": "constant plus six coordinate-bit rows",
            "novelty": "outside retained 32 catalog orbits",
            "rank": "not tested",
            "minimality": "not tested",
            "global_completeness": False,
        },
        "counters": counters,
        "discoveries": list(found.values()),
    }

    out = args.output / "NOVELTY-001-LEDGER.json"
    out.write_text(json.dumps(ledger, indent=2) + "\n")
    print("=== SIXBIT-NOVELTY-001 ===")
    print("CATALOG ORBIT UNION:", len(known))
    for k, v in counters.items():
        print(f"{k}: {v}")
    print("LEDGER:", out)
    print("CATALOG AUDIT: PASS" if len(known) == 206304 else "CATALOG AUDIT: FAIL")
    print("NOVEL ORBITS DISCOVERED:", len(found))
    print("CLAIM: balanced novelty candidates only; no circuit claim")

if __name__ == "__main__":
    main()
