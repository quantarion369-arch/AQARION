from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib
import json

N, M = 90, 16
c = [[0]*(M+1) for _ in range(N+1)]
P = [[0]*(M+1) for _ in range(N+1)]
c[0][0] = P[0][0] = 1

for n in range(1, N+1):
    for k in range(1, min(n, M)+1):
        c[n][k] = c[n-1][k-1] + (n-1)*c[n-1][k]
        P[n][k] = P[n-1][k-1] + P[n-k][k]

f = [factorial(n) for n in range(N+1)]
groups = {}

def check(group, condition):
    if not condition:
        raise AssertionError(group)
    groups[group] = groups.get(group, 0) + 1

def b(n, k):
    return F(f[k]*c[n][k], f[n])

def R(n, k):
    return b(n, k)/P[n][k]

part = [1] + [0]*N
for j in range(1, N+1):
    for n in range(j, N+1):
        part[n] += part[n-j]

expected = [F(1,3), F(5,12), F(29,60),
            F(89,120), F(31063,30240)]
for m, value in enumerate(expected, 1):
    check("boundary_initial_values", R(2*m+1,m) == value)

for m in range(2, 15):
    n = 2*m+1
    a = b(n,m)
    rho = b(n,m+1)/a
    tau = b(n,m-1)/a
    growth = b(n+2,m+1)/a
    exact = (
        F(m,2)*tau + F(4*m+3,2) + n*rho
    )/(2*m+3)
    check("complete_recurrence", growth == exact)
    check("newton_bound",
          rho >= F(2*(m+1)**2, m*(2*m+1)))
    check("corrected_tau_bound",
          tau >= F(m-1, m*(m+2)))
    check("boundary_growth",
          growth >= 2+F(m+8, 2*m*(m+2)*(2*m+3)))
    check("boundary_denominator",
          P[n][m] == part[m+1]-1)
    check("boundary_ratio_growth",
          R(n+2,m+1)/R(n,m) >=
          1+F(m+8, 4*m*(m+2)*(2*m+3)))

for k in range(2, N):
    check("partition_growth",
          part[k+1]-1 <= 2*(part[k]-1))

for m in range(2, 9):
    D = F(0)
    for n in range(m, N):
        D += F(1,n-1)
        q = F(c[n][m-1], c[n][m])
        s = F(P[n+1][m], P[n][m])
        check("harmonic_q_bound", q <= F(m-1)/D)
        check("fixed_m_recurrence",
              R(n+1,m)/R(n,m) == (n+q)/((n+1)*s))
        check("partition_injection_consequence", s >= 1)
        if D > m-1:
            check("eventual_decrease", R(n+1,m) < R(n,m))

control = R(32,15)/R(31,15)
check("negative_control",
      control == F(163550075392585167941,
                   163320823394942693408))
check("negative_control", control > 1)
check("negative_control", R(31,15) > 1 and R(32,15) > 1)

source = Path(__file__).read_bytes()
receipt = {
    "status": "PASS",
    "source_sha256": hashlib.sha256(source).hexdigest(),
    "test_groups": groups,
    "test_count": sum(groups.values()),
    "negative_control_ratio": str(control),
    "boundary_scope": "n=2m+1",
    "eventual_decrease_criterion": "H(n-1)-H(m-2)>m-1",
    "formal_certification": "OPEN",
    "novelty_clearance": "OPEN",
    "global_case_B_classification": "OPEN",
    "promotion": False,
    "git_operations": 0
}
Path("receipt.json").write_text(
    json.dumps(receipt, indent=2, sort_keys=True)
)
print("STATUS=PASS")
print("CHECKS=" + str(receipt["test_count"]))
for group, count in sorted(groups.items()):
    print(group.upper() + "=" + str(count))
print("NEGATIVE_CONTROL=" + str(control))
print("SOURCE_SHA256=" + receipt["source_sha256"])
print("RECEIPT_SHA256=" + hashlib.sha256(
    Path("receipt.json").read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(Path.cwd()))
print("FORMAL_CERTIFICATION=OPEN")
print("GLOBAL_CLASSIFICATION=OPEN")
print("PROMOTION=FALSE")
print("GIT_OPERATIONS=0")
