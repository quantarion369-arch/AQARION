"""Exact finite-map explanations; no census or import-time execution."""
from fractions import Fraction as Q
import importlib.util
from pathlib import Path

MAX_STATES = 16
ROOT = Path(__file__).resolve().parents[1]

def _load(relative):
    path = ROOT / relative
    spec = importlib.util.spec_from_file_location(
        "explanation_dependency_" + path.stem, path
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def _rref(rows):
    a = [[Q(x) for x in row] for row in rows]
    pivots = []
    if not a:
        return a, pivots
    for j in range(len(a[0])):
        r = len(pivots)
        pivot = next(
            (i for i in range(r, len(a)) if a[i][j]), None
        )
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        value = a[r][j]
        a[r] = [x / value for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][j]:
                value = a[i][j]
                a[i] = [
                    x - value*y for x, y in zip(a[i], a[r])
                ]
        pivots.append(j)
        if len(pivots) == len(a):
            break
    return a, pivots

def _normalize(labels):
    ids = {}
    return tuple(ids.setdefault(x, len(ids)) for x in labels)

def _strings(rows):
    return [[str(x) for x in row] for row in rows]

def _coordinates(basis, vector):
    d = len(basis[0])
    reduced, pivots = _rref([
        row + [vector[i]] for i, row in enumerate(basis)
    ])
    if pivots != list(range(d)):
        raise ArithmeticError("Vector outside claimed independent basis")
    return [reduced[j][-1] for j in range(d)]

def explain(T, labels):
    T, original = tuple(T), tuple(labels)
    n = len(T)
    if not 1 <= n <= MAX_STATES or len(original) != n:
        raise ValueError("Require equal input lengths and 1..16 states")
    if any(type(x) is not int or not 0 <= x < n for x in T):
        raise ValueError("Transitions must be integer indices; bool is invalid")
    if any(type(x) is not int for x in original):
        raise ValueError("Partition labels must be integers; bool is invalid")
    labels = _normalize(original)
    k = max(labels) + 1

    baseline = _load("quotient-audit-001/quotient_audit.py")
    arithmetic = _load(
        "closure-certificate-004/closure_certificate.py"
    )
    ok, compatible, witness, quotient, defect = baseline.evaluate(
        T, labels
    )
    if not ok:
        raise ArithmeticError("Maintained quotient checks disagree")

    partitions = [labels]
    while True:
        current = partitions[-1]
        nxt = _normalize(tuple(
            (current[x], current[T[x]]) for x in range(n)
        ))
        if len(set(nxt)) == len(set(current)):
            break
        partitions.append(nxt)

    stable = partitions[-1]
    m = len(set(stable))
    representatives = [stable.index(b) for b in range(m)]

    columns, descriptions, dimensions = [], [], []
    positions = list(range(n))
    for time in range(n + 1):
        for block in range(k):
            columns.append([
                Q(labels[positions[x]] == block) for x in range(n)
            ])
            descriptions.append({
                "time": time, "normalized_block": block
            })
        rows = [list(row) for row in zip(*columns)]
        dimension = len(_rref(rows)[1])
        dimensions.append(dimension)
        if time > 0 and dimension == dimensions[-2]:
            break
        positions = [T[x] for x in positions]
    else:
        raise ArithmeticError("Linear closure failed to stabilize")

    selected = _rref(rows)[1]
    C = [[row[j] for j in selected] for row in rows]
    d = len(selected)
    A = [list(row) for row in zip(*[
        _coordinates(C, v) for v in columns[:k]
    ])]
    shifted = [
        [C[T[x]][j] for x in range(n)] for j in range(d)
    ]
    M = [list(row) for row in zip(*[
        _coordinates(C, v) for v in shifted
    ])]
    B = [row[:k] for row in rows]
    KC = [C[T[x]] for x in range(n)]
    minor_rows = _rref([
        list(row) for row in zip(*C)
    ])[1]
    minor = arithmetic.determinant([C[i] for i in minor_rows])
    generated = all(
        [C[x][j] for x in range(n)] == columns[index]
        for j, index in enumerate(selected)
    )
    checks = {
        "initial_observables_contained":
            arithmetic.multiply(C, A) == B,
        "koopman_invariant":
            arithmetic.multiply(C, M) == KC,
        "basis_independent": minor != 0,
        "basis_from_named_time_shifts": generated,
    }
    if not all(checks.values()):
        raise ArithmeticError("Linear-closure certificate failed")

    class_rows = [C[x] for x in representatives]
    transpose = [list(row) for row in zip(*class_rows)]
    reduced, pivots = _rref(transpose)
    free = [j for j in range(m) if j not in pivots]
    annihilators = []
    for f in free:
        z = [Q(0)] * m
        z[f] = Q(1)
        for i, pivot in enumerate(pivots):
            z[pivot] = -reduced[i][f]
        if any(
            sum(z[x]*class_rows[x][j] for x in range(m))
            for j in range(d)
        ):
            raise ArithmeticError("Invalid stable-class annihilator")
        annihilators.append(z)

    repair = {"status": "not_needed"}
    if free:
        repair = None
        for i in range(d):
            for j in range(i, d):
                values = [row[i]*row[j] for row in class_rows]
                pairings = [
                    sum(a*b for a, b in zip(z, values))
                    for z in annihilators
                ]
                if not any(pairings):
                    continue
                after = len(_rref([
                    row + [v]
                    for row, v in zip(class_rows, values)
                ])[1])
                if after != d + 1:
                    raise ArithmeticError("Product did not increase rank")
                repair = {
                    "status": "rank_increasing",
                    "left": descriptions[selected[i]],
                    "right": descriptions[selected[j]],
                    "values_on_stable_classes":
                        [str(v) for v in values],
                    "annihilator_pairings":
                        [str(v) for v in pairings],
                    "rank_before": d,
                    "rank_after": after,
                    "complete_repair": after == m,
                }
                break
            if repair is not None:
                break
        if repair is None:
            raise ArithmeticError(
                "Positive deficiency without a product witness"
            )

    r = len(_rref(defect)[1])
    delta = len(set(
        partitions[min(1, len(partitions)-1)]
    )) - k
    R, L = delta-r, m-k-delta
    tail, deficiency = d-dimensions[1], m-d
    if not (
        r == dimensions[1]-k
        and 0 <= r <= delta <= m-k
        and R+L == deficiency+tail
        and len(annihilators) == deficiency
    ):
        raise ArithmeticError("Bridge identities failed")

    last = max(len(partitions), len(dimensions))-1
    profile = [{
        "time": t,
        "partition_blocks": len(set(
            partitions[min(t, len(partitions)-1)]
        )),
        "linear_dimension":
            dimensions[min(t, len(dimensions)-1)],
    } for t in range(last+1)]
    if any(
        row["linear_dimension"] > row["partition_blocks"]
        for row in profile
    ):
        raise ArithmeticError(
            "Linear dimensions exceed itinerary dimensions"
        )

    return {
        "T": list(T),
        "original_labels": list(original),
        "normalized_labels": list(labels),
        "k": k,
        "compatible": compatible,
        "first_ordered_witness": witness,
        "initial_quotient": quotient,
        "exact_defect_matrix": _strings(defect),
        "defect_rank": r,
        "refinement_trace": [list(p) for p in partitions],
        "linear_dimension_trace": dimensions,
        "round_profile": profile,
        "partition_stabilization_checked_at": len(partitions),
        "linear_stabilization_checked_at": len(dimensions)-1,
        "stable_class_labels": list(stable),
        "stable_class_count": m,
        "eventual_linear_dimension": d,
        "first_refinement_increase": delta,
        "stable_refinement_increase": m-k,
        "constraint_redundancy": R,
        "delayed_refinement_increase": L,
        "later_linear_growth": tail,
        "eventual_linear_deficiency": deficiency,
        "annihilator_coordinates":
            "stable classes in normalized order",
        "annihilator_basis": _strings(annihilators),
        "first_product_repair": repair,
        "linear_closure_certificate": {
            "basis": _strings(C),
            "initial_coordinates": _strings(A),
            "evolution_coordinates": _strings(M),
            "basis_generation":
                [descriptions[j] for j in selected],
            "minor_rows": minor_rows,
            "minor_determinant": str(minor),
            "checks": checks,
        },
        "scope": (
            "exact bounded-input explanation; "
            "no minimal-product or novelty claim"
        ),
    }
