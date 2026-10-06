# PB-CORE-006 — Exact Enumeration of Pullback-Fixed Equivalences

## 1. Definition

Let

    A_n
      =
    sum over all maps T : [n] -> [n]
      of
    |Stab(T)|.

Thus A_n counts pairs

    (T,E)

with

    T : [n] -> [n]
    E an equivalence relation
    T*E = E.

---

# 2. Permutation case

Let S_k be the total number of invariant equivalences over all
permutations of a k-element labeled set:

    S_k
      =
    sum_{σ ∈ Sym(k)}
      |Con([k],σ)|.

We obtain the exact identity

    S_k = k! p(k),

where p(k) is the number of integer partitions of k.

---

# 3. Proof of the permutation identity

Count pairs

    (σ,E)

directly by E rather than by σ.

Fix an equivalence relation E whose block sizes have multiplicities

    m_1, m_2, ...

where m_s is the number of E-blocks of size s.

The number of set partitions with this block-size profile is

    k!
    /
    product_s ((s!)^(m_s) m_s!).

For this fixed E, σ preserves E exactly when σ permutes blocks of
equal size and chooses a bijection between blocks.

Therefore the number of preserving permutations is

    product_s ( (s!)^(m_s) m_s! ).

Multiplying:

    k!

for every block-size profile.

The possible block-size profiles are precisely the integer partitions
of k.

Hence

    S_k = k! p(k).

This is an exact proof, not an empirical sequence fit.

---

# 4. Functional-graph decomposition

Every finite map T decomposes into:

    periodic core
        +
    rooted directed trees feeding into the core.

Let the periodic core have size k.

The restriction of T to the core is a permutation σ of k elements.

The remaining n-k vertices form a rooted forest whose roots are the
k core vertices.

For a fixed set of k labeled roots, the number of such forests is

    k n^(n-k-1)

for k < n,

with the value 1 when k=n.

This is the rooted-forest form of Cayley's formula.

---

# 5. Number of maps with a specified core permutation

Choose the k core vertices:

    binomial(n,k).

Choose the permutation of those k vertices:

    k!.

Attach the remaining vertices as a rooted forest:

    k n^(n-k-1).

Thus the contribution from all maps whose core has size k is

    binomial(n,k)
    k n^(n-k-1)
    S_k.

Substitute

    S_k = k! p(k).

We obtain

    A_n
      =
    sum_{k=1}^n
      binomial(n,k)
      k n^(n-k-1)
      k! p(k).

Simplifying:

    A_n
      =
    n!
    sum_{k=1}^n
      k p(k) n^(n-k-1)
      /
      (n-k)!.

Therefore

    ┌───────────────────────────────────────────┐
    │                                           │
    │  A_n = n! Σ_{k=1}^n                     │
    │        k p(k) n^(n-k-1)/(n-k)!            │
    │                                           │
    └───────────────────────────────────────────┘

is an exact enumeration formula.

---

# 6. Exact values

n = 1     A_n = 1
n = 2     A_n = 6
n = 3     A_n = 51
n = 4     A_n = 592
n = 5     A_n = 8565
n = 6     A_n = 148896
n = 7     A_n = 3018127
n = 8     A_n = 69844608
n = 9     A_n = 1816084233
n = 10    A_n = 52399129600
n = 11    A_n = 1660832066091
n = 12    A_n = 57351480413184

---

# 7. Independent exhaustive check

Direct enumeration of all maps was performed for:

    n = 1,...,7.

Number of maps at n=7:

    7^7 = 823543.

The exact direct count at n=7 is

    3018127,

matching the formula.

The previous counts

    1, 6, 51, 592, 8565, 148896

also match exactly.

---

# 8. Interpretation

A_n is not merely a sequence of "stable partitions".

It counts all finite deterministic systems together with a pullback-fixed
equivalence relation.

Equivalently:

    number of finite dynamical systems
    weighted by their pullback-fixed quotient structures.

The weighting factors through the eventual permutation core.

This is the strongest current computationally supported consequence
of PB-CORE-004/005.

---

# 9. Evidence status

The enumeration formula itself:

    [P]

The values obtained from the formula:

    [PV]

The direct n <= 7 enumeration:

    [V]

No OEIS or literature novelty claim is made from the sequence alone.

An absence of an indexed match is not evidence of mathematical novelty.
