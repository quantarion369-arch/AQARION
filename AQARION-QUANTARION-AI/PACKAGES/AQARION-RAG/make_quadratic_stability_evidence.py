#!/usr/bin/env python3
import hashlib
from pathlib import Path

CS = [-2.0, -1.0, -0.5, 0.0, 0.2, 0.25, 0.3, 0.5, 1.0, 1.5]
ITERS = 500

def bounded(c):
    x = 0.0
    for _ in range(ITERS):
        x = x * x + c
        if abs(x) > 2.0:
            return False
    return True

def attracting(c):
    disc = 1.0 - 4.0 * c
    if disc < 0:
        return False
    r = disc ** 0.5
    for xs in ((1 + r) / 2, (1 - r) / 2):
        if abs(2 * xs) < 1:
            return True
    return False

lines = [
    "# Quadratic stability witnesses",
    "",
    "Computed evidence for the real quadratic map x -> x^2 + c, starting at x = 0.",
    "",
    "Definitions:",
    "- bounded_orbit: the orbit remains with |x| <= 2 for 500 iterations.",
    "- attracting_fixed_point: a real fixed point x* exists with |2x*| < 1.",
    "",
    "These are two distinct readings of stability. Neither is assumed to imply the other.",
    "",
    "| c | bounded_orbit | attracting_fixed_point |",
    "|---|---|---|",
]
for c in CS:
    lines.append("| " + repr(c) + " | " + str(bounded(c)).lower() + " | " + str(attracting(c)).lower() + " |")
lines += [
    "",
    "Method: deterministic recomputation, standard library only, fixed iteration count.",
    "Witness rule: a row with bounded_orbit = false is a counterexample witness against any universal bounded-orbit stability claim over the reals.",
]
lines += [
    "",
    "## Witness statements (bounded_orbit reading)",
    "",
]
for c in CS:
    label = "stable" if bounded(c) else "unstable"
    lines.append("The quadratic map with c = " + repr(c) + " is " + label + " under the bounded_orbit reading.")
    lines.append("")

text = chr(10).join(lines) + chr(10)
out = Path("corpus/quadratic-stability-witnesses.md")
out.write_text(text)
print("WROTE", out)
print("SHA256", hashlib.sha256(text.encode("utf-8")).hexdigest())
print(text)
