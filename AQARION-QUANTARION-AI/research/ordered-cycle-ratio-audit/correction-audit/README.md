# Correction audit: canonical model and finite regressions

## Purpose

This addendum preserves a successful Termux correction audit.
It does not replace or alter earlier published results.

The audited objects are pairs (sigma,pi), where pi partitions [n] into m
blocks and sigma preserves pi setwise. The statistic K counts cycles of
sigma, including fixed points. Sampling is uniform over valid pairs.

## Normalization

The total pair count is n!P(n,m).
Each integer block-size profile contributes n! pairs.
Therefore a sum of conditional moments over profiles is divided by P(n,m);
the common factor n! cancels. The earlier criticism of that normalization
was incorrect.

## Corrected table

(n,m)  pairs  mean      variance
(3,1)      6  11/6      17/36
(3,2)      6  5/2       1/4
(4,1)     24  25/12     95/144
(4,2)     48  61/24     455/576
(5,1)    120  137/60    2951/3600
(5,2)    240  77/24     407/576

Direct pair enumeration, stabilizer polynomials, and the coefficient
moment recurrence agree on these six cases.

## Additional executed checks

- 55 polynomial pairs through n=10.
- 220 exact comparisons for derivative orders 0,1,2,3.
- Harmonic mean/variance checks for m=1 through n=10.
- 176 falling-factorial profile comparisons.
- 176 root-search comparisons: d=1,...,8 and 2d<=n<=30.
- The only equality in that finite root-search domain is (n,m)=(3,2).

R(2,1)=1/2. No deficit-one boundary repair is needed.

R(n,n-3)=n(n-1)(n-3)/144 for n>=6.
The defective rising-factorial expression returns 4 at n=6,
where the correct value is 5/8. The negative control detects this.

The all-ones deficit profile has weight 2^d d!, not d!.
The proposed leading-term cutoff is rejected by R(4,2)=11/24<1.

## Evidence boundaries

The source and execution receipt are preserved byte-for-byte.
The receipt binds the executed source by SHA-256 and records its runtime.
This note was authored afterward at packaging time.

The complete defective proposal is not included here. The source contains
targeted negative-control expressions; it does not claim to preserve or
execute the full defective script.

A separately reported independent checker is not included or certified
by this package.

This is a finite correction/regression record, not a new global theorem.
Case A is not reopened. Global ratio classification remains open.
No proof-assistant certification or novelty claim is asserted.
