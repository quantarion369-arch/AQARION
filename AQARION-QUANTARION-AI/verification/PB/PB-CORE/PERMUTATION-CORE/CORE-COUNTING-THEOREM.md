# Permutation-Core Aggregate

## Statement

Let X be a set of k elements. Let S_k count pairs (sigma, Pi),
where sigma is a permutation of X and Pi is a set partition of X
preserved by sigma.

Preserved means:
x and y are in the same Pi block if and only if sigma(x) and sigma(y)
are in the same Pi block.

Let p(k) be the ordinary integer-partition number, with p(0)=1.

Then:

    S_k = k! * p(k).

## Proof by relabeling orbits

The symmetric group G acts on the set P of set partitions by relabeling.
For sigma in G, a fixed point of this action is exactly a partition
preserved by sigma. Thus S_k is the sum of the fixed-point counts.

The fixed-point/orbit identity gives:

    S_k = |G| * |P/G|.

Two set partitions lie in the same orbit exactly when their multisets
of block sizes agree. Necessity follows because permutations preserve
block cardinalities. For sufficiency, match equal-sized blocks and
choose a bijection between each matched pair. Their disjoint union
is a permutation carrying one partition to the other.

These block-size multisets are exactly the integer partitions of k.
Every integer partition is realized by dividing X into blocks of
its specified sizes. Consequently |P/G|=p(k), and |G|=k!.
This proves the identity.

For k=0 there is one permutation, one empty set partition, and one
integer partition, so the identity gives 1=1.

The fixed-point/orbit identity is the classical Cauchy-Frobenius
or Burnside counting lemma. No novelty claim is made.

## Additional formulas checked by the verifier

For a block-size type with a_s blocks of size s, the stabilizer size is:

    product over s of (s!)^a_s * a_s!

A preserving permutation may permute the a_s equal-sized blocks and
independently choose a bijection on each matched pair of size-s blocks.
These choices account for all and only the preserving permutations.

By orbit-stabilizer, the number of set partitions of this type is k!
divided by that stabilizer size.

## Computational evidence

The accompanying verifier directly enumerates every permutation and
set partition for k=0..6, including the empty case.

Pairs examined: 152796.
Invariant-pair totals: 1, 1, 4, 18, 120, 840, 7920.

It separately checks partition enumeration counts, stabilizer sizes,
block-type cardinalities, integer-partition counts, and the aggregate.
Positive and negative invariance controls are included.

The Termux receipt identifies the full verifier-source SHA-256 and
execution environment. It is actual finite execution evidence.

## Boundaries

This is a mathematical argument and finite computational replay.
It is not an execution or certification of the existing Lean project.
It does not audit historical Lean revisions.
It does not verify the larger endofunction aggregate.
It does not authorize registry promotion or a novelty claim.
