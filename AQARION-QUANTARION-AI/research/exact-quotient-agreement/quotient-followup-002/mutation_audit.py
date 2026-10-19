#!/usr/bin/env python3
"""Follow-up fixtures and mutation audit; standard library only."""
import hashlib
import importlib.util
import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "quotient-audit-001"


def load_baseline():
    source = BASE / "quotient_audit.py"
    report = json.loads((BASE / "report.json").read_text())
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if report.get("status") != "PASS" or report.get("source_sha256") != digest:
        raise RuntimeError("baseline source/report check failed")
    spec = importlib.util.spec_from_file_location("baseline", source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, digest


def mutant_defect(module, T, labels, mutation):
    n = len(T)
    Q = module.Q
    P = []
    for i in range(n):
        row = []
        size = labels.count(labels[i])
        for j in range(n):
            value = Q(1, size) if labels[i] == labels[j] else Q(0)
            if mutation == "unnormalized_projection":
                value = Q(int(labels[i] == labels[j]))
            row.append(value)
        P.append(row)
    K = [[Q(int(j == T[i])) for j in range(n)] for i in range(n)]
    if mutation == "transposed_koopman":
        K = [list(row) for row in zip(*K)]
    KP = module.multiply(K, P)
    PKP = module.multiply(P, KP)
    return all(KP[i][j] == PKP[i][j] for i in range(n) for j in range(n))


def representative_only(T, labels):
    # Intentionally wrong: chooses successors without checking other members.
    quotient = []
    for block in range(max(labels) + 1):
        representative = labels.index(block)
        quotient.append(labels[T[representative]])
    return len(quotient) == max(labels) + 1


def main():
    module, baseline_hash = load_baseline()
    T, labels = (2, 3, 0, 1), (0, 0, 1, 1)
    ok, accepted, witness, quotient, D = module.evaluate(T, labels)
    fixture_pass = ok and accepted and quotient == [1, 0] and witness is None
    fixture = {"passed": fixture_pass,
               **module.case_record(T, labels, witness, quotient, D)}
    names = ["representative_only", "transposed_koopman", "unnormalized_projection"]
    results = {name: {"detected": False, "disagreements": 0, "witness": None}
               for name in names}
    cases = 0
    baseline_failures = 0
    for n in range(1, 4):
        for T in itertools.product(range(n), repeat=n):
            for labels in module.partitions(n):
                cases += 1
                ok, expected, witness, quotient, D = module.evaluate(T, labels)
                if not ok:
                    baseline_failures += 1
                for name in names:
                    actual = (representative_only(T, labels) if name == "representative_only"
                              else mutant_defect(module, T, labels, name))
                    if actual != expected:
                        row = results[name]
                        row["detected"] = True
                        row["disagreements"] += 1
                        if row["witness"] is None:
                            row["witness"] = {"expected_compatible": expected,
                                              "mutant_accepts": actual,
                                              **module.case_record(T, labels, witness, quotient, D)}
    passed = (fixture_pass and cases == 144 and baseline_failures == 0
              and all(row["detected"] for row in results.values()))
    output = {"experiment": "quotient follow-up 002", "status": "PASS" if passed else "FAIL",
              "baseline_source_sha256": baseline_hash,
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "python_version": sys.version,
              "nontrivial_quotient_fixture": fixture,
              "mutation_domain": "all maps and partitions for n=1..3",
              "cases": cases, "baseline_disagreements": baseline_failures,
              "mutations": results,
              "scope": "selected mutation detection; not completeness or a universal proof"}
    print(json.dumps(output, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
