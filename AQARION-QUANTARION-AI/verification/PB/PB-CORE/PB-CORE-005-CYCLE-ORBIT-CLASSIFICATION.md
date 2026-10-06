# PB-CORE-005 — Cycle-Orbit Classification of Pullback-Fixed Equivalences

## Status

Evidence:
- [P] finite pullback rigidity
- [P] eventual permutation-core restriction/extension
- [P] cycle-orbit classification
- [P] local phase-count formula
- [V] brute-force permutation checks through n = 6
- [V] formula-level permutation checks through n = 7
- [V] all finite maps through n = 6 for restriction/extension
- [V] all maps through n = 7 for aggregate stable-equivalence count

Lean:
- local setoid layer exists
- phaseRel_invariant remains the current local proof gate
- full classification theorem remains OPEN

Publication:
- BLOCKED pending independent formalization and literature-normalized presentation

Promotion:
- FALSE until formal proof and repository replay are complete

---

## 1. Finite pullback rigidity

Let X be finite, T : X -> X, and E an equivalence relation.

Define

    T*E = {(x,y) : T(x) E T(y)}.

If

    T*E ⊆ E,

then

    T*E = E.

### Proof

Let π : X -> X/E be the quotient map.

Then

    E = ker π

and

    T*E = ker (π ∘ T).

The inclusion

    ker(π ∘ T) ⊆ ker π

means that the quotient induced by π ∘ T is at least as fine as X/E.

Therefore

    |X/(T*E)| >= |X/E|.

But

    |X/(T*E)| = |im(π ∘ T)| <= |X/E|.

Because X is finite, equality holds throughout. Two equivalence
relations on a finite set cannot be a proper refinement while having
the same number of equivalence classes.

Hence

    T*E = E.

The finiteness assumption is essential.

---

## 2. Infinite counterexample

Let

    X = N
    T(n) = n + 1.

Let E have classes

    {0,1}, {2}, {3}, {4}, ...

Then

    T*E = Δ

while

    Δ ⊊ E.

Thus finite pullback rigidity does not extend to arbitrary infinite sets.

---

## 3. Eventual permutation core

Let

    P = Per(T)

be the set of periodic points.

For finite X, there exists h such that

    T^h(X) = P.

The restriction

    σ = T|P

is a permutation.

Define Stab(T) by

    Stab(T) = { E : E is an equivalence relation and T*E = E }.

For F in Con(P,σ), define

    Ext_h(F)

by

    x Ext_h(F) y
      iff
    T^h(x) F T^h(y).

Because σ is a permutation and F is σ-invariant,

    Ext_h(F)

is independent of the sufficiently large choice of h.

Restriction gives

    Res(E) = E|P.

Then

    Res : Stab(T) -> Con(P,σ)

and

    Ext : Con(P,σ) -> Stab(T)

are mutually inverse.

Therefore

    Stab(T) ≅ Con(P,σ).

This is the PB-CORE-004 eventual-permutation-core theorem.

---

# 4. Cycle decomposition

Write

    P = C_1 ⊔ ... ⊔ C_r

where σ acts as a cycle of length

    m_1,...,m_r.

An invariant equivalence relation θ partitions the set of cycles into
connected groups.

Fix one such group S of k cycles.

Suppose all cycles in S are linked by θ.

---

# 5. Local divisor classification

On one cycle C_m, every σ-invariant equivalence relation is determined
by a divisor

    d | m.

Its classes are residue classes modulo d.

Equivalently,

    x ~ y  iff  x ≡ y (mod d)

after choosing a cyclic coordinate.

This is classical monounary-algebra structure.

---

# 6. Cross-cycle compatibility

Suppose cycles C_i and C_j are θ-linked.

Their internal divisors must agree.

Therefore there exists

    d | gcd(m_i,m_j)

and, after cyclic coordinates are chosen, a phase offset relating
the two cycles.

For a connected collection S of cycles, a common divisor

    d | gcd(m_i : i in S)

is therefore necessary.

---

# 7. Phase representation

Let

    φ : S -> Z/dZ.

Define

    E_φ

by

    (i,x) E_φ (j,y)
    iff
    x + φ(i) ≡ y + φ(j) (mod d).

Because d divides every cycle length in S, σ preserves this relation.

Conversely every connected invariant equivalence relation on S has this
form.

---

# 8. Phase nonuniqueness

Two phase vectors φ and ψ determine the same equivalence relation iff

    exists t in Z/dZ
    such that
    ψ(i) = φ(i) + t

for every i in S.

Thus there is one redundant global phase.

Normalize one reference cycle by

    φ(i_0) = 0.

Then exactly

    d^(k-1)

distinct connected invariant equivalences occur for the divisor d.

---

# 9. Connected-component weight

For a nonempty set S of k cycles define

    g(S) = gcd(m_i : i in S).

The number of connected invariant equivalences on S is therefore

    W(S)
      =
    sum_{d | g(S)} d^(k-1).

---

# 10. Global classification

An arbitrary invariant equivalence relation first chooses a partition

    S_1 | ... | S_t

of the cycle-index set.

Each block S_j independently receives one connected invariant
equivalence.

Therefore

    |Con(P,σ)|
      =
    sum_{𝒮 ∈ Part({1,...,r})}
      product_{S ∈ 𝒮}
        sum_{d | gcd(m_i:i∈S)}
          d^(|S|-1).

This is the PB-CORE-005 cycle-orbit formula.

---

# 11. Important examples

## One cycle

For cycle length m,

    |Con(C_m,σ)| = τ(m).

## Two cycles

For lengths m,n,

    |Con(C_m ⊔ C_n,σ)|
      =
    τ(m)τ(n)
    +
    sum_{d | gcd(m,n)} d.

Examples:

    (2,2) -> 7
    (2,3) -> 5
    (3,3) -> 8
    (2,4) -> 9
    (4,4) -> 16

The value for (2,4) is 9, not 7.

## Three fixed points

For

    (1,1,1),

the formula gives

    5,

the Bell number B_3.

---

# 12. Critical scope distinction

The phase relation describes ONE connected group of cycles.

It does NOT itself describe arbitrary global congruences.

The global object is:

    set partition of cycles
        +
    one divisor per block
        +
    normalized phase data per block.

This distinction must remain explicit in the formalization.

---

# 13. AQARION claim boundary

The following should NOT be claimed:

    "AQARION discovered congruences of unary algebras."

That is false.

The cycle/divisor/gcd structure belongs to established monounary
algebra and G-set congruence theory.

The defensible AQARION result is the exact pullback formulation and
the finite dynamical decomposition:

    finite T
      -> pullback-fixed equivalences
      -> eventual permutation core
      -> explicit cycle-orbit phase classification
      -> exact executable census
      -> reproducible evidence ledger.

---

# 14. Current theorem ladder

PB-CORE-004:

    Stab(T) ≅ Con(Per(T), T|Per(T))       [P]

PB-CORE-005:

    explicit cycle-orbit classification     [P]

PB-CORE-005 computational verification:

    permutations n <= 6 brute force         [V]
    formula checks n <= 7                   [V]

Full finite-map verification:

    n <= 6 all maps                         [V]
    n = 7 aggregate census                  [V]

Lean:

    local phase-setoid layer                [V]
    phaseRel_invariant                      OPEN
    global assembly                         OPEN
    full theorem                            OPEN
