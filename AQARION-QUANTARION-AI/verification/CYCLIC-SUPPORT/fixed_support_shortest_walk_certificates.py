#!/usr/bin/env python3
"""AQARION fixed-support shortest-walk certificate verifier.

Reconstructed verifier for the eight certificate records supplied in chat.
No optimizer is used. All arithmetic is exact integer arithmetic.
"""

import hashlib
import json
import sys
from collections import Counter

CASES = {
    "3E7C": {
        "word": "001101011001",
        "n": {
            "0010": 1, "0011": 1, "0100": 1, "0101": 1,
            "0110": 2, "1001": 2, "1010": 1, "1011": 1,
            "1100": 1, "1101": 1,
        },
        "p": [0, 0, 0, 1, 1, 0, 0, 0],
        "length": 12,
    },
    "55BE": {
        "word": "000111000101",
        "n": {
            "0001": 2, "0010": 1, "0011": 1, "0100": 1,
            "0101": 1, "0111": 1, "1000": 2, "1010": 1,
            "1100": 1, "1110": 1,
        },
        "p": [1, 0, 0, 0, 2, 0, 0, 0],
        "length": 12,
    },
    "5DAE": {
        "word": "0001010111000111",
        "n": {
            "0001": 2, "0010": 1, "0011": 1, "0101": 2,
            "0111": 2, "1000": 2, "1010": 1, "1011": 1,
            "1100": 2, "1110": 2,
        },
        "p": [1, 0, 1, 5, 2, 0, 3, 4],
        "length": 16,
    },
    "6DB6": {
        "word": "0001011101",
        "n": {
            "0001": 1, "0010": 1, "0100": 1, "0101": 1,
            "0111": 1, "1000": 1, "1010": 1, "1011": 1,
            "1101": 1, "1110": 1,
        },
        "p": [0, 0, 0, 0, 0, 0, 0, 0],
        "length": 10,
    },
    "75BA": {
        "word": "0001110001110101",
        "n": {
            "0001": 2, "0011": 2, "0100": 1, "0101": 1,
            "0111": 2, "1000": 2, "1010": 2, "1100": 1,
            "1101": 1, "1110": 2,
        },
        "p": [4, 3, 0, 2, 5, 1, 0, 1],
        "length": 16,
    },
    "799E": {
        "word": "00011101110001",
        "n": {
            "0001": 2, "0010": 1, "0011": 1, "0100": 1,
            "0111": 2, "1000": 2, "1011": 1, "1100": 1,
            "1101": 1, "1110": 2,
        },
        "p": [1, 0, 0, 2, 2, 0, 0, 1],
        "length": 14,
    },
    "7DAA": {
        "word": "000111010111",
        "n": {
            "0001": 1, "0011": 1, "0101": 1, "0111": 2,
            "1000": 1, "1010": 1, "1011": 1, "1100": 1,
            "1101": 1, "1110": 2,
        },
        "p": [0, 0, 0, 2, 0, 0, 0, 1],
        "length": 12,
    },
    "D3CB": {
        "word": "000111100110",
        "n": {
            "0000": 1, "0001": 1, "0011": 2, "0110": 1,
            "0111": 1, "1000": 1, "1001": 1, "1100": 2,
            "1110": 1, "1111": 1,
        },
        "p": [0, 1, 0, 0, 0, 0, 1, 0],
        "length": 12,
    },
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def cyclic_windows(word):
    require(set(word) <= {"0", "1"}, "word is not binary")
    require(len(word) >= 4, "word is shorter than four bits")
    wrapped = word + word[:3]
    return Counter(wrapped[i:i + 4] for i in range(len(word)))


def verify(mask, case):
    word = case["word"]
    n = case["n"]
    p = case["p"]
    expected_length = case["length"]

    require(len(p) == 8, f"{mask}: expected eight potentials")
    require(len(n) == 10, f"{mask}: expected ten support edges")
    require(all(len(e) == 4 and set(e) <= {"0", "1"} for e in n),
            f"{mask}: malformed edge")
    require(all(isinstance(k, int) and k >= 1 for k in n.values()),
            f"{mask}: invalid multiplicity")
    require(all(isinstance(x, int) for x in p),
            f"{mask}: non-integer potential")

    # Check the claimed cyclic word against every edge multiplicity.
    observed = cyclic_windows(word)
    require(dict(sorted(observed.items())) == dict(sorted(n.items())),
            f"{mask}: cyclic word/multiplicity mismatch")

    E = [int(edge, 2) for edge in n]
    y = {e: n[f"{e:04b}"] - 1 for e in E}

    require(all(z >= 0 for z in y.values()),
            f"{mask}: uncovered edge")

    # Vertex v has outgoing edges where (e >> 1) == v
    # and incoming edges where (e & 7) == v.
    # b = indegree(base support) - outdegree(base support).
    b = [
        sum((e & 7) == v for e in E)
        - sum((e >> 1) == v for e in E)
        for v in range(8)
    ]

    for v in range(8):
        added_out = sum(y[e] for e in E if (e >> 1) == v)
        added_in = sum(y[e] for e in E if (e & 7) == v)
        require(
            added_out - added_in == b[v],
            f"{mask}: balance failure at vertex {v:03b}",
        )

    # Dual feasibility for every selected directed edge.
    for e in E:
        tail = e >> 1
        head = e & 7
        require(
            p[tail] - p[head] <= 1,
            f"{mask}: invalid dual bound on edge {e:04b}",
        )

    lower = sum(b[v] * p[v] for v in range(8))
    upper = sum(y.values())

    require(lower >= 0, f"{mask}: negative claimed lower bound")
    require(lower == upper, f"{mask}: primal/dual gap")
    require(
        len(word) == len(E) + lower == expected_length,
        f"{mask}: wrong optimum",
    )
    require(sum(n.values()) == len(word),
            f"{mask}: multiplicity total differs from word length")

    return {
        "support": mask,
        "length": len(word),
        "repeat_cost": upper,
        "lower_bound": lower,
        "upper_bound": upper,
        "dual_feasible": True,
        "primal_feasible": True,
        "cyclic_word_matches_multiplicities": True,
        "primal_dual_gap": 0,
    }


def main():
    print("AQARION EXACT FIXED-SUPPORT SHORTEST-WALK CERTIFICATE AUDIT")
    print("MODE: reconstructed verifier; no optimizer")

    results = []
    try:
        for mask, case in CASES.items():
            result = verify(mask, case)
            results.append(result)
            print(
                f"{mask} PASS minimum_length={result['length']} "
                f"repeat_cost={result['repeat_cost']} "
                f"lower_bound={result['lower_bound']} "
                f"upper_bound={result['upper_bound']}"
            )
    except (AssertionError, KeyError, TypeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    # Hash this reconstructed dataset, not the unavailable original file.
    canonical = json.dumps(
        CASES, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()

    print(f"CASES VERIFIED: {len(results)}")
    print(f"RECONSTRUCTED_DATA_SHA256: {digest}")
    print("PASS: all supplied primal/dual and cyclic-word checks passed")
    print("LIMIT: certificate validity is checked; source provenance is not")
    return 0


if __name__ == "__main__":
    sys.exit(main())
