from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
from math import factorial, lcm
from pathlib import Path
import platform
import sys
import time
from typing import Iterator

def partitions(n: int) -> Iterator[tuple[int, ...]]:
    """Yield each set partition of range(n) once as normalized block labels."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        yield ()
        return
    labels = [0] * n

    def visit(i: int, largest: int) -> Iterator[tuple[int, ...]]:
        if i == n:
            yield tuple(labels)
            return
        for label in range(largest + 2):
            labels[i] = label
            yield from visit(i + 1, max(largest, label))

    labels[0] = 0
    yield from visit(1, 0)

def is_pullback_fixed(t: tuple[int, ...], labels: tuple[int, ...]) -> bool:
    """Check E(x,y) iff E(Tx,Ty) directly, for every unordered pair."""
    n = len(t)
    return all(
        (labels[x] == labels[y]) == (labels[t[x]] == labels[t[y]])
        for x in range(n)
        for y in range(x + 1, n)
    )

def periodic_core(t: tuple[int, ...]) -> tuple[tuple[int, ...], tuple[int, ...], int]:
    """Return (sorted core vertices, retraction r=T^L values, exponent L)."""
    n = len(t)
    if n == 0:
        raise ValueError("maps on the empty set are not included in this audit")
    core: set[int] = set()
    depth = [0] * n
    cycle_lengths: set[int] = set()
    for start in range(n):
        seen: dict[int, int] = {}
        path: list[int] = []
        x = start
        while x not in seen:
            seen[x] = len(path)
            path.append(x)
            x = t[x]
        cycle_start = seen[x]
        cycle = path[cycle_start:]
        core.update(cycle)
        cycle_lengths.add(len(cycle))
        for i, v in enumerate(path[:cycle_start]):
            # Number of applications needed to first reach the cycle.
            depth[v] = cycle_start - i
    max_depth = max(depth, default=0)
    L = 1
    for c in cycle_lengths:
        L = lcm(L, c)
    if L < max_depth:
        L *= (max_depth + L - 1) // L
    # r=T^L; using repeated application avoids exponentiation ambiguity.
    r = []
    for x0 in range(n):
        x = x0
        for _ in range(L):
            x = t[x]
        r.append(x)
    return tuple(sorted(core)), tuple(r), L

def normalize_labels(labels: tuple[int, ...] | list[int]) -> tuple[int, ...]:
    renumber: dict[int, int] = {}
    out: list[int] = []
    for x in labels:
        if x not in renumber:
            renumber[x] = len(renumber)
        out.append(renumber[x])
    return tuple(out)

def direct_relations(
    t: tuple[int, ...],
    all_partitions: tuple[tuple[int, ...], ...],
) -> set[tuple[int, ...]]:
    """Enumerate using explicit relation-pair membership, not block-image logic."""
    n = len(t)
    accepted: set[tuple[int, ...]] = set()
    for p in all_partitions:
        relation = {
            (x, y)
            for x in range(n)
            for y in range(n)
            if p[x] == p[y]
        }
        if all(
            ((x, y) in relation) == ((t[x], t[y]) in relation)
            for x in range(n)
            for y in range(n)
        ):
            accepted.add(p)
    return accepted

def relation_set_mismatch(
    t: tuple[int, ...],
    direct: set[tuple[int, ...]],
    constructed: set[tuple[int, ...]],
    metadata: dict[str, object] | None = None,
) -> dict[str, object] | None:
    """Return a compact, reproducible diagnostic, or None when sets agree."""
    if direct == constructed:
        return None
    return {
        "map": t,
        "direct_only": sorted(direct - constructed)[:10],
        "constructed_only": sorted(constructed - direct)[:10],
        "metadata": metadata or {},
    }

def core_relations(
    t: tuple[int, ...],
    all_partitions_by_size: dict[int, tuple[tuple[int, ...], ...]],
) -> tuple[set[tuple[int, ...]], dict[str, object]]:
    """Construct fixed relations from invariant equivalences on the periodic core."""
    n = len(t)
    core, r, exponent = periodic_core(t)
    index = {v: i for i, v in enumerate(core)}
    core_t = tuple(index[t[v]] for v in core)

    invariant: list[tuple[int, ...]] = []
    for p in all_partitions_by_size[len(core)]:
        if is_pullback_fixed(core_t, p):
            invariant.append(p)

    extended = {
        normalize_labels(tuple(p[index[r[x]]] for x in range(n)))
        for p in invariant
    }

    # Verify the construction's defining invariants explicitly.
    if set(r) != set(core):
        raise AssertionError((t, core, r, "r(X) != P"))
    if not all(r[v] == v for v in core):
        raise AssertionError((t, core, r, "r|P != id"))
    if not all(r[t[x]] == t[r[x]] for x in range(n)):
        raise AssertionError((t, r, "rT != Tr"))

    core_set = set(core)
    return extended, {
        "core": core,
        "core_size": len(core),
        "transient_depth": max(
            (distance_to_core(t, x, core_set) for x in range(n)),
            default=0,
        ),
        "exponent": exponent,
        "invariant_core_relations": len(invariant),
    }

def distance_to_core(
    t: tuple[int, ...],
    x: int,
    core: set[int],
) -> int:
    d = 0
    while x not in core:
        x = t[x]
        d += 1
    return d

def partition_numbers(n: int) -> list[int]:
    """Exact p(0)..p(n), via Euler's generalized pentagonal recurrence."""
    if n < 0:
        raise ValueError("n must be non-negative")
    p = [1]
    for m in range(1, n + 1):
        total = 0
        k = 1
        while True:
            g1 = k * (3 * k - 1) // 2
            if g1 > m:
                break
            sign = 1 if k % 2 else -1
            total += sign * p[m - g1]
            g2 = k * (3 * k + 1) // 2
            if g2 <= m:
                total += sign * p[m - g2]
            k += 1
        p.append(total)
    return p

def aggregate_formula(n: int, p: list[int] | None = None) -> int:
    """Evaluate the candidate aggregate formula using exact integer arithmetic."""
    if n < 1:
        raise ValueError("n must be >= 1")
    if p is None or len(p) <= n:
        p = partition_numbers(n)

    total = factorial(n) * p[n]  # explicit full-core endpoint k=n
    for k in range(1, n):
        numerator = factorial(n) * k * (n ** (n - k - 1)) * p[k]
        denominator = factorial(n - k)
        if numerator % denominator != 0:
            raise ArithmeticError(
                f"non-integral aggregate summand at n={n}, k={k}"
            )
        total += numerator // denominator
    return total

def census(max_n: int = 4) -> dict[str, object]:
    """Exhaustively compare direct and core-construction relation sets for n<=max_n."""
    if not 1 <= max_n <= 6:
        raise ValueError("max_n must be between 1 and 6")

    by_size = {
        n: tuple(partitions(n))
        for n in range(1, max_n + 1)
    }
    p = partition_numbers(max_n)
    per_n: dict[str, object] = {}

    for n in range(1, max_n + 1):
        maps_checked = 0
        direct_total = 0
        constructed_total = 0
        mismatches = 0
        first_mismatch = None

        for t in product(range(n), repeat=n):
            maps_checked += 1
            direct = direct_relations(t, by_size[n])
            constructed, meta = core_relations(t, by_size)
            direct_total += len(direct)
            constructed_total += len(constructed)

            mismatch = relation_set_mismatch(t, direct, constructed, meta)
            if mismatch is not None:
                mismatches += 1
                if first_mismatch is None:
                    first_mismatch = mismatch

        formula = aggregate_formula(n, p)
        per_n[str(n)] = {
            "maps_checked": maps_checked,
            "direct_relation_total": direct_total,
            "constructed_relation_total": constructed_total,
            "relation_set_mismatches": mismatches,
            "formula_total": formula,
            "direct_minus_formula": direct_total - formula,
            "first_mismatch": first_mismatch,
        }

        if mismatches or direct_total != constructed_total or direct_total != formula:
            raise AssertionError(f"audit failed at n={n}: {per_n[str(n)]}")

    return {
        "audit_id": "PB-CORE-DIRECT-ENUM-001",
        "scope": f"all labelled maps [n]->[n] for n=1..{max_n}",
        "per_n": per_n,
        "status": "PASS for stated finite scope only",
    }

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=4)
    args = parser.parse_args()

    started_utc = datetime.now(timezone.utc).isoformat()
    started = time.monotonic()
    result = census(args.max_n)
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    result["started_utc"] = started_utc
    result["finished_utc"] = datetime.now(timezone.utc).isoformat()
    result["python_version"] = sys.version
    result["platform"] = platform.platform()
    result["command"] = [sys.executable, *sys.argv]
    result["source_sha256"] = sha256(Path(__file__).read_bytes()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))
