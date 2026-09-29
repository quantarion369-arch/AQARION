from itertools import product


def partitions(n):
    """All set partitions of range(n), encoded as restricted-growth strings."""
    out = []

    def rec(a, maximum):
        if len(a) == n:
            out.append(tuple(a))
            return

        for value in range(maximum + 2):
            rec(a + [value], max(maximum, value))

    if n == 0:
        return [()]

    rec([0], 0)
    return out


def pullback_stable(T, E):
    n = len(T)

    for x in range(n):
        for y in range(n):
            if E[T[x]] == E[T[y]] and E[x] != E[y]:
                return False

    return True


def join(E, F):
    """Join of two equivalence relations via connected components."""
    n = len(E)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        x = find(x)
        y = find(y)

        if x != y:
            parent[y] = x

    for relation in (E, F):
        classes = {}

        for x, c in enumerate(relation):
            classes.setdefault(c, []).append(x)

        for members in classes.values():
            root = members[0]

            for x in members[1:]:
                union(root, x)

    return tuple(find(x) for x in range(n))


def normalized_classes(E):
    labels = {}
    result = []

    for c in E:
        if c not in labels:
            labels[c] = len(labels)
        result.append(labels[c])

    return result


def incidence_data(T, E, F):
    """
    Return the incidence relation and induced class maps.

    The caller has already established pullback stability.
    """
    E = normalized_classes(E)
    F = normalized_classes(F)
    TE = normalized_classes(tuple(E[T[x]] for x in range(len(T))))
    TF = normalized_classes(tuple(F[T[x]] for x in range(len(T))))

    e_classes = max(E) + 1
    f_classes = max(F) + 1

    sigma_E = [None] * e_classes
    sigma_F = [None] * f_classes

    incidence = set()

    for x in range(len(T)):
        a = E[x]
        b = F[x]

        incidence.add((a, b))

        if sigma_E[a] is None:
            sigma_E[a] = TE[x]
        elif sigma_E[a] != TE[x]:
            raise AssertionError("E-class map is not well-defined")

        if sigma_F[b] is None:
            sigma_F[b] = TF[x]
        elif sigma_F[b] != TF[x]:
            raise AssertionError("F-class map is not well-defined")

    return incidence, sigma_E, sigma_F


def check_incidence_invariance(T, E, F):
    incidence, sigma_E, sigma_F = incidence_data(T, E, F)

    if len(set(sigma_E)) != len(sigma_E):
        raise AssertionError("E class action is not injective")

    if len(set(sigma_F)) != len(sigma_F):
        raise AssertionError("F class action is not injective")

    image = {
        (sigma_E[a], sigma_F[b])
        for (a, b) in incidence
    }

    return image == incidence


def audit(n):
    relations = partitions(n)

    ordered_stable_pairs = 0
    join_failures = 0
    incidence_failures = 0

    for T in product(range(n), repeat=n):
        stable = [
            E for E in relations
            if pullback_stable(T, E)
        ]

        ordered_stable_pairs += len(stable) ** 2

        for E in stable:
            for F in stable:
                G = join(E, F)

                if not pullback_stable(T, G):
                    join_failures += 1

                if not check_incidence_invariance(T, E, F):
                    incidence_failures += 1

    return (
        ordered_stable_pairs,
        join_failures,
        incidence_failures,
    )


EXPECTED = {
    1: (1, 0, 0),
    2: (10, 0, 0),
    3: (117, 0, 0),
    4: (1960, 0, 0),
    5: (40385, 0, 0),
    6: (1016496, 0, 0),
}


def main():
    for n in range(1, 7):
        result = audit(n)
        print(
            f"n={n} "
            f"ordered_stable_pairs={result[0]} "
            f"join_failures={result[1]} "
            f"incidence_failures={result[2]}"
        )

        if result != EXPECTED[n]:
            raise SystemExit(
                f"FAIL: expected {EXPECTED[n]}, got {result}"
            )

    print("RESULT=PASS")


if __name__ == "__main__":
    main()
