import itertools as it
import json
import math
import sys
import platform
from collections import Counter
from fractions import Fraction
from pathlib import Path


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def states(q, d):
    return list(it.product(range(q), repeat=d))


def number(z, q):
    r = 0
    for a in z:
        r = q * r + a
    return r


def order(p):
    seen = set()
    result = 1

    for start in range(len(p)):
        if start in seen:
            continue

        x = start
        length = 0

        while x not in seen:
            seen.add(x)
            length += 1
            x = p[x]

        result = math.lcm(result, length)

    return result


def dynamics(T, d, L, q):
    image = set(range(len(T)))
    sequence = []

    for t in range(d + 2):
        sequence.append(len(image))

        require(
            len(image) == q ** max(d - t, L),
            "Image sequence mismatch",
        )

        image = {T[x] for x in image}

    core = sorted(image)
    index = {x: i for i, x in enumerate(core)}

    core_permutation = tuple(index[T[x]] for x in core)

    require(
        len(set(core_permutation)) == len(core),
        "Stabilized image is not permuted",
    )

    return sequence, order(core_permutation)


def canonical(q, d):
    Z = states(q, d)
    output = []

    for j in range(d):
        for p in it.permutations(range(q)):
            T = tuple(
                number(z[1:] + (p[z[j]],), q)
                for z in Z
            )

            L = d - j
            output.append((T, L, L * order(p)))

    for constant in range(q):
        T = tuple(
            number(z[1:] + (constant,), q)
            for z in Z
        )

        output.append((T, 0, 1))

    require(
        len({T for T, _, _ in output})
        == d * math.factorial(q) + q,
        "Canonical descriptions collide",
    )

    return output


def prefix(T, q, d):
    H = q ** (d - 1)
    F = []

    for initial in range(len(T)):
        x = initial
        coordinates = []

        for _ in range(d):
            coordinates.append(x // H)
            x = T[x]

        F.append(number(coordinates, q))

    return tuple(F)


def rank(matrix):
    A = [
        [Fraction(value) for value in row]
        for row in matrix
    ]

    r = 0

    for c in range(len(A[0])):
        pivot = next(
            (i for i in range(r, len(A)) if A[i][c]),
            None,
        )

        if pivot is None:
            continue

        A[r], A[pivot] = A[pivot], A[r]

        value = A[r][c]
        A[r] = [x / value for x in A[r]]

        for i in range(len(A)):
            if i != r and A[i][c]:
                value = A[i][c]
                A[i] = [
                    a - value * b
                    for a, b in zip(A[i], A[r])
                ]

        r += 1

        if r == len(A):
            break

    return r


def binary_registers():
    rows = []

    for d in range(1, 6):
        Z = states(2, d)
        histogram = Counter()
        order_histogram = Counter()
        count = 0

        for tail in it.permutations(range(1, d)):
            path = (0,) + tail

            for signs in it.product(range(2), repeat=d):
                for terminal in range(-1, d):
                    transition = []

                    for z in Z:
                        y = [0] * d

                        for i in range(d - 1):
                            y[path[i]] = (
                                z[path[i + 1]] ^ signs[i]
                            )

                        if terminal == -1:
                            y[path[-1]] = signs[-1]
                        else:
                            y[path[-1]] = (
                                z[path[terminal]] ^ signs[-1]
                            )

                        transition.append(number(y, 2))

                    T = tuple(transition)

                    L = (
                        0 if terminal == -1
                        else d - terminal
                    )

                    sequence, actual_order = dynamics(
                        T, d, L, 2
                    )

                    if L == 0:
                        expected_order = 1
                    else:
                        parity = sum(signs[terminal:]) % 2
                        expected_order = L * (
                            2 if parity else 1
                        )

                    require(
                        actual_order == expected_order,
                        "Binary core order mismatch",
                    )

                    require(
                        len(set(prefix(T, 2, d))) == 2 ** d,
                        "Register is not separating",
                    )

                    histogram[2 ** L] += 1
                    order_histogram[
                        (2 ** L, actual_order)
                    ] += 1

                    count += 1

        each = 2 ** d * math.factorial(d - 1)

        require(
            count == each * (d + 1),
            "Register count mismatch",
        )

        require(
            dict(histogram)
            == {
                2 ** L: each
                for L in range(d + 1)
            },
            "Core histogram mismatch",
        )

        profiles = []

        for k in range(d + 1):
            monomials = [
                S
                for degree in range(k + 1)
                for S in it.combinations(range(d), degree)
            ]

            matrix = [
                [
                    math.prod(z[i] for i in S)
                    for S in monomials
                ]
                for z in Z
            ]

            profiles.append(rank(matrix))

        expected_profile = [
            sum(math.comb(d, r) for r in range(k + 1))
            for k in range(d + 1)
        ]

        require(
            profiles == expected_profile,
            "Exact cube rank profile mismatch",
        )

        rows.append({
            "d": d,
            "registers_checked": count,
            "periodic_core_histogram":
                dict(sorted(histogram.items())),
            "core_order_histogram": [
                {
                    "core_size": core,
                    "order": core_order,
                    "count": multiplicity,
                }
                for (
                    core,
                    core_order,
                ), multiplicity
                in sorted(order_histogram.items())
            ],
            "exact_cube_rank_profile": profiles,
            "image_sequences_and_orders": "PASS",
            "observation_separation": "PASS",
        })

        print(
            f"BINARY_REGISTERS d={d} count={count} PASS",
            flush=True,
        )

    return rows


def labeled(q, d, destination):
    n = q ** d
    H = q ** (d - 1)
    registers = canonical(q, d)

    seen = set()
    histogram = Counter()
    pairs = 0

    fiber_permutations = [
        list(it.permutations(range(a * H, (a + 1) * H)))
        for a in range(q)
    ]

    filename = destination / (
        f"labeled_q{q}_d{d}.jsonl"
    )

    with filename.open("w", encoding="utf-8") as stream:
        for blocks in it.product(*fiber_permutations):
            F = tuple(it.chain.from_iterable(blocks))
            inverse = [0] * n

            for x, y in enumerate(F):
                inverse[y] = x

            for S, L, expected_order in registers:
                T = tuple(
                    inverse[S[F[x]]]
                    for x in range(n)
                )

                pairs += 1

                require(
                    T not in seen,
                    "Duplicate canonical encoding",
                )

                seen.add(T)

                require(
                    prefix(T, q, d) == F,
                    "Encoding not recovered from prefix",
                )

                sequence, actual_order = dynamics(
                    T, d, L, q
                )

                require(
                    actual_order == expected_order,
                    "Labeled core order mismatch",
                )

                histogram[q ** L] += 1

                stream.write(
                    json.dumps({
                        "T": T,
                        "core_size": q ** L,
                        "core_order": actual_order,
                        "image_sizes": sequence,
                    }, separators=(",", ":")) + "\n"
                )

    encodings = math.factorial(H) ** q

    expected_histogram = {
        1: encodings * q,
        **{
            q ** L: encodings * math.factorial(q)
            for L in range(1, d + 1)
        },
    }

    require(
        dict(histogram) == expected_histogram,
        "Labeled histogram mismatch",
    )

    require(
        pairs
        == encodings * (d * math.factorial(q) + q),
        "Labeled count mismatch",
    )

    print(
        f"LABELED_MAPS q={q} d={d} "
        f"distinct={len(seen)} PASS",
        flush=True,
    )

    return {
        "q": q,
        "d": d,
        "encodings": encodings,
        "canonical_terminals": len(registers),
        "distinct_maps": len(seen),
        "periodic_core_histogram":
            dict(sorted(histogram.items())),
        "prefix_recovery_and_uniqueness": "PASS",
    }, seen


def exhaustive_small(d, expected):
    n = 2 ** d
    H = 2 ** (d - 1)
    found = set()
    total = 0

    for T in it.product(range(n), repeat=n):
        total += 1
        words = []

        for initial in range(n):
            x = initial
            word = []

            for _ in range(n):
                word.append(x // H)
                x = T[x]

            words.append(tuple(word))

        if len(set(words)) != n:
            continue

        monomials = [
            S
            for degree in range(d)
            for S in it.combinations(range(n), degree)
        ]

        matrix = [
            [
                math.prod(word[t] for t in S)
                for S in monomials
            ]
            for word in words
        ]

        if rank(matrix) < n:
            found.add(T)

    require(
        found == expected,
        "Exhaustive extremal-classification mismatch",
    )

    print(
        f"ALL_STATE_MAPS n={n} maps={total} "
        f"extremal={len(found)} PASS",
        flush=True,
    )

    return {
        "n": n,
        "all_maps_checked": total,
        "extremal_maps": len(found),
        "exact_set_equality": "PASS",
    }


def main(destination):
    report = {
        "scope": (
            "Binary register descriptions d=1..5; "
            "explicit canonical-encoding deduplication; "
            "exhaustive all-map comparisons only n=2,4."
        ),
        "arithmetic": (
            "Integers and fractions.Fraction; "
            "no floating-point ranks."
        ),
        "binary_registers": binary_registers(),
    }

    labeled_rows = []
    small_rows = []

    for q, d in [(2, 1), (2, 2), (2, 3), (3, 2)]:
        row, maps = labeled(q, d, destination)
        labeled_rows.append(row)

        if q == 2 and d <= 2:
            small_rows.append(
                exhaustive_small(d, maps)
            )

    report.update({
        "labeled_cases": labeled_rows,
        "small_all_map_cases": small_rows,
        "status": "PASS",
        "limitations": [
            "No exhaustive all-map n=8 census.",
            (
                "The spectral equality theorem is an "
                "external mathematical dependency, "
                "not machine-proved here."
            ),
            (
                "Cube ranks are checked directly; "
                "large labeled-map feature matrices "
                "are not independently ranked one by one."
            ),
            (
                "No Lean build, Git operation, "
                "claim enrollment, or promotion."
            ),
        ],
    })

    (destination / "results.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "dependencies": "Python standard library only",
    }

    (destination / "environment.json").write_text(
        json.dumps(environment, indent=2) + "\n",
        encoding="utf-8",
    )

    print("FLOATING_POINT_RANK_USED=NO", flush=True)
    print("ALL_MAP_N8_CENSUS=NOT_RUN", flush=True)
    print("REPOSITORY_OPERATIONS=NONE", flush=True)
    print("OVERALL_STATUS=PASS", flush=True)


if __name__ == "__main__":
    main(Path(sys.argv[1]))
