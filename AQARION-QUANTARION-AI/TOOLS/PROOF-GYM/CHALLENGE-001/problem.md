# ProofGym Challenge 001
## The Direction You Were Not Given

Let `X` be finite and let `T : X → X`.

Let `E` and `F` be equivalence relations on `X` satisfying

    T(x) E T(y) → x E y

and

    T(x) F T(y) → x F y.

Prove that

    T(x) (E ∨ F) T(y) → x (E ∨ F) y.

### Rules

You may use:

- finiteness of `X`;
- basic facts about equivalence relations;
- finite cardinality arguments.

You may NOT assume:

- `T` is surjective;
- `T` is injective;
- forward preservation of `E` or `F`;
- the conclusion for `E ∨ F`.

### Your tasks

1. Find the tempting but invalid proof step.
2. Prove finite pullback rigidity.
3. Construct the induced permutations on `X/E` and `X/F`.
4. Define the incidence relation.
5. Explain why forward incidence preservation becomes equality.
6. Deduce preservation of connected components.
7. Explain why the infinite case cannot be obtained by deleting
   the finite hypothesis.

### Evidence target

A successful informal solution is `[P-candidate]`.

A mechanically checked Lean proof is required for `[P]`.

A finite exhaustive replay is `[V]`.

No amount of bounded computation alone promotes the theorem to `[P]`.
