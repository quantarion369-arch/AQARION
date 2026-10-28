from collections import Counter
from fractions import Fraction
from functools import reduce
from itertools import combinations, permutations, product
from math import factorial, gcd, lcm, prod
from pathlib import Path
import json
import sys
import time

OUT = Path(sys.argv[1])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def rref(matrix):
    A = [[Fraction(x) for x in row] for row in matrix]
    rank = 0
    pivots = []

    for column in range(len(A[0]) if A else 0):
        pivot = next(
            (i for i in range(rank, len(A)) if A[i][column]),
            None,
        )

        if pivot is None:
            continue

        A[rank], A[pivot] = A[pivot], A[rank]
        value = A[rank][column]
        A[rank] = [x / value for x in A[rank]]

        for i in range(len(A)):
            if i != rank and A[i][column]:
                coefficient = A[i][column]
                A[i] = [
                    x - coefficient*y
                    for x, y in zip(A[i], A[rank])
                ]

        pivots.append(column)
        rank += 1

        if rank == len(A):
            break

    return A, pivots


def affine_relation(Y, L):
    matrix = (
        [[1] * len(Y)]
        + [
            [(word >> i) & 1 for word in Y]
            for i in range(L)
        ]
    )

    reduced, pivots = rref(matrix)
    rank = len(pivots)
    free = [i for i in range(len(Y)) if i not in pivots]

    if len(free) != 1:
        return rank, None

    relation = [Fraction(0)] * len(Y)
    relation[free[0]] = 1

    for row, pivot in enumerate(pivots):
        relation[pivot] = -reduced[row][free[0]]

    return rank, relation


def primitive_relation(values):
    scale = lcm(*(x.denominator for x in values))
    result = [int(x * scale) for x in values]
    common = reduce(gcd, result, 0)
    result = [x // common for x in result]

    if next(x for x in result if x) < 0:
        result = [-x for x in result]

    return result


def overlap_data(Y, L):
    mask = (1 << (L - 1)) - 1
    suffix = Counter(word >> 1 for word in Y)
    prefix = Counter(word & mask for word in Y)
    contexts = sorted(set(suffix) | set(prefix))

    balanced = all(
        suffix[u] == prefix[u]
        for u in contexts
    )

    permutation_count = (
        prod(factorial(suffix[u]) for u in contexts)
        if balanced else 0
    )

    deterministic_count = prod(
        prefix[u] ** suffix[u]
        for u in suffix
    )

    options = {
        word: [
            target for target in Y
            if word >> 1 == target & mask
        ]
        for word in Y
    }

    return {
        "contexts": [
            {
                "word": u,
                "suffix_count": suffix[u],
                "prefix_count": prefix[u],
            }
            for u in contexts
        ],
        "permutation_count": permutation_count,
        "deterministic_count": deterministic_count,
        "edges": [
            [word, target]
            for word in Y
            for target in options[word]
        ],
    }, options


def verify_small_overlap_counts():
    checked = 0
    realizations_checked = 0

    for L in (1, 2, 3):
        for selected in range(1, 1 << (1 << L)):
            Y = [
                word for word in range(1 << L)
                if (selected >> word) & 1
            ]

            data, options = overlap_data(Y, L)

            direct_permutations = sum(
                all(
                    target in options[word]
                    for word, target in zip(Y, order)
                )
                for order in permutations(Y)
            )

            direct_functions = 0

            for images in product(*(options[word] for word in Y)):
                T = dict(zip(Y, images))

                for initial in Y:
                    state = initial
                    observed = 0

                    for t in range(L):
                        observed |= (state & 1) << t
                        state = T[state]

                    require(
                        observed == initial,
                        "Overlap realization produced wrong history",
                    )

                direct_functions += 1

            require(
                direct_permutations == data["permutation_count"],
                "Permutation-count formula failed",
            )
            require(
                direct_functions == data["deterministic_count"],
                "Deterministic-count formula failed",
            )

            checked += 1
            realizations_checked += direct_functions

    require(checked == 273, "Small support count mismatch")
    require(
        realizations_checked == 982,
        "Small realization total mismatch",
    )

    print("SMALL_OVERLAP_SUPPORTS=273_PASS", flush=True)
    print("DETERMINISTIC_REALIZATIONS_RESIMULATED=982", flush=True)

    return {
        "supports": checked,
        "realizations_resimulated": realizations_checked,
    }


def verify_five_point_classification():
    rank_histogram = Counter()
    circuits = []
    permutation_realizable = []
    deterministic_realizable = []

    for index, Y in enumerate(combinations(range(16), 5), 1):
        rank, relation = affine_relation(Y, 4)
        rank_histogram[rank] += 1

        if rank == 4 and relation is not None and all(relation):
            weights = primitive_relation(relation)

            for deleted in range(5):
                remaining = [
                    word for i, word in enumerate(Y)
                    if i != deleted
                ]
                deletion_rank, _ = affine_relation(remaining, 4)
                require(
                    deletion_rank == 4,
                    "Circuit deletion is dependent",
                )

            data, options = overlap_data(Y, 4)

            record = {
                "support": list(Y),
                "primitive_relation": weights,
                **data,
            }

            if data["deterministic_count"] == 1:
                transition = {
                    word: options[word][0]
                    for word in Y
                }

                for initial in Y:
                    state = initial
                    observed = 0

                    for t in range(4):
                        observed |= (state & 1) << t
                        state = transition[state]

                    require(
                        observed == initial,
                        "Unique realization history failure",
                    )

                record["unique_transition"] = [
                    [word, transition[word]]
                    for word in Y
                ]

            circuits.append(record)

            if data["permutation_count"]:
                permutation_realizable.append(list(Y))

            if data["deterministic_count"]:
                deterministic_realizable.append(list(Y))

        if index % 512 == 0:
            print(f"SUPPORT_PROGRESS={index}/4368", flush=True)

    expected = [
        [0, 2, 4, 9, 15],
        [0, 6, 11, 13, 15],
    ]

    require(sum(rank_histogram.values()) == 4368, "Support total mismatch")
    require(
        dict(rank_histogram) == {4: 1360, 5: 3008},
        "Rank histogram mismatch",
    )
    require(len(circuits) == 160, "Circuit count mismatch")
    require(
        permutation_realizable == expected,
        "Permutation-realizable support mismatch",
    )
    require(
        deterministic_realizable == expected,
        "Deterministic-realizable support mismatch",
    )

    for record in circuits:
        if record["deterministic_count"]:
            require(
                record["deterministic_count"]
                == record["permutation_count"] == 1,
                "Expected unique realization",
            )

    cube3 = []

    for Y in combinations(range(8), 5):
        rank, relation = affine_relation(Y, 3)
        if rank == 4 and relation is not None and all(relation):
            cube3.append(Y)

    standard = {0, 1, 2, 4, 7}
    translated = {
        tuple(sorted(word ^ flip for word in standard))
        for flip in range(8)
    }

    require(
        set(cube3) == translated and len(cube3) == 8,
        "Three-cube circuit classification mismatch",
    )

    bad = [0, 1, 4, 10, 15]
    rank, relation = affine_relation(bad, 4)
    require(
        rank == 4 and relation is not None and all(relation),
        "Static-symmetry negative control is not a circuit",
    )

    bad_data, _ = overlap_data(bad, 4)
    require(
        bad_data["deterministic_count"] == 0,
        "Static-symmetry negative control unexpectedly realizable",
    )

    print("FIVE_POINT_SUPPORTS=4368", flush=True)
    print("AFFINE_CIRCUITS=160", flush=True)
    print("PERMUTATION_REALIZABLE_CIRCUITS=2", flush=True)
    print("DETERMINISTIC_REALIZABLE_CIRCUITS=2", flush=True)
    print("CIRCUIT_DELETION_CHECKS=800_PASS", flush=True)
    print("THREE_CUBE_CIRCUITS=8_PASS", flush=True)
    print("STATIC_SYMMETRY_NEGATIVE_CONTROL=PASS", flush=True)

    return {
        "supports_checked": 4368,
        "rank_histogram": {
            str(rank): count
            for rank, count in sorted(rank_histogram.items())
        },
        "circuit_count": len(circuits),
        "permutation_realizable": permutation_realizable,
        "deterministic_realizable": deterministic_realizable,
        "three_cube_circuit_count": len(cube3),
        "static_symmetry_negative_control": bad_data,
        "circuits": circuits,
    }


def rank_profile(rows):
    L = len(rows[0])
    result = []

    for degree in range(3):
        subsets = [
            S
            for k in range(degree + 1)
            for S in combinations(range(L), k)
        ]
        matrix = [
            [
                prod(row[t] for t in S)
                for S in subsets
            ]
            for row in rows
        ]
        result.append(len(rref(matrix)[1]))

    return result


def histories(Y, T, L):
    rows = []

    for initial in Y:
        state = initial
        row = []

        for _ in range(L):
            row.append(state & 1)
            state = T[state]

        rows.append(row)

    return rows


def verify_persistence_example():
    Y = [0, 1, 2, 4, 7]
    weights = [2, -1, -1, -1, 1]

    original = {0: 0, 7: 7, 1: 4, 4: 2, 2: 1}
    alternative = {0: 4, 7: 7, 1: 0, 4: 2, 2: 1}

    results = []

    for name, T, expected_profile, expected_moment in (
        ("persistent", original, [1, 4, 5], 0),
        ("obstruction_breaks", alternative, [1, 5, 5], 3),
    ):
        rows = histories(Y, T, 4)
        prefix_profile = rank_profile([row[:3] for row in rows])
        extended_profile = rank_profile(rows)
        moment = sum(
            weight * row[3]
            for weight, row in zip(weights, rows)
        )

        require(prefix_profile == [1, 4, 5], "Prefix profile mismatch")
        require(extended_profile == expected_profile, "Extension mismatch")
        require(moment == expected_moment, "Obstruction moment mismatch")

        results.append({
            "model": name,
            "profile_length_3": prefix_profile,
            "profile_length_4": extended_profile,
            "new_observation_moment": moment,
            "support_length_4": sorted(
                sum(bit << t for t, bit in enumerate(row))
                for row in rows
            ),
        })

    print("PERSISTENT_VS_TRANSIENT_OBSTRUCTION=PASS", flush=True)
    return results


PROOF = """# Temporal affine circuits: scope and proof

## Conventions

Coefficients are rational.
Time coordinate zero is the least significant bit.
Words are distinct and states are labelled by their words.
Transitions may have loops.
A circuit means minimal affine dependence: rows (1,y) are dependent,
and every proper subset is independent.

This note does not classify all temporal circuits or assert novelty.

## General overlap counts

For each length-(L-1) context u, let a_u count words ending in u
and b_u count words beginning in u.

All words ending in u can transition to all words beginning in u.
The bipartite matching graph splits into independent complete blocks.

Permutation realizations exist iff a_u=b_u for every u.
Their number is product(a_u!).
Arbitrary deterministic realizations number product(b_u^a_u : a_u>0).

These counts do not require a permanent algorithm.
They count finite-history realizations, not persistent dependencies.

## The five-point, four-bit classification

Claim:
Among five-point affine circuits in {0,1}^4, exactly the supports
{0,2,4,9,15} and {0,6,11,13,15} are deterministically realizable.
Each realization is unique and is a permutation with two fixed points
and one three-cycle.

Proof:
Realize a support as five states with binary observation h.
The affine circuit has rank four, so dim W_4=4, where
W_L=span_Q(1,h,...,h composed with T^(L-1)).

A pause W_(k+1)=W_k makes W_k invariant under composition with T.
Consequently the span cannot pause and later grow.
It follows that W_3=W_4=W_infinity has dimension four.

The first-three-observation map is injective: agreement there forces
agreement on all of W_infinity and hence on the given four-bit histories.
Its image is a five-point affine circuit C in the three-cube.

Such a C contains an antipodal pair, by pigeonhole among the four pairs.
It cannot contain two antipodal pairs, because their four points are
already dependent.

Flip coordinates to send the sole pair to 000 and 111.
The other three points choose one from each pair {e_i,1-e_i}.
A mixed choice contains a dependent parallelogram:
two one-hot choices and the remaining one-cold choice give one;
the complementary case gives another.
Only all three one-hot or all three one-cold choices remain.

Thus C is a coordinate-flip image of {0,1,2,4,7}.
Its primitive relation has coefficient pattern 2,1,-1,-1,-1.

Let w be that full-support relation. Invariance of W_infinity implies
T_*w=lambda*w, where (T_*w)(z)=sum(w(x):T(x)=z).

If T is not surjective, a missing image coordinate forces lambda=0.
Every nonempty fiber must then have weight sum zero and contain at
least two states. A fiber cannot contain three states: two would have
the same binary observation and the same successor, contradicting
observability. All fibers would therefore have size two, impossible
for five states. Hence T is a permutation.

A permutation preserves the multiset of relation coefficients.
Thus lambda is 1 or -1. The unequal positive/negative support sizes
exclude -1. The uniquely weighted coefficient-two and coefficient-one
states are fixed.

A fixed state's three-prefix is constant. The distinguished antipodal
pair must therefore be 000 and 111. The prefix circuit is consequently
{0,1,2,4,7} or its global complement.

The remaining overlap constraints force a three-cycle.
Appending its next output gives precisely the two four-bit supports
listed in the claim. Direct edge inspection proves their uniqueness.
End proof.

The finite enumeration in this package independently checks all
binomial(16,5)=4368 supports without symmetry pruning.

## Persistence is not finite realizability

The three-bit circuit {0,1,2,4,7} has two permutation realizations.
One extends to {0,2,4,9,15} with linear rank four.
The other extends to {1,2,4,8,15} with linear rank five.

The same separating finite support can therefore have different
eventual interpolation degrees under different transitions.

## Coefficient interpretation

For Y_m={0,1^m,e_0,...,e_(m-1)}, the primitive obstruction is
(m-1,1,-1,...,-1).

Its coefficient growth is not unavoidable decoder growth.
The zero-state indicator can be written
1-sum(g_i)+sum(g_0*g_i : i=1,...,m-1),
using only coefficients 0,1,-1.

## Boundaries

No general proof is machine-formalized here.
Finite exact checks are not originality clearance.
Static cube symmetries need not preserve temporal overlap.
No existing manuscript, application, or repository source is modified.
"""


def main():
    start = time.monotonic()

    small = verify_small_overlap_counts()
    classification = verify_five_point_classification()
    persistence = verify_persistence_example()

    report = {
        "status": "PASS",
        "scope": "Five-point affine circuits in the ordered four-bit cube",
        "coefficient_field": "Q",
        "time_encoding": "least significant bit first",
        "small_overlap_checks": small,
        "classification": classification,
        "persistence_example": persistence,
        "elapsed_seconds": time.monotonic() - start,
        "novelty": "not established",
        "general_proof_machine_checked": False,
        "old_state_map_censuses_rerun": False,
        "old_primitive_cycle_censuses_rerun": False,
        "application_sources_changed": False,
        "manuscript_changed": False,
        "git_operations": "none",
    }

    (OUT / "PROOF_AND_SCOPE.md").write_text(
        PROOF, encoding="utf-8"
    )

    result_path = OUT / "results.json"
    result_path.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    require(
        json.loads(result_path.read_text(encoding="utf-8")) == report,
        "JSON read-back mismatch",
    )

    print("SAVED_JSON_READBACK=PASS")
    print("GENERAL_PROOF_MACHINE_CHECKED=NO")
    print("NOVELTY=NOT_ESTABLISHED")
    print("OLD_STATE_MAP_CENSUSES_RERUN=NO")
    print("OLD_PRIMITIVE_CYCLE_CENSUSES_RERUN=NO")
    print("APPLICATION_SOURCES_CHANGED=NO")
    print("MANUSCRIPT_CHANGED=NO")
    print("GIT_OPERATIONS=NONE")
    print(
        "ELAPSED_SECONDS="
        + format(time.monotonic() - start, ".3f")
    )
    print("OVERALL_STATUS=PASS", flush=True)


if __name__ == "__main__":
    main()
