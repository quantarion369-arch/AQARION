import json, math, hashlib, sys
from pathlib import Path
from fractions import Fraction as F

def features(x):
    b = [(x >> i) & 1 for i in range(6)]
    return [1] + b + [b[i]*b[j] for i in range(6) for j in range(i+1,6)]

def matrix(points):
    v = [features(x) for x in points]
    return [[v[c][r] for c in range(len(points))] for r in range(22)]

def rref(m, n):
    a = [[F(x) for x in row] for row in m]
    piv, r = [], 0
    for c in range(n):
        p = next((i for i in range(r,len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = a[r][c]
        a[r] = [x/z for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [x-z*y for x,y in zip(a[i],a[r])]
        piv.append(c)
        r += 1
        if r == len(a):
            break
    return a[:r], piv

def rank(m,n):
    return len(rref(m,n)[1])

def primitive(v):
    d = math.lcm(*(x.denominator for x in v))
    z = [int(x*d) for x in v]
    g = math.gcd(*[abs(x) for x in z])
    z = [x//g for x in z]
    if next(x for x in z if x) < 0:
        z = [-x for x in z]
    return z

def kernel(m,n):
    a,p = rref(m,n)
    free = [j for j in range(n) if j not in p]
    if len(free) != 1:
        raise ValueError("Nullity is not one")
    v = [F(0)]*n
    v[free[0]] = F(1)
    for i,j in enumerate(p):
        v[j] = -a[i][free[0]]
    return primitive(v)

def normalize(v):
    if not isinstance(v,list) or len(v) != 12 or any(type(x) != int for x in v):
        raise ValueError("Invalid catalog kernel")
    g = math.gcd(*[abs(x) for x in v])
    if not g:
        raise ValueError("Zero catalog kernel")
    z = [x//g for x in v]
    if next(x for x in z if x) < 0:
        z = [-x for x in z]
    return z

def main():
    cat = Path(sys.argv[1])
    raw = cat.read_bytes()
    data = json.loads(raw)
    records = data["six_bit_simple_orbits"]
    if len(records) != 32:
        raise ValueError("Expected 32 records, found "+str(len(records)))

    results = []
    seen = set()

    for i,item in enumerate(records):
        s = item["support"]
        if len(s) != 12 or len(set(s)) != 12 or s != sorted(s):
            raise ValueError("Invalid support at record "+str(i))
        if any(type(x) != int or x < 0 or x > 63 for x in s):
            raise ValueError("Invalid point at record "+str(i))
        if tuple(s) in seen:
            raise ValueError("Duplicate support")
        seen.add(tuple(s))

        m = matrix(s)
        qrank = rank(m,12)
        if qrank != 11 or item.get("rank_Q") != 11:
            raise ValueError("Rank failure at record "+str(i))

        k = kernel(m,12)
        if any(x == 0 for x in k):
            raise ValueError("Zero kernel coefficient at record "+str(i))
        if k != normalize(item["primitive_kernel"]):
            raise ValueError("Kernel mismatch at record "+str(i))

        dr = [rank(matrix(s[:j]+s[j+1:]),11) for j in range(12)]
        if dr != [11]*12:
            raise ValueError("Deletion failure at record "+str(i))

        results.append({
            "record": i,
            "rank_Q": qrank,
            "nullity_Q": 1,
            "primitive_kernel": k,
            "deletion_ranks_Q": dr,
            "minimal_circuit": True
        })
        print("PASS",i+1,"/ 32",flush=True)

    report = {
        "gate":"SIXBIT-CIRCUIT-001",
        "status":"PASS",
        "feature_definition":"1, x_i, x_i*x_j (0<=i<j<6)",
        "bit_convention":"x_i=(x>>i)&1",
        "field":"Q",
        "matrix_shape":"22x12",
        "records_checked":len(results),
        "exact_rank_checks":32,
        "unique_kernel_checks":32,
        "nonzero_coefficient_checks":32,
        "deletion_rank_checks":384,
        "all_minimal_circuits":True,
        "catalog_sha256":hashlib.sha256(raw).hexdigest(),
        "results":results,
        "scope":"Catalogued supports only; no global completeness claim."
    }
    out = Path(__file__).resolve().parent / "PASS.json"
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("\nSIXBIT-CIRCUIT-001: PASS")
    print("Certificate:",out)

try:
    main()
except Exception as e:
    print("SIXBIT-CIRCUIT-001: FAIL")
    print(type(e).__name__+":",e)
    sys.exit(1)
