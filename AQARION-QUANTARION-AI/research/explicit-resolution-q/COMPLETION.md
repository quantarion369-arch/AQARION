# Explicit rational-resolution output checkpoint

Preserved from the supplied Termux completion output.
This is a transcription, not a fresh mathematical execution.

Core variables: A,E0,E1,E2,E3,B0,B1,B2,B3,C.
Z is reported as a free polynomial extension.

## Reported computation

- Input d1*d2: 35/35 PASS.
- d3: 35 explicit columns, degrees 6^8, 7^24, 8^3.
- d4: 14 explicit columns, degrees 8^6, 9^8.
- d5: one explicit column, degree 12.
- All consecutive compositions: PASS.
- All entries have positive weighted degree.
- Final map reported nonzero and injective.
- Total Betti sequence: (1,14,35,35,14,1).

Reported free-module shifts:

    F0 = P
    F1 = P(-3)^8 + P(-4)^6
    F2 = P(-4)^3 + P(-5)^24 + P(-6)^8
    F3 = P(-6)^8 + P(-7)^24 + P(-8)^3
    F4 = P(-8)^6 + P(-9)^8
    F5 = P(-12)

Alternating numerator:

    1 - 8t^3 - 3t^4 + 24t^5 - 24t^7 + 3t^8 + 8t^9 - t^12

The grading is weighted. The earlier all-variables-degree-one
Hilbert-series interpretation is not adopted.

## Proof dependencies

The reported global-exactness argument additionally uses prior ideal
identification, normality, canonical shift, Gorenstein duality, and
degree exhaustion. Zero compositions alone do not establish exactness.

This package does not include the full prior structural proofs, d1,
d2, definitions of the S basis, or the original construction program.
It does not assert novelty, characteristic independence, completed
Lean verification, or complete six-bit classification.

The two copied audit scripts are preserved separately; they are not
represented as the missing resolution-construction program.

The original run stated "No files written." This preservation step
writes its displayed results into repository files.
