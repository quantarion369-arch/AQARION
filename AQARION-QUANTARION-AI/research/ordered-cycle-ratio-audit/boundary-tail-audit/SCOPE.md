# Boundary and eventual-decrease computational audit

## Documentation provenance

This scope note was prepared after the original execution.
It was not present during that run and is not bound by its original receipt.
The five original evidence files are preserved byte-for-byte.

## Definitions

c(n,m) is the unsigned Stirling number of the first kind.
P(n,m) counts partitions of n into exactly m positive parts.

    R(n,m) = m! c(n,m) / (n! P(n,m)).

The source uses exact integers and fractions, with tables through
n=90 and m=16. It has no project-local imports.

## Exact tested scope

- Initial boundary values R(2m+1,m): m=1 through 5.
- Boundary recurrence, Newton bound, corrected tau bound,
  numerator growth, denominator identity, and ratio growth:
  m=2 through 14.
- Ordinary partition growth: k=2 through 89.
- Harmonic q bound, fixed-m ratio recurrence, and partition
  injection consequence: m=2 through 8, m<=n<=89.
  Each group contains 595 checks.
- Eventual-decrease implication: the 203 pairs in that grid
  satisfying H(n-1)-H(m-2)>m-1.
- Negative control: three exact checks involving n=31,32 and m=15.

The preserved receipt reports PASS, 2162 checks, and the execution
record reports exit code zero with empty stderr.

## Negative control

    R(32,15)/R(31,15)
      = 163550075392585167941/163320823394942693408
      > 1.

Both ratios are above one. This refutes blanket strict decrease
throughout Case B; it does not refute a one-crossing property.

## Evidence limits

The finite checks do not alone prove the displayed inequalities
for all parameters. This package is a computational audit, not
a substitute for general derivations or formal certification.

No global Case B classification, novelty clearance, or formal
certification is claimed.

This package is separate from m15-complete and case-b-padic-family.
Do not aggregate their check counts into one experiment.

## Reproduction caution

audit.py writes receipt.json in its current working directory.
To preserve this evidence package, reproduce in a separate scratch
directory rather than overwriting the preserved receipt.

stdout.txt retains the original execution-directory path.
SHA256SUMS binds the five original files and this new scope note.
