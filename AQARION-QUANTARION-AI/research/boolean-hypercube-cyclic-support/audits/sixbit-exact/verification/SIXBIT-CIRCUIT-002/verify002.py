import json, hashlib, math, sys
from pathlib import Path

PRIMES = (1000000007, 1000000009)

def features(x):
    b = [(x >> i) & 1 for i in range(6)]
    return [1] + b + [b[i]*b[j] for i in range(6) for j in range(i+1,6)]

def matrix(points):
    v = [features(x) for x in points]
    return [[v[c][r] for c in range(len(points))] for r in range(22)]

def rank_mod(m, n, p):
    a = [[x % p for x in row] for row in m]
    r = 0
    for c in range(n):
        pivot = next((i for i in range(r,len(a)) if a[i][c]),None)
        if pivot is None:
            continue
        a[r],a[pivot] = a[pivot],a[r]
        inv = pow(a[r][c],p-2,p)
        a[r] = [(x*inv)%p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                z = a[i][c]
                a[i] = [(x-z*y)%p for x,y in zip(a[i],a[r])]
        r += 1
        if r == len(a):
            break
    return r

def main():
    cat = Path(sys.argv[1])
    prior = Path(sys.argv[2])
    raw = cat.read_bytes()
    data = json.loads(raw)
    old = json.loads(prior.read_text())
    assert old["status"] == "PASS"
    records = data["six_bit_simple_orbits"]
    assert len(records) == 32

    checked = []
    for i,item in enumerate(records):
        s = item["support"]
        k = item["primitive_kernel"]
        assert len(s) == len(set(s)) == 12
        assert len(k) == 12
        assert math.gcd(*[abs(x) for x in k]) == 1

        m = matrix(s)

        # Exact integer identity M*k = 0.
        assert all(sum(m[r][j]*k[j] for j in range(12)) == 0
                   for r in range(22))

        ranks = {}
        for p in PRIMES:
            full = rank_mod(m,12,p)
            deletions = [
                rank_mod(matrix(s[:j]+s[j+1:]),11,p)
                for j in range(12)
            ]
            assert full == 11, (i,p,"full rank",full)
            assert deletions == [11]*12, (i,p,"deletion ranks",deletions)
            ranks[str(p)] = {"full_rank":full,"deletion_ranks":deletions}

        checked.append({"record":i,"field_ranks":ranks})
        print("PASS",i+1,"/ 32",flush=True)

    report = {
        "gate":"SIXBIT-CIRCUIT-002",
        "status":"PASS",
        "method":"Independent modular Gaussian elimination plus exact integer kernel identities",
        "primes":list(PRIMES),
        "records_checked":32,
        "full_matrix_rank_checks":64,
        "deletion_rank_checks":768,
        "exact_kernel_identity_checks":32,
        "catalog_sha256":hashlib.sha256(raw).hexdigest(),
        "prior_certificate_sha256":hashlib.sha256(prior.read_bytes()).hexdigest(),
        "scope":"Independent verification of the 32 catalogued supports only; no global completeness claim.",
        "results":checked
    }
    out = Path(__file__).resolve().parent / "PASS.json"
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("\nSIXBIT-CIRCUIT-002: PASS")
    print("Certificate:",out)

if __name__ == "__main__":
    main()
