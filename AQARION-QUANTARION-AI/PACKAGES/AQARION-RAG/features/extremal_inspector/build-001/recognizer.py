from math import comb, prod


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

    result["scope"] = (
        "The prefix separates all states, but the terminal is not "
        "constant or a signed coordinate literal. Full degree-(d-1) "
        "rank is theorem-derived; this recognizer does not compute ranks."
    )

    return result
