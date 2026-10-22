# Exact deficit-difference audit through n=500

## Scope and evidence

Two successful Termux executions are preserved byte-for-byte.
Both compare unsigned Stirling numbers with the partition-based denominator.
They use related exact recurrences, not independent global proofs.

The original implementation uses full tables and a cubic-loop construction
of the deficit-side partition counts. The optimized implementation uses a
quadratic partition table and rolling Stirling rows.

Each receipt records its source SHA-256. Packaging verifies those bindings.
No permutation census or deficit computation is repeated during packaging.

## Exact formulation

Let d=n-m, (n)_d=n!/(n-d)!, and P(n,m) count partitions into m positive parts.

    R(n,n-d) = c(n,n-d) / ((n)_d P(n,n-d)).
    Delta(n,d) = c(n,n-d) - (n)_d P(n,n-d).

The denominator is positive on 1<=m<=n. Therefore R=1 if and only if Delta=0.

Subtracting one from every positive part proves

    P(n,n-d) = p_{<=n-d}(d).

Partition conjugation converts the right side into partitions of d whose
largest part is at most n-d. Such counts satisfy

    Q(d,m) = Q(d,m-1) + Q(d-m,m),

where the second term is omitted for d<m and Q(0,m)=1.

## Recorded finite results

- Maximum n: 500.
- Pairs: 125250.
- Positive Delta: 114930.
- Negative Delta: 9819.
- Zero Delta: 501.
- Zeros: all (n,m)=(n,n), plus (3,2).
- Pairs with d>=3: 123753.
- Positive Delta with d>=3: 113938.
- Negative Delta with d>=3: 9815.
- Minimum absolute Delta with d>=3: 18 at (n,m,d,Delta)=(4,1,3,-18).
- Optimized special-formula and partition-bijection mismatches: none.

These finite results do not prove the global equality classification.

## Equality classification for deficits zero through three

Deficit zero:
    R(n,n)=1.

Deficit one:
    R(n,n-1)=(n-1)/2, n>=2.
Hence equality occurs exactly at n=3.

Deficit two:
    c(n,n-2)=2*binomial(n,3)+3*binomial(n,4).
For n>=4, P(n,n-2)=2, so
    R(n,n-2)=(n-2)(3n-1)/48.
Equality requires 3n^2-7n-46=0, whose discriminant 601 is not a square.
The remaining valid case n=3 has R(3,1)=1/3.

Deficit three:
Nontrivial cycle profiles are one 4-cycle, one 3-cycle with one 2-cycle,
or three 2-cycles. Therefore
    c(n,n-3)=6*binomial(n,4)+20*binomial(n,5)+15*binomial(n,6)
             =n^2(n-1)^2(n-2)(n-3)/48.
For n>=6, P(n,n-3)=3, so
    R(n,n-3)=n(n-1)(n-3)/144.
The numerator is strictly increasing for integers n>=6, and
    90 < 144 < 168
are its values at n=6, the equality target, and n=7.
Thus no integer n>=6 gives equality.
The remaining cases have R(4,1)=1/4 and R(5,2)=5/12.

Consequently the equality classification is proved for d=0,1,2,3.
The global question remains open for d>=4.

Delta does not have a uniform sign even for d=3:
    Delta(6,3)=-135.
    Delta(7,3)=105.

## Reproduction

Run the optimized source without modifying the preserved evidence:

    work="$(mktemp -d)"
    cp optimized/audit.py "$work/audit.py"
    python3 -B "$work/audit.py"

The original script hard-codes a home-directory output location and overwrites
its receipt there. It is preserved for provenance; use the optimized source
for a fresh reproduction.

## Publication scope

This supplement records finite exact verification and elementary proofs for
deficits at most three. It asserts no new global theorem, asymptotic remainder,
formal certification, or automatic change to project governance.

The original receipt's authorization fields are preserved as historical output,
not rewritten as part of packaging.

The parent manifest covers the original package files. This supplement's
manifest covers its own source, results, and report.
