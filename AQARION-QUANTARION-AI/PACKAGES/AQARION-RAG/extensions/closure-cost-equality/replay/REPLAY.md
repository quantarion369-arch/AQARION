# Closure-cost equality extension — local replay

Date: 2026-10-14

## Result

Seed 0 and seed 1 both passed locally. All reported counts matched the
Claude handoff exactly.

## Dependency qualification

prof.py is a compatible local reconstruction, not the Claude-reported
dependency (SHA-256 829be3fc...). This is therefore a semantic replay,
not a hash-verified byte-for-byte replay.

## Commands

python3 equality_check.py 0 > local_eq0_reconstructed.txt
python3 equality_check.py 1 > local_eq1_reconstructed.txt

## Outputs

See local_eq0_reconstructed.txt and local_eq1_reconstructed.txt.

## Status

Paper-level proof complete.
Exact exhaustive n<=5 checks passed locally on both seeds.
Sampled n in {8,9}, construction, and empty-profile checks passed locally.
Not Lean-formalized.
