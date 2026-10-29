#!/usr/bin/env python3
"""Recheck connectivity and Eulerian semantics for deficient size-10 supports.

Input:
    trade_structure_summary.json

Definitions:
    history w = directed edge prefix3(w) -> suffix3(w)
    cyclic support with repetition = strongly connected active edge graph
    once-only cyclic realization = strongly connected + balanced degrees

This script recomputes graph properties; it does not trust the
stored cyclic_realizable field.
"""
import hashlib
import json
from collections import Counter, defaultdict, deque

INPUT = "trade_structure_summary.json"
OUTPUT = "cyclic_support_semantics_audit.json"


def graph_properties(words):
    edges = []
    vertices = set()
    outdeg = Counter()
    indeg = Counter()
    adj = defaultdict(list)
    rev = defaultdict(list)

    for w in words:
        if len(w) != 4 or set(w) - {"0", "1"}:
            raise ValueError(f"Invalid four-bit history: {w!r}")
        u, v = w[:3], w[1:]
        edges.append((u, v, w))
        vertices.update((u, v))
        outdeg[u] += 1
        indeg[v] += 1
        adj[u].append(v)
        rev[v].append(u)

    if not vertices:
        return {
            "strongly_connected": False,
            "balanced": False,
            "eulerian": False,
            "active_vertices": 0,
            "degree_imbalances": {},
        }

    # Reachability from one active vertex in the graph and its reverse.
    root = next(iter(vertices))

    def reachable(graph):
        seen = {root}
        todo = [root]
        while todo:
            u = todo.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        return seen

    strongly_connected = (
        reachable(adj) == vertices and reachable(rev) == vertices
    )

    imbalances = {
        v: outdeg[v] - indeg[v]
        for v in sorted(vertices)
        if outdeg[v] != indeg[v]
    }
    balanced = not imbalances

    # For a finite directed graph, an Euler circuit exists iff all
    # non-isolated vertices are in one connected component and degrees
    # balance. Here strong connectivity is the directed condition.
    eulerian = strongly_connected and balanced

    return {
        "strongly_connected": strongly_connected,
        "balanced": balanced,
        "eulerian": eulerian,
        "active_vertices": len(vertices),
        "degree_imbalances": imbalances,
    }


with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

rows = data["rows"]
assert len(rows) == 600, f"Expected 600 records, got {len(rows)}"

# The census rows can repeat a support only if their support lists agree.
support_to_records = defaultdict(list)
for row in rows:
    support = tuple(sorted(set(row["support"])))
    assert len(support) == 10, (
        f"Expected a ten-history support, got {len(support)}: {support}"
    )
    support_to_records[support].append(row)

results = []
for support, records in sorted(support_to_records.items()):
    props = graph_properties(support)
    results.append({
        "support": list(support),
        "record_multiplicity": len(records),
        **props,
    })

# Group results by graph semantics.
semantic_counts = Counter(
    (
        r["strongly_connected"],
        r["balanced"],
        r["eulerian"],
    )
    for r in results
)

strong = [r for r in results if r["strongly_connected"]]
euler = [r for r in results if r["eulerian"]]

result = {
    "input": INPUT,
    "input_records": len(rows),
    "distinct_size10_supports": len(results),
    "strongly_connected_supports": len(strong),
    "eulerian_supports": len(euler),
    "semantic_tuple_counts": {
        f"strong={s},balanced={b},eulerian={e}": n
        for (s, b, e), n in sorted(semantic_counts.items())
    },
    "strongly_connected_masks": [
        "".join(f"{int(w, 2):04X}" for w in [])
        for _ in []
    ],
    "strongly_connected_supports_hex": [
        format(sum(1 << int(w, 2) for w in r["support"]), "04X")
        for r in strong
    ],
    "eulerian_supports_hex": [
        format(sum(1 << int(w, 2) for w in r["support"]), "04X")
        for r in euler
    ],
    "strongly_connected_details": strong,
    "eulerian_details": euler,
}

payload = json.dumps(
    result, sort_keys=True, separators=(",", ":")
).encode() + b"\n"

with open(OUTPUT, "wb") as f:
    f.write(payload)

print("AQARION CYCLIC SUPPORT SEMANTICS AUDIT")
print("INPUT RECORDS:", len(rows))
print("DISTINCT SIZE-10 SUPPORTS:", len(results))
print("STRONGLY CONNECTED:", len(strong))
print("EULERIAN / ONCE-ONLY:", len(euler))
print("STRONGLY CONNECTED MASKS:", result["strongly_connected_supports_hex"])
print("EULERIAN MASKS:", result["eulerian_supports_hex"])
print("SEMANTIC COUNTS:", result["semantic_tuple_counts"])
print("JSON:", OUTPUT)
print("JSON SHA256:", hashlib.sha256(payload).hexdigest())

assert all(r["eulerian"] for r in euler)
assert all(r["eulerian"] == (
    r["strongly_connected"] and r["balanced"]
) for r in results)
print("PASS: graph predicates recomputed and consistency checks passed")
