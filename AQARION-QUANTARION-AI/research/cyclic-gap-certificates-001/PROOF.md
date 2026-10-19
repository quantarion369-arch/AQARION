# Cyclic-gap proof note

Status: written mathematics for review; not a formal proof or novelty claim.

Definitions: q is least rotational period. C has successive left rotations
as rows. Delta_circ=q-rank_Q(C); Delta_obs=q-rank_Q([C|1]).
For nonzero binary words the column sum is weight(w)*1, so the gaps agree.
For the zero word Delta_circ=1 and Delta_obs=0.

Classical foundation: rank_Q(C)=n-deg gcd(f,z^n-1), where
f=sum(w_j*z^j). The left-rotation matrix is a row permutation of a
conventional circulant. Rational and complex ranks agree.
Source: https://www.math.stonybrook.edu/~sorin/eprints/circulant.pdf

Active cyclotomic orders have total totient cost equal to rank.
Their least common multiple equals q, by Fourier inversion.
Order 1 is active for every nonzero binary word.
If distinct cyclotomic factors divide f, their monic product divides f
in Z[z]. Evaluating at 1 gives a necessary divisibility condition on weight.

Prime powers: for full period n=p^a, order p^a must be active.
Thus rank >= 1+phi(p^a), and gap <= p^(a-1)-1.
Proper-period words reduce to a smaller prime power and obey no larger bound.
Attainment: put m=p^(a-1), w=1^m 0^(n-m).
Its unique cyclic 0-to-1 transition gives full period.
Its polynomial (z^m-1)/(z-1) divides z^n-1 and has degree m-1.
Therefore G(p^a)=p^(a-1)-1 over nonconstant binary words.

Length 18: proper period is at most 9, so its gap is at most 8.
For full period, non-DC orders 2,3,6,9,18 have costs 1,2,2,6,6.
Without active order 18, order 9 and either 2 or 6 are necessary,
giving rank at least 8.
With active order 18, rank is at least 7. Rank 7 forces support {1,18}.
Then Phi_2 Phi_3 Phi_6 Phi_9 divides f, so 18 divides weight.
This contradicts a nonconstant binary weight between 1 and 17.
Thus rank is at least 8 and gap at most 10.
The executable certificate for 101111111010000000 establishes full period,
a nonzero 8-by-8 minor, and ten independent annihilated kernel columns.
Therefore its rank is 8 and, together with the upper bound, G(18)=10.

Support {1,2,9} cannot be binary and primitive:
write w_j=a_j+b*(-1)^j with a of period 9 and b nonzero.
Binary differences w_j-w_(j+9)=2b*(-1)^j force |2b|=1.
Every pair then sums to 1, forcing a_j=1/2 and eliminating order 9.
The witness instead realizes active orders {1,2,18}.

The executable checks finite arithmetic, not these general arguments
mechanically. No general formula for other composite lengths is claimed.
