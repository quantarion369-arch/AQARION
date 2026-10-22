# Dual-thread enumeration and permutation-graph homology

## Scope

This addendum preserves the completed Termux audit and its four exact tables.
The proof note is written at packaging time; it is not represented as a
proof document hashed by the original execution receipt.

## Weighted endofunction identity

Let E(n,k)=binomial(n,k)k!F(n,k), with F(n,n)=1 and
F(n,k)=k*n^(n-k-1) for k<n. The periodic-core and prescribed-root-forest
decomposition counts endofunctions with k periodic labels.

The formula under study satisfies
    A(n,m)=sum_k E(n,k)P(k,m).
Consequently
    A(n)=sum_k E(n,k)p(k),
    sum_k E(n,k)=n^n.
Thus A(n)>n^n for n>=2.

The inequality alone does not identify the decorated objects.
It is consistent with the previously documented endofunction-congruence
interpretation through invariant partitions on the periodic core.
This audit checks formula identities, not a new direct census of those pairs.

## Invariant-partition cycle polynomial

Let C_j(t)=sum_k c(j,k)t^k.
For a fixed collection of a blocks of size j, a block-permutation cycle
of length l contributes
    (j!)^(l-1) C_j(t).
Choose l-1 bijections freely; the composite permutation on the initial
block determines the number of label cycles.

Summing over block permutations gives
    W_(j,a)(t)=product_(r=0)^(a-1)(C_j(t)+r*j!).

For a block-size profile (a_j), multiply these polynomials and then multiply
by the number of corresponding set partitions:
    n! / product_j((j!)^a_j a_j!).

Summing over profiles gives B(n,m;t). Its coefficient at t^k counts pairs
(sigma,Pi) with m invariant blocks and k cycles of sigma.

Since C_j(1)=j!, each profile contributes n! at t=1. Hence
    B(n,m;1)=n!P(n,m).

The corrected generator uses nondecreasing integer-part lists exactly once.
The faulty generator is retained only as a negative control: repeated sizes
can be selected recursively and their earlier multiplicities overwritten.

## Exact moment identity

At t=1 each block-size profile has equal total weight n!.
The logarithmic derivative of W_(j,a) at 1 is H_j H_a, where H_r is harmonic.
Therefore the first moment is the uniform profile average
    (1/P(n,m)) sum_profiles sum_j H_j H_(a_j).

The audit checks this identity independently of coefficient differentiation.
Second raw moments and variances are stored as exact rational numbers.

## Explicit topological model

Give each permutation one edge i->sigma(i) per label, retaining loops and
distinct edges. Its realization is a disjoint union of k circles when sigma
has k cycles. Thus ordinary integral homology is
    H_0=H_1=Z^k,
    H_q=0 for q>=2.
There is no torsion.

Accordingly B records the distribution of beta0=beta1 for this graph model.
It does not compute directed path homology, clique-complex homology,
or proper invariant-partition order-complex homology.

For ordered-cycle objects:
    A(n,m;t)=m!c(n,m)t^m.

For m<n, identity permutations contribute B objects with beta=n, absent
from A. For m=n>=2, B contains n-cycles with beta=1, absent from A.
Only (n,m)=(1,1) has matching full homology distributions.

At (3,2), equal totals coexist with different distributions:
    A=6t^2,
    B=3t^2+3t^3.
This topological mismatch does not explain the arithmetic equality criterion.

## Evidence boundaries

Polynomial and moment calculations cover n<=10.
Independent direct permutation/invariant-partition enumeration covers n<=6.
The all-n distribution mismatch is the argument above, not extrapolation.

Packaging verifies saved hashes and table arithmetic without rerunning
permutations. The global ratio equality classification remains open.
No novelty or proof-assistant certification is asserted.
