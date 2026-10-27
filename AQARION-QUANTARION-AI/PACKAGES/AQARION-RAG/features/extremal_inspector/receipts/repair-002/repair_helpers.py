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
