# Positive parity factorization and incidence variance

## Model

Use the incidence graph of the accompanying joint-incidence addendum.
Write B=beta1=n-K-m+Q and G_(n,m)(s)=sum_(sigma,pi) s^B.

Assume 1<=m<n. Every pi has a nonsingleton block. Choose two labels x,y
inside one such block by a deterministic rule depending only on pi.
Map (sigma,pi) to ((x y)sigma,pi).

## Involution

The map preserves pi and the induced permutation of its blocks.
Therefore it preserves Q. It is fixed-point-free and involutive.
Multiplication by a transposition either merges two permutation cycles
or splits one, so K changes by exactly one. Hence B changes by one.

Each orbit contributes s^l+s^(l+1)=s^l(1+s), with l>=0.
Consequently
    G_(n,m)(s)=(1+s) A_(n,m)(s),
where A has nonnegative integer coefficients.

The same statement holds separately in every nonempty fixed-Q stratum.

## Distribution and variance

Under uniform valid-pair sampling, select an involution orbit uniformly
and then one of its two elements fairly. Thus B has the distribution
    L+U,
where L is the lower B in that orbit and U is an independent fair Bernoulli.
This is a distributional representation; it does not assert that U is
independent of the original permutation-cycle statistic K.

It follows that even and odd B have equal probabilities and
    Var(B)=Var(L)+1/4 >= 1/4.

For d=n-m=1, B has support {0,1}; parity balance gives variance 1/4.

For d>=2, both B=0 and B=d occur:
- identity sigma gives B=0;
- fixing each block and using one cycle inside each block gives K=Q=m,
  hence B=d.
Therefore L cannot be constant, since constant L would give only two
adjacent B values. Thus Var(B)>1/4.

For m=n, the singleton-block incidence graph is a forest, so B=0.

The exact classification is therefore:
    Var(beta1)=0       for m=n,
    Var(beta1)=1/4     for m=n-1,
    Var(beta1)>1/4     for m<=n-2.

## Evidence and limits

The saved audit reads the prior joint coefficient artifact. It checks
45 off-diagonal factorizations, 137 fixed-Q factorizations, 36 strict
variance cases, and two invalid-polynomial negative controls.

It does not rerun the joint audit or directly enumerate the involution.
The all-parameter argument is the proof above.

This is an application of classical transposition/sign-involution methods.
No novelty, proof-assistant certification, or global ratio theorem is claimed.
This proof note was authored at packaging time.
