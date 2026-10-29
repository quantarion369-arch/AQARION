#!/usr/bin/env python3
"""Print canonical representatives and stabilizers for weighted trades."""
import itertools
import json
from collections import Counter

with open("trade_structure_summary.json", encoding="utf-8") as f:
    data = json.load(f)

perms = list(itertools.permutations(range(4)))
flips = list(itertools.product((0, 1), repeat=4))

def transform(word, perm, flip):
    x = tuple(map(int, word))
    return "".join(str(x[perm[j]] ^ flip[j]) for j in range(4))

def normalize(pairs):
    pairs = sorted(pairs)
    first = next(c for _, c in pairs if c)
    if first < 0:
        pairs = [(w, -c) for w, c in pairs]
    return tuple(sorted(pairs))

def image(pairs, perm, flip):
    return normalize([
        (transform(w, perm, flip), c) for w, c in pairs
    ])

def orbit(pairs):
    return {
        image(pairs, p, f)
        for p in perms for f in flips
    }

weighted = []
for r in data["rows"]:
    pairs = [
        (w, c) for w, c in zip(r["support"], r["dependency"]) if c
    ]
    if len(pairs) == 10:
        weighted.append(normalize(pairs))

assert len(weighted) == 40

unseen = set(weighted)
classes = []

while unseen:
    seed = min(unseen)
    images = orbit(seed)
    members = images & unseen
    # If a symmetry image is missing, the supplied 40 records are not
    # closed under the declared equivalence action.
    assert images <= set(weighted), (
        "Weighted census is not closed under the full symmetry group"
    )
    unseen -= members

    stabilizer = sum(
        image(seed, p, f) == seed
        for p in perms for f in flips
    )
    classes.append({
        "representative": seed,
        "orbit_size": len(images),
        "stabilizer_size": stabilizer,
    })

assert sum(c["orbit_size"] for c in classes) == 40
assert sorted(c["orbit_size"] for c in classes) == [8, 32]
assert all(c["orbit_size"] * c["stabilizer_size"] == 384
           for c in classes)

print("WEIGHTED TRADE ORBIT CERTIFICATE")
print("GROUP ORDER:", 384)
print("CLASSES:", len(classes))
for i, c in enumerate(sorted(classes, key=lambda x: x["orbit_size"]), 1):
    print(f"\nCLASS {i}")
    print("ORBIT SIZE:", c["orbit_size"])
    print("STABILIZER SIZE:", c["stabilizer_size"])
    print("SIGNED TERMS:")
    for word, coeff in c["representative"]:
        print(f"  {coeff:+d} * {word}")

print("\nPASS: orbit-stabilizer identity and closure verified")
