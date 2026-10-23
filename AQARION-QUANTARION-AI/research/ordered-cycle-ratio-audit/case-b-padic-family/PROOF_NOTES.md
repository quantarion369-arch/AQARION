# Case B prime-adic nonintegrality family

## Definitions

c(n,m) is the unsigned Stirling number of the first kind.
P(n,m) counts partitions of n into exactly m positive parts.

    R(n,m) = m! c(n,m) / (n! P(n,m)).

## Proposition

Let j >= 1 be an integer and p > 2j+1 be prime. Set

    n = (2j+1)p
    m = jp+j+1.

Then n > 2m and

    v_p(R(n,m)) = -(j+1) - v_p(P(n,m)) < 0.

Thus R is nonintegral and cannot equal 1. This does not classify
R as above or below 1 in the ordinary real ordering.

No prime power q^r, with q prime and integer r >= 1, satisfies

    (m-1)q^r <= n-1 < m q^r.

Only this witness criterion is excluded.

## Elementary proof

Put a = 2j+1. Then a < p, and p >= 2j+3.

Reducing the unsigned Stirling generating polynomial modulo p gives

    product_(i=0)^(ap-1) (x+i) == (x^p-x)^a
      = sum_(t=0)^a (-1)^(a-t) binom(a,t) x^(a+t(p-1)).

Since m = a+j(p-1), coefficient extraction yields

    c(n,m) == (-1)^(j+1) binom(2j+1,j) (mod p).

The binomial coefficient is a p-adic unit because 2j+1 < p.
Hence v_p(c(n,m)) = 0.

Also m = jp+(j+1), with 0 < j+1 < p, and m < n < p^2.
Therefore Legendre's formula gives

    v_p(m!) = j
    v_p(n!) = 2j+1.

Since P(n,m) is a positive integer, valuation additivity gives

    v_p(R) = j - (2j+1) - v_p(P)
           = -(j+1) - v_p(P) < 0.

The Case B condition follows from

    n-2m = p-2j-2 >= 1.

The witness criterion is equivalent to

    (n-1)/m < q^r <= (n-1)/(m-1).

The endpoint calculations are

    n-1-2m = p-2j-3 >= 0
    3(m-1)-(n-1) = (j-1)p+3j+1 > 0.

Thus any witness would require 2 < q^r < 3, impossible for an integer.

If p = 2j+3 is prime, n-1 = 2m. The strict lower inequality
excludes q^r = 2; the original criterion would require 2m < 2m.

## Computational evidence

Run from this directory:

    python3 -I case_b_family_test.py

The preserved Termux receipt reports PASS: 367 checks, 24 pairs,
1 <= j <= 6, primes p <= 19, and four endpoint cases.
The test cross-checks partitions using two different recurrences.

The bounded test corroborates the proof; enumeration does not prove
the infinite statement. Formal certification remains OPEN.

The receipt payload hash uses sorted compact JSON after removing
receipt_payload_sha256. SHA256SUMS contains ordinary file hashes.

## Scope and separation

No global classification, real-order classification, novelty claim,
or exclusion of other witness criteria is asserted.

This package is separate from the Case A e5c-proof-regression package,
the m=15 classification and its 378-check receipt, and the pending
README/dashboard repair. Do not aggregate their check counts.

The proof has no external theorem dependency. Hong-Qiu is comparison
literature, not a prerequisite. No stronger congruence is asserted.
