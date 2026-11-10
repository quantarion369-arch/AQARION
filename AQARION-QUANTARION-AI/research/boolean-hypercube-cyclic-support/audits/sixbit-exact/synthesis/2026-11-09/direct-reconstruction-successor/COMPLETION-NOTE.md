# Six-bit census: direct reconstruction successor

## Disposition

All six odd-eight base-local support lists have been reproduced by
direct full-feature-matrix enumeration. The checker does not execute
the historical quotient/projective-class generator or Gram filter.

The six rank-eight direction orbits were separately reconstructed and
shown to partition all 1045 eligible directions among all 1395
three-dimensional binary subspaces.

The odd-twelve families were reconstructed through all 126 affine
hyperplanes. Both historical canonical support-set digests matched.

## Counts

Base-local accepted supports: 0, 8, 56, 24, 48, 24.
Extensions examined across the six bases: 2203740.
Affine-flat weights: 240, 280, 1120, 1680, 2520, 2520.
Weighted odd-eight count: 286720.

Odd-twelve pattern counts:
- 1^12: 206304
- 1^10 3^2: 4032

Combined sector arithmetic: 497056.

## Coverage argument

A primitive rational circuit has a nonempty odd-coefficient support.
The parity equations identify this support with an RM(3,6) codeword.
The classical minimum-weight and low-weight classification restricts
its cardinality, within twelve points, to eight or twelve.

At weight eight, the odd support is an affine three-flat. Its eight
feature columns must be independent, since a dependency on that
proper subset would contradict circuit minimality. Rank-seven flats
are therefore excluded. Feature-preserving root swaps and translations,
together with the checked direction coverage, reduce to the six bases.
Every four-point extension of every base was directly examined.
Each circuit has a unique odd flat, so weighting does not double-count.

At weight twelve, the classical normal forms give affine dimension five
and hence a unique hyperplane. A suitable coordinate deletion is
bijective on this hyperplane. The exhaustive five-bit candidate ranks
are eleven or twelve; only rank eleven can project from a six-bit
rank-eleven circuit. Direct lifting tests all such candidates in all
126 hyperplanes. Projection and a full-support exact kernel certify
each accepted lifted circuit.

The sectors are disjoint because odd-support cardinality is determined
by the primitive kernel, which is unique up to sign.

## Literature locator

Ghorbani, Kamali, Khosrovshahi, Krotov:
On the Volumes and Affine Types of Trades, EJC 27(1), P1.29 (2020).
arXiv:1810.02296v2, Lemmas 2, 3, 11 and 12.
The low-weight normal-form locator is journal Lemma 13 versus
arXiv HTML Lemma 11. Preserve version-specific numbering.

## Limitations

This is a human-readable synthesis of computational lemmas and classical
theorems, not a machine-checked proof or novelty certification.
Individual execution reports retain their original narrower scope.
No historical report or source is modified.
This index references local validation artifacts; it does not by itself
make the complete reproduction dependency closure publicly available.
No staging, commit, push, PR, or promotion is authorized by this note.
