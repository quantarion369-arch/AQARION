#!/usr/bin/env python3
"""Exact quotient semantic checks. Standard library only."""
import hashlib
import importlib.util
import itertools
import json
import sys
from fractions import Fraction as Q
from pathlib import Path


def product(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def canonical(labels):
    names = {}
    return tuple(names.setdefault(x, len(names)) for x in labels)


def audit(base):
    failures = []
    failed_checks = 0
    counts = {"projection_checks": 0, "entry_formula_cases": 0,
              "relabeling_cases": 0, "constant_checks": 0,
              "multistep_cases": 0}

    def check(condition, name, T=None, labels=None):
        nonlocal failed_checks
        if not condition:
            failed_checks += 1
            if len(failures) < 20:
                failures.append({"check": name, "T": T, "labels": labels})

    for n in range(1, 4):
        for labels in base.partitions(n):
            sizes = {b: labels.count(b) for b in set(labels)}
            P = [[Q(int(labels[i] == labels[j]), sizes[labels[i]])
                  for j in range(n)] for i in range(n)]
            check(product(P, P) == P, "P squared equals P", labels=labels)
            check(P == [list(row) for row in zip(*P)], "P symmetric", labels=labels)
            check(all(sum(row) == 1 for row in P), "P preserves constants", labels=labels)
            counts["projection_checks"] += 3

            for T in itertools.product(range(n), repeat=n):
                ok, accepted, witness, quotient, D = base.evaluate(T, labels)
                check(ok, "baseline internal agreement", T, labels)

                # Independent entrywise oracle: no matrix multiplication.
                N = {}
                for x, target in enumerate(T):
                    key = (labels[x], labels[target])
                    N[key] = N.get(key, 0) + 1
                expected_D = []
                for i in range(n):
                    a = labels[i]
                    row = []
                    for j in range(n):
                        b = labels[j]
                        value = (Q(int(labels[T[i]] == b))
                                 - Q(N.get((a, b), 0), sizes[a])) / sizes[b]
                        row.append(value)
                    expected_D.append(row)
                check(D == expected_D, "entrywise defect formula", T, labels)
                counts["entry_formula_cases"] += 1

                check(all(sum(row) == 0 for row in D), "D annihilates constants", T, labels)
                counts["constant_checks"] += 1

                # State permutation h(x)=n-1-x; canonicalize block names.
                h = tuple(reversed(range(n)))
                new_T = tuple(h[T[h[z]]] for z in range(n))
                new_labels = canonical(tuple(labels[h[z]] for z in range(n)))
                new_ok, new_accept, _, _, new_D = base.evaluate(new_T, new_labels)
                check(new_ok and new_accept == accepted,
                      "compatibility invariant under relabeling", T, labels)
                check(new_D == [[D[h[i]][h[j]] for j in range(n)] for i in range(n)],
                      "defect transforms under relabeling", T, labels)
                counts["relabeling_cases"] += 1

                if accepted:
                    good = True
                    for x in range(n):
                        state, block = x, labels[x]
                        for step in range(7):
                            if labels[state] != block:
                                good = False
                            state = T[state]
                            block = quotient[block]
                    check(good, "quotient intertwines iterates 0 through 6", T, labels)
                    counts["multistep_cases"] += 1

    expected_counts = {"projection_checks": 24, "entry_formula_cases": 144,
                       "relabeling_cases": 144, "constant_checks": 144,
                       "multistep_cases": 108}
    check(counts == expected_counts, "expected coverage counts")
    fixture_T, fixture_labels = (1, 2, 2), (0, 0, 1)
    _, accepted, _, _, D = base.evaluate(fixture_T, fixture_labels)
    fixture_D = [[Q(1,4), Q(1,4), Q(-1,2)],
                 [Q(-1,4), Q(-1,4), Q(1,2)],
                 [Q(0), Q(0), Q(0)]]
    check(not accepted and D == fixture_D, "fixed rational defect fixture",
          fixture_T, fixture_labels)
    return {"experiment": "quotient semantic audit 003",
            "status": "PASS" if failed_checks == 0 else "FAIL",
            "domain": "all maps and partitions for n=1..3; one reversal per case",
            "coverage": counts, "failed_checks": failed_checks,
            "failure_examples": failures,
            "scope": "bounded semantic checks; not independent proof or novelty"}


def main():
    root = Path(__file__).resolve().parent.parent
    folder = root / "quotient-audit-001"
    source = folder / "quotient_audit.py"
    recorded = json.loads((folder / "report.json").read_text())
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if recorded.get("status") != "PASS" or digest != recorded.get("source_sha256"):
        raise RuntimeError("baseline source/report check failed")
    spec = importlib.util.spec_from_file_location("baseline", source)
    base = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(base)
    report = audit(base)
    report["baseline_source_sha256"] = digest
    report["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report["python_version"] = sys.version
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
