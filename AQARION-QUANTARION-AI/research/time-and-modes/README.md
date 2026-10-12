# AQARION Timing and Modes — Research Checkpoint 0.1

## Purpose

This package separates three research activities:

1. Validate a past-only estimator for tracked geometric signals.
2. Reproduce known resonance responses in mechanical and electrical models.
3. Specify a proposed pilot study of vortex-ring overtaking prediction.

It does not claim a unified physical mechanism across circuits, fluids,
stars, or cosmology.

## Research questions

### Software question

Do features computed at a prediction time remain unchanged when later
samples are modified or removed?

### Model question

Do numerical mechanical-displacement and series-RLC-current sweeps
agree with their analytical steady-state responses?

### Physical question — OPEN

Do past-only ring-radius asymmetry and its trailing rate of change
improve held-out prediction of future overtaking beyond motion and size?

No measured water-ring dataset is included.

## Contents

- README.md
- claim-status.csv
- causal_estimator.py
- test_causal_estimator.py
- timing_models.py
- vortex_protocol.json
- priority-review.md

## Dependencies

Python 3.10 or later.
Third-party dependencies: NumPy and SciPy.

The estimator requires NumPy.
The model sweep requires NumPy and SciPy.
Tests use Python's standard-library unittest framework.

No OpenCV, scikit-learn, plotting library, or hardware interface is needed.

Record actual Python, NumPy, and SciPy versions from each execution.
No particular dependency-version combination is certified by this release.

## Save and run

Save all seven files in one new folder.
Do not paste Markdown fences into the files.
Run commands from that folder.

Check syntax:

    python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py

Run estimator tests:

    python -m unittest -v test_causal_estimator

Run model sweeps:

    python timing_models.py

The model script creates a new uniquely named output directory in the
current folder. It does not overwrite an existing output directory.

Generated outputs:

- mechanical_sweep.csv
- rlc_current_sweep.csv
- run-receipt.json
- SHA256SUMS

SHA256SUMS records hashes of the CSVs, receipt, and model-script source.
It does not hash itself.

## Execution status

Earlier implementations of the mechanical and RLC sweeps were executed
in the accompanying conversation.

Earlier synthetic checks reproduced:
- the centered-difference future-spike defect;
- past-only protection in that example;
- the supplied synthetic geometry values.

This exact packaged implementation:
- supplied inline;
- not yet executed as a package;
- not independently replayed.

Do not transfer execution status from earlier code to this package without
running it.

## Model definitions

Mechanical model:

    x'' + 2*zeta*omega0*x' + omega0^2*x = F0*cos(omega_d*t)

Mass is set to 1 in model units.

Electrical model:

    q' = i
    i' = (V0*cos(omega_d*t) - R*i - q/C)/L

Current is measured in amperes.
Charge is measured in coulombs.

The illustrative circuit parameters are chosen to map its charge equation
to the mechanical displacement equation. Therefore this comparison is
structural model validation, not independent experimental evidence.

## Causal estimator

For each sample, estimate slope by a least-squares line fitted only to
samples within a trailing time window, ending at that sample.

Features at t0 use the last frame at or before t0.

The estimator:
- does not use future samples;
- does not interpolate using future frames;
- returns NaN when past history is insufficient;
- reports the selected frame timestamp.

Causality of the complete video pipeline is not established by these
function tests. Tracking and preprocessing must also be audited.

## Interpretation limits

A successful model sweep validates an implementation of a known equation.

It does not establish:
- new resonance physics;
- equal delivered energy at different forcing frequencies;
- real vortex-ring predictive performance;
- helicity conservation;
- reconnection from a side-view overlap;
- Möbius or Klein topology;
- a celestial or cosmological mechanism.

Fixed forcing amplitude is not fixed delivered energy.

## Physical protocol status

vortex_protocol.json is a DRAFT FOR APPARATUS DEVELOPMENT.

The full experimental protocol must be frozen after development trials
and before collecting the evaluation dataset.

Do not use development trials as held-out confirmation.

## Evidence practice

Preserve:
- source files;
- exact commands;
- dependency versions;
- stdout/stderr and exit status;
- raw measurements;
- trial exclusions and reasons;
- split assignments;
- output hashes;
- changes from previous versions.

A file hash identifies bytes. It does not establish correctness.

## Negative and null results

Report a failed estimator test, poor ring visibility, ambiguous trials,
or no predictive improvement as results rather than concealing them.

Priority and performance are separate questions.
