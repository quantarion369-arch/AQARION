# Bounded modular resolver research contract

Supported inputs: at most 64 positive integer denominators,
each at most 64 bits; prime p between 2 and 97;
integer degree from zero through sequence length;
precision or adaptive cap from 1 through 32.

RESOLVED: nonzero normalized residue determines exact valuation.
UNRESOLVED_AT_CAP: zero residue supplies only precision-W lower bound.
INVALID: unsupported input, invariant failure, or claim mismatch.

Arithmetic uses unchanged function definitions extracted from
the hash-verified published modular-lifting source.
The original module top-level audit is not executed.

Claim verification recomputes the declared fixed-precision result.
It does not establish identity of an untrusted remote runtime.
No claim of production integration or formal certification is made.
