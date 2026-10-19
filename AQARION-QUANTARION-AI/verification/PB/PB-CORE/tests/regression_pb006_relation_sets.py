#!/usr/bin/env python3
"""Bounded PB-006 relation-set regression against current local sources."""

import hashlib
import itertools
import json
import subprocess
import sys
import types
from pathlib import Path

LOADED_SOURCES = {}

BASE = Path("AQARION-QUANTARION-AI/verification/PB/PB-CORE")

SOURCES = {
    "implementation": BASE / "verify_pb_core_005_006.py",
    "arithmetic": BASE / "PB-CORE-006-ARITHMETIC-VERIFY.py",
}

EXPECTED = {
    1: (1, 1, 1),
    2: (4, 8, 6),
    3: (27, 135, 51),
    4: (256, 3840, 592),
}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def git(root, *args):
    return subprocess.check_output(
        ["git", "-C", str(root), *args]
    ).decode().strip()

def load_checked(root, key):
    relative = SOURCES[key]
    path = root / relative
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    LOADED_SOURCES[key] = (path, digest)

    print(json.dumps({
        "source": key,
        "path": relative.as_posix(),
        "sha256": digest,
        "source_binding": "current_local_bytes",
        "matches_pinned_revision": None,
    }), flush=True)

    module = types.ModuleType(f"pb_regression_{key}")
    module.__file__ = str(path)
    sys.modules[module.__name__] = module
    exec(compile(data, str(path), "exec"), module.__dict__)
    return module


def check_sources_unchanged():
    for key, (path, expected_digest) in LOADED_SOURCES.items():
        actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
        require(
            actual_digest == expected_digest,
            f"{key}: source changed during regression",
        )

    print(json.dumps({
        "status": "SOURCE_HASHES_UNCHANGED=PASS",
        "scope": "two loaded source files",
    }), flush=True)


def canonical(labels):
    numbering = {}
    result = []
    for label in labels:
        if label not in numbering:
            numbering[label] = len(numbering)
        result.append(numbering[label])
    return tuple(result)

def independent_partitions(n):
    return tuple(
        labels
        for labels in itertools.product(range(n), repeat=n)
        if canonical(labels) == labels
    )

def fixed(t, labels):
    n = len(t)
    return all(
        (labels[x] == labels[y])
        == (labels[t[x]] == labels[t[y]])
        for x in range(n)
        for y in range(n)
    )

def direct_oracle(t, partitions):
    return {p for p in partitions if fixed(t, p)}

def checked_output(function, t):
    rows = [tuple(p) for p in function(t)]
    require(
        all(len(p) == len(t) for p in rows),
        f"Invalid partition length for map {t}",
    )
    normalized = [canonical(p) for p in rows]
    require(
        len(normalized) == len(set(normalized)),
        f"Duplicate relations for map {t}",
    )
    return set(normalized)

def main():
    require(
        len(sys.argv) == 2,
        "Usage: python3 regression_pb006_relation_sets.py REPOSITORY_ROOT",
    )
    root = Path(sys.argv[1]).resolve()

    print(json.dumps({
        "status": "STARTED_NOT_YET_PASSED",
        "source_binding": "current_local_bytes",
        "local_head": git(root, "rev-parse", "HEAD"),
        "python": sys.version,
        "scope": "all self-maps and all partitions for n=1..4",
    }), flush=True)

    implementation = load_checked(root, "implementation")
    arithmetic = load_checked(root, "arithmetic")

    two = independent_partitions(2)
    require(
        direct_oracle((0, 0), two) == {(0, 0)},
        "Constant-map semantic control failed",
    )
    require(
        direct_oracle((0, 1), two) == set(two),
        "Identity semantic control failed",
    )

    duplicate_rejected = False
    try:
        checked_output(lambda _: [(0, 0), (0, 0)], (0, 0))
    except RuntimeError:
        duplicate_rejected = True
    require(duplicate_rejected, "Duplicate-detection control failed")

    partition_numbers = arithmetic.partition_numbers(4)
    results = []

    for n in range(1, 5):
        partitions = independent_partitions(n)
        require(
            len(partitions) == (1, 2, 5, 15)[n - 1],
            f"Partition enumeration failed for n={n}",
        )

        maps = candidates = accepted = 0

        for t in itertools.product(range(n), repeat=n):
            oracle = direct_oracle(t, partitions)
            actual = checked_output(implementation.stable_partitions, t)

            require(
                actual == oracle,
                f"Relation-set mismatch: map={t}; "
                f"missing={sorted(oracle - actual)}; "
                f"extra={sorted(actual - oracle)}",
            )

            maps += 1
            candidates += len(partitions)
            accepted += len(oracle)

        require(
            (maps, candidates, accepted) == EXPECTED[n],
            f"Unexpected coverage/counts for n={n}",
        )

        formula, _ = arithmetic.aggregate_formula(n, partition_numbers)
        require(
            formula == accepted,
            f"Arithmetic aggregate mismatch for n={n}",
        )

        row = {
            "n": n,
            "maps": maps,
            "candidate_pairs": candidates,
            "accepted_fixed_relations": accepted,
            "formula": formula,
            "status": "PASS",
        }
        results.append(row)
        print(json.dumps(row), flush=True)

    check_sources_unchanged()

    print(json.dumps({
        "status": "PB006_ACTUAL_MODULE_RELATION_SETS=PASS",
        "maps": sum(r["maps"] for r in results),
        "candidate_pairs": sum(r["candidate_pairs"] for r in results),
        "accepted_fixed_relations": sum(
            r["accepted_fixed_relations"] for r in results
        ),
        "termux_execution_established_by_this_source": False,
        "general_theorem_proved": False,
        "lean_verified": False,
        "promotion": False,
    }), flush=True)
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({
            "status": "PB006_ACTUAL_MODULE_RELATION_SETS=FAIL",
            "error": str(exc),
        }), file=sys.stderr, flush=True)
        raise SystemExit(1)
