# JOIN-STABILITY Fixtures

Fixtures are explicit, version-controlled test inputs.

## Required fixture contents

Every future fixture must state:

- fixture identifier and version;
- finite carrier set;
- deterministic map T;
- equivalence relations E and F;
- whether each input relation is pullback-stable;
- the expected relation E join F;
- the expected stability result;
- the method used to establish the expected result;
- source revision and SHA-256 of the fixture file.

## Integrity rules

- Do not silently regenerate expected outputs from the implementation
  being tested.
- Do not overwrite an adversarial fixture merely because a test fails.
- Keep counterexamples as permanent regression fixtures.
- Record any change to a fixture as a reviewable change.

## Current status

This directory defines the fixture policy. No standalone fixture
dataset is asserted to exist merely because this README exists.
