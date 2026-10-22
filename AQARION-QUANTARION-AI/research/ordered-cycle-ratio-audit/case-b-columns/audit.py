#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
import platform

ROOT = Path(__file__).resolve().parent
MAX_M = 10


def profile_z(lengths):
    return math.prod(
        length**count * math.factorial(count)
        for length, count in Counter(lengths).items()
    )


def maximum_profile_size(m):
    budget = math.factorial(m)
    best_sum = -1
    best_profile = None
    nodes = 0

    def visit(prefix, z, last, run):
        nonlocal best_sum, best_profile, nodes
        nodes += 1
        remaining = m - len(prefix)

        def accept(candidate):
            nonlocal best_sum, best_profile
            total = sum(candidate)
            if total > best_sum:
                best_sum = total
                best_profile = candidate

        if remaining == 1:
            if prefix and z * last * (run + 1) <= budget:
                accept(prefix + (last,))

            largest_new = budget // z
            minimum_new = last + 1 if prefix else 1
            if largest_new >= minimum_new:
                accept(prefix + (largest_new,))
            return

        length = last
        while z * length**remaining <= budget:
            new_run = (
                run + 1
                if prefix and length == last
                else 1
            )
            new_z = z * length * new_run
            if new_z <= budget:
                visit(
                    prefix + (length,),
                    new_z,
                    length,
                    new_run
                )
            length += 1

    visit((), 1, 1, 0)

    if best_profile is None:
        raise AssertionError("No admissible profile")

    if len(best_profile) != m:
        raise AssertionError("Invalid witness length")

    if profile_z(best_profile) > budget:
        raise AssertionError("Witness exceeds budget")

    return {
        "m": m,
        "B_m": best_sum,
        "maximizing_profile": list(best_profile),
        "witness_z": str(profile_z(best_profile)),
        "factorial_budget": str(budget),
        "search_nodes": nodes
    }


bounds = {
    m: maximum_profile_size(m)
    for m in range(1, MAX_M + 1)
}

N = max(row["B_m"] for row in bounds.values())
facts = [math.factorial(n) for n in range(N + 1)]

P = [[0] * (MAX_M + 1) for _ in range(N + 1)]
P[0][0] = 1

for n in range(1, N + 1):
    for m in range(1, min(n, MAX_M) + 1):
        P[n][m] = P[n - 1][m - 1]
        if n >= m:
            P[n][m] += P[n - m][m]

previous = [1] + [0] * MAX_M
certificates = []
unexpected_zeros = []
positive = negative = 0

for n in range(1, N + 1):
    current = [0] * (MAX_M + 1)

    for m in range(1, min(n, MAX_M) + 1):
        current[m] = (
            (n - 1) * previous[m] + previous[m - 1]
        )

        if 2 * m < n <= bounds[m]["B_m"]:
            difference = (
                facts[m] * current[m]
                - facts[n] * P[n][m]
            )

            certificates.append({
                "n": n,
                "m": m,
                "stirling_c": str(current[m]),
                "partition_count": str(P[n][m]),
                "integer_difference": str(difference)
            })

            if difference == 0:
                unexpected_zeros.append([n, m])
            elif difference > 0:
                positive += 1
            else:
                negative += 1

    previous = current

expected_checks = sum(
    max(0, row["B_m"] - 2 * m)
    for m, row in bounds.items()
)

complete = len(certificates) == expected_checks
passed = complete and not unexpected_zeros

proof = r"""# Case B: fixed-column tail reduction

Define
R(n,m) = m! c(n,m)/(n! P(n,m)),
where P(n,m) counts integer partitions into m positive parts.

For a cycle-length profile mu=1^a1 2^a2 ... with m parts, define
z_mu=product(j^aj aj!).
The cycle-type formula gives

    R(n,m) = (1/P(n,m)) sum_{mu partitions n, length(mu)=m} m!/z_mu.

Define
B_m=max{|mu| : length(mu)=m and z_mu<=m!}.

This maximum is finite. For cycle lengths r_1,...,r_m,

    z_mu >= product(r_i) >= 1+sum(r_i-1)=n-m+1.

Therefore z_mu<=m! implies n<=m!+m-1.
The admissible set is nonempty because m singleton cycles have z_mu=m!.

For n>B_m, every summand m!/z_mu is strictly less than one.
Hence R(n,m)<1. In Case B only 2m<n<=B_m needs checking.

The exact search generates nondecreasing cycle lengths.
Appending a length j multiplies z by j times its new multiplicity.

At a prefix with current z and r remaining lengths, all future lengths
are at least j. Their final z is at least z*j^r.
Therefore z*j^r>m! safely excludes that branch and every larger j.

When one length remains, there are two possibilities:
- repeat the last length, including its multiplicity increment;
- choose a strictly larger new length, for which the largest feasible
  choice is floor(m!/z).
These two cases give the exact largest completion sum for that prefix.

Consequently the search computes the exact B_m, not merely a witness
or an upper-bound estimate.

The receipt records B_m, maximizing witnesses, and exact comparisons
m!c(n,m)-n!P(n,m) for every 2m<n<=B_m in the selected columns.

No equality in those finite ranges, together with the tail theorem,
excludes equality throughout Case B for the selected m values.

Status: computer-assisted fixed-column result.
The global question for arbitrarily large m remains open.
This is not proof-assistant certification or a novelty assertion.
"""

proof_path = ROOT / "proof.md"
with proof_path.open("x", encoding="utf-8") as stream:
    stream.write(proof)

receipt = {
    "audit": "case_b_fixed_column_tail_certificate",
    "status": "PASS" if passed else "FAIL",
    "python": platform.python_version(),
    "completed_at_utc": datetime.now(timezone.utc).isoformat(),
    "script_sha256": hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest(),
    "proof_sha256": hashlib.sha256(
        proof_path.read_bytes()
    ).hexdigest(),
    "maximum_m": MAX_M,
    "maximum_finite_n": N,
    "bounds": list(bounds.values()),
    "expected_finite_comparisons": expected_checks,
    "actual_finite_comparisons": len(certificates),
    "positive_differences": positive,
    "negative_differences": negative,
    "unexpected_zeros": unexpected_zeros,
    "finite_certificates": certificates,
    "tail_statement": "n>B_m implies R(n,m)<1",
    "remaining_region": "m>=11 and 2m<n<=B_m",
    "global_equality_classification_proved": False,
    "git_operations": 0
}

out = ROOT / "receipt.json"
with out.open("x", encoding="utf-8") as stream:
    json.dump(receipt, stream, indent=2)

print("STATUS=" + receipt["status"])
print("COLUMNS_CHECKED=1..10")
for m, row in bounds.items():
    print("B_" + str(m) + "=" + str(row["B_m"]))
print("FINITE_COMPARISONS=" + str(len(certificates)))
print("POSITIVE_NEGATIVE=" + str([positive, negative]))
print("UNEXPECTED_ZEROS=" + str(unexpected_zeros))
print("SOURCE_SHA256=" + receipt["script_sha256"])
print("PROOF_SHA256=" + receipt["proof_sha256"])
print("RECEIPT_SHA256=" + hashlib.sha256(out.read_bytes()).hexdigest())
print("EVIDENCE_DIRECTORY=" + str(ROOT))
print("GLOBAL_CLASSIFICATION=OPEN")

if not passed:
    raise SystemExit(1)
