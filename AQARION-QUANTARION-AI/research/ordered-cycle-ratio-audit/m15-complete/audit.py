from pathlib import Path
from fractions import Fraction as F
from math import factorial, comb
import hashlib
import json

M, N = 15, 213
groups = {}

def check(group, condition):
    if not condition:
        raise AssertionError(group)
    groups[group] = groups.get(group, 0) + 1

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

c = [[0]*(M+1) for _ in range(N+1)]
P = [[0]*(M+1) for _ in range(N+1)]
c[0][0] = P[0][0] = 1

for n in range(1, N+1):
    for k in range(1, min(n,M)+1):
        c[n][k] = c[n-1][k-1] + (n-1)*c[n-1][k]
        P[n][k] = P[n-1][k-1] + P[n-k][k]

g = [1] + [0]*(N-M)
for j in range(1, M+1):
    for d in range(j, len(g)):
        g[d] += g[d-j]

f = [factorial(n) for n in range(N+1)]

def R(n):
    return F(f[M]*c[n][M], f[n]*P[n][M])

rows = []
for n in range(31,213):
    check("partition_crosscheck", P[n][M] == g[n-M])
    delta = f[M]*c[n][M] - f[n]*P[n][M]
    sign = (delta > 0) - (delta < 0)
    check("prefix_classification", sign == (1 if n <= 113 else -1))
    rows.append({"n": n, "sign": sign, "partition_count": P[n][M]})

for n in (31,32,113,114,212):
    e = [F(1)] + [F(0)]*14
    for j in range(1,n):
        for k in range(14,0,-1):
            e[k] += e[k-1]/j
    check("stirling_harmonic_crosscheck", f[n-1]*e[14] == c[n][M])

control = R(32)/R(31)
check("negative_control", control == F(
    163550075392585167941,163320823394942693408))
check("negative_control", control > 1)
check("negative_control", R(31) > 1 and R(32) > 1)

lhs = f[M]**2*comb(216,4)
rhs = 213*comb(212,14)*4**14
check("tail_certificate", lhs < rhs)
check("tail_certificate", F(lhs,rhs) == F(
    3376479023602312753125,3507494355269936326912))
check("fixed_witness_start",
      not (f[M]**2*comb(215,4) < 212*comb(211,14)*4**14))

check("prefix_counts", sum(x["sign"] == 1 for x in rows) == 83)
check("prefix_counts", sum(x["sign"] == -1 for x in rows) == 99)
check("prefix_counts", all(x["sign"] != 0 for x in rows))

proof = """# Fixed m=15: complete Case B classification

Definition: R(n,m)=m! c(n,m)/(n! P(n,m)).
Here c is unsigned first-kind Stirling and P counts partitions
into exactly m positive parts.

Conclusion:
R(n,15)>1 for 31<=n<=113.
R(n,15)<1 for every n>=114.
No equality occurs for n>=31.

FINITE PREFIX:
For every 31<=n<=212, the audit checks the exact integer sign of
15! c(n,15)-n! P(n,15).
There are 83 positive, 99 negative, and zero equality cases.
Partition counts are cross-checked by restricted-part generating
coefficients. Five Stirling coefficients are cross-checked through
(n-1)! e_14(1,1/2,...,1/(n-1)).

INFINITE TAIL:
Coefficient positivity gives
e_(m-1)(1,1/2,...,1/(n-1))
<= binom(n+t-1,t)/t^(m-1) for positive integer t.
Composition counting gives P(n,m)>=binom(n-1,m-1)/m!.
Thus R(n,m)<=V_t(n,m), where
V_t=(m!)^2 binom(n+t-1,t)/
[n binom(n-1,m-1)t^(m-1)].

For n>=m>=2 and 1<=t<=m,
V_t(n+1,m)/V_t(n,m)
=(n+t)(n-m+1)/[n(n+1)]<1,
because the denominator minus numerator equals
n(m-t)+t(m-1)>0.

The audit checks the integer certificate V_4(213,15)<1.
Therefore R(n,15)<1 for every n>=213.
Together with the finite prefix, this covers every n>=31.

LIMITATIONS:
The prefix is exhaustive machine-exact computation, not a
computation-free proof. The infinite tail uses the analytic
argument above and one exact integer certificate.
No monotonicity of R itself is assumed.
No conclusion for other m, novelty clearance, Lean certification,
or unrestricted Case B classification is claimed.
"""
Path("PROOF_NOTES.md").write_text(proof)
Path("prefix_signs.json").write_text(json.dumps(rows, indent=2))

receipt = {
    "status": "PASS",
    "claim": "fixed m=15 Case B classification",
    "above_one": [31,113],
    "below_one": {"from":114, "unbounded":True},
    "equalities": [],
    "prefix_size": len(rows),
    "tail_witness": {"N":213, "t":4},
    "tail_envelope": str(F(lhs,rhs)),
    "tail_integer_margin": rhs-lhs,
    "negative_control": str(control),
    "test_groups": groups,
    "test_count": sum(groups.values()),
    "files": {name:digest(name) for name in (
        "audit.py","PROOF_NOTES.md","prefix_signs.json")},
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_classification": "OPEN",
    "promotion": False,
    "git_operations": 0
}
Path("receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

print("STATUS=PASS")
print("CHECKS=" + str(receipt["test_count"]))
print("PREFIX_PAIRS=182")
print("ABOVE_ONE=31..113")
print("BELOW_ONE=114..INFINITY")
print("EQUALITY_CASES=0")
print("TAIL_WITNESS=N213_T4")
print("SOURCE_SHA256=" + digest("audit.py"))
print("RECEIPT_SHA256=" + digest("receipt.json"))
print("EVIDENCE_DIRECTORY=" + str(Path.cwd()))
print("FORMAL_CERTIFICATION=OPEN")
print("GLOBAL_CLASSIFICATION=OPEN")
print("PROMOTION=FALSE")
print("GIT_OPERATIONS=0")
