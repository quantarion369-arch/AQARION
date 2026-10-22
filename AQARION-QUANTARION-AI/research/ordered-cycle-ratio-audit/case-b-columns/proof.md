# Case B: fixed-column tail reduction

Define
R(n,m) = m! c(n,m)/(n! P(n,m)),
where P(n,m) counts integer partitions into m positive parts.

For a cycle-length profile mu=1^a1 2^a2 ... with m parts, define
z_mu=product(j^aj aj!).
The cycle-type formula gives

    R(n,m) = (1/P(n,m)) sum_{mu partitions n, length(mu)=m} m!/z_mu.

Define
B_m=max{|mu| : length(mu)=m and z_mu<=m!}.

This maximum is finite. For cycle lengths r_1,...,r_m,

    z_mu >= product(r_i) >= 1+sum(r_i-1)=n-m+1.

Therefore z_mu<=m! implies n<=m!+m-1.
The admissible set is nonempty because m singleton cycles have z_mu=m!.

For n>B_m, every summand m!/z_mu is strictly less than one.
Hence R(n,m)<1. In Case B only 2m<n<=B_m needs checking.

The exact search generates nondecreasing cycle lengths.
Appending a length j multiplies z by j times its new multiplicity.

At a prefix with current z and r remaining lengths, all future lengths
are at least j. Their final z is at least z*j^r.
Therefore z*j^r>m! safely excludes that branch and every larger j.

When one length remains, there are two possibilities:
- repeat the last length, including its multiplicity increment;
- choose a strictly larger new length, for which the largest feasible
  choice is floor(m!/z).
These two cases give the exact largest completion sum for that prefix.

Consequently the search computes the exact B_m, not merely a witness
or an upper-bound estimate.

The receipt records B_m, maximizing witnesses, and exact comparisons
m!c(n,m)-n!P(n,m) for every 2m<n<=B_m in the selected columns.

No equality in those finite ranges, together with the tail theorem,
excludes equality throughout Case B for the selected m values.

Status: computer-assisted fixed-column result.
The global question for arbitrarily large m remains open.
This is not proof-assistant certification or a novelty assertion.
