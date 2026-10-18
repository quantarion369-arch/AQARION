#!/usr/bin/env python3
"""Exact, instance-specific minimal Koopman closure certificate."""
import copy
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path


def matrix(rows):
    return [[Q(x) for x in row] for row in rows]


def multiply(A, B):
    return [[sum((a * b for a, b in zip(row, column)), Q(0))
             for column in zip(*B)] for row in A]


def determinant(A):
    A = matrix(A)
    n = len(A)
    value = Q(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if A[i][j] != 0), None)
        if pivot is None:
            return Q(0)
        if pivot != j:
            A[j], A[pivot] = A[pivot], A[j]
            value = -value
        pivot_value = A[j][j]
        value *= pivot_value
        for i in range(j + 1, n):
            factor = A[i][j] / pivot_value
            for k in range(j, n):
                A[i][k] -= factor * A[j][k]
    return value


def check(cert):
    T = cert["T"]
    B, C, A, M, H = [matrix(cert[name]) for name in ("B", "C", "A", "M", "H")]
    n, d = len(T), len(C[0])
    m = len(B[0])
    K = matrix([[int(j == T[i]) for j in range(n)] for i in range(n)])
    shapes = {"B": (n,m), "C": (n,d), "A": (d,m), "M": (d,d), "H": (2*m,d)}
    for name, X in zip(("B", "C", "A", "M", "H"), (B,C,A,M,H)):
        rows, cols = shapes[name]
        if len(X) != rows or any(len(row) != cols for row in X):
            raise ValueError("invalid matrix shape: " + name)
    if any(type(x) is not int or not 0 <= x < n for x in T):
        raise ValueError("invalid transition")
    rows = cert["minor_rows"]
    if len(rows) != d or len(set(rows)) != d or any(type(i) is not int or not 0 <= i < n for i in rows):
        raise ValueError("invalid minor rows")
    minor = determinant([C[i] for i in rows])
    KB = multiply(K, B)
    R = [B[i] + KB[i] for i in range(n)]
    checks = {
        "initial_observables_contained": multiply(C, A) == B,
        "basis_independent": minor != 0,
        "koopman_invariant": multiply(K, C) == multiply(C, M),
        "generated_from_initial_observables": multiply(R, H) == C,
    }
    return {"accepted": all(checks.values()), "checks": checks,
            "basis_minor_determinant": str(minor),
            "claimed_dimension": d}


def make_certificate():
    return {
        "T": [0,0,1,1],
        "B": [[1,0],[0,1],[1,0],[0,1]],
        "C": [[1,0,1],[0,1,1],[1,0,0],[0,1,0]],
        "A": [[1,0],[0,1],[0,0]],
        "M": [[0,1,1],[0,1,1],[1,-1,0]],
        "H": [[1,0,0],[0,1,0],[0,0,1],[0,0,0]],
        "minor_rows": [0,1,2],
    }


def run():
    certificate = make_certificate()
    valid = check(certificate)
    mutations = {}

    bad = copy.deepcopy(certificate)
    bad["M"][0][0] += 1
    mutations["corrupt_evolution_coefficient"] = check(bad)

    bad = copy.deepcopy(certificate)
    for row in bad["C"]:
        row[2] = row[0]
    mutations["dependent_claimed_basis"] = check(bad)

    bad = copy.deepcopy(certificate)
    bad["C"] = bad["B"]
    bad["A"] = [[1,0],[0,1]]
    bad["M"] = [[1,0],[0,1]]
    bad["H"] = [[1,0],[0,1],[0,0],[0,0]]
    bad["minor_rows"] = [0,1]
    mutations["omit_needed_direction"] = check(bad)

    bad = copy.deepcopy(certificate)
    bad["C"] = [[int(i == j) for j in range(4)] for i in range(4)]
    bad["A"] = bad["B"]
    bad["M"] = [[int(j == bad["T"][i]) for j in range(4)] for i in range(4)]
    bad["H"] = [[int(i == j) for j in range(4)] for i in range(4)]
    bad["minor_rows"] = [0,1,2,3]
    mutations["oversized_unreachable_space"] = check(bad)

    passed = valid["accepted"] and all(not x["accepted"] for x in mutations.values())
    return {
        "experiment": "minimal linear closure certificate 004",
        "status": "PASS" if passed else "FAIL",
        "certificate": certificate,
        "valid_certificate": valid,
        "certified_minimal_dimension": 3 if valid["accepted"] else None,
        "corrupted_certificates": mutations,
        "all_selected_corruptions_rejected": all(not x["accepted"] for x in mutations.values()),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": sys.version,
        "scope": "exact instance certificate; not a general generator, Lean proof, or novelty claim",
    }


if __name__ == "__main__":
    report = run()
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["status"] == "PASS" else 1)
