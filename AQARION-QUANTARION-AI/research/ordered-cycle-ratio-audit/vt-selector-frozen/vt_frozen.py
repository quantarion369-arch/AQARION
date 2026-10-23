#!/usr/bin/env python3
"""Exact Case B tail-witness selector, V_t envelope family (FROZEN SOURCE).

Hypotheses: integer m >= 2; Case B means integer n >= 2m+1; t in {1,...,m}.
Certificate:  V_t(n,m) < 1  <=>
    (m!)^2 * C(n+t-1, t) < n * C(n-1, m-1) * t^(m-1)        (integers only)
Facts used (derived on paper, not proved by this script):
    R(n,m) <= V_t(n,m) for n >= m and every integer t >= 1;
    V_t(n+1,m)/V_t(n,m) = (n+t)(n-m+1) / (n(n+1)), strictly < 1 for
    n >= m >= 2 and 1 <= t <= m, so the predicate "some permitted t
    certifies" is monotone in n.
The selected N is the earliest Case B cutoff certified by this V_t family.
It is NOT the true crossing of R and makes no one-crossing claim.

Conventions
  source_sha256   SHA-256 (hex) of the raw bytes of this file as read from
                  disk by this process. A file cannot contain its own hash,
                  so the hash is computed at run time, never embedded.
  receipt_sha256  SHA-256 (hex) of the UTF-8 bytes of
                  json.dumps(body, sort_keys=True, separators=(",", ":"),
                  ensure_ascii=True), where body is the receipt dictionary
                  without the receipt_sha256 field. body includes
                  source_sha256. Integers are exact JSON integers.
Every check raises RuntimeError or ValueError on failure; none uses assert.
Standard library only. Run:  python3 -I vt_frozen.py
"""
import hashlib
import json
from fractions import Fraction
from math import comb, factorial

SCHEMA = "aqarion-vt-selector-receipt-v1"
PILOT_M = (4, 5, 6, 8, 10, 15)
GRID_M = (2, 3, 4, 5, 6)
GRID_NMAX = 60
TM_M = tuple(range(2, 16))
TM_WINDOW = 399  # n runs over 2m+1 .. 2m+TM_WINDOW


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


# ---------------------------------------------------------------- core
def lhs(n, m, t):
    return factorial(m) ** 2 * comb(n + t - 1, t)


def rhs(n, m, t):
    return n * comb(n - 1, m - 1) * t ** (m - 1)


def certifies(n, m, t):
    return lhs(n, m, t) < rhs(n, m, t)


def certifying_ts(n, m):
    return [t for t in range(1, m + 1) if certifies(n, m, t)]


def predicate(n, m):
    return any(certifies(n, m, t) for t in range(1, m + 1))


def select_witness(m):
    """Exponential bracketing, then integer bisection on predicate(., m)."""
    if not isinstance(m, int) or isinstance(m, bool) or m < 2:
        raise ValueError("m must be an integer >= 2")
    start = 2 * m + 1
    if predicate(start, m):
        n_sel = start
    else:
        lo, hi = start, 2 * start  # invariant: predicate(lo) is False
        while not predicate(hi, m):  # terminates: V_1 = (m!)^2 / C(n-1,m-1) -> 0
            lo, hi = hi, 2 * hi
        while hi - lo > 1:  # invariant: predicate(lo) False, predicate(hi) True
            mid = (lo + hi) // 2
            if predicate(mid, m):
                hi = mid
            else:
                lo = mid
        n_sel = hi
    ts = certifying_ts(n_sel, m)
    if not ts:
        raise RuntimeError("selector returned N with no certifying t")
    return n_sel, ts


# ------------------------------------------------------ group A: pilot
def group_pilot():
    cases = []
    for m in PILOT_M:
        n_sel, ts = select_witness(m)
        t = ts[0]
        num, den = lhs(n_sel, m, t), rhs(n_sel, m, t)
        margin = den - num
        if margin <= 0:
            raise RuntimeError("non-positive margin at m=%d" % m)
        if n_sel < 2 * m + 1:
            raise RuntimeError("N below Case B start at m=%d" % m)
        v = Fraction(num, den)
        entry = {
            "m": m,
            "earliest_certified_N": n_sel,
            "selected_t": t,
            "all_certifying_t_at_N": ts,
            "V_unreduced_numerator": num,
            "V_unreduced_denominator": den,
            "V_reduced_numerator": v.numerator,
            "V_reduced_denominator": v.denominator,
            "positive_integer_margin": margin,
        }
        if n_sel > 2 * m + 1:
            deficits = {}
            for tt in range(1, m + 1):
                d = lhs(n_sel - 1, m, tt) - rhs(n_sel - 1, m, tt)
                if d < 0:
                    raise RuntimeError("t=%d certifies at N-1 for m=%d" % (tt, m))
                deficits[str(tt)] = d  # lhs - rhs >= 0 means V_t(N-1) >= 1
            entry["all_t_fail_at_N_minus_1"] = "YES"
            entry["N_minus_1_nonnegative_deficits_lhs_minus_rhs"] = deficits
        else:
            entry["all_t_fail_at_N_minus_1"] = "NOT_APPLICABLE"
            entry["N_minus_1_nonnegative_deficits_lhs_minus_rhs"] = None
        cases.append(entry)
    return {"status": "PASS", "pilot_cases": len(cases), "cases": cases}


# ------------------------------------- group B: independent linear scan
def v_fraction(n, m, t):
    return Fraction(factorial(m) ** 2 * comb(n + t - 1, t),
                    n * comb(n - 1, m - 1) * t ** (m - 1))


def group_linear_scan():
    rows = []
    total_n = total_pairs = 0
    for m in PILOT_M:
        n_sel, _ = select_witness(m)
        first = None
        scanned = 0
        pairs = 0
        for n in range(2 * m + 1, n_sel + 1):
            scanned += 1
            hit = False
            for t in range(1, m + 1):
                pairs += 1
                if v_fraction(n, m, t) < 1:
                    hit = True
            if hit:
                first = n
                break
        if first != n_sel:
            raise RuntimeError("linear scan %r != bisection %r at m=%d" % (first, n_sel, m))
        total_n += scanned
        total_pairs += pairs
        rows.append({"m": m, "bisection_N": n_sel, "linear_scan_first_N": first,
                     "n_values_scanned": scanned, "n_t_pairs_evaluated": pairs})
    return {"status": "PASS", "pilot_cases": len(rows),
            "total_n_values_scanned": total_n,
            "total_n_t_pairs_evaluated": total_pairs, "rows": rows}


# --------------------------- groups C, D: bounded exact grid (not proof)
def build_tables(nmax):
    c = [[0] * (nmax + 1) for _ in range(nmax + 1)]
    p = [[0] * (nmax + 1) for _ in range(nmax + 1)]
    c[0][0] = 1
    p[0][0] = 1
    for n in range(1, nmax + 1):
        for k in range(1, n + 1):
            c[n][k] = c[n - 1][k - 1] + (n - 1) * c[n - 1][k]
            p[n][k] = p[n - 1][k - 1] + (p[n - k][k] if n >= k else 0)
    return c, p


def group_r_le_v(c, p):
    checks = 0
    for m in GRID_M:
        for n in range(m, GRID_NMAX + 1):
            r = Fraction(factorial(m) * c[n][m], factorial(n) * p[n][m])
            for t in range(1, m + 1):
                checks += 1
                if r > v_fraction(n, m, t):
                    raise RuntimeError("R > V_t at n=%d m=%d t=%d" % (n, m, t))
    return {"status": "PASS", "checks": checks, "violations": 0,
            "m_values": list(GRID_M), "n_range_inclusive": [2, GRID_NMAX],
            "note": "n runs from m to %d for each m" % GRID_NMAX}


def group_ratio_positivity():
    checks = 0
    for m in GRID_M:
        for n in range(m, GRID_NMAX):
            for t in range(1, m + 1):
                checks += 1
                ratio = v_fraction(n + 1, m, t) / v_fraction(n, m, t)
                if ratio != Fraction((n + t) * (n - m + 1), n * (n + 1)):
                    raise RuntimeError("ratio identity fails n=%d m=%d t=%d" % (n, m, t))
                if not ratio < 1:
                    raise RuntimeError("ratio not below 1 n=%d m=%d t=%d" % (n, m, t))
                lead = n * (n + 1) - (n + t) * (n - m + 1)
                if lead != n * (m - t) + t * (m - 1):
                    raise RuntimeError("positivity identity fails n=%d m=%d t=%d" % (n, m, t))
                if lead <= 0:
                    raise RuntimeError("positivity not strict n=%d m=%d t=%d" % (n, m, t))
    return {"status": "PASS", "checks": checks, "violations": 0,
            "m_values": list(GRID_M), "note": "n runs from m to %d for each m" % (GRID_NMAX - 1)}


# ----------------------------------------------- group E: t = m window
def group_t_equals_m():
    checks = 0
    for m in TM_M:
        if factorial(m) ** 2 < m ** m:
            raise RuntimeError("(m!)^2 < m^m at m=%d" % m)
        for n in range(2 * m + 1, 2 * m + 1 + TM_WINDOW):
            checks += 1
            if certifies(n, m, m):
                raise RuntimeError("t=m certifies at n=%d m=%d" % (n, m))
    return {"status": "PASS", "checks": checks, "violations": 0,
            "m_values": [TM_M[0], TM_M[-1]],
            "n_window_per_m": TM_WINDOW,
            "note": "finite window only; the all-n claim rests on the paper derivation"}


# ------------------------------------------------------------- receipt
def source_sha256():
    try:
        path = __file__
    except NameError:
        raise RuntimeError("source path unavailable; run as a file, not via stdin")
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def canonical_hash(body):
    text = json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main():
    c, p = build_tables(GRID_NMAX)
    body = {
        "schema": SCHEMA,
        "hypotheses": {"m_min": 2, "case_B": "n >= 2m+1", "t_range": "1..m",
                       "envelope": "V_t(n,m) < 1 via integer inequality"},
        "source_sha256": source_sha256(),
        "groups": {
            "A_pilot_selector": group_pilot(),
            "B_independent_linear_scan": group_linear_scan(),
            "C_R_le_Vt_exact_grid": group_r_le_v(c, p),
            "D_ratio_positivity_exact_grid": group_ratio_positivity(),
            "E_t_equals_m_window": group_t_equals_m(),
        },
    }
    receipt = {"body": body, "receipt_sha256": canonical_hash(body)}
    print(json.dumps(receipt, indent=1, sort_keys=True))
    print("SOURCE_SHA256=" + body["source_sha256"])
    print("RECEIPT_SHA256=" + receipt["receipt_sha256"])


if __name__ == "__main__":
    main()
