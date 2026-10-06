from itertools import product, permutations
from collections import Counter, defaultdict
from math import factorial, gcd


# ------------------------------------------------------------
# Integer partitions of n, represented as nonincreasing tuples
# ------------------------------------------------------------

def integer_partitions(n, maxpart=None):
    if n == 0:
        yield ()
        return

    if maxpart is None or maxpart > n:
        maxpart = n

    for first in range(maxpart, 0, -1):
        rest_n = n - first
        if rest_n == 0:
            yield (first,)
        else:
            for rest in integer_partitions(rest_n, min(first, rest_n)):
                yield (first,) + rest


def ppart(n):
    return sum(1 for _ in integer_partitions(n))


# ------------------------------------------------------------
# Restricted-growth-string enumeration of set partitions
# ------------------------------------------------------------

def rgs_partitions(n):
    if n == 0:
        return [()]

    out = []
    a = [0] * n

    def rec(pos, current_max):
        if pos == n:
            out.append(tuple(a))
            return

        for x in range(current_max + 2):
            a[pos] = x
            rec(pos + 1, max(current_max, x))

    a[0] = 0
    rec(1, 0)
    return out


# ------------------------------------------------------------
# Permutation cycle data
# ------------------------------------------------------------

def cycle_lengths(p):
    n = len(p)
    seen = [False] * n
    lengths = []

    for i in range(n):
        if seen[i]:
            continue

        x = i
        length = 0

        while not seen[x]:
            seen[x] = True
            length += 1
            x = p[x]

        lengths.append(length)

    return tuple(sorted(lengths))


# ------------------------------------------------------------
# PB-CORE-005 cycle formula
# ------------------------------------------------------------

def phase_weight(lengths_for_block):
    k = len(lengths_for_block)

    g = 0
    for m in lengths_for_block:
        g = gcd(g, m)

    return sum(
        d ** (k - 1)
        for d in range(1, g + 1)
        if g % d == 0
    )


def formula_count(lengths):
    """
    Number of invariant equivalence relations for a permutation
    with cycle lengths 'lengths'.
    """

    r = len(lengths)
    total = 0

    for blocks in rgs_partitions(r):
        groups = defaultdict(list)

        for i, block_id in enumerate(blocks):
            groups[block_id].append(i)

        contribution = 1

        for indices in groups.values():
            block_lengths = [lengths[i] for i in indices]
            contribution *= phase_weight(block_lengths)

        total += contribution

    return total


# ------------------------------------------------------------
# Brute-force invariant equivalence count for a permutation
# ------------------------------------------------------------

def same_partition(a, b):
    n = len(a)

    for i in range(n):
        for j in range(n):
            if (a[i] == a[j]) != (b[i] == b[j]):
                return False

    return True


def brute_invariant_count(p):
    n = len(p)
    total = 0

    for E in rgs_partitions(n):
        ok = True

        for x in range(n):
            for y in range(n):
                if E[x] == E[y] and E[p[x]] != E[p[y]]:
                    ok = False
                    break

            if not ok:
                break

        if ok:
            total += 1

    return total


# ------------------------------------------------------------
# Periodic core of a finite map
# ------------------------------------------------------------

def periodic_core(p):
    n = len(p)

    indegree = [0] * n

    for y in p:
        indegree[y] += 1

    stack = [
        x for x in range(n)
        if indegree[x] == 0
    ]

    removed = [False] * n

    while stack:
        x = stack.pop()
        removed[x] = True

        y = p[x]
        indegree[y] -= 1

        if indegree[y] == 0:
            stack.append(y)

    return [
        x for x in range(n)
        if not removed[x]
    ]


# ------------------------------------------------------------
# Invariant partitions of the periodic core
# ------------------------------------------------------------

def invariant_core_partitions(p, core):
    index = {
        x: i
        for i, x in enumerate(core)
    }

    q = [
        index[p[x]]
        for x in core
    ]

    for E in rgs_partitions(len(core)):
        if all(
            E[i] != E[j]
            for i in range(len(core))
            for j in range(len(core))
            if E[i] == E[j] and E[q[i]] != E[q[j]]
        ):
            yield E


# ------------------------------------------------------------
# Extend a core equivalence to the whole finite map
# ------------------------------------------------------------

def stable_partitions(p):
    n = len(p)
    core = periodic_core(p)

    # n iterations are certainly enough to reach the periodic core.
    image = list(range(n))

    for _ in range(n):
        image = [p[x] for x in image]

    core_index = {
        x: i
        for i, x in enumerate(core)
    }

    result = []

    for E_core in invariant_core_partitions(p, core):
        labels = [
            E_core[core_index[image[x]]]
            for x in range(n)
        ]

        # Normalize labels into restricted-growth form.
        relabel = {}
        next_label = 0
        normalized = []

        for label in labels:
            if label not in relabel:
                relabel[label] = next_label
                next_label += 1

            normalized.append(relabel[label])

        result.append(tuple(normalized))

    return result


# ------------------------------------------------------------
# Join of two equivalence relations
# ------------------------------------------------------------

def join_partitions(a, b):
    n = len(a)
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

    for relation in (a, b):
        classes = defaultdict(list)

        for i, label in enumerate(relation):
            classes[label].append(i)

        for cls in classes.values():
            for x in cls[1:]:
                union(cls[0], x)

    relabel = {}
    next_label = 0
    result = []

    for i in range(n):
        root = find(i)

        if root not in relabel:
            relabel[root] = next_label
            next_label += 1

        result.append(relabel[root])

    return tuple(result)


# ------------------------------------------------------------
# Full-map audit
# ------------------------------------------------------------

def audit_maps(n, check_join=False):
    map_count = 0
    stable_count = 0
    pair_count = 0
    join_failures = []

    for p in product(range(n), repeat=n):
        map_count += 1

        stable = stable_partitions(p)
        stable_count += len(stable)

        if check_join:
            pair_count += len(stable) * (len(stable) + 1) // 2

            stable_set = set(stable)

            for i, E in enumerate(stable):
                for F in stable[i:]:
                    J = join_partitions(E, F)

                    if J not in stable_set:
                        join_failures.append(
                            (p, E, F, J)
                        )
                        return (
                            map_count,
                            stable_count,
                            pair_count,
                            join_failures,
                        )

    return (
        map_count,
        stable_count,
        pair_count,
        join_failures,
    )


# ------------------------------------------------------------
# Exact labeled-map enumeration formula
# ------------------------------------------------------------

def exact_A(n):
    total = 0

    for k in range(1, n + 1):
        if k == n:
            forest_count = 1
        else:
            forest_count = k * n ** (n - k - 1)

        total += (
            factorial(n)
            * k
            * ppart(k)
            * n ** (n - k - 1)
            // factorial(n - k)
            if k < n
            else factorial(n) * ppart(n)
        )

    return total


# ------------------------------------------------------------
# Main audit
# ------------------------------------------------------------

if __name__ == "__main__":

    print("=== PB-CORE-005 permutation formula audit ===")

    for n in range(1, 7):
        mismatches = 0

        for p in permutations(range(n)):
            formula = formula_count(cycle_lengths(p))
            brute = brute_invariant_count(p)

            if formula != brute:
                mismatches += 1

        print(
            f"n={n}: permutation mismatches={mismatches}"
        )

    print()
    print("=== PB-CORE-004/005 full-map audit ===")

    expected = {
        1: 1,
        2: 6,
        3: 51,
        4: 592,
        5: 8565,
        6: 148896,
        7: 3018127,
    }

    for n in range(1, 7):
        result = audit_maps(
            n,
            check_join=(n == 6),
        )

        map_count, stable_count, pair_count, failures = result

        print(
            f"n={n}: maps={map_count}, "
            f"stable={stable_count}, "
            f"join_pairs={pair_count}, "
            f"join_failures={len(failures)}"
        )

    print()
    print("=== Exact enumeration formula ===")

    for n in range(1, 13):
        print(
            f"n={n}: A_n={exact_A(n)}"
  )
