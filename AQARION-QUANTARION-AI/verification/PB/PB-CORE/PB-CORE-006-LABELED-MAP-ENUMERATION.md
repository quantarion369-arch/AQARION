
# PB-CORE-006 — Exact Enumeration of Pullback-Fixed Equivalences

## 1. Definition

For n >= 1, let

    A_n = sum_{T : [n] -> [n]} |Stab(T)|,

where [n] = {1,...,n} and

    Stab(T) = {E : E is an equivalence relation on [n]
                  and T*E = E}.

Equivalently, A_n counts pairs (T,E) such that T is a labeled
self-map of [n], E is an equivalence relation, and

    x E y  iff  T(x) E T(y).

## 2. Permutation aggregate

Let S_k denote the aggregate number of invariant equivalences over
all permutations of a labeled k-element set:

    S_k = sum_{σ in Sym(k)} |Con([k],σ).

Let p(k) be the number of integer partitions of k.

The exact identity is

    S_k = k! p(k).

## 3. Proof of the permutation identity

Count pairs (σ,E), where σ is a permutation and E is an equivalence
relation preserved by σ, by first fixing E.

Suppose the block-size profile of E has m_s blocks of size s.
Then

    sum_{s >= 1} s m_s = k.

The number of set partitions with this profile is

    k! / product_{s >= 1} ((s!)^(m_s) m_s!).

For a fixed E, a preserving permutation may permute the m_s blocks
of each size s and choose a bijection on each block. Therefore the
number of preserving permutations is

    product_{s >= 1} ((s!)^(m_s) m_s!).

Multiplying the two quantities gives exactly k! for every block-size
profile.

The possible block-size profiles are precisely the integer
partitions of k. There are p(k) such profiles. Hence

    S_k = k! p(k).

This is an exact counting proof, not a fit to a computed sequence.

## 4. Functional-graph decomposition

Every self-map of a finite set has a functional graph consisting of
directed cycles and directed trees feeding into those cycles.

Let the periodic core have size k. The restriction of the map to
that core is a permutation of the k core vertices. Every remaining
vertex belongs to a rooted tree feeding into exactly one core vertex.

For a fixed set of k labeled roots in an n-element labeled set, the
number of rooted forests in which each component contains exactly
one of those roots is

    F(n,k) = k n^(n-k-1),   1 <= k < n,

and

    F(n,n) = 1.

The endpoint k=n is a separate case: there are no transient vertices,
so the unique forest is the empty forest.

## 5. Counting maps by core size

Fix 1 <= k <= n.

Choose the core vertices in

    binomial(n,k)

ways.

Choose the permutation on those vertices. Summing the number of
invariant equivalences over all possible core permutations gives

    S_k = k! p(k).

For k<n, attach the remaining vertices as a rooted forest in

    k n^(n-k-1)

ways.

Thus the total contribution from maps with core size k<n is

    binomial(n,k) * k n^(n-k-1) * k! p(k).

For k=n, there are no transient vertices, so the contribution is

    n! p(n).

Therefore the boundary-safe exact formula is

    A_n =
      sum_{k=1}^{n-1}
        binomial(n,k) k n^(n-k-1) k! p(k)
      + n! p(n).

Using

    binomial(n,k) k! = n!/(n-k)!,

we obtain the equivalent form

    A_n =
      n! * sum_{k=1}^{n-1}
        k p(k) n^(n-k-1)/(n-k)!
      + n! p(n).

This is the canonical formula for this artifact.

The sum stops at n-1. The all-core contribution n! p(n) is added
separately. No negative exponent or 0^(-1) convention is needed.

## 6. Exact values

The formula gives:

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

These values are exact integer values of the formula.

## 7. Boundary checks

### n = 1

The only map on a one-element set is the identity, and there is
exactly one equivalence relation. Thus

    A_1 = 1! p(1) = 1.

The summation from k=1 to n-1 is empty, so the formula returns the
correct value without evaluating a negative exponent.

### n = 2

Here p(1)=1 and p(2)=2. The k=1 contribution is

    binomial(2,1) * 1 * 2^(0) * 1! p(1) = 2.

The k=2 contribution is

    2! p(2) = 4.

Therefore

    A_2 = 2 + 4 = 6.

This is a mandatory regression test for any implementation of the
formula.

### General endpoint

At k=n, the forest count is 1, not an expression involving
n^(n-k-1). The endpoint contribution is exactly

    n! p(n).

## 8. Computational evidence

The repository receipt records the following direct finite-map
aggregates:

    n = 1     1
    n = 2     6
    n = 3     51
    n = 4     592
    n = 5     8565
    n = 6     148896
    n = 7     3018127

It records an exhaustive n=7 census of

    7^7 = 823543

maps, with aggregate stable-equivalence count 3018127.

These are repository-recorded results. They should not be described
as a fresh execution unless the current source revision is run and
its output is captured.

The formula has a mathematical derivation through the permutation
aggregate and rooted-forest decomposition. Independent direct
enumeration provides [V] evidence for the tested finite sizes; it
does not replace the proof.

## 9. Evidence status

Permutation aggregate S_k = k! p(k):
    [P] by block-size-profile counting.

Rooted-forest factor:
    [P] by the rooted-forest form of Cayley's formula.

Aggregate formula A_n:
    [P] provided the stated decomposition and standard forest-count
    theorem are accepted or independently established in the proof
    chain.

Exact values from the formula:
    [V] when evaluated by exact integer arithmetic.

Direct map enumeration through n=7:
    [V] as recorded by the repository; reproduce before claiming a
    new run.

Lean formalization of the complete enumeration theorem:
    OPEN unless a corresponding complete proof and successful build
    are recorded.

Publication:
    BLOCKED pending formalization, independent reproduction, and
    literature review.

No novelty claim is made from the sequence of values alone.
