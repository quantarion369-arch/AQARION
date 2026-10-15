#!/usr/bin/env python3
"""
Independent assessment layer + mutation harness for the EC fixtures.

Verdict rule (the one in the checkpoint report):
    REFUTED  iff  exists witness w with  D(w) and H(w) and not C(w)
    OPEN     otherwise (finite witnesses can never establish a universal claim)

Key design points
  * C(w) is RECOMPUTED from the witness parameter c -- never read from the
    witness's own label (that was the rejected circularity flaw).
  * "stable" is not defined in the fixtures, so it is an explicit parameter.
    Two readings are implemented; results are reported under both.
Stdlib only.
"""
import json, sys

# ---------------------------------------------------------------- stability
def stable_bounded_orbit(c, iters=500):
    """x -> x^2 + c on the reals, start x=0; stable iff orbit stays bounded."""
    x = 0.0
    for _ in range(iters):
        x = x * x + c
        if abs(x) > 2.0:          # once |x|>2 (and |c|<=2) it provably escapes
            return False
    return True

def stable_attracting_fixed_point(c):
    """stable iff a real fixed point x* of x^2+c exists with |2x*| < 1."""
    disc = 1.0 - 4.0 * c
    if disc < 0:
        return False
    r = disc ** 0.5
    for xs in ((1 + r) / 2, (1 - r) / 2):
        if abs(2 * xs) < 1:
            return True
    return False

READINGS = {"bounded_orbit": stable_bounded_orbit,
            "attracting_fixed_point": stable_attracting_fixed_point}

# ------------------------------------------------------------------ claims
def make_claim(name, H, stable):
    return {"name": name,
            "D": lambda w: w.get("family") == "quadratic",   # domain
            "H": H,                                          # hypothesis
            "C": lambda w: stable(w["c"])}                   # conclusion (recomputed)

# ---------------------------------------------------------------- assessor
def assess(claim, witnesses, trust_labels=False, ignore_H=False,
           flip_C=False, ignore_D=False):
    """Returns (verdict, decisive_ids). The flags are deliberate MUTANTS."""
    decisive = []
    for w in witnesses:
        in_D = True if ignore_D else claim["D"](w)
        in_H = True if ignore_H else claim["H"](w)
        if trust_labels:
            c_holds = (w["label"] == "stable")      # MUTANT: believes the label
        else:
            c_holds = claim["C"](w)
        if flip_C:
            c_holds = not c_holds
        if in_D and in_H and not c_holds:
            decisive.append(w["id"])
    return ("REFUTED" if decisive else "OPEN"), decisive

# --------------------------------------------------------------- fixtures
def W(i, c, label): return {"id": i, "family": "quadratic", "c": c, "label": label}

def fixtures(stable, reading):
    univ = make_claim("EC-04 universal", lambda w: True, stable)
    lt1  = make_claim("EC-05 |c|<1",    lambda w: abs(w["c"]) < 1, stable)
    cubic = {"id": "E-010", "family": "cubic", "c": 1.5, "label": "unstable"}
    # expected verdicts are decided by hand, independent of assess():
    sens = "OPEN" if reading == "bounded_orbit" else "REFUTED"   # c=-1: definition-sensitive
    return [
        ("EC-04  c=0.5 vs universal",        univ, [W("E-003", 0.5, "unstable")], "REFUTED"),
        ("EC-05  c=1.5 out of scope",        lt1,  [W("E-003", 1.5, "unstable")], "OPEN"),
        ("EC-05b c=0.5 IN scope of |c|<1",   lt1,  [W("E-003", 0.5, "unstable")], "REFUTED"),
        ("EC-06  label lies (c=0.2 stable)", univ, [W("E-009", 0.2, "unstable")], "OPEN"),
        ("EC-06b c=-1 (definition-sensitive)", univ, [W("E-011", -1.0, "unstable")], sens),
        ("EC-07  no witnesses",              lt1,  [],                             "OPEN"),
        ("EC-08  out-of-domain (cubic)",     univ, [cubic],                        "OPEN"),
    ]

MUTANTS = {
    "M1 ignore hypothesis":   dict(ignore_H=True),
    "M2 trust witness label": dict(trust_labels=True),
    "M3 flip conclusion":     dict(flip_C=True),
    "M4 ignore domain":       dict(ignore_D=True),
}

def run(reading):
    stable = READINGS[reading]
    fx = fixtures(stable, reading)
    print(f"\n=== reading: {reading} ===")
    base_ok = True
    for name, claim, ws, expected in fx:
        v, ids = assess(claim, ws)
        base_ok &= (v == expected)
        print(f"  {'PASS' if v == expected else 'FAIL'}  {name:38s} -> {v:8s} {ids}  (expected {expected})")
    if not base_ok:
        print("  baseline failed: mutant results below are NOT meaningful")
    caught = 0
    for mname, kw in MUTANTS.items():
        killed = any(assess(cl, ws, **kw)[0] != assess(cl, ws)[0] for _, cl, ws, _ in fx)
        caught += killed
        print(f"  mutant {mname:26s} {'CAUGHT' if killed else 'SURVIVED'}")
    print(f"  baseline_all_pass={base_ok}  mutants caught: {caught}/{len(MUTANTS)}")
    return base_ok and caught == len(MUTANTS)

if __name__ == "__main__":
    print("Ground truth of the witnesses under each reading of 'stable':")
    for c in (-1.0, 0.0, 0.2, 0.5, 1.5):
        print(f"  c={c:5}: " + ", ".join(f"{r}={f(c)}" for r, f in READINGS.items()))
    results = [run(r) for r in READINGS]
    sys.exit(0 if all(results) else 1)

