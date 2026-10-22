#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import platform

ROOT = Path(__file__).resolve().parent
N = 300

primes = [
    p for p in range(2, N + 1)
    if all(p % q for q in range(2, math.isqrt(p) + 1))
]

C = [[0] * (N + 1) for _ in range(N + 1)]
C[0][0] = 1

for n in range(1, N + 1):
    for m in range(1, n + 1):
        C[n][m] = (
            (n - 1) * C[n - 1][m]
            + C[n - 1][m - 1]
        )

checks = 0
failure_count = 0
failure_examples = []
witnesses = []
witness_failure_count = 0

for p in primes:
    for n in range(p, N + 1):
        a, r = divmod(n, p)

        for m in range(1, min(p - 1, n) + 1):
            k = m - a
            expected = (
                ((-1) ** a * C[r][k]) % p
                if 0 <= k <= r else 0
            )
            observed = C[n][m] % p
            checks += 1

            if observed != expected:
                failure_count += 1
                if len(failure_examples) < 20:
                    failure_examples.append({
                        "n": n,
                        "m": m,
                        "p": p,
                        "observed": observed,
                        "expected": expected
                    })

    for m in range(1, p):
        for a in range(1, m + 1):
            d = a * (p - 1)
            n = m + d

            if n > N or d <= m:
                continue

            observed = C[n][m] % p
            expected = ((-1) ** a) % p

            denominator_divisible = (
                (math.factorial(n) // math.factorial(m)) % p == 0
            )

            if observed != expected or not denominator_divisible:
                witness_failure_count += 1

            witnesses.append({
                "n": n,
                "m": m,
                "d": d,
                "prime": p,
                "a": a,
                "stirling_residue": observed,
                "expected_residue": expected
            })

pairs = {(w["n"], w["m"]) for w in witnesses}
new_pairs = {
    (w["n"], w["m"])
    for w in witnesses
    if w["m"] >= 11
}

passed = failure_count == 0 and witness_failure_count == 0

proof = r"""# Prime obstruction for ordered-cycle ratio equality

Let c(n,m) denote the unsigned Stirling number of the first kind, and
R(n,m)=m!c(n,m)/(n!P(n,m)), where P(n,m) counts partitions into m parts.

The classical generating polynomial is
    F_n(x)=product_{j=0}^{n-1}(x+j)=sum_m c(n,m)x^m.

For prime p,
    product_{j=0}^{p-1}(x+j)=x^p-x modulo p.
This follows because both monic degree-p polynomials have every element
of the field with p elements as a root.

Write n=ap+r, 0<=r<p. Grouping the factors into complete residue blocks gives
    F_n(x)=(x^p-x)^a F_r(x) modulo p.

Assume a>=1 and 1<=m<p.
The lowest term of (x^p-x)^a is (-1)^a x^a.
Every other term has degree at least a+p-1>=p.
Therefore
    c(n,m)=(-1)^a c(r,m-a) modulo p.
Use c(0,0)=1 and zero for invalid indices.

Choose a prime p>m and 1<=a<=m, and let
    d=a(p-1), n=m+d=ap+(m-a).
Then 0<=m-a<p and
    c(n,m)=(-1)^a c(m-a,m-a)=(-1)^a modulo p,
which is nonzero.

But n>=p>m, so p divides n!/m!.
Equality R(n,m)=1 would require
    c(n,m)=(n!/m!)P(n,m),
contradicting the nonzero residue.

Thus equality is excluded for this entire family.
Its Case B portion is selected by d>m.

In particular, if d>m and d+1 is prime, choose a=1 and p=d+1.
This excludes every Case B pair with prime d+1.

The accompanying finite check compares the congruence with exact
Stirling integers through n=300. It is an implementation check, not
the justification of the infinite theorem.

The global equality classification remains open.
No novelty or proof-assistant certification is asserted.

Normalization warning:
A_d(m)=m!c(m+d,m)/(m+d)! is generally rational.
Multiplying it by m! does not generally make it integral.
The exact integer normalization is
    ((m+d)!/m!) A_d(m)=c(m+d,m).
"""

proof_path = ROOT / "proof.md"
with proof_path.open("x", encoding="utf-8") as stream:
    stream.write(proof)

receipt = {
    "audit": "prime_block_congruence_and_equality_obstruction",
    "status": "PASS" if passed else "FAIL",
    "maximum_n": N,
    "python": platform.python_version(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "proof_sha256": hashlib.sha256(
        proof_path.read_bytes()
    ).hexdigest(),
    "general_congruence_checks": checks,
    "congruence_failure_count": failure_count,
    "congruence_failure_examples": failure_examples,
    "family_witness_failure_count": witness_failure_count,
    "family_witness_count": len(witnesses),
    "distinct_case_b_pairs": len(pairs),
    "distinct_case_b_pairs_m_ge_11": len(new_pairs),
    "witnesses": witnesses,
    "global_equality_classification_proved": False,
    "git_operations": 0
}

out = ROOT / "receipt.json"
with out.open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, indent=2)

print("STATUS=" + receipt["status"])
print("MAX_N=" + str(N))
print("CONGRUENCE_CHECKS=" + str(checks))
print("CONGRUENCE_FAILURES=" + str(failure_count))
print("WITNESS_FAILURES=" + str(witness_failure_count))
print("FAMILY_WITNESSES=" + str(len(witnesses)))
print("DISTINCT_CASE_B_PAIRS=" + str(len(pairs)))
print("DISTINCT_CASE_B_PAIRS_M_GE_11=" + str(len(new_pairs)))
print("SOURCE_SHA256=" + receipt["script_sha256"])
print("PROOF_SHA256=" + receipt["proof_sha256"])
print("RECEIPT_SHA256=" + hashlib.sha256(out.read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("GLOBAL_CLASSIFICATION=OPEN")

if not passed:
    raise SystemExit(1)
