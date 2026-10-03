# D22 Operator Jordan Certificate

Under the locked convention

K e_j = e_{j-1},
u_d = e_0 - e_d,

P_d = I - (1/2)u_d u_d^T,
Q_d = (1/2)u_d u_d^T,

D_d = Q_d K P_d.

The direct factorization gives

D_d = (1/2) u_d a_d^T

with

a_d^T = u_d^T K P_d.

Since P_d u_d = 0,

a_d^T u_d = 0.

Therefore

D_d^2 = 0.

The explicit factor a_d is nonzero for every
k >= 3 and 1 <= d < k.

Hence

rank(D_d) = 1,

minimal_polynomial(D_d) = x^2,

and the Jordan form is

J_2(0) ⊕ 0_(k-2).

Furthermore,

||D_d||_2 = ||D_d||_F

and

||D_d||_2 =
    sqrt(3)/2,  d = 1 or d = k-1,
    1,          2 <= d <= k-2.

Thus the complete nonzero singular spectrum is determined
exactly by whether d is a boundary lag.

This theorem concerns only the explicitly locked operator
convention. It does not establish equivalence with an external
canonical D22 source.
