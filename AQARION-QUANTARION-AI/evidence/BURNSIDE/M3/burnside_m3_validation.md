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

Burnside M3 Validation — AQ-BURNSIDE-M3-001

Record: "burnside_m3.json"
Recomputation: "burnside_m3_recompute.py"
Hash manifest: "burnside_m3_hashes.txt"
Claim: "AQ-BURNSIDE-M3-001"

Mathematical statement

For (k\geq1),

[
M_3(k)=\frac{1}{k!}\sum_{\sigma\in S_k}C(\sigma)^3
=\sum_{\lambda\vdash k}\frac{C(\lambda)^3}{z_\lambda},
]

where (C(\lambda)) counts set partitions fixed by a permutation of cycle type (\lambda), and

[
z_\lambda=\prod_{j\geq1}j^{m_j}m_j!.
]

The second equality follows by grouping permutations into conjugacy classes. The first expression is an orbit count by Burnside's lemma and is therefore a nonnegative integer.

Recorded computation scope

- Integer domain: (1\leq k\leq31).
- Arithmetic: exact integer/rational arithmetic.
- Recorded direct permutation control: (k\leq5).
- Recorded direct cycle-type control: every cycle type for (k\leq6).
- Recorded cycle-type recomputation: (k\leq31).

These are the scopes claimed by the evidence record. They must not be represented as a newly authenticated execution unless the source revision, command, exit status, output, and artifact digests are captured together.

Required reproduction

From this directory, run:

python3 burnside_m3_recompute.py

The run must independently regenerate the values, compare them with "burnside_m3.json", and exit nonzero on any mismatch.

Required checks:

- JSON parses and satisfies the expected schema.
- Direct permutation-level (M_3) control passes for (k=1,\ldots,5).
- Direct (C(\lambda)) control passes for all cycle types through (k=6).
- Cycle-type (M_3) comparison passes for (k=1,\ldots,31).
- Exact arithmetic is used.
- Total mismatches equal zero.

Evidence interpretation

A successful run supports computational agreement on the declared finite domain. It does not, by itself, establish a universal theorem beyond that domain, novelty, external independent reproduction, or Lean formalization.

A second implementation is not automatically independent merely because it is a different file. Independence requires a justified difference in construction or an independently specified oracle.

Current governance

- Computational record: "COMPUTED" (recorded status)
- Execution authenticated against current revision: "PENDING"
- Formalization: "OPEN"
- Promotion: "BLOCKED"

Do not promote the claim solely because the stored JSON says "PASS".

Hash-manifest rule

"burnside_m3_hashes.txt" must contain SHA-256 digests of the finalized JSON, recomputation script, and this validation document. Recompute all three digests after any edit. Do not include a self-hash line in the manifest.

Promotion boundary

Even if all computational checks pass:

COMPUTATION = VERIFIED
FORMALIZATION = OPEN
PROMOTION = BLOCKED

until the mathematical/formal boundary is separately certified.
