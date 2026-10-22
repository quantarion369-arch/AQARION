#!/usr/bin/env python3
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
from math import factorial, comb, isqrt
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import platform
import sys
import traceback


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def partitions(n, low=1):
    if n == 0:
        yield ()
    for j in range(low, n + 1):
        for rest in partitions(n - j, j):
            yield (j,) + rest


def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def setparts(n):
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


def audit():
    N = 30
    L = 10
    order = 3

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

    def ratio(n, m):
        return F(
            factorial(m) * C[n][m],
            factorial(n) * P[n][m]
        )

    print("RUNNING=exact-moment-recurrence", flush=True)

    local = [
        [F(0)] * (order + 1)
        for _ in range(L + 1)
    ]

    for j in range(1, L + 1):
        for a in range(order + 1):
            local[j][a] = F(
                sum(
                    C[j][k] * factorial(k) // factorial(k - a)
                    for k in range(a, j + 1)
                ),
                factorial(j)
            )

    D = [
        [[F(0)] * (L + 1) for _ in range(L + 1)]
        for _ in range(order + 1)
    ]
    D[0][0][0] = F(1)

    for n in range(1, L + 1):
        for m in range(1, n + 1):
            for s in range(order + 1):
                D[s][n][m] = sum(
                    (
                        comb(s, a)
                        * local[j][a]
                        * D[s - a][n - j * r][m - r]
                        for j in range(1, n + 1)
                        for r in range(1, min(m, n // j) + 1)
                        for a in range(s + 1)
                    ),
                    F(0)
                ) / m

    print("RUNNING=independent-profile-polynomials", flush=True)

    B = {}
    derivative_checks = 0

    for n in range(1, L + 1):
        for lam in partitions(n):
            m = len(lam)
            poly = [1]
            denominator = 1

            for j, a in Counter(lam).items():
                denominator *= factorial(j) ** a * factorial(a)

                for r in range(a):
                    factor = C[j][:j + 1].copy()
                    factor[0] += r * factorial(j)
                    poly = mul(poly, factor)

            out = B.setdefault((n, m), [0] * (n + 1))

            need(
                factorial(n) % denominator == 0,
                "Nonintegral profile multiplicity"
            )

            for k, value in enumerate(poly):
                out[k] += factorial(n) // denominator * value

    for (n, m), poly in B.items():
        need(
            sum(poly) == factorial(n) * P[n][m],
            "Pair normalization mismatch"
        )

        for s in range(order + 1):
            exact = F(
                sum(
                    value * factorial(k) // factorial(k - s)
                    for k, value in enumerate(poly)
                    if k >= s
                ),
                factorial(n)
            )
            need(
                exact == D[s][n][m],
                "Derivative mismatch at " + str((n, m, s))
            )
            derivative_checks += 1

    print("RUNNING=six-case-direct-pair-enumeration", flush=True)

    expected = {
        (3, 1): (6, F(11, 6), F(17, 36)),
        (3, 2): (6, F(5, 2), F(1, 4)),
        (4, 1): (24, F(25, 12), F(95, 144)),
        (4, 2): (48, F(61, 24), F(455, 576)),
        (5, 1): (120, F(137, 60), F(2951, 3600)),
        (5, 2): (240, F(77, 24), F(407, 576)),
    }

    cases = []

    for (n, m), wanted in expected.items():
        histogram = [0] * (n + 1)
        eligible = [
            a for a in setparts(n)
            if max(a) + 1 == m
        ]

        for permutation in permutations(range(n)):
            k = cycles(permutation)
            for partition in eligible:
                if invariant(permutation, partition):
                    histogram[k] += 1

        need(
            histogram == B[n, m],
            "Direct histogram mismatch"
        )

        mass = sum(histogram)
        mean = F(
            sum(k * value for k, value in enumerate(histogram)),
            mass
        )
        variance = F(
            sum(k * k * value for k, value in enumerate(histogram)),
            mass
        ) - mean * mean

        need(
            (mass, mean, variance) == wanted,
            "Expected moment table mismatch"
        )
        need(
            mean == D[1][n][m] / D[0][n][m],
            "Recurrence mean mismatch"
        )
        need(
            variance
            == (D[2][n][m] + D[1][n][m]) / D[0][n][m]
            - mean * mean,
            "Recurrence variance mismatch"
        )
        need(
            1 <= mean <= n and variance >= 0,
            "Invalid moment bounds"
        )

        cases.append(dict(
            n=n,
            m=m,
            pairs=mass,
            mean=str(mean),
            variance=str(variance)
        ))

    harmonic_checks = 0

    for n in range(1, L + 1):
        h = sum((F(1, j) for j in range(1, n + 1)), F(0))
        h2 = sum((F(1, j*j) for j in range(1, n + 1)), F(0))
        mean = D[1][n][1] / D[0][n][1]
        variance = (
            (D[2][n][1] + D[1][n][1]) / D[0][n][1]
            - mean * mean
        )
        need(
            mean == h and variance == h - h2,
            "Harmonic boundary mismatch"
        )
        harmonic_checks += 1

    print("RUNNING=deficit-formulas-and-root-regressions", flush=True)

    for n in range(2, N + 1):
        need(
            ratio(n, n - 1) == F(n - 1, 2),
            "Deficit-one formula mismatch"
        )

    for n in range(6, N + 1):
        need(
            ratio(n, n - 3) == F(n * (n - 1) * (n - 3), 144),
            "Deficit-three formula mismatch"
        )

    profile_checks = 0

    for d in range(1, 9):
        pd = sum(P[d])
        profiles = list(partitions(d))

        for n in range(2 * d, N + 1):
            m = n - d
            total = F(0)

            for lam in profiles:
                length = len(lam)
                weight = 1

                for j, a in Counter(lam).items():
                    weight *= (j + 1) ** a * factorial(a)

                falling = factorial(m) // factorial(m - length)
                total += F(falling, weight)

            need(
                total / pd == ratio(n, m),
                "Falling-factorial profile formula mismatch"
            )
            profile_checks += 1

        ones = next(lam for lam in profiles if len(lam) == d)
        leading_weight = 1

        for j, a in Counter(ones).items():
            leading_weight *= (j + 1) ** a * factorial(a)

        need(
            leading_weight == 2 ** d * factorial(d),
            "Leading coefficient weight mismatch"
        )

    roots = {
        d: [
            n for n in range(2 * d, N + 1)
            if ratio(n, n - d) == 1
        ]
        for d in range(1, 9)
    }

    need(
        roots == {
            1: [3],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: []
        },
        "Unexpected finite root"
    )

    need(ratio(2, 1) == F(1, 2), "Deficit-one boundary")

    bad = F(3, 4) + F(3 * 4, 6) + F(3 * 4 * 5, 48)
    need(
        bad == 4 and bad != ratio(6, 3),
        "Deficit-three negative control not detected"
    )
    need(
        ratio(4, 2) == F(11, 24) < 1,
        "False-cutoff negative control"
    )
    need(
        isqrt(601) ** 2 != 601,
        "Discriminant check"
    )

    return dict(
        status="PASS",
        six_cases=cases,
        polynomial_pairs=len(B),
        exact_derivative_checks=derivative_checks,
        derivative_orders=[0, 1, 2, 3],
        direct_case_checks=len(cases),
        harmonic_checks=harmonic_checks,
        falling_profile_checks=profile_checks,
        root_comparisons=profile_checks,
        roots=roots,
        negative_controls=dict(
            defective_deficit3_n6=str(bad),
            correct_R_6_3="5/8",
            false_cutoff_R_4_2="11/24"
        ),
        global_ratio_classification="OPEN",
        case_a_reopened=False,
        git_operations=0
    )


def main():
    root = Path(__file__).resolve().parent
    report = audit()

    report.update(
        python=platform.python_version(),
        executable=sys.executable,
        termux_executable_path_detected="com.termux" in sys.executable,
        completed_at_utc=datetime.now(timezone.utc).isoformat(),
        source_sha256=hashlib.sha256(
            Path(__file__).read_bytes()
        ).hexdigest()
    )

    receipt = root / "receipt.json"
    with receipt.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2)

    print("STATUS=PASS")

    for row in report["six_cases"]:
        print(
            "CASE=" + str((row["n"], row["m"]))
            + " PAIRS=" + str(row["pairs"])
            + " MEAN=" + row["mean"]
            + " VAR=" + row["variance"]
        )

    print(
        "EXACT_DERIVATIVE_CHECKS="
        + str(report["exact_derivative_checks"])
    )
    print(
        "FALLING_PROFILE_CHECKS="
        + str(report["falling_profile_checks"])
    )
    print("ROOT_COMPARISONS=" + str(report["root_comparisons"]))
    print("ROOTS=" + str(report["roots"]))
    print("NEGATIVE_CONTROLS=DETECTED")
    print("SOURCE_SHA256=" + report["source_sha256"])
    print(
        "RECEIPT_SHA256="
        + hashlib.sha256(receipt.read_bytes()).hexdigest()
    )
    print("EVIDENCE_DIRECTORY=" + str(root))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        with (
            Path(__file__).resolve().parent / "failure.txt"
        ).open("a", encoding="utf-8") as stream:
            stream.write(traceback.format_exc())
        raise
