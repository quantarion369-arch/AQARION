# PB-CORE-005 — Execution Report and Adversarial Audit

**Program:** AQARION / PB-CORE  
**Claim:** Cycle-Orbit Classification of Pullback-Fixed Equivalences  
**Execution status:** INDEPENDENTLY EXECUTED  
**Formalization status:** OPEN  
**Repository CI status:** NOT CLAIMED VERIFIED ON CURRENT HEAD

---

# 1. What was actually tested

The computational investigation was divided into independent tests.

## Test A — permutation formula

For every permutation of

\[
n=1,\ldots,6,
\]

the computation:

1. enumerated every set partition of the domain;
2. tested whether the partition was invariant under the permutation;
3. counted the invariant equivalences;
4. decomposed the permutation into cycles;
5. evaluated the closed PB-CORE-005 formula;
6. compared the two counts.

Result:

```text
n = 1: zero mismatches
n = 2: zero mismatches
n = 3: zero mismatches
n = 4: zero mismatches
n = 5: zero mismatches
n = 6: zero mismatches
