AQ-BURNSIDE-M3-001 — Independent M3 Recompute

Purpose

This document specifies the independent recomputation required to validate the Burnside M_3 evidence object.

The recomputation is deliberately separate from the stored evidence.

The stored M3 table must not be treated as the computational oracle.

---

Mathematical quantity

For each k,

[
M_3(k)

\frac{1}{k!}
\sum_{\sigma\in S_k} C(\sigma)^3.
]

Equivalently, using cycle types,

[
M_3(k)

\sum_{\lambda\vdash k}
\frac{C(\lambda)^3}{z_\lambda},
]

where

[
z_\lambda

\prod_{j\ge1}j^{m_j}m_j!
]

for

[
\lambda=1^{m_1}2^{m_2}\cdots.
]

All arithmetic is exact.

No floating-point computation is permitted.

---

Required independent checks

1. JSON integrity

The stored evidence object must parse successfully and contain the expected M3 table.

JSON_INTEGRITY=PASS

This check validates structure only. It does not validate the mathematical values.

---

2. Direct permutation control

For

[
k=1,\ldots,5,
]

enumerate all permutations in S_k, compute C(\sigma) independently, and evaluate

[
\frac1{k!}\sum_{\sigma\in S_k}C(\sigma)^3.
]

The result must agree exactly with the corresponding cycle-type computation.

Required result:

DIRECT_PERMUTATION_M3_K1_5=PASS

---

3. Direct cycle-type control

For

[
k=1,\ldots,6,
]

compute C(\lambda) independently for every partition \lambda\vdash k.

Then compare the resulting cycle-type values against the independently enumerated permutation values.

Required result:

DIRECT_CYCLE_TYPE_C_K1_6=PASS

with

MISMATCHES=0

---

4. Full cycle-type M3 computation

For

[
k=1,\ldots,31,
]

compute

[
M_3(k)

\sum_{\lambda\vdash k}
\frac{C(\lambda)^3}{z_\lambda}.
]

The calculation must regenerate the values from the underlying C(\lambda) computation.

It must not simply read the claimed M3 values and reproduce them.

Required result:

CYCLE_TYPE_M3_K1_31=PASS

---

Corrected transcription targets

The following five entries were previously transcribed incorrectly and must be regenerated and checked against the independent computation.

k=25
CORRECT=...2082042010781

k=27
CORRECT=...21060616858881

k=28
CORRECT=...7521576062705103

k=29
CORRECT=...628859141458156260

k=30
CORRECT=...6237961731886193129380

The omitted leading portions above are intentionally not reconstructed here.

The authoritative values must come from the exact recomputation.

No manually reconstructed integer is accepted as evidence.

---

Why the second computation is required

The previous M3 pass demonstrated that a computational pipeline can produce a table containing transcription errors.

Therefore:

[
\text{stored table}
\neq
\text{oracle}.
]

The validation must independently regenerate the mathematical quantities and then compare them with the stored evidence.

This is the reason the recomputation is a separate evidence-control step.

---

Required final receipt

Only after the actual recomputation has been executed may the following receipt be emitted:

AQ-BURNSIDE-M3-001
JSON_INTEGRITY=PASS
DIRECT_PERMUTATION_M3_K1_5=PASS
DIRECT_CYCLE_TYPE_C_K1_6=PASS
CYCLE_TYPE_M3_K1_31=PASS
EXACT_INTEGER_ARITHMETIC=PASS
MISMATCHES=0
FORMALIZATION=OPEN
PROMOTION=BLOCKED

Until the execution has actually occurred, these are required receipt fields, not a prewritten PASS receipt.

---

Governance boundary

A successful recomputation establishes computational consistency of the finite M3 evidence.

It does not by itself establish:

- Lean formalization;
- a publication-level theorem certificate;
- novelty;
- asymptotic consequences beyond the verified finite data;
- promotion status.

Therefore the required terminal state remains:

FORMALIZATION=OPEN
PROMOTION=BLOCKED

until those separate conditions are satisfied.
