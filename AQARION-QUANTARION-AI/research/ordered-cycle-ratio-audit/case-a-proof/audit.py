#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone
import hashlib
import json
import math
import platform

ROOT = Path(__file__).resolve().parent
LAST_FINITE_DEFICIT = 195

p = [1] + [0] * LAST_FINITE_DEFICIT
for part in range(1, LAST_FINITE_DEFICIT + 1):
    for total in range(part, LAST_FINITE_DEFICIT + 1):
        p[total] += p[total - part]

previous = [1]
checks = []
failures = []
crossings = {}

for n in range(1, 2 * LAST_FINITE_DEFICIT + 1):
    current = [0] * (n + 1)

    for m in range(1, n + 1):
        old = previous[m] if m < len(previous) else 0
        current[m] = (n - 1) * old + previous[m - 1]

    if n == 8:
        crossings["R(8,4)"] = str(Fraction(
            math.factorial(4) * current[4],
            math.factorial(8) * 5
        ))

    if n == 9:
        crossings["R(9,5)"] = str(Fraction(
            math.factorial(5) * current[5],
            math.factorial(9) * 5
        ))

    if n % 2 == 0:
        d = n // 2
        if 5 <= d <= LAST_FINITE_DEFICIT:
            lhs = math.factorial(d) * current[d]
            rhs = math.factorial(n) * p[d]
            checks.append({
                "d": d,
                "stirling_c_2d_d": str(current[d]),
                "partition_p_d": str(p[d]),
                "positive_integer_difference": str(lhs - rhs)
            })
            if lhs <= rhs:
                failures.append(d)

    previous = current

crossing_pass = crossings == {
    "R(8,4)": "967/1200",
    "R(9,5)": "1069/720"
}
passed = len(checks) == 191 and not failures and crossing_pass

proof = r"""# Case A: equality classification in m >= d

Let g(x)=-log(1-x)/x and
A_d(m)=[x^d]g(x)^m
      =sum_{lambda partitions d} (m)_{length(lambda)}/w(lambda)
for integer m>=d.

For d>=1, A_d(m) is strictly increasing on integer m>=d:
all falling factorials in the profile sum are strictly increasing and
all their coefficients are positive.

The ratio is R(m+d,m)=A_d(m)/p(d).

Coefficientwise, g(x)>=exp(x/2), since
1/(j+1)>=1/(2^j j!) for every j>=0.
Consequently A_d(d)>=d^d/(2^d d!).

Monotonicity of log gives
log(d!)<=d log d-d+1+log d.
Thus
log A_d(d)>=d(1-log 2)-1-log d
          >3d/10-1-sqrt(d).

Here log 2<7/10 and log d<=sqrt(d).
For the first inequality, the first four terms of exp(7/10)
already sum to more than 2.
For the second, the maximum of log(x)/sqrt(x), x>=1,
is 2/e<1.

The partition bound is p(d)<=exp(pi sqrt(2d/3)).
For completeness, with t>0 and B=pi^2/6,
log product_{j>=1}(1-exp(-tj))^-1
=sum_{r>=1}1/(r(exp(tr)-1))
<=B/t.
Hence p(d)<=exp(td+B/t); optimize at t=sqrt(B/d).
Also pi sqrt(2/3)<3.

For d>=196, put u=sqrt(d)>=14.
The polynomial 3u^2/10-4u-1 is positive at 14
(value 9/5), and strictly increasing thereafter.
Therefore log A_d(d)>3sqrt(d)>log p(d).

The attached exact checks prove
d! c(2d,d)>(2d)! p(d) for each 5<=d<=195.
Together, these establish A_d(d)>p(d) for every d>=5.
Strict monotonicity then gives R(m+d,m)>1 for all m>=d>=5.

For d=4:
R(8,4)=967/1200<1 and R(9,5)=1069/720>1.
Strict monotonicity excludes equality for every integer m>=4.

The preceding elementary classifications for d=0,1,2,3 complete Case A:
equality occurs only at d=0 and at (n,m)=(3,2).

Status: computer-assisted argument with 191 finite exact base checks.
The infinite tail is bounded analytically.
Case B, m<d, remains unresolved by this argument.
No novelty or formal-proof-assistant certification is asserted.
"""

proof_path = ROOT / "proof.md"
with proof_path.open("x", encoding="utf-8") as stream:
    stream.write(proof)

receipt = {
    "audit": "case_a_boundary_certificate",
    "status": "PASS" if passed else "FAIL",
    "python": platform.python_version(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "proof_sha256": hashlib.sha256(
        proof_path.read_bytes()
    ).hexdigest(),
    "finite_deficits": [5, LAST_FINITE_DEFICIT],
    "finite_boundary_checks": len(checks),
    "failures": failures,
    "deficit_four_crossings": crossings,
    "analytic_tail_starts_at": 196,
    "case_b_m_less_than_d": "OPEN",
    "exact_boundary_certificates": checks,
    "git_operations": 0
}

out = ROOT / "receipt.json"
with out.open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, indent=2)

print("STATUS=" + receipt["status"])
print("FINITE_BOUNDARY_CHECKS=" + str(len(checks)))
print("FAILURES=" + str(failures))
print("DEFICIT_FOUR_CROSSINGS=" + str(crossings))
print("ANALYTIC_TAIL_STARTS_AT=196")
print("CASE_A=COMPUTER_ASSISTED_ARGUMENT" if passed else "CASE_A=NOT_ACCEPTED")
print("CASE_B=OPEN")
print("SOURCE_SHA256=" + receipt["script_sha256"])
print("PROOF_SHA256=" + receipt["proof_sha256"])
print("RECEIPT_SHA256=" + hashlib.sha256(out.read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(ROOT))

if not passed:
    raise SystemExit(1)
