#AQARION — Repository Overview

Date: October 14, 2026  
Repository: github.com/quantarion369-arch/AQARION  
Branch: main — clean, synced with origin/main  
HEAD: e941e5a (ledger update) → 1dfd095 (equality replay)

---

## Executive status

| Lane | Status | Evidence label |
|---|---|---|
| Closure-cost equality — proof | Paper-level complete | Not machine-checked |
| Closure-cost equality — replay | Local semantic replay, seeds 0 & 1 | Not hash-verified |
| Stability-notions clarification | Accepted | Framework correction + randomized corroboration |
| Join/meet closure of forward-stable partitions | Accepted | Proof + 18,737 non-bijective n=6 checks |
| Kaprekar forward vs pullback distinction | Accepted case verification | Not a general theorem |
| Dependency provenance (`prof.py`) | Qualified | Reconstruction, not original artifact |
| Lean formalization | Deferred | Separate gate |
| Publication / C4 | Blocked | By policy |

---

## What tonight produced

```text
    Claude handoff
         |
         v
    Local replay attempt
         |
         +--> missing files discovered
         |
         v
    Files created locally
         |
         +--> equality_check.py   (corrected checker)
         +--> prof.py             (compatible reconstruction)
         |
         v
    First run: 3,413 cases
         |
         +--> rgs() bug found
         |
         v
    rgs() patched
         |
         v
    Bell-number sanity check
         |
         +--> 1, 2, 5, 15, 52  ✓
         |
         v
    Full exhaustive sweep
         |
         +--> 166,484 cases
         |
         v
    Seed 0 output == reported output
         |
         v
    Seed 1 output == reported output
         |
         v
    REPLAY.md + outputs + checker + reconstruction
         |
         v
    commit 1dfd095  --> pushed
         |
         v
    EVIDENCE-LEDGER.md updated
         |
         v
    commit e941e5a  --> pushed
         |
         v
    DURABLE STATE
```

---

## Closure-cost equality — formal statement

For a finite deterministic system \(T:X\to X\), a partition \(\pi\) with \(k\)
blocks, the Koopman operator \(K\), and the block projector \(P\):

\[
W_j=\operatorname{span}\{e_b\circ T^i:b<k,\ i\le j\}
\]

\[
\delta_j=\dim W_j-\dim W_{j-1}
\]

Let \(s\) be the number of itinerary classes. Let the positive profile be
\(\delta_1,\ldots,\delta_{d-1}\), with \(\delta_d=0\).

### Upper bound

\[
s-k\le k\left(\prod_{j=1}^{d-1}(1+\delta_j)-1\right)
\]

### Equality criterion

Equality holds if and only if the length-\(d\) itinerary-prefix set is a full
Cartesian product

\[
A_0\times A_1\times\cdots\times A_{d-1}
\]

with \(|A_0|=k\) and \(|A_j|=1+\delta_j\).

### Structural consequence

When equality holds, the letter sets are nested:

\[
A_0\supseteq A_1\supseteq\cdots\supseteq A_{d-1}
\]

and the next letter is determined by one common coordinate through a feedback
map.

---

## Replay evidence

```text
SEED 0                                     SEED 1
───────────────────────────────            ───────────────────────────────
exhaustive n<=5      166,484               exhaustive n<=5      166,484
attained              43,488               attained              43,488
nonempty profile       2,352               nonempty profile       2,352
empty profile         41,136               empty profile         41,136
random n=8,9          34,017               random n=8,9          34,078
random attained        1,531               random attained        1,497
constructions        300/300               constructions        300/300
empty constructions 2000/2000              empty constructions 2000/2000
result              PASSED                 result              PASSED
```

Both seed outputs matched the reported stdout line for line.

---

## Dependency boundary

```text
    Reported dependency
        prof.py
        sha256 829be3fc64d139a9...
              |
              |   NOT RECOVERED
              v
    Local compatible reconstruction
        prof.py
        profile / stable_size / corrected rgs
              |
              v
    Same checker results on both seeds
              |
              v
    SEMANTIC REPLAY
    not hash-verified byte-for-byte replay
```

The reconstruction implements the same API and conventions, uses exact
`Fraction` arithmetic, and produces identical outputs across every checked
category. It is not the original reported file.

---

## Stability-notions clarification

A separate framework correction. Not part of the equality theorem.

```text
    D = (I - P) K P = 0
              |
              v
    block-constant functions stay block-constant
              |
              v
        FORWARD STABILITY
              |
              x
              |
              v
        [K, P] = 0     NOT implied
```

\(D=0\) certifies one-directional compatibility. It does not imply \(KP=PK\).

```text
    FORWARD-STABLE PARTITIONS
        |
        +--> closed under join
        +--> closed under meet
        +--> many can exist for non-invertible T

    PULLBACK-STABLE PARTITIONS
        |
        +--> T(x) = T(y)  ==>  x ~ y
        +--> injectivity-like condition
        +--> often only trivial for dissipative maps
```

For Kaprekar, many forward-stable partitions coexist with only the trivial
pullback-stable partition. That is the expected signature of a non-invertible
map — not a contradiction.

---

## Repository structure

```text
AQARION/
├── EVIDENCE-LEDGER.md
│     ├── Closure-cost equality extension — local replay complete
│     └── Stability-notions clarification — accepted
│
├── research/closure-cost/
│     ├── THEOREM.md
│     ├── AUDIT.md
│     ├── check_actual_source.py
│     └── actual-source-n4.txt
│
└── extensions/closure-cost-equality/
      ├── OVERVIEW.md
      ├── local-dependency/
      │     ├── prof.py
      │     └── prof.sha256
      └── replay/
            ├── REPLAY.md
            ├── equality_check.py
            ├── prof.py
            ├── local_eq0_reconstructed.txt
            └── local_eq1_reconstructed.txt
```

`prof.py` means **profile**, not proof. It provides the profile, stable-size,
and partition-generation functions used by the checker.

---

## Lane separation

```text
┌─────────────────────────────┬─────────────────────────────┐
│  CLOSURE-COST EQUALITY      │  STABILITY CLARIFICATION    │
│  ─────────────────────────  │  ─────────────────────────  │
│  Paper proof: complete      │  Forward ≠ commutation      │
│  Local replay: complete     │  Join/meet closure: held    │
│  Lean: deferred             │  Kaprekar: case verified    │
│  Lane: FROZEN               │  Lane: framework correction │
└─────────────────────────────┴─────────────────────────────┘
                     │
                     │  do not merge
                     v
       Two distinct evidence records
       Two distinct status lines
       Two distinct future gates
```

---

## What is not claimed

- No Lean formalization.
- No novelty claim.
- No publication readiness.
- No claim that the sampled checks are exhaustive.
- No claim that the stability clarification is a new all-systems theorem.
- No claim that reconstructed `prof.py` is the original reported artifact.
- No claim that a hash-verified byte-for-byte replay occurred.

---

## Position

AQARION holds a completed, pushed, honestly labeled local semantic replay of
the all-\(k\) closure-cost equality checker, together with a corrected
stability framework — without overclaiming formal certification, dependency
identity, novelty, or publication readiness.
```

Save and push:

```bash
cd ~/AQARION/extensions/closure-cost-equality
nano OVERVIEW.md
# paste the document, then Ctrl+O, Enter, Ctrl+X

cd ~/AQARION
git add extensions/closure-cost-equality/OVERVIEW.md
git commit -m "Add polished repository overview for closure-cost equality extension"
git push
