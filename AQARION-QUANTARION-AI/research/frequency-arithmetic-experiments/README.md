# AQARION Arithmetic Boundary Experiments

## Purpose

Exact Python-integer research fixtures for transform representations,
modular reduction, bounded signed CRT reconstruction, and reference
composition. This is not a production cryptographic implementation.

## Selected experiments

| Unit | Recorded scope |
|---|---|
| ntt-boundary-inline-01 | Scalar-negacyclic and quadratic-component mechanics, direct-transform and product oracles |
| montgomery-reduction-01-lrPAGMfw | Generic REDC, encoding, multiplication, decoding, ranges, and fault controls |
| barrett-crt-01-mww3hgfy | Generic Barrett reduction, signed wrapper, bounded signed CRT, and integer products |
| whole-pipeline-reference-01-ye6mjc21 | Standalone scalar pipeline for linear and degree-16 negacyclic products |

The integration experiment is a separate reference implementation.
It does not import or establish adapter integration of the historical scripts.

## Recorded coverage

- NTT boundary: 24 full-negacyclic and 12 ML-KEM quadratic-component cases.
- Montgomery: 4568 REDC, 89 conversion, and 2361 product cases.
- Barrett/CRT: 4313 unsigned reductions, 2591 signed-wrapper cases,
  509 CRT integer cases, and 204 polynomial products.
- Reference integration: 32 linear and 32 negacyclic products,
  384 direct forward-transform comparisons.

Operation-call counts are not counts of independent test vectors.

## Montgomery radices are not transform lengths

The integration log's RADICES field means Montgomery radices:

| Modulus q | Montgomery R | Linear NTT length | Negacyclic degree | Root order |
|---|---|---|---|---|
| 97 | 128 | 32 | 16 | 32 |
| 193 | 256 | 32 | 16 | 32 |
| 257 | 512 | 32 | 16 | 32 |

R = 2**q.bit_length() is greater than q and coprime to q.
There is no requirement that R divide q-1.

The primitive order-32 roots are 19, 8, and 15, respectively.
The negacyclic path uses twisting and an order-16 cyclic transform.

## Arithmetic contracts

- Generic unsigned Barrett: 0 <= T < q*q; canonical output.
- Its signed wrapper is separately defined; consult the unit source.
- Generic unsigned REDC: 0 <= T < q*R; output represents T/R modulo q.
- Montgomery multiplication preserves encoding only with the declared scaling.
- Signed CRT requires Q > 2*C and a reconstructed value within [-C,C].
- Linear convolution requires sufficient zero padding.
- Negacyclic multiplication includes the sign change from X**16 = -1.

Different tests use different valid representative conventions.
Congruence alone does not establish canonicality.

## Reproduction

Python 3.8 or newer is required for the arithmetic scripts' modular inverses.
Consult each saved environment record for the actual execution environment.

From a selected experiment directory:

    python3 -u experiment.py

The selected experiment scripts emit their test results.
The original launcher created the surrounding evidence files.

For a replay, capture output and exit status in a separate destination.
Do not overwrite the original logs, environments, or checksum manifests.
Verify saved checksums before interpreting archived evidence.

## Negative-control interpretation

Distinguish numerical mutants, expected invalid-input/configuration
rejections, invariant-checker selftests, and unexpected execution errors.

The NTT unit's direct scalar DFT comparison covers the small
n=8, q=17 case. Its degree-256 scalar case is checked through round trips
and the schoolbook product oracle. Its quadratic components are also
checked by direct evaluation.

The preserved WRONG_INVERSE_SIGN_MUTANT label refers to substituting the
forward-transform mode for the inverse. That changes root direction and
omits inverse normalization together. It is a combined wrong-inverse-mode
control, not an isolated sign-only mutation.

The Montgomery inverse-sign control checks failure of the required
divisibility identity. Other controls include direct numerical misuse
witnesses and invalid-input/configuration checks. These control categories
are not presented as a uniform score of source-level mutants.

Several integration faults are caught by the final CRT coefficient bound.
That rejects the corrupted pipeline but does not uniquely diagnose its cause.

Unsigned-word-wrap examples are deliberately emulated negative controls.
They do not prove correctness of a native fixed-width implementation.

## Evidence and review limits

Preparation checks source identities, syntax, existing checksum records,
saved exits, and success markers. It does not rerun the experiments.

A checksum binds bytes; it is not an execution-authenticity certificate.
A newly generated collection manifest records the current artifact snapshot.

Full independent line-by-line review of every selected source is not asserted.
The sources, declared contracts, and recorded tests are available for scrutiny.

## Nonclaims

- No production PQC integration or complete ML-KEM/ML-DSA implementation.
- No ML-KEM quadratic-component integration in the whole-pipeline program.
- No NIST conformance or cryptographic-module validation.
- No fixed-width overflow-safety guarantee.
- No constant-time, side-channel, or cryptographic security claim.
- No performance superiority or cryptographic timing benchmark.
- No formal verification or established novelty claim.
- No independent reproduction by a second research team is asserted.

## Selection boundary

This publication selection comprises the four units listed above.
Additional fuzz reports, quantum follow-ups, graph experiments, backups,
working directories, and unrelated verification files are not included.

The additional fuzz report's control accounting requires separate review.
Its omission from this selection does not delete or invalidate its evidence.

## Source links

- Montgomery explanation:
  https://www.nayuki.io/page/montgomery-reduction-algorithm
- Barrett explanation:
  https://www.nayuki.io/page/barrett-reduction-algorithm
- Chinese remainder theorem:
  https://dlmf.nist.gov/27.15
- ML-KEM standard, for comparison rather than a conformance claim:
  https://csrc.nist.gov/pubs/fips/203/final
- ML-DSA standard, for comparison rather than a conformance claim:
  https://csrc.nist.gov/pubs/fips/204/final
