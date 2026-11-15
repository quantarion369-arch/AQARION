#!/usr/bin/env python3
import argparse
import collections
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import sympy as sp

SHIFTS = [
    [0],
    [3]*8 + [4]*6,
    [4]*3 + [5]*24 + [6]*8,
    [6]*8 + [7]*24 + [8]*3,
    [8]*6 + [9]*8,
    [12],
]
EXPECTED = {1: 1, 2: 13, 3: 22, 4: 13, 5: 1}

def say(*x):
    print(*x, flush=True)

def expand_matrix(M):
    return M.applyfunc(sp.expand)

def basic_report():
    say("=== REPORTED-SHIFT CALCULATIONS; NOT MATRIX VERIFICATION ===")
    say("Expected ranks D1..D5: 1, 13, 22, 13, 1")
    say("D3 expected rank = 35 - 14 + 1 = 22")
    counts = collections.Counter(
        b-a for a in SHIFTS[2] for b in SHIFTS[3]
    )
    say("D3 required entry degrees/counts:", dict(sorted(counts.items())))
    a = sorted(SHIFTS[2])
    b = sorted(SHIFTS[3])
    say("D3 nonzero 22-minor degree bounds:",
        sum(b[:22])-sum(a[-22:]),
        sum(b[-22:])-sum(a[:22]))
    t = sp.Symbol("t")
    N = sp.expand(sum(
        (-1)**i * sum(t**a for a in row)
        for i, row in enumerate(SHIFTS)
    ))
    say("Alternating numerator:", N)
    say("Factorization:", sp.factor(N))
    say("Standard ten-variable h-polynomial:",
        sp.cancel(N/(1-t)**5))
    say("Standard ten-variable conditional a-invariant: 12-10 = 2")
    say("Normal positive semigroup interpretation requires a < 0.")
    say("Correct duality-reduced grade targets: D2 >= 4; D3 >= 3")

def parse_polynomial(text, symbols, local):
    expr = sp.expand(sp.sympify(str(text).replace("^", "**"),
                               locals=local))
    if expr.free_symbols - set(symbols):
        raise ValueError("Undeclared symbols in: " + str(text))
    sp.Poly(expr, *symbols, domain=sp.QQ)
    return expr

def weighted_degrees(expr, symbols, weights):
    if expr == 0:
        return set()
    p = sp.Poly(expr, *symbols, domain=sp.QQ)
    return {
        sum(e*w for e, w in zip(mon, weights))
        for mon, coefficient in p.terms() if coefficient != 0
    }

def singular_height(polys, names, target, timeout):
    if not polys:
        say("NO CERTIFICATE: no selected nonzero minors.")
        return
    executable = shutil.which("Singular")
    if not executable:
        say("NOT RUN: Singular is not on PATH.")
        say("No grade certificate has been obtained.")
        return
    generators = ",".join(str(p).replace("**", "^") for p in polys)
    code = f"""
ring r=0,({','.join(names)}),dp;
ideal J={generators};
ideal G=std(J);
if (reduce(1,G)==0)
{{
  print("AQ_UNIT_IDEAL");
}}
else
{{
  print("AQ_DIM="+string(dim(G)));
}}
quit;
"""
    try:
        run = subprocess.run(
            [executable, "-q"],
            input=code, text=True, capture_output=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        say("INCONCLUSIVE: Singular time limit exceeded.")
        return
    if run.stdout.strip():
        say(run.stdout.strip())
    if run.stderr.strip():
        say(run.stderr.strip())
    if run.returncode != 0:
        say("INCONCLUSIVE: Singular exited unsuccessfully.")
        return
    if "AQ_UNIT_IDEAL" in run.stdout:
        say("PASS: selected minors generate the unit ideal.")
        return
    result = re.search(r"AQ_DIM=(-?\d+)", run.stdout)
    if not result:
        say("INCONCLUSIVE: no quotient dimension returned.")
        return
    dimension = int(result.group(1))
    height = len(names) - dimension
    say("Ambient polynomial variables:", len(names))
    say("Dimension P/J:", dimension)
    say("Height/grade of selected-minor ideal J:", height)
    if height >= target:
        say("PASS: full determinantal ideal has grade >=", target)
    else:
        say("INCONCLUSIVE for full minor ideal: selected height <",
            target)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="audit-input.json")
    parser.add_argument("--ranks", action="store_true",
                        help="exact symbolic ranks; may be expensive")
    parser.add_argument("--timeout", type=int, default=300,
                        help="seconds per Singular calculation")
    args = parser.parse_args()
    basic_report()

    path = Path(args.input)
    if not path.is_file():
        say("\nINPUT MISSING:", path)
        say("Actual matrices/weights were not checked.")
        say("Supply the JSON input described with this script.")
        return 2

    data = json.loads(path.read_text())
    names = data["variables"]
    if (not names or len(set(names)) != len(names)
        or any(not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", n)
               for n in names)
        or any(n in {"I", "E", "O", "oo", "nan"} for n in names)):
        raise ValueError("Use distinct plain polynomial variable names.")
    symbols = tuple(sp.Symbol(n) for n in names)
    local = dict(zip(names, symbols))
    weights = data["weights"]
    if (len(weights) != len(names)
        or any(type(w) is not int or w <= 0 for w in weights)):
        raise ValueError("One positive integer weight per variable required.")

    shifts = data.get("shifts", SHIFTS)
    if shifts != SHIFTS:
        raise ValueError("This audit targets the reported ordered shifts.")

    say("\n=== ACTUAL INPUT RING ===")
    say("P = QQ[" + ",".join(names) + "]")
    say("Weights:", weights, "sum =", sum(weights))
    predicted_a = shifts[5][0] - sum(weights)
    say("Conditional a-invariant =", predicted_a)
    if predicted_a >= 0:
        say("OBSTRUCTION: incompatible with a positive normal semigroup")
        say("ring if the reported exact minimal resolution applies.")
    else:
        say("PASS necessary negative-a test; not proof of normality.")

    if "semigroup_matrix" in data:
        A = sp.Matrix(data["semigroup_matrix"])
        if A.cols != len(names):
            raise ValueError("Semigroup matrix must have one column per variable.")
        if any(not x.is_Integer for x in A):
            raise ValueError("Semigroup matrix must be integral.")
        say("Semigroup matrix rank:", A.rank())
        solution = sp.linsolve((A.T, sp.Matrix(weights)))
        say("Solutions of A^T ell = weights:", solution)
        if solution == sp.EmptySet:
            say("FAIL: weights do not descend from these semigroup degrees.")
        else:
            say("PASS: weights descend from the supplied semigroup matrix.")
        say("This does not certify semigroup saturation or graph identification.")

    matrices = {}
    failed = False
    zero = {x: 0 for x in symbols}
    for i in range(1, 6):
        key = "D" + str(i)
        raw = data.get("matrices", {}).get(key)
        if raw is None:
            say(key, "MISSING")
            continue
        M = sp.Matrix([
            [parse_polynomial(e, symbols, local) for e in row]
            for row in raw
        ])
        want = (len(shifts[i-1]), len(shifts[i]))
        if M.shape != want:
            raise ValueError(f"{key}: shape {M.shape}, expected {want}")
        matrices[i] = M
        bad = []
        units = []
        for r in range(M.rows):
            for c in range(M.cols):
                e = M[r, c]
                actual = weighted_degrees(e, symbols, weights)
                expected = shifts[i][c] - shifts[i-1][r]
                if actual and actual != {expected}:
                    bad.append((r+1, c+1, expected, sorted(actual)))
                if e.subs(zero) != 0:
                    units.append((r+1, c+1, str(e.subs(zero))))
        say("\n", key, "shape", M.shape)
        say("Homogeneity:", "PASS" if not bad else "FAIL")
        for item in bad[:30]:
            say("  row,column,required,observed:", item)
        say("Zero constant terms:", "PASS" if not units else "FAIL")
        for item in units[:30]:
            say("  row,column,constant:", item)
        failed |= bool(bad or units)
        if args.ranks:
            rank = M.rank()
            say("Exact QQ(variables) rank:", rank,
                "expected:", EXPECTED[i])
            failed |= rank != EXPECTED[i]

    say("\n=== COMPLEX IDENTITIES ===")
    for i in range(1, 5):
        if i not in matrices or i+1 not in matrices:
            say(f"D{i}*D{i+1}: MISSING INPUT")
            continue
        product = expand_matrix(matrices[i] * matrices[i+1])
        ok = product == sp.zeros(product.rows, product.cols)
        say(f"D{i}*D{i+1}:", "PASS" if ok else "FAIL")
        failed |= not ok

    say("\n=== LITERAL TRANSPOSE CHECKS ===")
    say("FAIL here may mean different bases, not failure of all possible dualities.")
    for a, b in ((4, 2), (5, 1)):
        if a in matrices and b in matrices:
            if matrices[a].shape == matrices[b].T.shape:
                same = expand_matrix(matrices[a]-matrices[b].T)
                opposite = expand_matrix(matrices[a]+matrices[b].T)
                z = sp.zeros(*same.shape)
                say(f"D{a}=D{b}^T:", same == z)
                say(f"D{a}=-D{b}^T:", opposite == z)

    say("\n=== SELECTED MINOR CERTIFICATES ===")
    certificates = data.get("minor_witnesses", {})
    for i, size, target in ((2, 13, 4), (3, 22, 3)):
        key = "D" + str(i)
        choices = certificates.get(key, [])
        if i not in matrices or not choices:
            say(key, "NO MINOR CERTIFICATE INPUT")
            continue
        M = matrices[i]
        polys = []
        for k, choice in enumerate(choices, 1):
            rr = [v-1 for v in choice["rows"]]
            cc = [v-1 for v in choice["cols"]]
            if (len(rr) != size or len(cc) != size
                or len(set(rr)) != size or len(set(cc)) != size
                or any(v < 0 or v >= M.rows for v in rr)
                or any(v < 0 or v >= M.cols for v in cc)):
                raise ValueError(f"Invalid {key} witness {k}")
            degree = (
                sum(shifts[i][c] for c in cc)
                - sum(shifts[i-1][r] for r in rr)
            )
            say(key, "minor", k, "expected degree", degree,
                "computing determinant...")
            q = sp.expand(M.extract(rr, cc).det(method="domain-ge"))
            say("Nonzero:", q != 0)
            if q != 0:
                say("Observed weighted degrees:",
                    sorted(weighted_degrees(q, symbols, weights)))
                polys.append(q)
                say("Determinant:", q)
        say("Height calculation for selected", key, "minors:")
        singular_height(polys, names, target, args.timeout)

    say("\n=== AUDIT BOUNDARY ===")
    say("Entry/degree/rank failures detected:", failed)
    say("No overall exactness claim is inferred automatically.")
    say("Missing matrices, unchecked basis dualities, endpoint height,")
    say("and missing minor-grade certificates remain open obligations.")
    say("All arithmetic above is over QQ, not all characteristics.")
    return 1 if failed else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        say("AUDIT STOPPED:", type(exc).__name__, str(exc))
        sys.exit(2)
