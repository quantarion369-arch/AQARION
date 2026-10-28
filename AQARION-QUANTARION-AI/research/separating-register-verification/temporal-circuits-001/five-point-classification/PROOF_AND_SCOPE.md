# Temporal affine circuits: scope and proof

## Conventions

Coefficients are rational.
Time coordinate zero is the least significant bit.
Words are distinct and states are labelled by their words.
Transitions may have loops.
A circuit means minimal affine dependence: rows (1,y) are dependent,
and every proper subset is independent.

This note does not classify all temporal circuits or assert novelty.

## General overlap counts

For each length-(L-1) context u, let a_u count words ending in u
and b_u count words beginning in u.

All words ending in u can transition to all words beginning in u.
The bipartite matching graph splits into independent complete blocks.

Permutation realizations exist iff a_u=b_u for every u.
Their number is product(a_u!).
Arbitrary deterministic realizations number product(b_u^a_u : a_u>0).

These counts do not require a permanent algorithm.
They count finite-history realizations, not persistent dependencies.

## The five-point, four-bit classification

Claim:
Among five-point affine circuits in {0,1}^4, exactly the supports
{0,2,4,9,15} and {0,6,11,13,15} are deterministically realizable.
Each realization is unique and is a permutation with two fixed points
and one three-cycle.

Proof:
Realize a support as five states with binary observation h.
The affine circuit has rank four, so dim W_4=4, where
W_L=span_Q(1,h,...,h composed with T^(L-1)).

A pause W_(k+1)=W_k makes W_k invariant under composition with T.
Consequently the span cannot pause and later grow.
It follows that W_3=W_4=W_infinity has dimension four.

The first-three-observation map is injective: agreement there forces
agreement on all of W_infinity and hence on the given four-bit histories.
Its image is a five-point affine circuit C in the three-cube.

Such a C contains an antipodal pair, by pigeonhole among the four pairs.
It cannot contain two antipodal pairs, because their four points are
already dependent.

Flip coordinates to send the sole pair to 000 and 111.
The other three points choose one from each pair {e_i,1-e_i}.
A mixed choice contains a dependent parallelogram:
two one-hot choices and the remaining one-cold choice give one;
the complementary case gives another.
Only all three one-hot or all three one-cold choices remain.

Thus C is a coordinate-flip image of {0,1,2,4,7}.
Its primitive relation has coefficient pattern 2,1,-1,-1,-1.

Let w be that full-support relation. Invariance of W_infinity implies
T_*w=lambda*w, where (T_*w)(z)=sum(w(x):T(x)=z).

If T is not surjective, a missing image coordinate forces lambda=0.
Every nonempty fiber must then have weight sum zero and contain at
least two states. A fiber cannot contain three states: two would have
the same binary observation and the same successor, contradicting
observability. All fibers would therefore have size two, impossible
for five states. Hence T is a permutation.

A permutation preserves the multiset of relation coefficients.
Thus lambda is 1 or -1. The unequal positive/negative support sizes
exclude -1. The uniquely weighted coefficient-two and coefficient-one
states are fixed.

A fixed state's three-prefix is constant. The distinguished antipodal
pair must therefore be 000 and 111. The prefix circuit is consequently
{0,1,2,4,7} or its global complement.

The remaining overlap constraints force a three-cycle.
Appending its next output gives precisely the two four-bit supports
listed in the claim. Direct edge inspection proves their uniqueness.
End proof.

The finite enumeration in this package independently checks all
binomial(16,5)=4368 supports without symmetry pruning.

## Persistence is not finite realizability

The three-bit circuit {0,1,2,4,7} has two permutation realizations.
One extends to {0,2,4,9,15} with linear rank four.
The other extends to {1,2,4,8,15} with linear rank five.

The same separating finite support can therefore have different
eventual interpolation degrees under different transitions.

## Coefficient interpretation

For Y_m={0,1^m,e_0,...,e_(m-1)}, the primitive obstruction is
(m-1,1,-1,...,-1).

Its coefficient growth is not unavoidable decoder growth.
The zero-state indicator can be written
1-sum(g_i)+sum(g_0*g_i : i=1,...,m-1),
using only coefficients 0,1,-1.

## Boundaries

No general proof is machine-formalized here.
Finite exact checks are not originality clearance.
Static cube symmetries need not preserve temporal overlap.
No existing manuscript, application, or repository source is modified.
