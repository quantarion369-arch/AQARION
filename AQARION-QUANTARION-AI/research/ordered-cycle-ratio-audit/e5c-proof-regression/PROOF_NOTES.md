# E5C Case A proof notes

Canonical ratio: R(n,m)=m!*c(n,m)/(n!*P(n,m)).
Off-diagonal Case A: 1<=m<n<=2m; d=n-m>=1; n>=2d.
Only in this domain is P(n,n-d)=p(d) used.

Cycle types with sum(j*b_j)=d and ell=sum(b_j) give
F_d(n)=p(d)*R(n,n-d)
=sum((n-d)_falling_ell / product((j+1)^b_j*b_j!)).

The identity (x+1)_falling_ell-x_falling_ell
=ell*x_falling_(ell-1), together with positive coefficients,
gives F_d(n+1)-F_d(n)>=1/(d+1).
Thus R increases strictly at fixed d for n>=2d.

Let A_d=[z^(2d)](-log(1-z))^d.
Nonnegative coefficient convolution gives A_(a+b)>=A_a*A_b.
Five exact bases d=5,...,9 satisfy A_d>p(d).

External dependency: Bessenrodt-Ono, Theorem 2.1,
Maximal Multiplicative Properties of Partitions.
For a,b>=2 and a+b>9, p(a)*p(b)>p(a+b).
Source: https://uva.theopenscholar.com/files/ken-ono/files/149_8.pdf

For d>=10, use a=5,b=d-5 and induction:
A_d>=A_5*A_(d-5)>p(5)*p(d-5)>p(d).
This proves R(2d,d)>1 for d>=5; monotonicity extends it.

Deficits 1,...,4 are handled by the recorded closed forms.
Case A below-one exceptions:
(2,1),(4,2),(5,3),(6,3),(8,4).
Only off-diagonal Case A equality: (3,2).
Every diagonal has R(n,n)=1.

The argument is derived and depends on the cited theorem.
Finite tests corroborate it; they do not prove the external
partition inequality or provide Lean certification.
No arbitrary-total Case B classification is asserted.
Novelty clearance and formal certification remain OPEN.
