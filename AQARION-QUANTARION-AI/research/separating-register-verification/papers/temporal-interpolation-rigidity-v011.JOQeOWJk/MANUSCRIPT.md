# Maximal Temporal Interpolation Degree in Finite Boolean Dynamics

AQARION research manuscript
Version 0.1.1 — 27 October 2026

Author list: to be supplied and approved before circulation.
Status: working manuscript for independent mathematical review.
No novelty clearance, peer review, or machine-checked proof is claimed.

## Abstract

Let a deterministic system have 2^d states and a binary observation.
Products of temporal observations define bounded-degree polynomial
function spaces on its itinerary support. We characterize the extremal
systems for which degree d-1 fails to reconstruct every state function.

For any separating observation window of length at least d+1, such a
rank defect occurs precisely when the first d observations identify the
state and, in those coordinates, the transition is a shift register
whose terminal is constant or a coordinate literal or its complement.
The proof combines the published minimum-support equality theorem for
hypercube functions with an elementary stabilization argument for
temporal observation spans.

The characterization determines the complete stabilized Hilbert profile,
gives exact labelled counts, and rules out this extremal rank defect on
a single cycle of length 2^d whenever d>=3. A completed local census of
all 4,080 primitive binary necklaces of length sixteen agrees with the
cycle consequence. We distinguish the mathematical argument from its
external dependency, finite checks, and unpublished local evidence.

## 1. Introduction and position in the literature

Recovering an initial state from an output sequence is an observability
problem. Here we distinguish that question from the algebraic complexity
of reconstructing arbitrary state functions using polynomials in the
measured outputs.

For a Boolean point set, dimensions of bounded-degree polynomial
function spaces are Hilbert-function values. Their least full degree is
the interpolation degree. These objects and their connections with
shattering and VC dimension are established in Moran and Rashtchian
[MR]; we do not introduce a new invariant.

Our question concerns the restrictions imposed by deterministic time
evolution on an extremal itinerary support. The principal external
ingredient is Valyuzhenich's support bound and equality classification
[V, Theorems 1 and 2]. We derive a temporal classification from that
geometry. The support theorem itself, its trade-theoretic foundations,
and the general observability problem are not claimed as contributions.

The older null-design literature must also be distinguished from
our temporal conclusion. Frankl-Pach [FP] proves the weighted support
bound and supplies the trace mechanism. Disjoint-block trade geometry
appears in Krotov [K] and Ghorbani et al. [GKKK].

The output-preserving encoding factor ((2^(d-1))!)^2 appears explicitly
in Li-Zhu-Lu [LZL, Remark 2]. Xiong-Zhong-Lin [XZL, Appendix B] explicitly
uses a temporal-coordinate bijection. We do not claim those ingredients
as new. The specific criterion requiring priority comparison is the
rational temporal rank defect forcing the constant/literal terminal class.

The accessible preview of [XZL] does not expose its complete main text.
No complete theorem-level non-overlap assessment is claimed.

This manuscript supplies a proof for review. Whether the resulting
dynamical characterization has appeared elsewhere remains to be
established by a dedicated prior-art comparison.

## 2. Observation spaces and conventions

Let X be a nonempty finite state set, T:X->X a deterministic
transition, and h:X->{0,1} a binary observation. Observation lengths
L and degree cutoffs j are nonnegative integers. Put

    a_t = h composed with T^t.

The length-L itinerary of x is

    Phi_L(x) = (a_0(x),...,a_(L-1)(x)).

A window separates states if Phi_L is injective.

Over Q, define V_(L,j) as the span of the functions

    product(a_t : t in S),  S subset {0,...,L-1}, |S|<=j,

including the empty product 1. Write H(L,j)=dim_Q V_(L,j).
Equivalently, H(L,j) is the rank of the associated evaluation matrix,
with states as rows and temporal monomials as columns.

When Phi_L is injective, this is the Hilbert function of the itinerary
set Y_L=Phi_L(X). Degree j gives full reconstruction if H(L,j)=|X|.

Let V_(infinity,j) be the span using arbitrary finite sets of
nonnegative observation times. Its dimension is H(infinity,j).

All classification and counting results below use rational ranks.
Binary observations do not imply that ranks are taken over F2.

## 3. A stabilization lemma

Lemma 3.1 (no pause).
Let

    W_L = span_Q(1,a_0,...,a_(L-1)),  W_0=span_Q(1).

Write W_infinity=span_Q({1} union {a_t:t>=0}).

If W_(L+1)=W_L, then W_L contains every later observation.

Proof.
Let K(g)=g composed with T. Equality means a_L belongs to W_L.
The operator K sends 1 to 1, and each a_t among the generators of W_L
to a_(t+1), which also belongs to W_L. Thus K(W_L) is contained in W_L.
Repeated application of K proves the assertion. This also covers L=0.
End proof.

Corollary 3.2.
If r=dim W_infinity, then W_(r-1)=W_infinity.

Proof.
Before stabilization each step increases dimension by exactly one.
The chain starts at dimension one and cannot pause and later grow.
End proof.

For Boolean observations the entire degree profile stabilizes by this
same horizon:

    H(r-1,j)=H(infinity,j),  j>=0.

Indeed, later observations are affine combinations of the earlier ones.
Substituting into a product of at most j observations preserves degree
at most j. Repeated powers reduce by a_t^2=a_t.

This squarefree-feature conclusion requires Boolean observations.
For arbitrary rational-valued observations, ordinary polynomial
features allowing repeated powers would be required instead.

The lemma is an elementary finite-dimensional cyclic-subspace argument.
No novelty is claimed for this linear-algebraic mechanism.

## 4. The external support result used here

We use the following specialization of [V, Theorems 1 and 2].

Let v be a nonzero real-valued function on {0,1}^L, orthogonal to every
Walsh character of weight less than d. Then

    |supp(v)| >= 2^d.

If equality holds, the support is, up to a hypercube automorphism, a
product of d two-point blocks and fixed coordinates.

More explicitly, there are d nonempty disjoint coordinate blocks.
Within each block all coordinates equal one free bit. Coordinates
outside the blocks are fixed. Permuting coordinates and flipping
individual coordinates yields the general equivalent support.

Consequently each coordinate, as a function on that support, is
constant or a literal of one of d independent binary parameters.

Explanation of the specialization.
The orthogonality condition places v in U_[d,L](L).
Theorem 1 applies with i=d and j=L. At equality, Theorem 2 gives a
tensor product of d functions phi_t and a fixed-coordinate factor.
Each phi_t is supported on the all-zero and all-one vectors in its
block. The parity restrictions in the general theorem add no
restriction here because L-j=0.

An automorphism of the Boolean hypercube permutes coordinates and
flips individual bits. Thus the literal-coordinate description follows.

This result is cited, not reproved or machine-verified in this work.

## 5. Main classification

Theorem 5.1.
Let d>=1, let |X|=n=2^d, and let L>=d+1.
Assume Phi_L separates states. The following are equivalent.

(A) H(L,d-1)<n.

(B) Phi_d is bijective onto {0,1}^d and, in these coordinates,

        T_f(u_1,...,u_d)=(u_2,...,u_d,f(u)),

    where

        f in {0,1,u_1,1-u_1,...,u_d,1-u_d}.

(C) For every L'>=d and j>=0,

        H(L',j)=sum(binomial(d,k), k=0..min(j,d)).

In particular the defect in (A) is exactly one.

Proof of (A) implies (B).
A nonzero left-null vector of the degree-(d-1) evaluation matrix
assigns rational weights to the n distinct itinerary points. Extend
those weights by zero to the full L-dimensional Boolean cube.

For A subset {0,...,L-1}, the Walsh character is

    chi_A(y)=product(1-2*y_t : t in A).

Conversely, a monomial y_S equals
2^(-|S|)*product(1-chi_{t}(y):t in S).
Thus low-degree monomials and low-weight Walsh characters span the
same filtered polynomial space over Q and R. The extension v
therefore belongs to U_[d,L](L).

The external support bound gives |supp(v)|>=2^d=n. Since v is
supported on an n-point itinerary set, equality holds and every
itinerary has nonzero weight.

The equality geometry of Section 4 supplies independent parameters
b_1,...,b_d such that every a_t in the window is constant or a literal
of one parameter. Every parameter occurs. Hence

    dim W_L=d+1.

We claim dim W_d=d+1. Otherwise, among the d steps from W_0 to W_d,
one step must fail to increase dimension. Lemma 3.1 would then
prevent W_L from reaching dimension d+1, a contradiction.

Independence of 1,a_0,...,a_(d-1), together with their literal form,
forces the first d observations to use all d parameters, with no
constant coordinate and no repeated parameter. Thus Phi_d is bijective.

In these prefix coordinates the transition shifts the first d-1
coordinates, and its terminal is a_d. Since L>=d+1, this observation
belongs to the classified window. It is constant or a literal of a
parameter, and hence constant or a literal of the prefix coordinates.
This proves (B).

Proof of (B) implies (C).
Under a constant/literal terminal every future observation remains
constant or a literal of an original prefix coordinate. Therefore a
product of at most j temporal observations is a polynomial of degree
at most j in those original coordinates.

Conversely, the first d observations provide every original coordinate,
so their monomials span the entire ordinary degree-j space on the
d-cube. Its dimension is the stated binomial sum.

Proof of (C) implies (A).
At j=d-1 the binomial sum is 2^d-1.
End proof.

Remark 5.2 (why the extra observation matters).
At L=d, any bijective cube prefix already has rank 2^d-1 through
degree d-1, regardless of its terminal. The terminal has not yet been
observed. Thus the constant/literal terminal conclusion cannot follow
from that window alone. The condition L>=d+1 is essential in general.

Corollary 5.3.
For a system whose infinite itineraries separate its 2^d states, the
least full temporal interpolation degree equals d if and only if the
system has the form in (B). Otherwise degree at most d-1 suffices.

Proof.
Choose a sufficiently long separating window with L>=d+1.
If degree d-1 is deficient, Theorem 5.1 gives the complete cube
profile. Otherwise that window already reconstructs all functions
at degree at most d-1.
End proof.

## 6. Exact obstruction and labelled counts

Corollary 6.1.
In the extremal class, the annihilator at degree d-1 is one-dimensional.
In prefix coordinates it is generated by

    v(u)=(-1)^(u_1+...+u_d).

Proof.
Parity annihilates every polynomial of degree less than d on the
full d-cube. Every temporal monomial of degree at most d-1 is such
a polynomial. Theorem 5.1 gives rank n-1, proving uniqueness up to scale.
End proof.

Corollary 6.2.
Fix a labelled set X of size n=2^d and a balanced observation h,
meaning both observation fibers have size n/2.
The number of transitions in the extremal separating class is

    ((n/2)!)^2 * (2d+2).

For an unbalanced observation the number is zero.
Counting over all observations gives (2d+2)n! observed pairs.

Proof.
A coordinate bijection q:X->{0,1}^d with first coordinate h has
((n/2)!)^2 choices. There are 2d+2 permitted terminals.
Conjugating the canonical register by q constructs an observed
transition with prefix map exactly q:

    Phi_d(x)=q(x).

Conversely, q is recovered from (T,h) as Phi_d, and its terminal
is then recovered from T. Thus the construction has no duplicates.
Theorem 5.1 supplies completeness. A bijective prefix forces h to
be balanced.

There are binomial(n,n/2) balanced observations. Multiplying yields
(2d+2)n!. These counts distinguish labelled states; they are not
counts up to dynamical isomorphism.
End proof.

For d=3 and fixed h=00001111, the count is

    (4!)^2 * 8 = 4608.

This is a mathematical consequence of the classification, not a new
enumeration of all eight-state transition maps.

## 7. Exclusion of primitive power-of-two cycles

Corollary 7.1.
For d>=3, every separating binary observation on a single cycle of
length n=2^d has full rank through degree d-1 on its length-n itineraries.

Proof.
Suppose otherwise. Theorem 5.1 identifies the system with a
constant/literal-terminal register.

For that register to be bijective, its terminal must distinguish two
states differing only in u_1. Among the permitted terminals, only
u_1 and 1-u_1 do so.

The first fixes the all-zero state and cannot be one n-cycle.
For the second, T^d is global complementation and T^(2d)=identity.
Every orbit has length at most 2d, whereas 2^d>2d for d>=3.
This is a contradiction.
End proof.

For d=2 the complemented rotation gives the four-cycle represented
by the observation word 0011. Its degree-one rank is three.
This is a genuine nonvacuous boundary example.

An alternative cycle-only proof uses the affine-support consequence
of the external theorem. A full 2^d-cycle on an affine d-space would
give an affine transformation of order 2^d. Its homogeneous matrix
has dimension d+1 and is unipotent in characteristic two, so its
order divides 2^ceil(log2(d+1)), which is smaller for d>=3.

For the alternative argument, a single full cycle makes the affine
map's order exactly 2^d. Its homogeneous matrix M satisfies
(M-I)^(2^d)=0 in characteristic two. Thus M-I is nilpotent of
index at most d+1, which gives the stated power-of-two order bound.

The register proof above additionally identifies the noncyclic
extremal systems.

## 8. Computational evidence and reproducibility

A completed Termux run enumerated all 4,080 primitive binary
necklaces of length sixteen. Each matrix had sixteen rows and

    1+16+binomial(16,2)+binomial(16,3)=697

squarefree feature columns.

The implementation encoded binary evaluation columns as integers.
It certified full rank modulo p=2147483647 for every necklace.
A full-rank minor modulo p has a nonzero integer determinant, so
this certifies rational rank sixteen.

The run reported:

    primitive necklaces:                  4080
    rational rank sixteen:                4080
    deficient cases:                         0
    separating four-prefixes:               16
    full-rank cases with prefix collision: 4064
    exact fallback calls in the census:       0

It also passed three direct rational sample checks, exact-fallback
self-tests, JSON read-back, and checksum verification.

The script-reported elapsed time was 4.96 seconds on the user's
Termux installation. This is not a controlled cross-platform benchmark.

A separate bit-vector computation over F2 also found rank sixteen
in all 4,080 cases. Its execution was reported in the research
conversation; it is not part of the source-bound Termux receipt
archived in this batch.

The cycle computation checks Corollary 7.1 in one finite case.
It does not replace the general proof, certify the external equality
theorem, or provide a nonvacuous test of the rank-defect implication.

The accompanying local evidence includes the original census source,
per-case results, terminal output, exit status, checksum manifest,
and subsequent receipt review. Local preservation is not public
archival availability. Publication of a reviewed artifact set remains
a separate step.

### 8.1 Unrestricted eight-state finite check

A subsequent completed Termux audit enumerated all 8^8=16,777,216
transition arrays with fixed observation h=00001111. It found:

    separating transition maps:                    1612800
    F2 degree-two deficient candidates:                9216
    Q degree-two rank-seven maps:                      4608
    Q degree-two rank-eight maps among candidates:     4608
    Q degree-two full-rank separating maps overall:  1608192

Every F2-full-rank matrix is full rank over Q by the integer-minor
argument. Every F2-deficient candidate received exact rational rank
using integer elimination with gcd reduction.

All 9,216 candidates had a bijective three-prefix and induced one
of the sixteen affine Boolean feedback functions. Each feedback
occurred 576 times. The eight constant/literal functions gave rational
rank seven; the other eight affine functions gave rational rank eight.

The rational-defect set agreed exactly with the independently generated
observation-preserving relabelings of the eight constant/literal
registers. All 4,608 parity obstructions and cubic witnesses passed.
The sixteen canonical representatives were also checked using separate
Fraction Gaussian elimination.

For increasing transition code
m=sum(T[i]*8^i, i=0..7), encoded as one ASCII decimal integer plus LF
per record, the 4,608 rational-defect codes have SHA-256:

    12a3ef626871915fa3c9a69a00a6701ff14c88e792e5f3f54db78c7ad1fb72af

This is a finite check for one fixed balanced observation, not a proof
of Theorem 5.1 for arbitrary d. The attached audit also contains
partition-ratio and trade-matrix checks; those are separate research
lanes and are not dependencies of this manuscript.

## 9. Field and scope limitations

The rational coefficient field is material.

For example, in the three-bit register with terminal u_1 XOR u_2,
the temporal outputs run through the seven nonzero linear forms
over F2 in the initial bits. Over F2, constants and linear temporal
features span dimension four.

Over Q, each such Boolean linear form equals (1-chi)/2 for a
different nontrivial Walsh character. Together with the constant
they span all eight state functions. Thus the eventual profiles are

    Q:  [1,8,8,8]
    F2: [1,4,7,8].

The present classification does not assert the same list of terminals
over F2.

The assumption of a separating observation window is also essential:
without it, ranks concern observable equivalence classes rather than
all original states.

No controlled Boolean-network inputs, noisy observations, approximate
ranks, or infinite state spaces are considered here.

## 10. Review status and remaining work

The manuscript contains a complete written derivation under the
published support/equality theorem. Its main review targets are:

1. The exact disjoint-block specialization of [V, Theorem 2].
2. The no-pause argument and its use at the first d observations.
3. Uniqueness and completeness in the labelled counting argument.
4. Prior literature on temporal polynomial reconstruction and
   feedback-register classifications.

The numerical evidence is complete for the sixteen-cycle census
and the fixed-observation unrestricted eight-state census.
Neither finite check replaces the general proof.
A larger cycle census is not required for the theorem.

Independent proof review, authorship approval, novelty assessment,
public artifact preparation, and any machine formalization remain open.
No publication, acceptance, or claim-registry promotion is implied.

## Bibliographic dependencies

[V] Alexandr Valyuzhenich.
Optimal functions with spectral constraints in hypercubes.
Discrete Mathematics 347(3), Article 113816, 2024.
Primary statements used: Theorems 1 and 2.
Consulted preprint: arXiv:2303.10995v1.

[MR] Shay Moran and Cyrus Rashtchian.
Shattered Sets and the Hilbert Function.
MFCS 2016, LIPIcs 58, Article 70, pages 70:1-70:14.
DOI: 10.4230/LIPIcs.MFCS.2016.70.
Related full preprint: arXiv:1511.08245.

[FP] Peter Frankl and Janos Pach.
On the Number of Sets in a Null t-Design.
European Journal of Combinatorics 4(1), 21-23, 1983.
DOI: 10.1016/S0195-6698(83)80004-3.

[K] Denis S. Krotov.
On the gaps of the spectrum of volumes of trades.
Journal of Combinatorial Designs 26(3), 119-126, 2018.
DOI: 10.1002/jcd.21592.

[GKKK] E. Ghorbani, S. Kamali, G. B. Khosrovshahi, D. S. Krotov.
On the volumes and affine types of trades.
Electronic Journal of Combinatorics 27(1), P1.29, 2020.
DOI: 10.37236/8367.

[LZL] Bowen Li, Shiyong Zhu, Jianquan Lu.
Improved transformation between Fibonacci FSRs and Galois FSRs
based on semi-tensor product.
Consulted preprint: arXiv:1911.01588v2, 26 June 2020.
Remark 2 is the encoding-count comparison.

[XZL] Jingtao Xiong, Jianghua Zhong, Dongdai Lin.
Studying the isomorphism of NFSRs via a general framework of bijections.
Designs, Codes and Cryptography 93, 2823-2853, 2025.
DOI: 10.1007/s10623-025-01622-y.
Publisher abstract and accessible appendices inspected.
Complete main-text comparison remains pending.
