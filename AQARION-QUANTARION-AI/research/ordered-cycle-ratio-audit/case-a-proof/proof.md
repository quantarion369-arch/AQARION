# Case A: equality classification in m >= d

Let g(x)=-log(1-x)/x and
A_d(m)=[x^d]g(x)^m
      =sum_{lambda partitions d} (m)_{length(lambda)}/w(lambda)
for integer m>=d.

For d>=1, A_d(m) is strictly increasing on integer m>=d:
all falling factorials in the profile sum are strictly increasing and
all their coefficients are positive.

The ratio is R(m+d,m)=A_d(m)/p(d).

Coefficientwise, g(x)>=exp(x/2), since
1/(j+1)>=1/(2^j j!) for every j>=0.
Consequently A_d(d)>=d^d/(2^d d!).

Monotonicity of log gives
log(d!)<=d log d-d+1+log d.
Thus
log A_d(d)>=d(1-log 2)-1-log d
          >3d/10-1-sqrt(d).

Here log 2<7/10 and log d<=sqrt(d).
For the first inequality, the first four terms of exp(7/10)
already sum to more than 2.
For the second, the maximum of log(x)/sqrt(x), x>=1,
is 2/e<1.

The partition bound is p(d)<=exp(pi sqrt(2d/3)).
For completeness, with t>0 and B=pi^2/6,
log product_{j>=1}(1-exp(-tj))^-1
=sum_{r>=1}1/(r(exp(tr)-1))
<=B/t.
Hence p(d)<=exp(td+B/t); optimize at t=sqrt(B/d).
Also pi sqrt(2/3)<3.

For d>=196, put u=sqrt(d)>=14.
The polynomial 3u^2/10-4u-1 is positive at 14
(value 9/5), and strictly increasing thereafter.
Therefore log A_d(d)>3sqrt(d)>log p(d).

The attached exact checks prove
d! c(2d,d)>(2d)! p(d) for each 5<=d<=195.
Together, these establish A_d(d)>p(d) for every d>=5.
Strict monotonicity then gives R(m+d,m)>1 for all m>=d>=5.

For d=4:
R(8,4)=967/1200<1 and R(9,5)=1069/720>1.
Strict monotonicity excludes equality for every integer m>=4.

The preceding elementary classifications for d=0,1,2,3 complete Case A:
equality occurs only at d=0 and at (n,m)=(3,2).

Status: computer-assisted argument with 191 finite exact base checks.
The infinite tail is bounded analytically.
Case B, m<d, remains unresolved by this argument.
No novelty or formal-proof-assistant certification is asserted.
