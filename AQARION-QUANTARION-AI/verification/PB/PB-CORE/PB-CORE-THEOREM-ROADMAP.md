# PB-CORE Theorem Roadmap

## T0 — Finite Pullback Rigidity

Statement:

    T*E ⊆ E -> T*E = E

for finite X.

Status:

    [P]

---

## T1 — Eventual Permutation Core

Statement:

    Stab(T) ≅ Con(Per(T), T|Per(T)).

Status:

    [P]

Lean:

    OPEN

---

## T2 — Single-Cycle Congruence

For an m-cycle:

    Con(C_m) ≅ {d : d | m}.

Status:

    [P]

Literature:

    classical

---

## T3 — Connected Multi-Cycle Classification

For cycle lengths m_i in a connected congruence block S:

    choose d | gcd(m_i)

and

    d^(|S|-1)

normalized phase choices.

Status:

    [P]

Lean:

    OPEN

---

## T4 — Global Cycle Formula

    |Con(P,σ)|
      =
    sum over cycle-index partitions
    of products of connected weights.

Status:

    [P]

Lean:

    OPEN

---

## T5 — Permutation Aggregate

    Σ_{σ∈S_n}|Con(σ)| = n! p(n).

Status:

    [P]

Proof:

    count pairs (σ,E) by E-block-size profile.

---

## T6 — Finite-Map Aggregate

    A_n
      =
    n!
    Σ_{k=1}^n
      k p(k)n^(n-k-1)/(n-k)!.

Status:

    [P]

Proof ingredients:

    T1
    T5
    Cayley rooted-forest enumeration.

---

## T7 — Exhaustive Verification

All maps:

    n <= 7

Status:

    [V]

Exact n=7 map count:

    823543

Exact stable-pair total:

    3018127

---

## T8 — Lean Formalization

Target:

    formal proofs T0-T6.

Status:

    OPEN

No claim of formal certification until build and sorry-count
requirements are independently satisfied.
