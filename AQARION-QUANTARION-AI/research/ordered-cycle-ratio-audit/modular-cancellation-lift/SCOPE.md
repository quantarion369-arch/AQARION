# Modular cancellation lifting

This package preserves modular resolution of the 2212 tied-zero
rows in the published reciprocal-polynomial certificate dataset.
All are resolved at precision 9 in that finite domain.
The observed maximum depth is 8, not a universal bound.

The computation uses modular inverses and scaled elementary
symmetric recurrences, not exact rational arithmetic.
Saved exact valuations are comparison references only.

A separate 320-case check compares the modular calculation
with the telescoping identity for f(i)=i(i+1), k=1.

Elementary structural derivation:
E_1=sum(1/(i(i+1)), i=1,...,N)=N/(N+1).
W=max vp(i(i+1))=floor(log_p(N+1)), since consecutive
integers cannot both be divisible by p and the interval
contains every integer from 2 through N+1 as a factor.
Thus depth t=W+vp(N)-vp(N+1).
For N=p^h, W=h and t=2h, so depths are unbounded.
The N=32, p=2 control has depth 10.

These reciprocal-sum results are not automatically canonical
ratio certificates. No new global classification is asserted.
The layer decomposition has established literature precedent;
no novelty clearance is claimed.

Executed source retains its original local dependency path.
This package does not claim standalone portable replay.
Formal certification and novelty clearance remain OPEN.
Promotion remains false.
