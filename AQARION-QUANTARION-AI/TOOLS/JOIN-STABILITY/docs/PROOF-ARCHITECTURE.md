# JOIN-STABILITY Proof Architecture

## Target

Let X be finite and T : X -> X.

Let E and F be equivalence relations on X.

Assume:

    T^{-1}(E) <= E
    T^{-1}(F) <= F

Target:

    T^{-1}(E vee F) <= E vee F

## Stages

### JS-00 — Definitions

Define:

- finite set X
- deterministic map T
- equivalence relations
- pullback relation
- lattice join

### JS-01 — Quotient map

Associate a quotient map to a pullback-stable equivalence.

### JS-02 — Kernel refinement

Identify the kernel structure induced by the quotient.

### JS-03 — Finite kernel equality

Use finiteness explicitly.

This is a load-bearing step.

### JS-04 — Forward equivalence

Establish the required equivalence between E-related states and their T-images.

### JS-05 — Quotient permutation

Derive the finite quotient permutation structure.

### JS-06 — Second quotient

Apply the same structure to F.

### JS-07 — Join-chain characterization

Characterize E vee F by finite alternating chains.

### JS-08 — Chain lifting

Lift the join-chain structure through T.

### JS-11 — Theorem target

Conclude pullback stability of E vee F.

## Evidence boundary

A finite exhaustive computation can verify declared finite instances.

It cannot replace the mathematical proof of JS-11.

A formal Lean proof is a separate evidence lane.

The proof and computational verification must remain independently identifiable.
