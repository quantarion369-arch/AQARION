# Spectral-to-register reduction: proof-review draft

## Status and dependency

This is a written mathematical derivation for independent review.
It is not a Lean proof, novelty clearance, or claim promotion.

External dependency:
Alexandr Valyuzhenich, Optimal functions with spectral constraints
in hypercubes, arXiv:2303.10995, Theorems 1 and 2.
The external theorem is not machine-proved by this package.

## Exact scope

Let d>=1, n=2^d, X a set of n states, T:X->X, and
h:X->{0,1}. Put a_t=h composed with T^t.

Assume length-n itineraries distinguish all states.
All polynomial ranks below are over Q.

Let H(n,j) be the rank of the evaluation matrix containing the
constant and every squarefree temporal monomial of degree <=j.

## Classification statement

H(n,d-1)<n if and only if the system, in its first-d-observation
coordinates, is a canonical shift register with a constant or
coordinate-literal/complement terminal.

In that case H(n,d-1)=n-1 and the stabilized degree-j dimension is
sum(binomial(d,k), k=0..min(j,d)).

## Forward proof

Rank deficiency gives a nonzero rational left annihilator.
Extend it by zero from the itinerary support Y to {0,1}^n.

Low-degree monomials and Walsh characters span the same filtered
space over Q and R. Thus the extension belongs to U_[d,n](n).

Theorem 1 gives support size >=2^d=n. Since |Y|=n, its support is Y.
Theorem 2 applies at equality.

Keep the full disjoint-block conclusion of that theorem:
there are d independent binary parameters b_1,...,b_d, and each
temporal coordinate is constant, b_i, or 1-b_i.
All d parameters occur. Hence dim span(1,a_0,...,a_(n-1))=d+1.

Define W_L=span_Q(1,a_0,...,a_(L-1)), with W_0=span_Q(1).

If W_(L+1)=W_L, then a_L lies in W_L. Composition K(g)=g composed
with T maps every generator of W_L into W_L, including K(1)=1.
Therefore W_L is K-invariant and all later observations lie in W_L.

The chain cannot pause and subsequently grow. It follows that
dim W_d=d+1. Otherwise an earlier pause would prevent W_n from
having dimension d+1.

Independence of 1,a_0,...,a_(d-1), together with their literal form,
forces the first d observations to use all d different parameters.
The prefix map is consequently bijective.

In those prefix coordinates the transition is
(u_1,...,u_d)->(u_2,...,u_d,f(u)).
Since d<n, the next observation a_d lies in the classified window,
so f is constant or a literal/complement.

This argument works on functions on X. It does not assume that
truncated itinerary supports are shift-closed.

## Converse

A constant/literal terminal produces only constants and literals
of the original prefix bits at all future times.
The first d observations already provide those original bits.

Thus degree-j temporal features span precisely the ordinary
degree-j polynomial functions on the full d-cube.
Their dimension is sum(binomial(d,k), k=0..min(j,d)).
At j=d-1 this is n-1.

## Single-cycle consequence

A bijective canonical constant/literal register must have terminal
u_1 or 1-u_1. The first fixes the all-zero state.
For the second, T^d is global complementation and T^(2d)=identity.

For d>=3, 2^d>2d, so neither transition is a single 2^d-cycle.
Therefore every separating observation on one 2^d-cycle has full
degree-(d-1) rational rank for d>=3.

This explains the cycle censuses. It does not make their
rank-defect implication nonvacuous.

## Labelled-map count for fixed balanced observation

Fix h with two fibers of size n/2.
A prefix coordinate bijection preserving h has ((n/2)!)^2 choices.
There are 2d+2 constant/literal terminals.

The prefix map is recovered uniquely from T and h, so distinct
encodings cannot represent the same observed transition.
The classification therefore gives
((n/2)!)^2 * (2d+2) represented extremal maps.

For d=3 this is (4!)^2*8=4608.

This is a mathematical completeness consequence under the external
dependency, not a new exhaustive eight-state computation.

## Evidence boundaries

The earlier Termux census is preserved, not rerun here.
Its manifest, recorded case structure, primitive representative
coverage, and prefix flags are checked by prepare.py.

That receipt review does not recompute its modular ranks and does
not authenticate its historical execution independently.
A checksum establishes current byte consistency, not proof validity.

The external equality theorem, this proof's correctness, and its
novelty require their own review. No application source changes,
claim enrollment, Git staging, commit, fetch, or push occur here.
