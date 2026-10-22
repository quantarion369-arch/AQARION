#!/usr/bin/env python3
"""AQARION joint K,Q and incidence audit. Standard library only."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import permutations
from math import factorial, comb
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import json
import platform
import sys
import time
import traceback

N = 10
DIRECT_N = 6
AK, AQ = 3, 2


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def falling(n, r):
    return factorial(n) // factorial(n-r) if 0 <= r <= n else 0


def profiles(n, low=1):
    if n == 0:
        yield ()
    for j in range(low, n+1):
        for rest in profiles(n-j, j):
            yield (j,) + rest


def multiply(p, q):
    out = Counter()
    for (k, u), a in p.items():
        for (l, v), b in q.items():
            out[k+l, u+v] += a*b
    return out


def setparts(n):
    def rec(a):
        if len(a) == n:
            yield tuple(a)
            return
        for j in range(max(a)+2):
            yield from rec(a+[j])
    yield from rec([0])


def cycle_labels(p):
    labels = [-1] * len(p)
    count = 0
    for i in range(len(p)):
        if labels[i] < 0:
            j = i
            while labels[j] < 0:
                labels[j] = count
                j = p[j]
            count += 1
    return labels, count


def rank_mod(matrix, prime):
    a = [[x % prime for x in row] for row in matrix]
    rank = 0

    for col in range(len(a[0]) if a else 0):
        pivot = next(
            (i for i in range(rank, len(a)) if a[i][col]),
            None
        )
        if pivot is None:
            continue

        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], -1, prime)
        a[rank] = [(x*inverse) % prime for x in a[rank]]

        for i in range(rank+1, len(a)):
            scale = a[i][col]
            if scale:
                a[i] = [
                    (x-scale*y) % prime
                    for x, y in zip(a[i], a[rank])
                ]
        rank += 1

    return rank


def audit():
    C = [[0] * (N+1) for _ in range(N+1)]
    P = [[0] * (N+1) for _ in range(N+1)]
    C[0][0] = P[0][0] = 1

    for n in range(1, N+1):
        for m in range(1, n+1):
            C[n][m] = (
                (n-1)*C[n-1][m]
                + C[n-1][m-1]
            )

    for m in range(1, N+1):
        for n in range(1, N+1):
            P[n][m] = (
                P[n-1][m-1]
                + (P[n-m][m] if n >= m else 0)
            )

    print("RUNNING=joint-profile-polynomials", flush=True)
    J = {}

    for n in range(1, N+1):
        for lam in profiles(n):
            m = len(lam)
            poly = Counter({(0, 0): 1})
            denominator = 1

            for j, a in Counter(lam).items():
                denominator *= factorial(j)**a * factorial(a)

                for r in range(a):
                    factor = Counter({
                        (k, 1): C[j][k]
                        for k in range(1, j+1)
                    })
                    if r:
                        factor[0, 0] = r*factorial(j)
                    poly = multiply(poly, factor)

            need(
                factorial(n) % denominator == 0,
                "Nonintegral profile multiplicity"
            )

            out = J.setdefault((n, m), Counter())
            for key, value in poly.items():
                out[key] += factorial(n)//denominator * value

    for (n, m), poly in J.items():
        need(
            sum(poly.values()) == factorial(n)*P[n][m],
            "Joint normalization mismatch"
        )
        need(
            all(
                1 <= q <= m
                and 1 <= k <= n
                and n-k-m+q >= 0
                for (k, q), value in poly.items()
                if value
            ),
            "Invalid joint support"
        )

    print("RUNNING=mixed-factorial-recurrence", flush=True)

    local = [
        [F(0)] * (AK+1)
        for _ in range(N+1)
    ]

    for j in range(1, N+1):
        for i in range(AK+1):
            local[j][i] = F(
                sum(
                    C[j][k]*falling(k, i)
                    for k in range(j+1)
                ),
                factorial(j)
            )

    D = {
        (a, b): [
            [F(0)] * (N+1)
            for _ in range(N+1)
        ]
        for a in range(AK+1)
        for b in range(AQ+1)
    }
    D[0, 0][0][0] = F(1)

    for n in range(1, N+1):
        for m in range(1, n+1):
            for a, b in D:
                total = F(0)

                for j in range(1, n+1):
                    for r in range(1, min(m, n//j)+1):
                        for i in range(a+1):
                            for h in range(min(1, b)+1):
                                total += (
                                    comb(a, i)
                                    * comb(b, h)
                                    * local[j][i]
                                    * D[a-i, b-h][n-j*r][m-r]
                                )

                D[a, b][n][m] = total/m

    mixed = []

    for (n, m), poly in sorted(J.items()):
        for a, b in D:
            exact = F(
                sum(
                    value*falling(k, a)*falling(q, b)
                    for (k, q), value in poly.items()
                ),
                factorial(n)
            )

            need(
                exact == D[a, b][n][m],
                "Mixed recurrence mismatch " + str((n, m, a, b))
            )

            mixed.append(dict(
                n=n,
                m=m,
                K_order=a,
                Q_order=b,
                polynomial=str(exact),
                recurrence=str(D[a, b][n][m]),
                status="PASS"
            ))

    print("RUNNING=joint-and-incidence-moments", flush=True)
    moments = []

    for (n, m), poly in sorted(J.items()):
        mass = sum(poly.values())

        def expectation(function):
            return F(
                sum(
                    function(k, q)*value
                    for (k, q), value in poly.items()
                ),
                mass
            )

        ek = expectation(lambda k, q: k)
        eq = expectation(lambda k, q: q)
        eb = expectation(lambda k, q: n-k-m+q)

        vk = expectation(lambda k, q: k*k) - ek*ek
        vq = expectation(lambda k, q: q*q) - eq*eq
        cov = expectation(lambda k, q: k*q) - ek*eq
        vb = expectation(lambda k, q: (n-k-m+q)**2) - eb*eb

        need(eb == n-m-ek+eq, "Incidence mean identity")
        need(vb == vk+vq-2*cov, "Incidence covariance identity")
        need(min(vk, vq, vb) >= 0, "Negative variance")

        moments.append(dict(
            n=n,
            m=m,
            pairs=mass,
            mean_K=str(ek),
            variance_K=str(vk),
            mean_Q=str(eq),
            variance_Q=str(vq),
            covariance_K_Q=str(cov),
            mean_beta0=str(eq),
            mean_beta1=str(eb),
            variance_beta1=str(vb)
        ))

    reference = {
        (2, 1): ("3/2", "1", "1/2", "1/4"),
        (3, 2): ("5/2", "2", "1/2", "1/4"),
        (4, 2): ("61/24", "7/4", "29/24", "263/576"),
        (4, 3): ("3", "5/2", "1/2", "1/4"),
        (5, 3): ("79/24", "5/2", "29/24", "263/576"),
        (6, 3): ("32/9", "22/9", "17/9", "221/324"),
    }

    for row in moments:
        key = (row["n"], row["m"])
        if key in reference:
            actual = tuple(
                row[name] for name in [
                    "mean_K",
                    "mean_Q",
                    "mean_beta1",
                    "variance_beta1"
                ]
            )
            need(
                actual == reference[key],
                "Reference table mismatch " + str(key)
            )

    direct = []
    valid_pairs = 0
    direct_permutations = 0

    for n in range(1, DIRECT_N+1):
        print(
            "RUNNING=direct-pairs-and-boundary-ranks n=" + str(n),
            flush=True
        )

        observed = defaultdict(Counter)
        partitions = list(setparts(n))
        per_m = Counter()

        for permutation in permutations(range(n)):
            direct_permutations += 1
            cycle_id, k = cycle_labels(permutation)

            for blocks in partitions:
                m = max(blocks)+1
                tau = [None] * m
                compatible = True

                for i, block in enumerate(blocks):
                    destination = blocks[permutation[i]]

                    if (
                        tau[block] is not None
                        and tau[block] != destination
                    ):
                        compatible = False
                        break

                    tau[block] = destination

                if not compatible:
                    continue

                need(
                    sorted(tau) == list(range(m)),
                    "Induced map is not a permutation"
                )

                _, q = cycle_labels(tau)

                boundary = [[0] * n for _ in range(k+m)]
                for i in range(n):
                    boundary[cycle_id[i]][i] = -1
                    boundary[k+blocks[i]][i] = 1

                r2 = rank_mod(boundary, 2)
                r3 = rank_mod(boundary, 3)

                need(
                    r2 == r3 == k+m-q,
                    "Boundary-rank identity"
                )
                need(k+m-r2 == q, "Boundary beta0")
                need(
                    n-r2 == n-k-m+q >= 0,
                    "Boundary beta1"
                )

                observed[m][k, q] += 1
                valid_pairs += 1
                per_m[m] += 1

        for m in range(1, n+1):
            need(
                observed[m] == J[n, m],
                "Direct joint distribution " + str((n, m))
            )
            direct.append(dict(
                n=n,
                m=m,
                valid_pairs=per_m[m],
                joint_distribution="PASS",
                rank_F2="PASS",
                rank_F3="PASS"
            ))

    print("RUNNING=counterexample-family-checks", flush=True)
    counterexamples = []

    for n in range(2, N+1):
        left = Counter()
        right = Counter()

        for (k, q), value in J[n, 1].items():
            left[k] += value

        for (k, q), value in J[n, n].items():
            right[k] += value

        need(
            left == right == Counter({
                k: C[n][k] for k in range(1, n+1)
            }),
            "Extreme-column cycle distributions"
        )

        m = n-1
        beta = Counter()

        for (k, q), value in J[n, m].items():
            beta[n-k-m+q] += value

        mass = sum(beta.values())

        need(
            {b: F(value, mass) for b, value in beta.items()}
            == {0: F(1, 2), 1: F(1, 2)},
            "Incidence counterexample family"
        )

        ratio = F(
            factorial(m)*C[n][m],
            factorial(n)*P[n][m]
        )
        need(ratio == F(n-1, 2), "Near-diagonal ratio")

        counterexamples.append(dict(
            n=n,
            m=m,
            prob_beta1_zero="1/2",
            prob_beta1_one="1/2",
            ratio=str(ratio),
            R_n_1=str(F(1, n)),
            R_n_n="1"
        ))

    joint_rows = []

    for (n, m), poly in sorted(J.items()):
        for (k, q), value in sorted(poly.items()):
            joint_rows.append(dict(
                n=n,
                m=m,
                K=k,
                Q=q,
                beta0=q,
                beta1=n-k-m+q,
                count=value
            ))

    need(
        len(J) == 55
        and len(mixed) == 660
        and len(direct) == 21
        and valid_pairs == 8903,
        "Acceptance counts differ"
    )

    tables = {
        "joint_coefficients.csv": joint_rows,
        "mixed_checks.csv": mixed,
        "moments.csv": moments,
        "direct_checks.csv": direct,
        "counterexamples.csv": counterexamples
    }

    report = dict(
        status="PASS",
        joint_max_n=N,
        direct_max_n=DIRECT_N,
        K_orders=[0, AK],
        Q_orders=[0, AQ],
        joint_polynomial_pairs=len(J),
        mixed_factorial_comparisons=len(mixed),
        direct_joint_distribution_checks=len(direct),
        direct_valid_pairs=valid_pairs,
        direct_permutations=direct_permutations,
        boundary_rank_field_computations=2*valid_pairs,
        boundary_rank_failures=0,
        recurrence_failures=0,
        reference_table_checks=len(reference),
        incidence_covariance_checks=len(moments),
        counterexample_family_checks=len(counterexamples),
        fields=[2, 3],
        integral_Smith_normal_form_computed=False,
        source_independence=(
            "different representations; shared exact local Stirling table"
        ),
        global_ratio_classification="OPEN",
        git_operations=0
    )

    return tables, report


def main():
    root = Path(__file__).resolve().parent
    source = Path(__file__).read_bytes()
    started = time.monotonic()

    tables, report = audit()
    artifacts = {}

    for name, rows in tables.items():
        with (root/name).open(
            "x", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(rows[0])
            )
            writer.writeheader()
            writer.writerows(rows)

        raw = (root/name).read_bytes()
        artifacts[name] = dict(
            rows=len(rows),
            bytes=len(raw),
            sha256=hashlib.sha256(raw).hexdigest()
        )

    need(
        source == Path(__file__).read_bytes(),
        "Source changed during execution"
    )

    report.update(
        python=platform.python_version(),
        executable=sys.executable,
        termux_executable_path_detected="com.termux" in sys.executable,
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        elapsed_seconds=round(time.monotonic()-started, 3),
        source_sha256=hashlib.sha256(source).hexdigest(),
        artifacts=artifacts,
        scope=(
            "exact finite joint-statistic and incidence graph checks; "
            "no global ratio theorem"
        )
    )

    receipt = root/"receipt.json"
    with receipt.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)

    for key in [
        "status",
        "joint_polynomial_pairs",
        "mixed_factorial_comparisons",
        "direct_joint_distribution_checks",
        "direct_valid_pairs",
        "boundary_rank_field_computations",
        "boundary_rank_failures",
        "recurrence_failures",
        "reference_table_checks",
        "counterexample_family_checks"
    ]:
        print(key.upper() + "=" + str(report[key]))

    print("SOURCE_SHA256=" + report["source_sha256"])
    print(
        "RECEIPT_SHA256="
        + hashlib.sha256(receipt.read_bytes()).hexdigest()
    )
    print("EVIDENCE_DIRECTORY=" + str(root))
    print("GLOBAL_CLASSIFICATION=OPEN")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        error = dict(
            status="FAIL",
            python=platform.python_version(),
            executable=sys.executable,
            source_sha256=hashlib.sha256(
                Path(__file__).read_bytes()
            ).hexdigest(),
            traceback=traceback.format_exc(),
            git_operations=0
        )
        with (
            Path(__file__).resolve().parent/"failure.json"
        ).open("x", encoding="utf-8") as stream:
            json.dump(error, stream, indent=2)
        raise
