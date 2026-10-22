# Joint stabilizer statistics and incidence homology

## Objects and normalization

Objects are valid pairs (sigma,pi), with pi an m-block set partition and
sigma preserving pi setwise. K counts cycles of sigma. Q counts cycles
of its induced permutation on the blocks.

For C_j(t)=sum_k c(j,k)t^k, the joint local enumerator is
    W_(j,a)(u,t)=product_(r=0)^(a-1)(u C_j(t)+r j!).
A cycle of the block permutation contributes one power of u and the
cycle enumerator of the composed permutation on a representative block.

Summing over block profiles gives
    Z(q,z;u,t)=product_(j>=1)(1-z q^j)^(-u C_j(t)/j!),
where [q^n z^m]Z=H_B(n,m;u,t)/n!.
At u=t=1 this is the partition product.

## Mixed factorial recurrence

Let D_(a,b)(n,m)=[q^n z^m] partial_t^a partial_u^b Z at u=t=1,
and f_(j,i) be derivative i of C_j(t)/j! at 1.
Differentiating z partial_z Z gives the finite recurrence

D_(a,b)(n,m) =
  (1/m) sum_(j,r>=1; jr<=n,r<=m)
        sum_(i=0)^a sum_(h=0)^min(1,b)
        binomial(a,i) binomial(b,h) f_(j,i)
        D_(a-i,b-h)(n-jr,m-r).

The base is D_(0,0)(0,0)=1; other empty derivatives and invalid indices
are zero. The h<=1 restriction follows from the linear factor u f_j(t).

## Incidence graph

Left vertices are permutation cycles; right vertices are partition blocks.
One edge is retained per label, including parallel edges.
A cycle of sigma visits all blocks in one induced block orbit.
Consequently connected components are exactly the Q block orbits.

The oriented edge boundary is block_vertex-cycle_vertex. Thus
    beta0=Q,
    beta1=n-K-m+Q.
Integral homology is free in degrees zero and one, and zero above.
This is a graph realization, not a surface embedding or directed-path model.

In particular,
    E[beta1]=n-m-E[K]+E[Q],
    Var(beta1)=Var(K)+Var(Q)-2 Cov(K,Q).

## Evidence and limits

The executed audit compares 660 mixed coefficients with joint polynomials
on 55 parameter pairs through n=10. Direct enumeration through n=6 checks
21 joint distributions and boundary matrices for 8903 valid pairs over
the fields with two and three elements.

No Smith normal form is computed. Integral torsion-freeness follows from
graph structure, not from the two finite-field calculations.

Counterexample families show that normalized K distributions alone, or
incidence beta1 distributions alone, cannot recover the arithmetic ratio
throughout the domain. Additional parameters or structure may still matter.

This proof note was authored at packaging time. The preserved execution
receipt binds the source and CSV artifacts, not this later note.
The global ratio classification remains open.
