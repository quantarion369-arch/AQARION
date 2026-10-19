#!/usr/bin/env python3
import argparse, copy, hashlib, itertools, json, platform
from pathlib import Path
import sympy as s

z = s.Symbol("z")
WORD = "101111111010000000"

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def bits(w):
    w = tuple(w)
    need(bool(w) and all(type(c) is int and c in (0, 1) for c in w),
         "invalid binary input")
    return w

def matrix(w):
    w = bits(w)
    return s.Matrix([w[j:] + w[:j] for j in range(len(w))])

def spectral(w):
    w = bits(w)
    n = len(w)
    q = next(int(d) for d in s.divisors(n)
             if all(w[j] == w[j % d] for j in range(n)))
    f = s.Poly.from_list(list(reversed(w)), z, domain=s.QQ)
    r = n - int(s.gcd(f, s.Poly(z**n - 1, z, domain=s.QQ)).degree())
    return dict(
        period=q, rank=r, circulant_gap=q-r,
        observable_gap=q-r-int(not any(w))
    )

def certificate_check(c):
    need(c.get("word") == WORD, "wrong word")
    cols = c.get("kernel_columns")
    need(isinstance(cols, list) and len(cols) == 10, "wrong column count")
    need(all(isinstance(v, list) and len(v) == 18 for v in cols),
         "wrong column shape")
    need(all(isinstance(a, str) for v in cols for a in v),
         "expected rational strings")
    V = s.Matrix([[s.Rational(a) for a in v] for v in cols]).T
    C = matrix(tuple(map(int, WORD)))
    need(C[:8, :8].det() == -1, "minor failed")
    need(V.rank() == 10 and C*V == s.zeros(18, 10), "kernel failed")
    need(spectral(tuple(map(int, WORD)))["period"] == 18, "period failed")

def rejected(action):
    try:
        action()
    except (ValueError, TypeError):
        return True
    return False

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--certificate", type=Path)
    p.add_argument("--exhaustive", action="store_true")
    a = p.parse_args()
    out = a.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=False)

    def save(name, value):
        (out/name).write_text(
            json.dumps(value, indent=2, sort_keys=True) + chr(10),
            encoding="utf-8"
        )

    save("status.json", dict(complete=False))
    here = Path(__file__).resolve().parent
    names = ["verify_cyclic_gap.py", "requirements.txt", "README.md", "PROOF.md"]
    save("input-hashes.json", {
        n: hashlib.sha256((here/n).read_bytes()).hexdigest() for n in names
    })

    try:
        w = tuple(map(int, WORD))
        C = matrix(w)
        c = (
            json.loads(a.certificate.read_text())
            if a.certificate else dict(
                word=WORD,
                kernel_columns=[[str(x) for x in v] for v in C.nullspace()],
                origin="generated in this execution"
            )
        )
        certificate_check(c)
        need(C.rank() == 8 and spectral(w)["rank"] == 8,
             "rank cross-check failed")

        bad = copy.deepcopy(c)
        bad["kernel_columns"][0][0] = str(
            s.Rational(bad["kernel_columns"][0][0]) + 1
        )
        need(rejected(lambda: certificate_check(bad)), "corruption accepted")

        bad = copy.deepcopy(c)
        bad["kernel_columns"][1] = list(bad["kernel_columns"][0])
        need(rejected(lambda: certificate_check(bad)),
             "dependent columns accepted")

        bad = copy.deepcopy(c)
        bad["kernel_columns"][0].pop()
        need(rejected(lambda: certificate_check(bad)), "bad shape accepted")

        for invalid in [(), (2,), (-1, 1), ("0",), (True,)]:
            need(rejected(lambda v=invalid: spectral(v)),
                 "invalid input accepted")

        powers = []
        for n in range(2, 33):
            factors = s.factorint(n)
            if len(factors) != 1:
                continue
            prime = int(next(iter(factors)))
            k = n // prime
            r = spectral((1,)*k + (0,)*(n-k))
            need(r["period"] == n and r["circulant_gap"] == k-1,
                 "attainment failed")
            powers.append(dict(n=n, gap=k-1))

        support = []
        ds = [2, 3, 6, 9, 18]
        for mask in range(32):
            active = [d for j, d in enumerate(ds) if mask & (1 << j)]
            rank = 1 + sum(int(s.totient(d)) for d in active)
            if int(s.ilcm(1, 1, *active)) == 18 and rank <= 8:
                weight = int(s.prod(
                    s.cyclotomic_poly(d, z).subs(z, 1)
                    for d in ds if d not in active
                ))
                support.append(dict(
                    active=[1]+active, rank=rank, weight_multiple=weight
                ))
        need(
            len(support) == 3
            and [r for r in support if r["rank"] < 8] == [
                dict(active=[1, 18], rank=7, weight_multiple=18)
            ],
            "support check failed"
        )

        count = comparisons = 0
        if a.exhaustive:
            for n in range(1, 10):
                for u in itertools.product((0, 1), repeat=n):
                    M = matrix(u)
                    r = int(M.rank())
                    aug = int(M.row_join(s.ones(n, 1)).rank())
                    q = len({u[j:]+u[:j] for j in range(n)})
                    for rep in [list(u), tuple(u)]:
                        need(
                            spectral(rep) == dict(
                                period=q, rank=r,
                                circulant_gap=q-r, observable_gap=q-aug
                            ),
                            "exhaustive mismatch"
                        )
                        comparisons += 1
                    count += 1
            need(count == 1022 and comparisons == 2044, "count mismatch")

        report = dict(
            result="PASS",
            scope="standalone arithmetic; not production replay or formal proof",
            python=platform.python_version(),
            sympy=s.__version__,
            binary_words_checked=count,
            list_tuple_comparisons=comparisons,
            certificate_corruptions_rejected=3,
            invalid_inputs_rejected=5,
            witness=dict(
                word=WORD, **spectral(w),
                minor_determinant=-1, kernel_rank=10
            ),
            prime_power_checks=powers,
            length18_supports=support
        )
        save("certificate.json", c)
        save("report.json", report)
        save("status.json", dict(complete=True, result="PASS"))
        print(
            "PASS: words=" + str(count)
            + " comparisons=" + str(comparisons)
            + " corruptions_rejected=3"
        )
        print("WITNESS: period=18 rank=8 gap=10")
        print("RECEIPT:", out)
        return 0
    except Exception as e:
        save("status.json", dict(
            complete=True, result="FAIL",
            error=type(e).__name__ + ": " + str(e)
        ))
        print("FAIL:", type(e).__name__, str(e))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
