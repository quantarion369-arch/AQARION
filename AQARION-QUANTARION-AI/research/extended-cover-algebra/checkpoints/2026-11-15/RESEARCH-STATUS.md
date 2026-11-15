# Resolution research checkpoint — 2026-11-15

## Preservation scope

Actual local AQARION evidence and scripts have been copied unchanged.
Original home-directory files and the Yang–Mills checkout were not moved.

The c.py and h.py copies are intentionally UNCLASSIFIED.
Their presence here preserves them; it does not assert that both belong
to the resolution project. Review their contents before publication.

Singular-orbit files and other supplemental audit scripts are preserved
as intake evidence. This checkpoint does not independently validate
their mathematical conclusions.

The separate research-preservation archive was inventoried, not copied.
No original evidence archive was modified.

## Archived resolution

Complex SHA-256:
1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0

Original evidence archive SHA-256:
b0231475bb60dd70eafca56752f1f14d36d2ed3ed9ff86dd79cd179257600e77

User-reported device checks:
- All consecutive polynomial compositions vanish.
- Scalar and semigroup homogeneity pass.
- Zero constant terms in all differentials.
- Coefficients are 237 occurrences of -1 and 317 occurrences of +1.
- Q*T=D2, det(T)=-1, and D1*Q=0.
- Generic ranks are 1,13,22,13,1.
- Archived D1 ideal equals the rational toric kernel.
- D5 entry ideal equals D1 ideal; gcd(D5)=1.
- Final scalar shift 12; final multidegree (4,4,4,4;4).
- Exactness windows:
  H1 degrees 3..6; H2 degrees 4..8;
  H3 degrees 6..9; H4 degrees 8..12.
- Smith calculations found no nonunit invariant factors in required
  component maps.
- A separate unit-pivot audit reported zero residual blocks.
- Modular checks and endpoint Hilbert checks passed at 2,3,5,7.

These are summaries of terminal results supplied in the conversation,
not a claim that all later transcripts are present as raw local logs.

## Mathematical argument supplied in the conversation

S consists of lattice points ai>=0, ai+aj>=k.
For k<=0 use A and Ei. If ai=0 and k>0 use Bi^k.
If all ai>0, subtract C while k>=2, then finish at k=0 or 1.
This gives saturation.

The interior translate is kappa=(1,1,1,1;1), represented by AC.
It yields canonical module R(-3).
The weight sum is 15, so Gorenstein duality has final shift 12.
Low-degree kernel checks and duality bound all required generator
degrees, closing the finite-window rational exactness argument.

The archived D1 generators are pure differences of monomials.
The integral quotient is free abelian on monomial-congruence classes.
Rational toric-kernel equality therefore lifts to the integral endpoint.
Together with the integer window checks and characteristic-free
structural arguments, the conversation supplies an integral and
arbitrary-base-change exactness argument.

This is computation-supported mathematics, NOT independent
proof-assistant formal verification.

## General family: research, not part of the frozen original evidence

For Kn:
A=t^-1; Ei=xi; Bi=(product xj, j!=i)t;
C=(product xi)t^2.
Weights: A,Ei=1; Bi,C=n-2.
Dimension and codimension are n+1.
Canonical shift is -(n-1); final resolution shift is n(n-1).

Put Ui=product(Ej,j!=i), Uij=product(El,l not i,j),
Uijk=product(El,l not i,j,k).
Relations:
fi=A*Bi-Ui
gi=Ei*Bi-A*C
hij=Bi*Bj-C*Uij

Explicit syzygies:
Ei*fi-Er*fr-A*(gi-gr)=0 for fixed r.
For i<j:
A*hij-Bj*fi-Uij*gj=0
A*hij-Bi*fj-Uij*gi=0
Ei*hij-Bj*gi-C*fj=0
Ej*hij-Bi*gj-C*fi=0
For i<j<k:
Bk*hij-Bj*hik-C*Uijk*(gj-gk)=0
Bk*hij-Bi*hjk-C*Uijk*(gi-gk)=0

Proposed full second-module polynomial:
(n-1)t^n + 2n(n-1)t^(2n-3) + 2*C(n,3)t^(3n-6).

Reported assistant-side global QQ module comparisons:
K5: 64 proposed columns generate the full kernel.
K6: 105 proposed columns generate the full kernel.
These computations still need independent local reproduction.

Reported K5 rational free-module shifts:
F1: 4^10,6^10
F2: 5^4,7^40,9^20
F3: 8^15,10^60,12^15
F4: 11^20,13^40,15^4
F5: 14^10,16^10
F6: 20^1
Total ranks: 1,20,64,90,64,20,1.
Explicit higher matrices were constructed assistant-side, but those
matrix objects are NOT preserved by this intake checkpoint.

Four local divisor-complex types:
(ones;0): wedge of n-1 circles.
(2ones-ei-ej;1): wedge of two circles.
(2ones-ej;2): isomorphic to the first type.
(3ones-ei-ej-ek;3): isomorphic to the second type.
Vertex permutations:
A<->Bj, C<->Ej for the first isomorphism;
A<->Bk, C<->Ek for the second.
The conversation gives facet-based uniform proofs.
This supplies the proposed local contributions in every field.
Excluding ALL other degrees remains open for arbitrary n.

## Literature and claim boundaries

Known generators and structural tools:
Herzog–Hibi–Trung (2007), arXiv:math/0512423.
Divisor-complex correspondence:
Bruns–Herzog, Semigroup rings and simplicial complexes (1997).
Squarefree-Veronese symbolic-power comparison:
Ficarra–Moradi (2025), arXiv:2502.19998.

The total Betti sequences occur for other rings in Stanley's 1979
Invariants of finite groups and their applications to combinatorics.
Matching totals are not a novelty claim or a ring identification.

Novelty remains unestablished.
Do not extrapolate the archived K4 characteristic certificate to
the new K5/K6 matrices without their own audit.

## Remaining preservation tasks

- Review unclassified c.py and h.py.
- Review the separate preservation archive's inventory and contents.
- Consolidate and rerun later local audits with hash-bound receipts.
- Preserve actual K5/K6 construction code and matrices when reproduced.
- Audit shared storage, ignored material, and other devices separately.
