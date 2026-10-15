# Closure-cost bound and equality characterization

Status: paper proof reviewed in the 2026-10-14 work session.
Not machine-checked. Novelty not established.

## Setup

Let X be finite and nonempty, T:X->X, and pi a partition into
k nonempty blocks. Work over Q. Let V_pi be the functions constant
on pi-blocks, and Kf=f composed with T.

For j>=0 define:
  W_j = V_pi + K V_pi + ... + K^j V_pi.

For j>=1 define:
  delta_j = dim W_j - dim W_(j-1).
  C = sum_j delta_j.

P_j groups states whose pi-labels agree at times 0,...,j.
Let P_infinity be the stabilized itinerary partition and
s = number of its blocks.

## Stabilization

If delta_j=0, then W_j=W_(j-1).
Moreover K W_(j-1) is contained in W_j, so W_(j-1) is K-invariant.
All later increments vanish.

Two states are in the same P_j-block exactly when every function
in W_j agrees on those states. Thus feature-space stabilization
also stabilizes the itinerary partition.

Dimensions are bounded by |X|, so stabilization occurs in finite time.

## Two-sided bound

C <= s-k <= k * (product_j(1+delta_j) - 1).

Proof of the lower bound:
W_infinity is contained in V_(P_infinity), so
k+C = dim W_infinity <= s.

Proof of the upper bound:
Fix B in P_(j-1), with m children in P_j.
Every function in W_(j-1) is constant on B. Restriction modulo
constants therefore induces a map

  W_j/W_(j-1) -> Q^B / span{1_B}.

The new time-j label indicators restrict to the m child indicators.
Their span modulo constants has dimension m-1. Hence

  m-1 <= delta_j.

Summing child counts gives
  |P_j| <= (1+delta_j)|P_(j-1)|.

Multiplication from |P_0|=k proves the upper bound.

## Upper-equality criterion

Upper equality holds iff every B in P_(j-1) has exactly
1+delta_j children at every stage j>=1.

Proof:
Each stage inequality is equality exactly when every child count
is maximal. Any strict stage inequality stays strict under the
remaining positive multiplicative factors. Conversely, equality
at every stage gives equality in the product.

## Binary all-ones-profile characterization

Let x_0:X->{0,1} take both values, x_i=x_0 composed with T^i.
Then W_j=span_Q{1,x_0,...,x_j}, and k=2.

Fix d>=2. The following are equivalent:

A. delta_1=...=delta_(d-1)=1, delta_d=0, and upper equality holds.

B. Both:
   (i) x -> (x_0(x),...,x_(d-1)(x)) is onto {0,1}^d.
   (ii) x_d is constant 0, constant 1, x_i, or 1-x_i
        for some 0<=i<d.

Proof A implies B:
Maximal splitting doubles every block at each of the first d-1
stages. Thus all 2^d words occur.
Since delta_d=0, x_d is rational-affine in the first d coordinates.
A rational-affine function Boolean-valued on the full cube is
constant, a coordinate, or a complemented coordinate:
evaluate at zero, unit vectors, and the all-ones vector.

Proof B implies A:
Full-cube coverage makes 1,x_0,...,x_(d-1) independent.
Each of the first d-1 increments is therefore 1.
The feedback relation gives delta_d=0, hence permanent stabilization.
Thus P_infinity=P_(d-1), s=2^d, and

  s-2 = 2*(2^(d-1)-1),

which is upper equality.

This describes the itinerary quotient, not necessarily X itself.
Multiple states can share an itinerary.
Affine means over Q (or R), not F_2; XOR is not included.
