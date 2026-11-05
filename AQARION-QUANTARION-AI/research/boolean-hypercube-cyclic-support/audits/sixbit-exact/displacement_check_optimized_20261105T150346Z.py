from fractions import Fraction
from math import gcd, lcm
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT / "independent-incidence-completeness-20261105T141430Z"
SOURCE = AUDIT / "independent_incidence_completeness_audit.py"

spec = importlib.util.spec_from_file_location("inc_audit", SOURCE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def fast_projective_key(q):
    q = tuple(q)
    den = 1
    for x in q:
        x = Fraction(x)
        den = lcm(den, x.denominator)

    vals = [
        Fraction(x).numerator * (den // Fraction(x).denominator)
        for x in q
    ]

    g = 0
    for x in vals:
        g = gcd(g, abs(x))

    if g == 0:
        return None

    vals = [x // g for x in vals]
    first = next(x for x in vals if x)
    if first < 0:
        vals = [-x for x in vals]
    return tuple(vals)

def xor_span(basis):
    span = {0}
    for v in basis:
        span |= {x ^ v for x in tuple(span)}
    return span

def main():
    census_path = ROOT / "flat_census.json"
    history_path = ROOT / "ten_point_circuit_search.json"

    for p in (census_path, history_path):
        if not p.is_file():
            raise RuntimeError(f"Missing input: {p}")

    census = json.loads(census_path.read_text())
    history = json.loads(history_path.read_text())

    print("CENSUS KEYS:", list(census))
    print("HISTORY KEYS:", list(history))

    flats = census["flats"]
    circuits = history["circuits"]

    print("flats:", len(flats), "historical circuits:", len(circuits))
    if circuits:
        print("historical circuit record keys:", list(circuits[0]))

    V = mod.V
    nullspace = mod.nullspace

    checked_flats = 0
    pair_occurrences = 0
    zero_quotient_points = 0
    displacement_failures = []
    reconstructed = set()

    for fi, flat in enumerate(flats):
        if flat.get("rank_Q") != 8:
            continue

        fid = flat["flat_id"]
        did = flat["direction_id"]
        points = flat["points"]
        direction = xor_span(flat["direction_rref"])

        A = [V[x] for x in points]
        ns = nullspace(A)

        classes = {}

        for x in range(64):
            if x in points:
                continue

            q = tuple(
                sum((V[x][j] * ns[k][j] for j in range(len(V[x]))), Fraction(0))
                for k in range(len(ns))
            )

            key = fast_projective_key(q)
            if key is None:
                zero_quotient_points += 1
                continue

            classes.setdefault(key, []).append(x)

        for group in classes.values():
            if len(group) < 2:
                continue

            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    x, y = group[i], group[j]
                    pair_occurrences += 1

                    if (x ^ y) not in direction:
                        displacement_failures.append((fid, did, x, y))

                    support = tuple(sorted(points + [x, y]))
                    reconstructed.add((fid, did, support))

        checked_flats += 1

        if checked_flats % 250 == 0:
            print(
                "progress flats=", checked_flats,
                "pairs=", pair_occurrences,
                "zero_quotient_points=", zero_quotient_points,
                flush=True
            )

    # Exact incidence-level reconciliation against historical records.
    from collections import Counter

    historical_keys = []
    malformed = []

    for i, record in enumerate(circuits):
        try:
            key = (
                record["flat_id"],
                record["direction_id"],
                tuple(sorted(record["points"]))
            )
            if len(key[2]) != 10 or len(set(key[2])) != 10:
                malformed.append((i, "support is not ten distinct points"))
            historical_keys.append(key)
        except Exception as exc:
            malformed.append((i, repr(exc)))

    historical_counter = Counter(historical_keys)
    reconstructed_counter = Counter(reconstructed)

    missing = list((historical_counter - reconstructed_counter).elements())
    extra = list((reconstructed_counter - historical_counter).elements())
    duplicate_historical = [
        (key, count) for key, count in historical_counter.items() if count > 1
    ]

    incidence_match = (
        not malformed
        and not missing
        and not extra
        and not duplicate_historical
        and len(historical_keys) == len(reconstructed)
    )

    print("\\n=== HISTORICAL INCIDENCE RECONCILIATION ===")
    print("historical records:", len(historical_keys))
    print("historical unique incidence keys:", len(historical_counter))
    print("reconstructed unique incidence keys:", len(reconstructed))
    print("malformed historical records:", len(malformed))
    print("duplicate historical incidence keys:", len(duplicate_historical))
    print("historical keys missing from reconstruction:", len(missing))
    print("unexpected reconstructed keys:", len(extra))
    print("EXACT INCIDENCE MATCH:", incidence_match)

    if malformed:
        print("first malformed records:", malformed[:5])
    if missing:
        print("first missing keys:", missing[:5])
    if extra:
        print("first unexpected keys:", extra[:5])
    if duplicate_historical:
        print("first duplicate keys:", duplicate_historical[:5])

    print("\n=== DISPLACEMENT AUDIT ===")
    print("rank-eight flats:", checked_flats)
    print("proportional quotient pairs:", pair_occurrences)
    print("zero quotient points:", zero_quotient_points)
    print("displacement failures:", len(displacement_failures))
    print("reconstructed incidence keys:", len(reconstructed))

    if displacement_failures:
        print("first failures:", displacement_failures[:10])

    print("\n=== STATUS ===")
    if displacement_failures:
        print("FAIL: displacement containment counterexample found")
    else:
        print("PASS: displacement containment on reconstructed proportional pairs")

    print("NOTE: historical incidence reconciliation is not yet asserted.")
    print("This run does not establish a general-dimensional theorem.")

if __name__ == "__main__":
    main()
