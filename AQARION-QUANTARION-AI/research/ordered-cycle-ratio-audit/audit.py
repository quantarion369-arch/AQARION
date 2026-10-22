#!/usr/bin/env python3
"""Exact ordered-cycle audit; standard library only."""
import argparse
import csv
import itertools
import json
import math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path


def cycle_types(n, minimum=1):
    if n == 0:
        yield ()
    for j in range(minimum, n + 1):
        for tail in cycle_types(n-j, j):
            yield (j,) + tail


def permutation_type(p):
    seen = set()
    lengths = []
    for i in range(len(p)):
        if i not in seen:
            j, length = i, 0
            while j not in seen:
                seen.add(j)
                length += 1
                j = p[j]
            lengths.append(length)
    return tuple(sorted(lengths))


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def analyze(N, brute_max, out):
    C = [[0]*(N+1) for _ in range(N+1)]
    P = [[0]*(N+1) for _ in range(N+1)]
    C[0][0] = P[0][0] = 1

    for n in range(1, N+1):
        for m in range(1, n+1):
            C[n][m] = (n-1)*C[n-1][m] + C[n-1][m-1]

    for m in range(1, N+1):
        for n in range(1, N+1):
            P[n][m] = P[n-1][m-1]
            if n >= m:
                P[n][m] += P[n-m][m]

    ratios = []
    distributions = []
    equalities = []
    totals = [1]

    for n in range(1, N+1):
        print("RUNNING n=" + str(n), flush=True)
        grouped = defaultdict(list)
        type_counts = {}

        for lengths in cycle_types(n):
            multiplicities = Counter(lengths)
            z = math.prod(
                j**a * math.factorial(a)
                for j, a in multiplicities.items()
            )
            count = math.factorial(n)//z
            m = len(lengths)
            ordered = math.factorial(m)*count
            type_counts[lengths] = count
            grouped[m].append((z, count))

            distributions.append(dict(
                n=n,
                m=m,
                cycle_lengths=' '.join(map(str, lengths)),
                multiplicities=json.dumps(
                    dict(sorted(multiplicities.items()))
                ),
                z_lambda=z,
                permutations=count,
                ordered_cycle_objects=ordered,
                probability=str(Fraction(1, z))
            ))

        require(
            sum(type_counts.values()) == math.factorial(n),
            "Cycle-type total failed"
        )

        if n <= brute_max:
            brute = Counter(
                permutation_type(p)
                for p in itertools.permutations(range(n))
            )
            require(
                dict(brute) == type_counts,
                "Direct permutation distribution mismatch"
            )

        for m in range(1, n+1):
            O = math.factorial(m)*C[n][m]
            D = math.factorial(n)*P[n][m]
            R = Fraction(O, D)

            require(
                sum(count for z, count in grouped[m]) == C[n][m],
                "Stirling versus cycle-type sum failed"
            )
            require(
                len(grouped[m]) == P[n][m],
                "Integer-partition profile count failed"
            )

            profile_ratio = (
                math.factorial(m)
                * sum(
                    (Fraction(1, z) for z, count in grouped[m]),
                    Fraction(0)
                )
                / P[n][m]
            )
            require(profile_ratio == R, "Profile ratio failed")

            if n >= 2:
                rhs = Fraction(0)

                if P[n-1][m]:
                    previous = Fraction(
                        math.factorial(m)*C[n-1][m],
                        math.factorial(n-1)*P[n-1][m]
                    )
                    rhs += (
                        Fraction(n-1, n)
                        * P[n-1][m] * previous
                    )

                if P[n-1][m-1]:
                    previous = Fraction(
                        math.factorial(m-1)*C[n-1][m-1],
                        math.factorial(n-1)*P[n-1][m-1]
                    )
                    rhs += (
                        Fraction(m, n)
                        * P[n-1][m-1] * previous
                    )

                require(
                    R == rhs/P[n][m],
                    "Exact ratio recurrence failed"
                )

            require(
                O == (
                    (n-1)*math.factorial(m)*C[n-1][m]
                    + m*math.factorial(m-1)*C[n-1][m-1]
                ),
                "Ordered-cycle recurrence failed"
            )

            if m == 1:
                require(R == Fraction(1, n), "One-cycle formula")

            if m == n:
                require(R == 1, "Diagonal formula")

            if n >= 2 and m == n-1:
                require(
                    R == Fraction(n-1, 2),
                    "First near-diagonal formula"
                )

            if n >= 4 and m == n-2:
                require(
                    R == Fraction((n-2)*(3*n-1), 48),
                    "Second near-diagonal formula"
                )

            if R == 1:
                equalities.append([n, m])

            ratios.append(dict(
                n=n,
                m=m,
                unsigned_stirling=C[n][m],
                cycle_count=O,
                exact_partitions=P[n][m],
                comparison_count=D,
                ratio=str(R),
                decimal=float(R)
            ))

        total = sum(
            math.factorial(m)*C[n][m]
            for m in range(1, n+1)
        )
        require(
            total == sum(
                math.comb(n, j)*math.factorial(j-1)*totals[n-j]
                for j in range(1, n+1)
            ),
            "Ordered row-sum recurrence failed"
        )
        totals.append(total)

    out.mkdir(parents=True, exist_ok=True)

    for name, rows in [
        ("ratios.csv", ratios),
        ("cycle_length_distributions.csv", distributions)
    ]:
        with (out/name).open("w", newline="") as stream:
            writer = csv.DictWriter(
                stream, fieldnames=list(rows[0])
            )
            writer.writeheader()
            writer.writerows(rows)

    report = dict(
        max_n=N,
        ratio_rows=len(ratios),
        cycle_type_rows=len(distributions),
        brute_force_max=brute_max,
        ratio_equals_one=equalities,
        ordered_row_totals=totals,
        all_exact_assertions="PASS",
        scope=(
            "Ordered cycle objects; "
            "no original cycle_count source imported"
        )
    )

    with (out/"receipt.json").open("w") as stream:
        json.dump(report, stream, indent=2)

    print("n m c(n,m) cycle_count p_exact ratio")
    for row in ratios:
        print(
            row["n"],
            row["m"],
            row["unsigned_stirling"],
            row["cycle_count"],
            row["exact_partitions"],
            row["ratio"]
        )

    print(json.dumps(report, indent=2))
    print("RESULTS_DIRECTORY=" + str(out))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=10)
    parser.add_argument("--brute-max", type=int, default=10)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path.home()/"aqarion_cycle_analysis"
    )
    args = parser.parse_args()

    require(1 <= args.max_n <= 10, "max-n must be 1..10")
    require(
        0 <= args.brute_max <= args.max_n,
        "brute-max must be 0..max-n"
    )

    analyze(args.max_n, args.brute_max, args.out)


if __name__ == "__main__":
    main()
