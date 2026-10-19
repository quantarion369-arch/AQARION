# PB-CORE-006 / PB-ASYM-001 - Asymptotic Proof Audit

Date: 2026-10-19
Artifact type: mathematical proof draft for independent review
Asymptotic subject: PB-ASYM-001
Counting dependency: PB-CORE-006
Repository baseline: 0d9b2933aa1cf57d853418efa56ea82738273b9f

## Status and claim boundary

A leading-equivalent proof argument is supplied below.
Independent mathematical review remains pending.
No Lean compilation, new numerical execution, CI result, novelty
determination, certification, or publication promotion is claimed.
This note does not modify governing theorem or receipt statuses.

The analytic argument concerns the explicitly defined weighted sum.
Interpreting it as an asymptotic count of pullback-fixed equivalences
depends separately on the exact PB-CORE-006 aggregate identity.

## 1. Definitions and proposed conclusion

Let p(k) be the integer partition function, not the Bell number.

For positive integers n and 1 <= k <= n, define

    q(n,k) = product over 1 <= j <= k-1 of (1-j/n),
    W(n)   = sum over 1 <= k <= n of k*p(k)*q(n,k).

The empty product is 1. The k=n term is included exactly.

Set

    a     = pi*sqrt(2/3),
    alpha = (a/2)^(2/3),
    C     = (3/2)*alpha^2.

The conclusion of the argument is

    W(n) ~ (sqrt(pi)/6)*exp(-a^2/24)
           *sqrt(n)*exp(C*n^(1/3)).

Since a^2/24 = pi^2/36, these constant expressions agree.

The exact aggregate normalization under review is

    A(n) = n^(n-1)*W(n).

It follows algebraically from

    A(n) = sum over 1 <= k < n of
           binom(n,k)*k!*p(k)*k*n^(n-k-1)
           + n!*p(n).

No product expansion near k=n is used below.

## 2. Classical analytic input

Use the Hardy-Ramanujan leading equivalent

    p(k) ~ exp(a*sqrt(k))/(4*sqrt(3)*k).

Consequently,

    k*p(k) = exp(a*sqrt(k))/(4*sqrt(3))*(1+epsilon(k)),

where epsilon(k) tends to zero.

There exists a finite constant B such that

    k*p(k) <= B*exp(a*sqrt(k))

for every positive integer k: use the equivalent for sufficiently
large k, then enlarge B to cover the remaining finite set.

Classical source:
G. H. Hardy and S. Ramanujan,
"Asymptotic Formulae in Combinatory Analysis" (1918).
DOI: 10.1112/plms/s2-17.1.75.

The partition equivalent is an external classical input, not a
new result of AQARION.

## 3. Saddle and localization window

For real x>0 define

    f_n(x) = a*sqrt(x)-x^2/(2*n).

Its unique stationary point is

    k_star = alpha*n^(2/3).

Direct differentiation gives

    f_n(k_star)   = C*n^(1/3),
    f_n''(k_star) = -3/(2*n),
    f_n'''(x)     = 3*a/(8*x^(5/2)).

Choose the integer window

    I_n = {k: 1 <= k <= n,
           abs(k-k_star) <= sqrt(n)*log(n)}.

All limiting arguments concern sufficiently large n.
The relative window width is n^(-1/6)*log(n), which tends to zero.
Thus k/(alpha*n^(2/3)) tends uniformly to 1 on I_n.

In particular, the minimum index in I_n tends to infinity.
Therefore epsilon(k) tends uniformly to zero on I_n.
A quantitative partition-error estimate is not required for this
leading equivalent.

## 4. Uniform logarithmic product estimate

For 0 <= u <= 1/2, the logarithmic series gives

    abs(log(1-u)+u+u^2/2) <= (2/3)*u^3.

Indeed, bound the sum over powers r>=3 by
u^3/(3*(1-u)).

Eventually k/n < 1/2 throughout I_n. Summing this estimate gives

    log q(n,k)
      = -k*(k-1)/(2*n)
        -k*(k-1)*(2*k-1)/(12*n^2)
        + O(k^4/n^3)

uniformly on I_n.

Rearranging,

    log q(n,k)
      = -k^2/(2*n)-k^3/(6*n^2)
        + O(k/n+k^2/n^2+k^4/n^3).

The error tends uniformly to zero because k is of order n^(2/3).

Also, uniformly on I_n,

    k^3/(6*n^2) = alpha^3/6 + o(1) = a^2/24 + o(1).

Combining with the partition equivalent,

    k*p(k)*q(n,k)
      = exp(-a^2/24)/(4*sqrt(3))
        *exp(f_n(k))*(1+o(1))

uniformly on I_n.

## 5. Uniform local exponent expansion

For h=k-k_star within the chosen window, Taylor's theorem gives

    f_n(k)
      = C*n^(1/3)-3*h^2/(4*n)
        + O(n^(-1/6)*(log(n))^3).

To see the remainder, f_n''' is O(n^(-5/3)) throughout the
interval between k and k_star, while
abs(h)^3 <= n^(3/2)*(log(n))^3.

The remainder tends uniformly to zero.

## 6. Shifted discrete Gaussian

The lattice spacing after rescaling by sqrt(n) is 1/sqrt(n).
The fractional part of k_star only shifts that lattice.

For every fixed M, the Gaussian Riemann sums on [-M,M] converge
uniformly in this shift by uniform continuity.

Their tails are uniformly negligible as M tends to infinity.
For example, on either monotone Gaussian tail, a mesh-weighted
sum is bounded by its first rectangle plus the corresponding
tail integral, with an endpoint discrepancy of at most one mesh.

Since the window expands to abs(u) <= log(n), it follows that

    (1/sqrt(n))*sum over k in I_n of
        exp(-3*(k-k_star)^2/(4*n))
      -> integral over all real u of exp(-3*u^2/4) du
       = sqrt(4*pi/3).

Thus the central contribution is

    (sqrt(pi)/6)*exp(-a^2/24)
    *sqrt(n)*exp(C*n^(1/3))*(1+o(1)).

The Gaussian factor is sqrt(4*pi*n/3), not sqrt(pi*n).

## 7. Global tails, including the endpoint

For every 1 <= k <= n, log(1-u) <= -u gives

    log q(n,k)
      <= -k*(k-1)/(2*n)
      <= -k^2/(2*n)+1/2.

Consequently,

    k*p(k)*q(n,k) <= B*exp(1/2)*exp(f_n(k)).

Globally for x>0,

    f_n''(x) = -a/(4*x^(3/2))-1/n <= -1/n.

Strong concavity and f_n'(k_star)=0 therefore imply

    f_n(k)
      <= C*n^(1/3)-(k-k_star)^2/(2*n).

Outside I_n, every summand is at most

    B*exp(1/2)*exp(C*n^(1/3)-(log(n))^2/2).

There are at most n terms. Relative to
sqrt(n)*exp(C*n^(1/3)), their sum is bounded by

    B*exp(1/2)*sqrt(n)*exp(-(log(n))^2/2),

which tends to zero.

This single bound covers small indices, large indices, and k=n.
It requires no local product expansion outside I_n.

## 8. Conclusion and aggregate conversion

The central estimate and negligible tails establish the displayed
weighted-sum equivalent within this proof argument:

    W(n) ~ (sqrt(pi)/6)*exp(-pi^2/36)
           *sqrt(n)*exp(C*n^(1/3)).

If the exact aggregate identity A(n)=n^(n-1)*W(n) is adopted,
Stirling's formula gives

    A(n) ~ exp(-pi^2/36)/(6*sqrt(2))
           *(n!*exp(n)/n)*exp(C*n^(1/3)).

Neither this implication nor the analytic argument establishes the
independent combinatorial identity or a novelty claim.

## 9. Required independent review

Reviewers should check:

- The exact normalization and endpoint convention.
- Uniformity of the product remainder on I_n.
- The shifted Gaussian sum and its tail justification.
- The strong-concavity inequality on the whole positive axis.
- The distinction between the analytic sum and its counting meaning.
- The distinction between proof review and formal verification.

No quantitative convergence rate or next asymptotic coefficient
is claimed. No unresolved lemma is intentionally hidden; independent
review may identify a gap requiring revision.

## 10. Evidence and governance separation

The published bounded regression is located at

    tests/regression_pb006_relation_sets.py

It tests all maps through n=4 against an independent relation oracle.
It is separate computational evidence, not a premise of this
analytic proof and not a substitute for proof review.

Existing theorem statuses, receipts, CI configuration, Lean status,
C4 disposition, and promotion settings are unchanged by this note.

Status: PROOF-DRAFT / INDEPENDENT-REVIEW-PENDING.
