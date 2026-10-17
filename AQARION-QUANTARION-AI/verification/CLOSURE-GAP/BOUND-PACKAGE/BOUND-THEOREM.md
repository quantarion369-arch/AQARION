# Closure-Gap General Upper Bound

Date: 2026-10-16
Scope: nonempty finite deterministic systems, arbitrary initial partitions.
Status: mathematical proof with finite computational checks.
Not claimed: novelty, sharpness for every n, Lean certification.

## 1. Original closure definitions

Let X have n >= 1 states, T: X -> X, and let
Pi = {B_0,...,B_(k-1)} partition X into nonempty blocks.
Work over Q.

Define the pullback operator U on Q^X by (Uf)(x)=f(T(x)).
Let

    W = span_Q { U^t 1_B : t >= 0, B in Pi },
    c_lin = dim_Q W.

A partition is T-stable if T maps each block into a single block.
Let Pi* be the coarsest T-stable refinement of Pi. Set

    c_part = |Pi*|,
    gap = c_part - c_lin.

## 2. Stable classes equal itinerary classes

Define x ~ y if, for every t >= 0, the states T^t(x) and T^t(y)
belong to the same block of Pi.

This equivalence relation refines Pi and is T-stable. Conversely,
states together in any T-stable refinement remain together under
every iterate, so they have identical Pi labels at every time.
Therefore the ~ classes form exactly Pi*.

Since U acts on an n-dimensional space, Cayley-Hamilton expresses
every U^t for t >= n as a linear combination of I,U,...,U^(n-1).
Consequently, agreement of every block indicator at times 0,...,n-1
implies agreement at all later times.

Define the binary matrix K with states as rows and time/block pairs
as columns:

    K[x,(t,b)] = 1 if T^t(x) belongs to B_b, otherwise 0,
    0 <= t < n, 0 <= b < k.

Its distinct rows correspond exactly to Pi* classes.
Delete duplicate rows to obtain M. Write

    m = number of rows of M = c_part <= n,
    r = rank_Q(M).

The columns of K span W by Cayley-Hamilton. Deleting duplicate rows
preserves rank. Hence r=c_lin and gap=m-r.

Every column is constant on Pi* classes, so r <= m and gap >= 0.
At any fixed time, summing all block-indicator columns gives the
all-ones column. Thus 1 lies in col(M), and r >= 1.

## 3. Independent-coordinate lemma

If a binary matrix A has m distinct rows, rank r, and the all-ones
column in its column space, then

    m <= 2^(r-1).

Proof: Extend the nonzero vector 1 to a column-space basis using
r-1 original columns c_1,...,c_(r-1). These columns are binary.

If two rows agree on those selected columns, they also agree on 1.
They therefore agree on every linear combination of the basis,
hence on every original column. Distinct rows cannot do this.

The projection onto the selected r-1 binary coordinates is
injective. There are at most 2^(r-1) coordinate patterns. QED.

This includes r=1, where there is one empty coordinate pattern.

The geometric ingredient is standard: an affine subspace of
dimension a meets a Boolean cube in at most 2^a vertices.
Reference: Nguyen Le Thanh Dung, "When lattice cubes meet affine
subspaces: a short note" (2019), Theorem 1, arXiv:1909.03542.
The elementary geometric lemma is not claimed new.

## 4. Main bound

For every system above,

    0 <= gap
       <= m-1-ceil(log2(m))
       <= n-1-ceil(log2(n)).

Proof: Section 3 gives m <= 2^(r-1), so
r >= 1+ceil(log2(m)). Subtract from m.

For positive integers t, define f(t)=t-1-ceil(log2(t)).
When t increases by one, ceil(log2(t)) increases by zero or one.
Thus f increases by one or zero, never decreases.
Since m <= n, f(m) <= f(n). QED.

For positive integer t, (t-1).bit_length() equals ceil(log2(t)).
The implementation therefore uses no floating-point logarithms.

## 5. Explicit attainment witnesses

Indices and partition labels are zero-based.
Equal labels denote membership in the same initial block.

n=5:
    T=(0,0,0,1,1)
    labels=(0,1,0,0,1)
    m=4, r=3, gap=1, state bound=1

n=6:
    T=(1,2,3,4,5,0)
    labels=(0,0,0,1,1,1)
    m=6, r=4, gap=2, state bound=2

n=7:
    T=(1,5,5,1,2,6,6)
    labels=(0,0,1,1,0,0,1)
    m=7, r=4, gap=3, state bound=3

n=8:
    T=(5,6,6,5,0,2,0,2)
    labels=(0,0,1,1,0,0,1,1)
    m=8, r=4, gap=4, state bound=4

These establish maximum gaps 1,2,3,4 at n=5,6,7,8 respectively,
when combined with the general upper bound.
In particular, gap four at seven states is impossible.
Only the six-state fixture is cyclic.
Sharpness for every n is not established here.

## 6. Computational evidence and limits

The verifier enumerates all maps and all set partitions through n=4.
Expected counts are n^n times Bell(n):

    n=1: 1
    n=2: 8
    n=3: 135
    n=4: 3840
    Total: 3984

The four larger witnesses are checked separately.
For each evaluated system the verifier checks:
- finite itinerary classes against stable partition refinement;
- rank invariance on adjoining the constant column;
- nonnegative gap;
- the binary-row inequality;
- class-count and state-count gap bounds.

It enforces enumeration counts and witness attainment.
The accompanying tests exercise malformed systems, incorrect
witnesses, incomplete counts, corrupted calculations, and output
overwrite protection.

A receipt records the full verifier-source SHA-256 and environment.
The hash identifies source bytes; it is not a signature.
The program never substitutes synthetic receipts.

These finite checks test the implementation, not the universal
theorem. The universal proof is Sections 1-4.
No registry promotion, novelty, Lean certification, or publication
approval follows automatically from a successful replay.
