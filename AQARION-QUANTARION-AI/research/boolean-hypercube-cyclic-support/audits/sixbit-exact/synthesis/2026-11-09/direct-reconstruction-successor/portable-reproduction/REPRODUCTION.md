# Portable reproduction

## Purpose

These additional files remove the direct odd-eight checkers' dependency
on a private home-directory input location. All archived execution
sources and reports remain unchanged.

The included six circuit files are byte-identical to the files bound
by the frozen six-flat report. An empty Base 1 file is intentional.

## Requirements

Python 3, Git, and SymPy. The original six-flat generator is not executed.

The commands below are optional reruns. They have NOT been executed by
assembling this package. They create new outputs and do not replace the
preserved execution receipts.

Use absolute paths for RELEASE, FROZEN, and OUTROOT.

RELEASE is the checkout containing this successor and validation runs.
FROZEN is a separate checkout whose HEAD is exactly:
5093e2af9db66567cba85caaff34220f1f8a0b35

For example, a user may deliberately create a detached Git worktree:
git -C "$RELEASE" worktree add --detach "$FROZEN" \
    5093e2af9db66567cba85caaff34220f1f8a0b35

This command changes Git worktree metadata. It is not run automatically.

## Set paths

Set RELEASE, FROZEN, and OUTROOT first. OUTROOT must exist and should be
outside the release evidence directories.

A="$RELEASE/AQARION-QUANTARION-AI/research/boolean-hypercube-cyclic-support/audits/sixbit-exact"
V="$A/validation-runs"
P="$A/synthesis/2026-11-09/direct-reconstruction-successor/portable-reproduction"

test "$(git -C "$FROZEN" rev-parse HEAD)" = \
    5093e2af9db66567cba85caaff34220f1f8a0b35

## Odd-eight direct completeness

PILOT_OUT="$(mktemp -d "$OUTROOT/base1-XXXXXXXX")"

HOME="$P/input-home" python3 -B -u \
    "$V/direct-odd8-base1-UsreglHb/check.py" \
    "$FROZEN" "$PILOT_OUT"

Require PASS_FOR_BASE1_LOCAL_COMPLETENESS before proceeding.

FIVE_OUT="$(mktemp -d "$OUTROOT/bases2to6-XXXXXXXX")"

HOME="$P/input-home" python3 -B -u \
    "$V/direct-odd8-bases2to6-b0hP586v/check.py" \
    "$FROZEN" "$PILOT_OUT" "$FIVE_OUT"

Require PASS_FOR_BASES_2_TO_6_LOCAL_COMPLETENESS.

HOME is overridden only for each child process. It supplies the expected
input layout; it does not change the user's shell HOME. The archived
scripts are not edited.

## Direction coverage

DIRECTION_OUT="$(mktemp -d "$OUTROOT/directions-XXXXXXXX")"

python3 -B -u \
    "$V/direction-coverage-zupjowEB/check_directions.py" \
    "$FROZEN" "$V/termux-verifier-Nua1RvUQ" "$DIRECTION_OUT"

Require PASS_FOR_DIRECTION_COVERAGE_ONLY.

This uses the archived bounded-verifier receipt and source as an input.
It does not execute that verifier's main program.

## Odd-twelve reconstruction

STAGE1_OUT="$(mktemp -d "$OUTROOT/odd12-stage1-XXXXXXXX")"

python3 -B -u \
    "$V/independent-odd12-stage1-T6tbrkW2/reconstruct.py" \
    "$STAGE1_OUT"

Require PASS_FOR_FIVEBIT_CANDIDATE_LAYER before proceeding.

STAGE2_OUT="$(mktemp -d "$OUTROOT/odd12-stage2-XXXXXXXX")"

python3 -B -u \
    "$V/independent-odd12-stage2-7muy2t5i/lift_all_hyperplanes.py" \
    "$FROZEN" "$STAGE1_OUT" "$STAGE2_OUT"

Require PASS_FOR_DIRECT_ODD12_RECONSTRUCTION and matching historical
support-set hashes.

## Evidence boundaries

New output directories are new executions, with their own hashes.
Timing, paths, source locations and report hashes can differ.

A reconstructed support-family digest should match its declared
canonical reference even when an execution-report digest differs.

This package does not supply external provenance authentication,
formal proof, peer review, or novelty certification.
