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
