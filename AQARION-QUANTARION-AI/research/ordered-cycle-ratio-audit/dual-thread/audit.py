#!/usr/bin/env python3
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction as F
from datetime import datetime, timezone
import csv
import hashlib
import itertools
import json
import math
import platform
import traceback


def need(ok, message):
    if not ok:
        raise AssertionError(message)


def parts(n, low=1):
    if n == 0:
        yield ()
    for j in range(low, n + 1):
        for tail in parts(n - j, j):
            yield (j,) + tail


def broken(n, m):
    def rec(total, slots, low):
        if slots == 0:
            if total == 0:
                yield {}
            return
        for j in range(low, total - slots + 2):
            for a in range(1, min(total // j, slots) + 1):
                if total - j * a >= slots - a:
                    for rest in rec(total - j * a, slots - a, j):
                        yield {j: a, **rest}
    yield from rec(n, m, 1)


def mul(p, q):
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return out


def labels(n):
    def rec(a):
        if len(a) == n:
            yield tuple(a)
            return
        for j in range(max(a) + 2):
            yield from rec(a + [j])
    yield from rec([0])


def cycles(p):
    seen = set()
    count = 0
    for i in range(len(p)):
        if i not in seen:
            count += 1
            j = i
            while j not in seen:
                seen.add(j)
                j = p[j]
    return count


def invariant(p, a):
    image = {}
    for i, block in enumerate(a):
        target = a[p[i]]
        if block in image and image[block] != target:
            return False
        image[block] = target
    return True


def run():
    N = 13
    PN = 10
    DN = 6

    facts = [math.factorial(n) for n in range(N + 1)]
    C = [[0] * (N + 1) for _ in range(N + 1)]
    P = [[0] * (N + 1) for _ in range(N + 1)]
    C[0][0] = P[0][0] = 1

    for n in range(1, N + 1):
        for m in range(1, n + 1):
            C[n][m] = (
                (n - 1) * C[n - 1][m]
                + C[n - 1][m - 1]
            )

    for m in range(1, N + 1):
        for n in range(1, N + 1):
            P[n][m] = (
                P[n - 1][m - 1]
                + (P[n - m][m] if n >= m else 0)
            )

    H = [F(0)]
    for n in range(1, N + 1):
        H.append(H[-1] + F(1, n))

    def profile_poly(profile):
        poly = [1]
        denominator = 1

        for j, a in profile.items():
            denominator *= facts[j] ** a * facts[a]
            for r in range(a):
                factor = C[j][:j + 1].copy()
                factor[0] += r * facts[j]
                poly = mul(poly, factor)

        return poly, denominator

    print("RUNNING=weighted-endofunction-identities", flush=True)
    enumeration = []

    for n in range(1, N + 1):
        E = {
            k: math.comb(n, k) * facts[k]
            * (1 if k == n else k * n ** (n - k - 1))
            for k in range(1, n + 1)
        }

        ordinary = sum(E.values())
        by_m = [
            sum(E[k] * P[k][m] for k in range(m, n + 1))
            for m in range(1, n + 1)
        ]
        total = sum(by_m)

        need(ordinary == n ** n, "Plain endofunction identity")
        need(
            total == sum(E[k] * sum(P[k]) for k in E),
            "Weighted endofunction identity"
        )
        need(
            total == ordinary if n == 1 else total > ordinary,
            "Weighted total inequality"
        )

        enumeration.append(dict(
            n=n,
            A_total=total,
            endofunction_total=ordinary,
            ratio=str(F(total, ordinary)),
            counts_by_m=json.dumps(by_m)
        ))

    print("RUNNING=profile-polynomials-and-exact-moments", flush=True)

    B = {}
    polynomials = []
    moments = []
    matches = []
    profile_count = 0

    for n in range(1, PN + 1):
        grouped = defaultdict(list)

        for lam in parts(n):
            grouped[len(lam)].append(Counter(lam))
            profile_count += 1

        for m in range(1, n + 1):
            need(len(grouped[m]) == P[n][m], "Profile count")

            total = [0] * (n + 1)
            mean_check = F(0)

            for profile in grouped[m]:
                need(
                    sum(j * a for j, a in profile.items()) == n,
                    "Profile size"
                )
                need(sum(profile.values()) == m, "Profile blocks")

                poly, denominator = profile_poly(profile)
                need(
                    facts[n] % denominator == 0,
                    "Set-partition multinomial denominator"
                )

                for k, value in enumerate(poly):
                    total[k] += facts[n] // denominator * value

                mean_check += sum(
                    (H[j] * H[a] for j, a in profile.items()),
                    F(0)
                )

            B[n, m] = total
            mass = sum(total)

            need(
                mass == facts[n] * P[n][m],
                "Polynomial normalization"
            )

            first = sum(k * value for k, value in enumerate(total))
            second = sum(
                k * k * value for k, value in enumerate(total)
            )
            mean = F(first, mass)
            variance = F(second, mass) - mean * mean

            need(
                mean == mean_check / P[n][m],
                "Independent harmonic first-moment identity"
            )
            need(variance >= 0, "Negative variance")

            A = [0] * (n + 1)
            A[m] = facts[m] * C[n][m]

            if A == total:
                matches.append([n, m])

            if m in (1, n):
                need(
                    total == C[n][:n + 1],
                    "Extreme-column cycle polynomial"
                )

            polynomials.append(dict(
                n=n,
                m=m,
                A=json.dumps(A),
                B=json.dumps(total),
                A_total=sum(A),
                B_total=mass
            ))

            moments.append(dict(
                n=n,
                m=m,
                mean_beta0=str(mean),
                mean_beta1=str(mean),
                second_raw_moment=str(F(second, mass)),
                variance=str(variance)
            ))

    need(matches == [[1, 1]], "Homology-distribution matches")

    print("RUNNING=broken-generator-negative-control", flush=True)
    bad = []

    for n in range(1, 9):
        for m in range(1, n + 1):
            mass = 0

            for profile in broken(n, m):
                poly, denominator = profile_poly(profile)
                mass += facts[n] // denominator * sum(poly)

            expected = facts[n] * P[n][m]
            if mass != expected:
                bad.append([n, m, mass, expected])

    need(
        [2, 2, 4, 2] in bad,
        "Faulty profile-generator negative control not detected"
    )

    print("RUNNING=direct-permutation-partition-check", flush=True)
    direct = []
    permutation_count = 0

    for n in range(1, DN + 1):
        partitions = list(labels(n))
        observed = defaultdict(Counter)

        for permutation in itertools.permutations(range(n)):
            permutation_count += 1
            k = cycles(permutation)

            for partition in partitions:
                if invariant(permutation, partition):
                    observed[max(partition) + 1][k] += 1

        for m in range(1, n + 1):
            values = [
                observed[m][k] for k in range(n + 1)
            ]

            need(
                values == B[n, m],
                "Direct invariant-pair distribution mismatch"
            )

            direct.append(dict(
                n=n,
                m=m,
                observed=json.dumps(values),
                status="PASS"
            ))

    tables = {
        "enumeration.csv": enumeration,
        "polynomials.csv": polynomials,
        "moments.csv": moments,
        "direct_checks.csv": direct
    }

    report = dict(
        status="PASS",
        enumeration_max_n=N,
        polynomial_max_n=PN,
        polynomial_pairs=len(polynomials),
        profiles=profile_count,
        exact_moment_checks=len(moments),
        broken_generator_failures=len(bad),
        broken_generator_examples=bad[:3],
        direct_max_n=DN,
        direct_distribution_checks=len(direct),
        direct_permutations=permutation_count,
        homology_distribution_matches=matches,
        selected_polynomials={
            str(pair): B[pair]
            for pair in [(3, 2), (4, 2), (4, 3), (5, 3)]
        },
        homology_model=(
            "ordinary integral homology; permutation graph "
            "keeps loops and distinct edges"
        ),
        global_ratio_classification="OPEN",
        git_operations=0
    )

    return tables, report


def main():
    root = Path(__file__).resolve().parent
    tables, report = run()
    artifacts = {}

    for name, rows in tables.items():
        with (root / name).open(
            "x", newline="", encoding="utf-8"
        ) as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(rows[0])
            )
            writer.writeheader()
            writer.writerows(rows)

        data = (root / name).read_bytes()
        artifacts[name] = dict(
            bytes=len(data),
            sha256=hashlib.sha256(data).hexdigest()
        )

    report.update(
        python=platform.python_version(),
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        artifacts=artifacts
    )

    with (root / "receipt.json").open(
        "x", encoding="utf-8"
    ) as stream:
        json.dump(report, stream, indent=2)

    for key in [
        "status",
        "enumeration_max_n",
        "polynomial_pairs",
        "exact_moment_checks",
        "broken_generator_failures",
        "direct_distribution_checks",
        "direct_permutations",
        "homology_distribution_matches"
    ]:
        print(key.upper() + "=" + str(report[key]))

    for pair, poly in report["selected_polynomials"].items():
        print("B_" + pair + "=" + str(poly))

    print("SOURCE_SHA256=" + report["source_sha256"])
    print(
        "RECEIPT_SHA256="
        + hashlib.sha256(
            (root / "receipt.json").read_bytes()
        ).hexdigest()
    )
    print("EVIDENCE_DIRECTORY=" + str(root))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        root = Path(__file__).resolve().parent
        with (root / "failure.txt").open(
            "a", encoding="utf-8"
        ) as stream:
            stream.write(traceback.format_exc())
        raise
