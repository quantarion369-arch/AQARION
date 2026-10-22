# Ordered-cycle ratio audit

## Scope

A reproducible finite verification of classical permutation-cycle identities
for 1 <= n <= 10. This is not a claim of a new Stirling-number theorem.

The tested model counts permutations together with an ordering of their cycles.
The original, separately discussed `cycle_count` implementation is not imported
or certified by this package.

This package does not establish the AQARION fourth-order asymptotic expansion,
a uniform saddle-point remainder, Lean certification, or a change to C4 status.

## Definitions

- c(n,m): permutations of n labels with exactly m cycles.
- O(n,m): the same permutations with their m cycles ordered.
- P(n,m): integer partitions of n into exactly m positive parts.
- R(n,m) = O(n,m)/(n! P(n,m)), for 1 <= m <= n.

Cycles are identified under cyclic rotation. Ordering the separate cycles does
not choose a starting point within each cycle.

## Ordered-cycle identity

Each permutation with m cycles admits exactly m! orders of those cycles.
Therefore O(n,m) = m! c(n,m).

The Stirling recurrence is

    c(n,m) = (n-1)c(n-1,m) + c(n-1,m-1).

Label n either joins one of the n-1 insertion positions in existing cycles or
forms a singleton cycle. Multiplication by m! gives

    O(n,m) = (n-1)O(n-1,m) + m O(n-1,m-1).

## Exact cycle-length distributions

Write a profile as lambda = 1^a1 2^a2 ..., where sum(j aj)=n and sum(aj)=m.
Set

    z_lambda = product(j^aj aj!).

There are n!/z_lambda permutations with this profile: divide n! by the
rotations of each cycle and by permutations of equal-length cycles.

Consequently

    c(n,m) = n! sum_{lambda partitions n, length(lambda)=m} 1/z_lambda,

and

    R(n,m) = (m!/P(n,m)) sum_{lambda partitions n, length(lambda)=m} 1/z_lambda.

The ratio is a uniform average of m!/z_lambda over integer-partition profiles.
That uniform profile distribution differs from the cycle-type distribution of
a uniform random permutation, whose probability at lambda is 1/z_lambda.

## Meaning of the comparison count

The quantity n! P(n,m) counts pairs (sigma,Pi), where sigma is a permutation
and Pi is a sigma-invariant set partition with m blocks.

For a block-size profile with aj blocks of size j, there are

    n! / product((j!)^aj aj!)

set partitions. Each admits product(aj! (j!)^aj) preserving permutations.
Their product is n! for each profile; summing over P(n,m) profiles proves
the count.

These pairs are not the same objects as ordered permutation cycles.

## Ratio recurrence

Integer partitions satisfy

    P(n,m) = P(n-1,m-1) + P(n-m,m).

For valid n,m,

    R(n,m) =
        (n-1)P(n-1,m)R(n-1,m)/(n P(n,m))
        + m P(n-1,m-1)R(n-1,m-1)/(n P(n,m)).

Terms with zero partition count are omitted; R(0,0)=1.
The coefficients need not sum to one.

## Special cases

    R(n,1)   = 1/n.
    R(n,n)   = 1.
    R(n,n-1) = (n-1)/2,                    n >= 2.
    R(n,n-2) = (n-2)(3n-1)/48,             n >= 4.

The last identity follows from

    c(n,n-2) = 2 binomial(n,3) + 3 binomial(n,4),

corresponding to a 3-cycle or two transpositions, and P(n,n-2)=2.

## Generating functions

With L(x)=-log(1-x),

    sum_n O(n,m)x^n/n! = L(x)^m,
    sum_n P(n,m)x^n = x^m / product_{j=1}^m (1-x^j).

If T_n=sum_m O(n,m) and T_0=1, then

    sum_n T_n x^n/n! = 1/(1+log(1-x)),
    T_n = sum_{j=1}^n binomial(n,j)(j-1)! T_{n-j}.

## Executed verification

The preserved receipt reports exhaustive permutation enumeration through n=10,
55 ratio entries, 138 cycle profiles, and all exact assertions passing.
Across n=1,...,10, exhaustive enumeration covers 4,037,913 permutations.

Within this finite range R=1 exactly at (n,n) and at (3,2).
No all-n classification of off-diagonal equality cases is asserted.

The source independently enumerates permutations and compares their observed
cycle profiles with the exact profile formulas. It also checks ratio and
ordered-cycle recurrences, profile averages, special cases, and row sums.
The decimal CSV column is display-only; ratios use exact rational arithmetic.

## Reproduction

From this package directory, use a fresh output directory:

    python3 -B audit.py --max-n 10 --brute-max 10 --out /path/to/fresh-output

The script uses only the Python standard library. It writes outputs to the
specified directory. Compare the exact fields and counts; decimal formatting
is not the mathematical evidence.

## Evidence and provenance

- audit.py: byte-preserved source inspected after the successful Termux run.
- results/ratios.csv: preserved original 55-row output.
- results/cycle_length_distributions.csv: preserved original 138-row output.
- results/receipt.json: preserved original execution summary.
- manifest.json: hashes and packaging metadata recorded afterward.

The original receipt did not record a source hash, timestamp, or Python version.
The manifest binds the collected source and outputs at packaging time; it is
not a retroactive claim of cryptographic source binding at execution time.
The packaging validation checks hashes and table consistency without repeating
permutation enumeration.

## Classical background

- Unsigned Stirling numbers and permutation cycles:
  https://www.whitman.edu/mathematics/cgt_online/book/section01.08.html
- Integer partitions and generating functions:
  https://math.berkeley.edu/~mhaiman/math172-spring10/partitions.pdf

No license is added by this package; the repository's applicable terms remain
unchanged.
