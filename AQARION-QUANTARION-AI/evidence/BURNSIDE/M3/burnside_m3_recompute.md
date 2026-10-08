AQ-BURNSIDE-M3-001

Independent recomputation specification.

This program must compute C(lambda) and M3(k) independently

of the stored evidence JSON.

Exact arithmetic only.

No floating point.

No hard-coded claimed M3 values.

from future import annotations

from collections import Counter
from fractions import Fraction
from itertools import permutations
from math import factorial, gcd

def partitions(n: int, lo: int = 1):
if n == 0:
yield ()
return

for first in range(lo, n + 1):
    for rest in partitions(n - first, first):
        yield (first,) + rest

def z_lambda(lam):
c = Counter(lam)
z = 1
for part, multiplicity in c.items():
z *= (part ** multiplicity) * factorial(multiplicity)
return z

def permutation_cycles(p):
n = len(p)
seen = [False] * n
cycles = []

for i in range(n):
    if seen[i]:
        continue

    j = i
    length = 0

    while not seen[j]:
        seen[j] = True
        length += 1
        j = p[j]

    cycles.append(length)

return tuple(sorted(cycles))

def enumerate_set_partitions(n):
"""
Independent partition generator for small-k direct controls.

Returns partitions of range(n) as tuples of blocks.
"""
blocks = []

def rec(i):
    if i == n:
        yield tuple(tuple(b) for b in blocks)
        return

    for j in range(len(blocks)):
        blocks[j].append(i)
        yield from rec(i + 1)
        blocks[j].pop()

    blocks.append([i])
    yield from rec(i + 1)
    blocks.pop()

yield from rec(0)

def canonical_partition(partition):
return tuple(sorted(tuple(sorted(block)) for block in partition))

def permutation_respects_partition(p, partition):
"""
Placeholder for the exact C(lambda) predicate.

This MUST be replaced by the already-established independent
semantic definition of C for the AQARION Burnside object.

Do not substitute a guessed formula here.
"""
raise NotImplementedError(
    "Bind to the independently established C(lambda) definition."
)

def direct_C_for_permutation(p):
"""
Direct small-k control.

Counts partitions satisfying the exact semantic predicate.
"""
n = len(p)
total = 0

for part in enumerate_set_partitions(n):
    if permutation_respects_partition(p, part):
        total += 1

return total

def direct_M3(n):
total = 0

for p in permutations(range(n)):
    c = direct_C_for_permutation(p)
    total += c ** 3

return Fraction(total, factorial(n))

def cycle_type_M3(n, C_by_lambda):
total = Fraction(0, 1)

for lam in partitions(n):
    c = C_by_lambda(lam)
    total += Fraction(c ** 3, z_lambda(lam))

return total

def main():
print("AQ-BURNSIDE-M3-001")
print("EXACT_INTEGER_ARITHMETIC=REQUIRED")
print("STORED_EVIDENCE_IS_NOT_USED_AS_ORACLE")

# Small direct control.
#
# The semantic C implementation must be bound before execution.
for k in range(1, 6):
    value = direct_M3(k)
    print(f"DIRECT_M3[{k}]={value}")

print("DIRECT_PERMUTATION_M3_K1_5=REQUIRES_SEMANTIC_C_BINDING")

# Cycle-type computation must use the independently established
# C(lambda) evaluator.
print("CYCLE_TYPE_M3_K1_31=REQUIRES_SEMANTIC_C_BINDING")

print("FORMALIZATION=OPEN")
print("PROMOTION=BLOCKED")

if name == "main":
main()
