from math import comb, prod


def _repair_truth(truth):
    if not isinstance(truth, (list, tuple)):
        raise ValueError("Terminal truth table must be an array")

    n = len(truth)

    if n < 2 or n & (n - 1):
        raise ValueError(
            "Truth-table length must be a power of two >=2"
        )

    if any(type(v) is not int or v not in (0, 1) for v in truth):
        raise ValueError(
            "Truth table must contain integer binary values"
        )

    return list(truth), n.bit_length() - 1


def terminal_repair_certificate(truth):
    values, d = _repair_truth(truth)
    n = len(values)
    coefficients = values[:]

    for bit in range(d):
        for mask in range(n):
            if mask & (1 << bit):
                coefficients[mask] -= coefficients[
                    mask ^ (1 << bit)
                ]

    choices = [
        mask for mask in range(n)
        if mask.bit_count() >= 2 and coefficients[mask]
    ]

    if not choices:
        return None

    support = max(
        choices,
        key=lambda mask: (mask.bit_count(), mask),
    )

    nonlinear = [
        j for j in range(d)
        if support & (1 << (d - 1 - j))
    ]
    multiplier = [
        j for j in range(d)
        if j not in nonlinear
    ]

    moment = sum(
        (-1) ** x.bit_count() * values[x]
        for x in range(n)
        if all(
            (x >> (d - 1 - j)) & 1
            for j in multiplier
        )
    )

    certificate = {
        "parameter_dimension": d,
        "nonlinear_support": nonlinear,
        "coefficient": coefficients[support],
        "multiplier_prefix_coordinates": multiplier,
        "temporal_product_coordinates": multiplier + [d],
        "temporal_product_degree": len(multiplier) + 1,
        "parity_moment": moment,
        "full_rank_degree": d - 1,
        "full_rank": n,
        "method": "INTEGER_MOBIUS_AND_DIRECT_PARITY",
    }

    if not verify_terminal_repair(values, certificate):
        raise AssertionError(
            "Constructed repair certificate failed"
        )

    return certificate


def verify_terminal_repair(truth, certificate):
    try:
        values, d = _repair_truth(truth)
        n = len(values)

        if not isinstance(certificate, dict):
            return False

        support = certificate["nonlinear_support"]

        if not isinstance(support, list) or len(support) < 2:
            return False

        if any(
            type(j) is not int or not 0 <= j < d
            for j in support
        ):
            return False

        if support != sorted(set(support)):
            return False

        multiplier = [
            j for j in range(d)
            if j not in support
        ]

        expected_ints = {
            "parameter_dimension": d,
            "temporal_product_degree": 1 + len(multiplier),
            "full_rank_degree": d - 1,
            "full_rank": n,
        }

        for key, expected in expected_ints.items():
            if (
                type(certificate[key]) is not int
                or certificate[key] != expected
            ):
                return False

        expected_lists = {
            "multiplier_prefix_coordinates": multiplier,
            "temporal_product_coordinates": multiplier + [d],
        }

        for key, expected in expected_lists.items():
            actual = certificate[key]
            if (
                not isinstance(actual, list)
                or any(type(v) is not int for v in actual)
                or actual != expected
            ):
                return False

        if type(certificate["coefficient"]) is not int:
            return False
        if type(certificate["parity_moment"]) is not int:
            return False
        if certificate.get("method") != "INTEGER_MOBIUS_AND_DIRECT_PARITY":
            return False

        mask = sum(
            1 << (d - 1 - j)
            for j in support
        )

        # Independent subset-sum coefficient calculation.
        coefficient = sum(
            (-1) ** (len(support) - x.bit_count()) * values[x]
            for x in range(n)
            if x & mask == x
        )

        # Independent direct evaluation of the proposed feature.
        moment = sum(
            (-1) ** x.bit_count() * values[x]
            for x in range(n)
            if all(
                (x >> (d - 1 - j)) & 1
                for j in multiplier
            )
        )

        return (
            coefficient == certificate["coefficient"]
            and moment == certificate["parity_moment"]
            and moment != 0
            and moment == (-1) ** d * coefficient
            and 1 + len(multiplier) <= d - 1
        )

    except (ValueError, TypeError, KeyError):
        return False


def recognize_extremal(T, h):
    if not isinstance(T, (list, tuple)):
        raise ValueError("T must be an array")
    if not isinstance(h, (list, tuple)):
        raise ValueError("h must be an array")

    n = len(T)

    if n < 2 or n & (n - 1) or len(h) != n:
        raise ValueError(
            "Equal lengths required; state count must be a power of two >=2"
        )

    if any(type(v) is not int or not 0 <= v < n for v in T):
        raise ValueError("T must contain integer state indices")

    if any(type(v) is not int or v not in (0, 1) for v in h):
        raise ValueError("h must contain integer binary labels")

    d = n.bit_length() - 1
    prefixes = []
    ends = []

    for initial in range(n):
        x = initial
        u = []

        for _ in range(d):
            u.append(h[x])
            x = T[x]

        prefixes.append(tuple(u))
        ends.append(x)

    result = {
        "classification": "PREFIX_COLLISION",
        "n": n,
        "d": d,
        "prefixes": [list(u) for u in prefixes],
        "rank_profile_theorem_derived": None,
    }

    first = {}

    for x, u in enumerate(prefixes):
        if u in first:
            result["collision"] = {
                "states": [first[u], x],
                "prefix": list(u),
            }
            result["scope"] = (
                "Outside the separating extremal class. "
                "This prefix collision alone does not decide "
                "whether longer itineraries separate states."
            )
            return result

        first[u] = x

    terminal = [None] * n

    for x, u in enumerate(prefixes):
        index = 0
        for bit in u:
            index = 2 * index + bit

        terminal[index] = h[ends[x]]

    result.update({
        "classification": "NONLITERAL_TERMINAL",
        "terminal_truth_table": terminal,
        "prefix_bijection_computed": True,
    })

    candidates = [
        (
            {"kind": "constant", "value": bit},
            [bit] * n,
        )
        for bit in (0, 1)
    ]

    for coordinate in range(d):
        for complement in (0, 1):
            table = [
                ((index >> (d - 1 - coordinate)) & 1)
                ^ complement
                for index in range(n)
            ]

            candidates.append((
                {
                    "kind": "literal",
                    "coordinate": coordinate,
                    "complement": bool(complement),
                },
                table,
            ))

    for rule, table in candidates:
        if terminal != table:
            continue

        weights = [
            (-1) ** sum(u)
            for u in prefixes
        ]

        detecting_moment = sum(
            weight * prod(u)
            for weight, u in zip(weights, prefixes)
        )

        result.update({
            "classification": "EXTREMAL_REGISTER",
            "terminal_rule": rule,
            "rank_profile_theorem_derived": [
                sum(comb(d, r) for r in range(k + 1))
                for k in range(d + 1)
            ],
            "certificate": {
                "state_weights": weights,
                "detecting_temporal_coordinates": list(range(d)),
                "weighted_sum": detecting_moment,
            },
            "scope": (
                "Positive register normal form and parity certificate. "
                "Completeness of the classification uses the "
                "spectral-to-register reduction."
            ),
        })

        return result

    result["repair_certificate"] = terminal_repair_certificate(terminal)
    if result["repair_certificate"] is None:
        raise AssertionError("Nonliteral terminal lacks a repair certificate")

    result["scope"] = (
        "The prefix separates all states, but the terminal is not "
        "constant or a signed coordinate literal. Full degree-(d-1) "
        "rank is theorem-derived; this recognizer does not compute ranks."
    )

    return result
