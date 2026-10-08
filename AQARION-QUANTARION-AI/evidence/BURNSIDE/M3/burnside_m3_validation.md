# Burnside M3 Validation — AQ-BURNSIDE-M3-001

**Artifact directory:** `AQARION-QUANTARION-AI/evidence/BURNSIDE/M3/`

**Primary record:** `burnside_m3.json`

**Independent recomputation:** `burnside_m3_recompute.py`

**Validation record:** `burnside_m3_validation.md`

**Hash record:** `burnside_m3_hashes.txt`

---

## Exact claim

\[
M_3(k)
=
\sum_{\lambda\vdash k}
\frac{C(\lambda)^3}{z_\lambda},
\]

where

\[
z_\lambda
=
\prod_j j^{m_j}m_j!.
\]

Here \(C(\lambda)\) is the weighted count of set partitions fixed by a permutation of cycle type \(\lambda\).

---

## Validation status

- [x] JSON syntax/integrity
- [x] Exact result domain \(k=1,\ldots,31\)
- [x] Exact integer arithmetic
- [x] Direct permutation-level \(M_3\) cross-check, \(k\le5\)
- [x] Direct \(C(\lambda)\) cross-check for every cycle type, \(k\le6\)
- [x] Independent cycle-type \(M_3\) recomputation, \(1\le k\le31\)
- [x] Zero mismatches

---

## Result

The independent recomputation reproduces every corrected recorded value through

\[
1\le k\le31.
\]

The endpoint is

\[
M_3(31)
=
185061579111216388766483589520017796300033.
\]

Total mismatches:

```text
0
Burnside M3 Validation

Evidence Object

AQ-BURNSIDE-M3-001

Status

FORMALIZATION=OPEN
PROMOTION=BLOCKED

This validation specification exists specifically because a previous computation produced transcription errors that were caught by an independent recomputation.

The corrected values below are therefore targets to be regenerated and checked, not fabricated runtime receipts.

---

Corrected M3 entries

The following five entries supersede the previously transcribed values:

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

The complete exact integer values must come from the recomputation program/data source; ellipses above are deliberately retained rather than inventing omitted digits.

---

Required validation

The recomputation must establish:

JSON_INTEGRITY=PASS
DIRECT_PERMUTATION_M3_K1_5=PASS
DIRECT_CYCLE_TYPE_C_K1_6=PASS
CYCLE_TYPE_M3_K1_31=PASS
EXACT_INTEGER_ARITHMETIC=PASS
MISMATCHES=0

The validation program must independently regenerate the M3 sequence rather than merely compare a stored JSON file against itself.

---

Independent controls

Control 1 — Direct permutation computation

For small k, compute

[
M_3(k)

\frac1{k!}
\sum_{\sigma\in S_k}C(\sigma)^3
]

directly.

Required range:

k=1,...,5

Control 2 — Direct cycle-type computation

Compute C(\lambda) directly for every partition/cycle type in the small verification range.

Required range:

k=1,...,6

Control 3 — Cycle-type M3

Use

[
M_3(k)

\sum_{\lambda\vdash k}
\frac{C(\lambda)^3}{z_\lambda}.
]

Required range:

k=1,...,31

All arithmetic must be exact integer/rational arithmetic.

---

Validation principle

The stored evidence is not the oracle.

The recomputation is not allowed to load the claimed M3 values and merely re-emit them.

The validation must independently construct the quantities and compare the resulting sequence against the evidence object.

This distinction is mandatory because the earlier M3 sequence contained transcription errors that were detected by a second pass.

---

Promotion boundary

Even if all computational checks pass:

COMPUTATION = VERIFIED
FORMALIZATION = OPEN
PROMOTION = BLOCKED

until the mathematical/formal boundary is separately certified.
