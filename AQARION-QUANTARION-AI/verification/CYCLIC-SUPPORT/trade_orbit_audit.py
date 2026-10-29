#!/usr/bin/env python3
"""Classify trade dependencies under coordinate permutations and bit flips."""
import hashlib
import itertools
import json
from collections import Counter

with open("trade_structure_summary.json", "r", encoding="utf-8") as f:
    data = json.load(f)

records = data["rows"]
assert len(records) == 600

PERMS = list(itertools.permutations(range(4)))
FLIPS = list(itertools.product((0, 1), repeat=4))
assert len(PERMS) * len(FLIPS) == 384

def transform_word(word, perm, flip):
    x = tuple(map(int, word))
    return "".join(
        str(x[perm[j]] ^ flip[j]) for j in range(4)
    )

def normalized_pairs(pairs):
    pairs = sorted(pairs)
    first = next(c for _, c in pairs if c)
    if first < 0:
        pairs = [(w, -c) for w, c in pairs]
    return tuple(sorted(pairs))

def support_orbit_key(words):
    images = []
    for p in PERMS:
        for f in FLIPS:
            images.append(tuple(sorted(
                transform_word(w, p, f) for w in words
            )))
    return min(images)

def dependency_orbit_key(words, coeff):
    pairs = list(zip(words, coeff))
    images = []
    for p in PERMS:
        for f in FLIPS:
            mapped = [
                (transform_word(w, p, f), c)
                for w, c in pairs
            ]
            images.append(normalized_pairs(mapped))
    return min(images)

# Collapse the 560 extensions to their underlying 8-point dependencies.
bases = {}
weighted = []

for r in records:
    pairs = [
        (w, c) for w, c in zip(r["support"], r["dependency"]) if c
    ]
    if len(pairs) == 8:
        words = tuple(w for w, _ in pairs)
        key = tuple(sorted(words))
        coeffs = tuple(c for _, c in pairs)
        if key in bases:
            old = bases[key]
            # Same null vector up to an overall sign.
            assert normalized_pairs(list(zip(old[0], old[1]))) == \
                   normalized_pairs(list(zip(words, coeffs)))
        else:
            bases[key] = (words, coeffs)
    elif len(pairs) == 10:
        weighted.append((r["support"], r["dependency"]))
    else:
        raise AssertionError(("unexpected dependency support size", len(pairs)))

assert len(bases) == 20
assert len(weighted) == 40

base_orbits = Counter()
for words, coeffs in bases.values():
    base_orbits[support_orbit_key(words)] += 1

weighted_orbits = Counter()
for words, coeffs in weighted:
    weighted_orbits[dependency_orbit_key(words, coeffs)] += 1

def orbit_summary(counter):
    classes = {}
    for key, multiplicity in counter.items():
        classes.setdefault(str(multiplicity), 0)
        classes[str(multiplicity)] += 1
    return {
        "number_of_orbits": len(counter),
        "orbit_size_distribution": dict(sorted(
            Counter(counter.values()).items()
        )),
        "representatives": [
            {
                "orbit_size": multiplicity,
                "representative": [list(x) if isinstance(x, tuple) else x
                                   for x in key],
            }
            for key, multiplicity in sorted(
                counter.items(), key=lambda item: repr(item[0])
            )
        ],
    }

result = {
    "group": "coordinate permutations and independent bit flips",
    "group_order": 384,
    "base_support_count": len(bases),
    "base_support_orbits": orbit_summary(base_orbits),
    "weighted_dependency_count": len(weighted),
    "weighted_dependency_orbits": orbit_summary(weighted_orbits),
}

payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
with open("trade_orbit_summary.json", "wb") as f:
    f.write(payload + b"\n")

print("AQARION TRADE ORBIT AUDIT")
print("CUBE SYMMETRY GROUP ORDER:", 384)
print("MINIMAL BASE SUPPORTS:", len(bases))
print("BASE ORBITS:", len(base_orbits))
print("BASE ORBIT SIZES:", dict(Counter(base_orbits.values())))
print("WEIGHTED DEPENDENCIES:", len(weighted))
print("WEIGHTED ORBITS:", len(weighted_orbits))
print("WEIGHTED ORBIT SIZES:", dict(Counter(weighted_orbits.values())))
print("JSON: trade_orbit_summary.json")
print("JSON SHA256:", hashlib.sha256(payload + b"\n").hexdigest())
print("PASS: orbit keys computed")
