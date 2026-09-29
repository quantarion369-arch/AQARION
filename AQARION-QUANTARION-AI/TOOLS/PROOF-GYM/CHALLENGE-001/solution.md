# JOIN-001 — Reference Solution

## Trap 1: Direction reversal

The hypothesis is

    T(x) E T(y) -> x E y.

A tempting proof silently uses

    x E y -> T(x) E T(y).

That implication is not available initially.

## Repair

For finite X:

    T*E ⊆ E
        ->
    T*E = E.

Thus the reverse inclusion follows:

    E ⊆ T*E.

Therefore

    x E y -> T(x) E T(y).

The same holds for F.

## Trap 2: "Forward incidence" is not automatically "graph automorphism"

The induced class maps are permutations.

Define

    I ⊆ (X/E) × (X/F)

by

    (A,B) ∈ I  iff  A ∩ B ≠ ∅.

If `(A,B) ∈ I`, choose `x ∈ A ∩ B`.

Then

    T(x) ∈ σ_E(A) ∩ σ_F(B),

so

    σ(I) ⊆ I.

But this alone would not be sufficient.

The product quotient is finite and σ is a permutation, so

    |σ(I)| = |I|.

Hence

    σ(I) = I.

Therefore the incidence graph is genuinely preserved in both
directions.

## Join

The connected components of the incidence graph correspond
exactly to the equivalence classes of `E ∨ F`.

Graph automorphisms preserve connected components.

Therefore

    T(x) (E ∨ F) T(y)
        ->
    x (E ∨ F) y.

Hence `E ∨ F` is pullback-stable.
