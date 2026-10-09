#!/usr/bin/env python3
"""SM003 exact-rational theorem and mutation audit.

Usage:
python3 verification/SM/SM003/mutations.py

Exhaustively checks all maps and set partitions for n <= 4.
Every mutant is evaluated against the correct defect-rank oracle.
This script is a test harness; its output must be retained as evidence.
"""

from fractions import Fraction as F
from itertools import product
import json
import platform
import sys

def partitions(n):
"""Generate each set partition of range(n) exactly once."""
if n == 0:
yield ()
return
for part in partitions(n - 1):
yield part + ((n - 1,),)
for i in range(len(part)):
yield part[:i] + (part[i] + (n - 1,),) + part[i + 1:]

def mat_zero(n, m):
return [[F(0) for _ in range(m)] for _ in range(n)]

def identity(n):
a = mat_zero(n, n)
for i in range(n):
a[i][i] = F(1)
return a

def transpose(a):
return [list(row) for row in zip(*a)]

def add(a, b):
return [[x + y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]

def sub(a, b):
return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]

def mul(a, b):
if not a or not b or len(a[0]) != len(b):
raise ValueError("incompatible matrix dimensions")
bt = transpose(b)
return [
[sum((x * y for x, y in zip(row, col)), F(0)) for col in bt]
for row in a
]

def rank(a):
"""Exact rank by rational row reduction."""
if not a:
return 0
a = [row[:] for row in a]
rows, cols = len(a), len(a[0])
r = 0
for col in range(cols):
pivot = next((i for i in range(r, rows) if a[i][col]), None)
if pivot is None:
continue
a[r], a[pivot] = a[pivot], a[r]
p = a[r][col]
a[r] = [x / p for x in a[r]]
for i in range(rows):
if i != r and a[i][col]:
q = a[i][col]
a[i] = [x - q * y for x, y in zip(a[i], a[r])]
r += 1
if r == rows:
break
return r

def koopman(t):
n = len(t)
k = mat_zero(n, n)
for x, y in enumerate(t):
k[x][y] = F(1)
return k

def projector(part, n):
p = mat_zero(n, n)
for block in part:
size = F(len(block))
for x in block:
for y in block:
p[x][y] = F(1) / size
return p

def graph_component_count(t, part):
"""Count components in the undirected target-block co-occurrence graph."""
nblocks = len(part)
block_of = {}
for j, block in enumerate(part):
for x in block:
block_of[x] = j

adj = [set() for _ in range(nblocks)]
for source in part:
    targets = sorted({block_of[t[x]] for x in source})
    for u in targets:
        for v in targets:
            if u != v:
                adj[u].add(v)
                adj[v].add(u)

seen = set()
components = 0
for start in range(nblocks):
    if start in seen:
        continue
    components += 1
    stack = [start]
    seen.add(start)
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
return components

def inspect_case(t, part):
n = len(t)
k_blocks = len(part)
K = koopman(t)
P = projector(part, n)
I = identity(n)
D = mul(sub(I, P), mul(K, P))
expected = k_blocks - graph_component_count(t, part)
actual = rank(D)

mutants = {
    "M-K-transpose": transpose(K),
    "M-commutator-KP-minus-PK": sub(mul(K, P), mul(P, K)),
    "M-left-projection-I-minus-P-times-K": mul(sub(I, P), K),
    "M-projected-K-PKP": mul(P, mul(K, P)),
    "M-left-projection-times-K-transpose":
        mul(sub(I, P), transpose(K)),
    "M-KP-times-I-minus-P": mul(K, mul(P, sub(I, P))),
}
results = {
    name: rank(matrix) != expected
    for name, matrix in mutants.items()
}
# Deliberately wrong graph oracle: returns c instead of k-c.
results["M-R-c-only-variant"] = (
    graph_component_count(t, part) != expected
)
return actual, expected, results

def main():
max_n = 4
cases = 0
theorem_mismatches = []
mutant_kills = {}
mutant_first_kill = {}

for n in range(1, max_n + 1):
    for t in product(range(n), repeat=n):
        for part in partitions(n):
            cases += 1
            actual, expected, results = inspect_case(t, part)
            if actual != expected:
                theorem_mismatches.append({
                    "n": n, "map": t, "partition": part,
                    "matrix_rank": actual, "graph_rank": expected,
                })
            for name, killed in results.items():
                mutant_kills.setdefault(name, 0)
                if killed:
                    mutant_kills[name] += 1
                    mutant_first_kill.setdefault(
                        name,
                        {
                            "n": n,
                            "map": t,
                            "partition": part,
                            "correct_rank": expected,
                        },
                    )

report = {
    "schema": "AQ-SM003-MUTATION-REPORT-1.0",
    "status": "PASS" if not theorem_mismatches else "FAIL",
    "scope": {
        "maps_and_partitions": "exhaustive",
        "n": f"1..{max_n}",
        "cases": cases,
        "arithmetic": "exact rational",
    },
    "environment": {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
    },
    "theorem_mismatch_count": len(theorem_mismatches),
    "theorem_mismatch_examples": theorem_mismatches[:10],
    "mutation_kill_counts": mutant_kills,
    "mutation_survivors": [
        name for name, count in mutant_kills.items() if count == 0
    ],
    "first_kill_witnesses": mutant_first_kill,
    "warning": (
        "This report covers only the mutations implemented here and "
        "the enumerated finite scope. It does not establish Lean proof, "
        "publication readiness, or certification."
    ),
}
print(json.dumps(report, indent=2, sort_keys=True))
return 0 if not theorem_mismatches else 1

if name == "main":
raise SystemExit(main())
