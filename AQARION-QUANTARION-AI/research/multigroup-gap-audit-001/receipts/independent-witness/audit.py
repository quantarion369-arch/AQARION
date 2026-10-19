
import hashlib
import json
import platform
import sys
import traceback
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
T = (5, 6, 6, 5, 0, 2, 0, 2)
CASES = [
    ("binary", (0,0,1,1,0,0,1,1), (8,4,4)),
    ("three_group", (0,0,1,1,0,0,1,2), (8,5,3)),
    ("four_group", (0,1,2,3,1,0,2,3), (8,5,3)),
]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def save(name, value):
    (ROOT / name).write_text(
        json.dumps(value, indent=2, sort_keys=True) + chr(10)
    )


def equivalent(labels, x, y):
    seen = set()
    while (x, y) not in seen:
        if labels[x] != labels[y]:
            return False
        seen.add((x, y))
        x, y = T[x], T[y]
    return True


save("status.json", {"complete": False})
results = []

try:
    n = len(T)
    A = sp.zeros(n)
    for x, target in enumerate(T):
        A[target, x] = 1

    for name, labels, expected in CASES:
        relation = [
            [equivalent(labels, x, y) for y in range(n)]
            for x in range(n)
        ]
        classes = []
        for x in range(n):
            if not any(x in block for block in classes):
                classes.append([y for y in range(n) if relation[x][y]])

        flattened = [x for block in classes for x in block]
        need(sorted(flattened) == list(range(n)),
             name + ": behavioral classes do not form a partition")

        groups = sorted(set(labels))
        H = sp.Matrix([
            [int(label == group) for label in labels]
            for group in groups
        ])

        power = sp.eye(n)
        blocks = []
        ranks = []
        observation = None
        for horizon in range(1, 2*n + 1):
            blocks.append(H * power)
            observation = sp.Matrix.vstack(*blocks)
            ranks.append(int(observation.rank()))
            if horizon == n:
                observation_n = observation
            power = power * A

        stable = len(classes)
        rank = ranks[n-1]
        gap = stable - rank
        need((stable, rank, gap) == expected,
             name + ": expected " + repr(expected)
             + ", observed " + repr((stable, rank, gap)))
        need(ranks == sorted(ranks), name + ": rank decreased")
        need(all(value == rank for value in ranks[n-1:]),
             name + ": rank grew beyond n observations")

        row = {
            "name": name,
            "labels": labels,
            "behavioral_classes": classes,
            "stable_classes": stable,
            "observable_rank": rank,
            "gap": gap,
            "expected": expected,
            "rank_by_horizon_1_to_16": ranks,
            "observation_matrix_at_horizon_8": [
                [int(value) for value in matrix_row]
                for matrix_row in observation_n.tolist()
            ],
        }
        results.append(row)
        save(name + ".json", row)
        print("PASS:", name, "classes=", stable, "rank=", rank, "gap=", gap)
        print("  ranks by horizon:", ranks)

    save("report.json", {
        "result": "PASS",
        "scope": "three witnesses for one fixed eight-state map",
        "transition_map": T,
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "sympy": sp.__version__,
        "behavioral_method": "pair trajectories until mismatch or pair repeat",
        "rank_method": "exact SymPy rank of stacked H*A**t",
        "production_evaluator_imported": False,
        "expected_values_origin": "earlier production census in session",
        "results": results,
        "full_4140_partition_audit": False,
    })
    save("status.json", {"complete": True, "result": "PASS"})
    print("PASS: all three witnesses independently matched.")
except Exception as error:
    save("status.json", {
        "complete": True,
        "result": "FAIL",
        "error": type(error).__name__ + ": " + str(error),
    })
    traceback.print_exc()
    sys.exit(1)
