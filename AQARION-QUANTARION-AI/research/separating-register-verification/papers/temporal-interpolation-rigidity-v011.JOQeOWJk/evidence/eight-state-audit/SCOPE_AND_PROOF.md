# Scope and elementary m=3 proof

The program reruns all 8^8 maps for fixed h=00001111.
Its C sieve uses F2; every deficient candidate receives exact Q rank.
Canonical Fraction elimination is a separate rank cross-check,
not SymPy. Generated-set equality and parity certificates are checked.

## Case B

Let R(n,3)=6*c(n,3)/(n!*p_3(n)).
Here c counts permutations with three cycles and p_3 counts
partitions into exactly three positive parts.

R(3,3)=1 and R(4,3)=3/2.

Direct exact checks give:
R(5..8,3)=7/8, 5/8, 29/60, 469/1200.

For n>=9, take the seven partitions of 9 into three parts:
(1,1,7), (1,2,6), (1,3,5), (1,4,4),
(2,2,5), (2,3,4), (3,3,3).

Adding n-9 to the largest part gives seven distinct partitions of n.
Thus p_3(n)>=7.

Since 0<c(n,3)<=n!, we have 0<R(n,3)<=6/7<1.

Consequently R(n,3) is integral exactly for n=3, among n>=3.
This written all-n proof is not machine formalized.

Finite ratio checks, a corrected Kummer helper, and the harmonic
Stirling identity are tested separately. No false harmonic/binomial
identity is used. This ratio lane is separate from the dynamics paper.

## Trade-matrix example

The program checks the explicit four-by-six matrices and 49 coefficient
pairs. It does not prove a general intersection-matrix rank theorem.

## Boundaries

No arbitrary-dimension dynamics theorem, novelty, publication,
or claim promotion is certified.

Application sources are not modified. No Git operation is performed.
