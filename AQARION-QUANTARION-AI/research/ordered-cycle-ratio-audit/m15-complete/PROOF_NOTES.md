# Fixed m=15: complete Case B classification

Definition: R(n,m)=m! c(n,m)/(n! P(n,m)).
Here c is unsigned first-kind Stirling and P counts partitions
into exactly m positive parts.

Conclusion:
R(n,15)>1 for 31<=n<=113.
R(n,15)<1 for every n>=114.
No equality occurs for n>=31.

FINITE PREFIX:
For every 31<=n<=212, the audit checks the exact integer sign of
15! c(n,15)-n! P(n,15).
There are 83 positive, 99 negative, and zero equality cases.
Partition counts are cross-checked by restricted-part generating
coefficients. Five Stirling coefficients are cross-checked through
(n-1)! e_14(1,1/2,...,1/(n-1)).

INFINITE TAIL:
Coefficient positivity gives
e_(m-1)(1,1/2,...,1/(n-1))
<= binom(n+t-1,t)/t^(m-1) for positive integer t.
Composition counting gives P(n,m)>=binom(n-1,m-1)/m!.
Thus R(n,m)<=V_t(n,m), where
V_t=(m!)^2 binom(n+t-1,t)/
[n binom(n-1,m-1)t^(m-1)].

For n>=m>=2 and 1<=t<=m,
V_t(n+1,m)/V_t(n,m)
=(n+t)(n-m+1)/[n(n+1)]<1,
because the denominator minus numerator equals
n(m-t)+t(m-1)>0.

The audit checks the integer certificate V_4(213,15)<1.
Therefore R(n,15)<1 for every n>=213.
Together with the finite prefix, this covers every n>=31.

LIMITATIONS:
The prefix is exhaustive machine-exact computation, not a
computation-free proof. The infinite tail uses the analytic
argument above and one exact integer certificate.
No monotonicity of R itself is assumed.
No conclusion for other m, novelty clearance, Lean certification,
or unrestricted Case B classification is claimed.
