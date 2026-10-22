# Prime obstruction for ordered-cycle ratio equality

Let c(n,m) denote the unsigned Stirling number of the first kind, and
R(n,m)=m!c(n,m)/(n!P(n,m)), where P(n,m) counts partitions into m parts.

The classical generating polynomial is
    F_n(x)=product_{j=0}^{n-1}(x+j)=sum_m c(n,m)x^m.

For prime p,
    product_{j=0}^{p-1}(x+j)=x^p-x modulo p.
This follows because both monic degree-p polynomials have every element
of the field with p elements as a root.

Write n=ap+r, 0<=r<p. Grouping the factors into complete residue blocks gives
    F_n(x)=(x^p-x)^a F_r(x) modulo p.

Assume a>=1 and 1<=m<p.
The lowest term of (x^p-x)^a is (-1)^a x^a.
Every other term has degree at least a+p-1>=p.
Therefore
    c(n,m)=(-1)^a c(r,m-a) modulo p.
Use c(0,0)=1 and zero for invalid indices.

Choose a prime p>m and 1<=a<=m, and let
    d=a(p-1), n=m+d=ap+(m-a).
Then 0<=m-a<p and
    c(n,m)=(-1)^a c(m-a,m-a)=(-1)^a modulo p,
which is nonzero.

But n>=p>m, so p divides n!/m!.
Equality R(n,m)=1 would require
    c(n,m)=(n!/m!)P(n,m),
contradicting the nonzero residue.

Thus equality is excluded for this entire family.
Its Case B portion is selected by d>m.

In particular, if d>m and d+1 is prime, choose a=1 and p=d+1.
This excludes every Case B pair with prime d+1.

The accompanying finite check compares the congruence with exact
Stirling integers through n=300. It is an implementation check, not
the justification of the infinite theorem.

The global equality classification remains open.
No novelty or proof-assistant certification is asserted.

Normalization warning:
A_d(m)=m!c(m+d,m)/(m+d)! is generally rational.
Multiplying it by m! does not generally make it integral.
The exact integer normalization is
    ((m+d)!/m!) A_d(m)=c(m+d,m).
