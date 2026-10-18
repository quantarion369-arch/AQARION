# Exact Quotient Agreement

Bounded computational cross-checks for finite deterministic dynamics,
partition-compatible quotients, and block-constant observable defects.

## Recorded execution

Executed in the maintainer's phone-based Ubuntu environment using
Python 3.14.4.

## Baseline experiment

Directory: quotient-audit-001

For every map and every set partition on labeled state spaces of
sizes 1 through 4, compare:

1. Pairwise forward compatibility.
2. Direct construction of a well-defined quotient map.
3. Exact vanishing of the observable defect.

| States | Map-partition cases | Compatible | Incompatible |
|---|---:|---:|---:|
| 1 | 1 | 1 | 0 |
| 2 | 8 | 8 | 0 |
| 3 | 135 | 99 | 36 |
| 4 | 3840 | 1728 | 2112 |
| Total | 3984 | 1836 | 2148 |

All three formulations agreed on every case.
The experiment returned exit status 0.

## Mathematical conventions

Observables are column vectors.

K[i,j] = 1 exactly when j = T[i], so (Kf)[i] = f[T[i]].

P is the block-averaging orthogonal projection for the counting
inner product.

D = (I-P)KP = KP-PKP.

Matrix calculations use exact rational arithmetic without a
floating-point zero tolerance.

## Follow-up experiment

Directory: quotient-followup-002

The follow-up imports the baseline and checks its source hash
against the recorded baseline report.

A nontrivial successful quotient was checked:

- Transition map: [2, 3, 0, 1].
- Block labels: [0, 0, 1, 1].
- Quotient map: [1, 0].
- Observable defect: zero.

Three deliberately incorrect implementations were tested across
all 144 map-partition pairs on state spaces of sizes 1 through 3.

| Mutation | Disagreements with the correct baseline |
|---|---:|
| Inspect only one representative per block | 36 |
| Transpose the specified Koopman matrix | 59 |
| Omit block-size normalization from P | 76 |

All three mutations were detected.
The experiment returned exit status 0.

The disagreement counts overlap and must not be added as distinct cases.
Matrices labeled D in mutation witnesses are the correct baseline
defects, not the mutated operators' defects.

## Reproduce

Keep both experiment directories as siblings.

From this directory, run:

    python3 quotient-audit-001/quotient_audit.py
    python3 quotient-followup-002/mutation_audit.py

These commands print new reports without replacing preserved reports.
The follow-up requires the existing baseline report.json.

Check preserved file contents:

    (cd quotient-audit-001 && sha256sum -c SHA256SUMS)
    (cd quotient-followup-002 && sha256sum -c SHA256SUMS)

Only the Python standard library is required.

## Preserved artifacts

Each experiment directory contains six files:

- Python source.
- report.json.
- stderr.txt.
- exit-status.txt.
- environment.txt.
- SHA256SUMS.

The checksum manifest covers the other five files in its directory.
The environment record is minimal, not a complete reconstruction.

## Scope and limitations

This package records bounded implementation cross-checks and detection
of three selected implementation errors.

It is not a universal proof, Lean proof, completeness result,
independent implementation audit, or novelty claim.

The implementations share input conventions and computational
infrastructure.

Checksums establish consistency with the recorded manifest, not
authenticity or mathematical correctness.

No real genomic data or neutrino observations are analyzed here.
