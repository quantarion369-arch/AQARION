# AQARION audit scope

This is an independent exact-arithmetic reproduction.
It is not a Lean build, peer review, or formal verification of Section 6.

Paper:
https://arxiv.org/abs/2608.22564v1

All computations use Python's standard library.

Modular arithmetic discovers pivot columns only. Exact Fraction inversion,
nonzero exact determinants, and all-state rational closure checks establish
the D5/D6 linear certificates.

D5/D6 domain:
Sorted decimal digit multisets excluding the ten repdigits.
Leading zeroes are retained.
Weights count all fixed-width decimal strings:
n! / product of digit-count factorials.

F sorts K's output.
h = (maximum-minus-minimum, second-largest-minus-third-largest).

The two-cycle census tests exact period two and excludes fixed points.

Family 3 is counted once per unordered off-diagonal parameter pair.
Its output-count identity is verified coefficientwise.
Family membership does not prove Section 6's converse.

The no-nine reconstruction is conditional on preceding paper lemmas and their
necessary pair-count equations. Exact Fourier-Motzkin checks rational
feasibility with unbounded multiplicities, not a digit-length bound.

The even-base sweep is bounded evidence, not an all-base theorem or an
independent Lean axiom audit.

The 30-digit quadratic indicator is restricted to the two exhibited orbits.
It is not asserted to label every 30-digit transient globally.
D5/D6 indicators are checked on every state of the declared domains.

The entropy test concerns the definition's zero denominator.
It does not inspect Dahl's implementation or plots.

Full default:
- census n=2..13
- even bases 2..256
- Family 3 z=2..30
- Family 2 x=2..50
- 324 exact no-nine endpoint cases
- complete D5/D6 closures, partitions, projectors and basin certificates

Quick mode lowers only census/base/family bounds.
D5/D6 checks remain complete.

Files include:
receipt.json
exact matrix JSON files
full state CSV files
minor witnesses
cycle and family tables
source
SHA256SUMS

A .tar.gz archive is created beside the output directory.
Existing output folders are refused.

Read CSV digit strings as TEXT to avoid spreadsheet precision loss.
