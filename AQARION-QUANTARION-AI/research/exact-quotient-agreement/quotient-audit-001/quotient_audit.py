#!/usr/bin/env python3
"""Bounded exact quotient agreement test. Python standard library only."""
import hashlib
import itertools
import json
import sys
from fractions import Fraction as Q


def partitions(n):
    """Generate each partition once as restricted-growth block labels."""
    def extend(labels):
        if len(labels) == n:
            yield tuple(labels)
            return
        for label in range(max(labels) + 2):
            yield from extend(labels + [label])
    yield from extend([0])


def pairwise_test(T, labels):
    for x in range(len(T)):
        for y in range(x + 1, len(T)):
            if labels[x] == labels[y] and labels[T[x]] != labels[T[y]]:
                return False, {
                    "x": x, "y": y, "Tx": T[x], "Ty": T[y],
                    "input_block": labels[x],
                    "Tx_block": labels[T[x]], "Ty_block": labels[T[y]],
                }
    return True, None


def quotient_test(T, labels):
    quotient = []
    for block in range(max(labels) + 1):
        targets = {labels[T[x]] for x in range(len(T))
                   if labels[x] == block}
        if len(targets) != 1:
            return False, None
        quotient.append(next(iter(targets)))
    return True, quotient


def multiply(A, B):
    return [[sum((A[i][k] * B[k][j] for k in range(len(B))), Q(0))
             for j in range(len(B[0]))] for i in range(len(A))]


def defect_test(T, labels):
    n = len(T)
    sizes = [labels.count(block) for block in range(max(labels) + 1)]
    P = [[Q(1, sizes[labels[i]]) if labels[i] == labels[j] else Q(0)
          for j in range(n)] for i in range(n)]
    # Column observable vectors: (K f)[i] = f[T[i]].
    K = [[Q(int(j == T[i])) for j in range(n)] for i in range(n)]
    KP = multiply(K, P)
    PKP = multiply(P, KP)
    D = [[KP[i][j] - PKP[i][j] for j in range(n)] for i in range(n)]
    return all(value == 0 for row in D for value in row), D


def evaluate(T, labels):
    a, witness = pairwise_test(T, labels)
    b, quotient = quotient_test(T, labels)
    c, D = defect_test(T, labels)
    witness_valid = witness is None
    if witness is not None:
        x, y = witness["x"], witness["y"]
        witness_valid = (labels[x] == labels[y]
                         and labels[T[x]] != labels[T[y]])
    quotient_valid = quotient is None
    if quotient is not None:
        quotient_valid = all(quotient[labels[x]] == labels[T[x]]
                             for x in range(len(T)))
    consistent = (a == b == c and witness_valid and quotient_valid
                  and ((witness is None) == a)
                  and ((quotient is not None) == b))
    return consistent, a, witness, quotient, D


def case_record(T, labels, witness, quotient, D):
    return {"T": list(T), "labels": list(labels),
            "witness": witness, "quotient": quotient,
            "D": [[str(value) for value in row] for row in D]}


def run():
    by_size = []
    disagreements = []
    first_compatible = None
    first_incompatible = None
    total = compatible = incompatible = 0
    for n in range(1, 5):
        parts = list(partitions(n))
        row = {"states": n, "maps": n ** n, "partitions": len(parts),
               "cases": 0, "compatible": 0, "incompatible": 0}
        for T in itertools.product(range(n), repeat=n):
            for labels in parts:
                ok, accepted, witness, quotient, D = evaluate(T, labels)
                total += 1
                row["cases"] += 1
                if accepted:
                    compatible += 1
                    row["compatible"] += 1
                    if first_compatible is None:
                        first_compatible = case_record(T, labels, witness, quotient, D)
                else:
                    incompatible += 1
                    row["incompatible"] += 1
                    if first_incompatible is None:
                        first_incompatible = case_record(T, labels, witness, quotient, D)
                if not ok:
                    disagreements.append(case_record(T, labels, witness, quotient, D))
        by_size.append(row)

    # Explicit fixtures: one proper quotient and one incompatible partition.
    fixtures = []
    for name, T, labels, expected in (
        ("proper_quotient", (1, 2, 2), (0, 0, 0), True),
        ("incompatible_partition", (1, 2, 2), (0, 0, 1), False),
    ):
        ok, accepted, witness, quotient, D = evaluate(T, labels)
        fixtures.append({"name": name, "passed": ok and accepted == expected,
                         "expected_compatible": expected,
                         **case_record(T, labels, witness, quotient, D)})

    expected_counts = [1, 8, 135, 3840]
    counts_ok = [row["cases"] for row in by_size] == expected_counts
    passed = counts_ok and not disagreements and all(x["passed"] for x in fixtures)
    with open(__file__, "rb") as handle:
        source_hash = hashlib.sha256(handle.read()).hexdigest()
    return {"experiment": "exact quotient agreement 001",
            "status": "PASS" if passed else "FAIL",
            "arithmetic": "exact rational; no floating-point tolerance",
            "operator_convention": "column f; K[i,j]=1 iff j=T[i]; D=KP-PKP",
            "domain": "all maps and set partitions on labeled states for n=1..4",
            "cases": total, "compatible": compatible, "incompatible": incompatible,
            "disagreement_count": len(disagreements),
            "disagreement_examples": disagreements[:10],
            "expected_case_counts_pass": counts_ok,
            "by_size": by_size, "fixtures": fixtures,
            "first_compatible": first_compatible,
            "first_incompatible": first_incompatible,
            "source_sha256": source_hash,
            "python_version": sys.version,
            "scope": "bounded implementation cross-check; not a universal or Lean proof"}


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["status"] == "PASS" else 1)
