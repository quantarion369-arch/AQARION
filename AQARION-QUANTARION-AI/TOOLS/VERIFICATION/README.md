AQARION TOOLS — VERIFICATION

Reusable verification infrastructure for AQARION research.

Purpose

"VERIFICATION/" contains reusable mechanisms for independently checking computational research artifacts.

It is distinct from research-specific verification code.

Verification families

- "exact/" — exact finite computation and recomputation utilities.
- "independent/" — reconstructions that do not import the producer implementation when independence is required.
- "adversarial/" — hostile or mutation-based checks.
- "negative-controls/" — deliberately invalid inputs used to test verifier sensitivity.
- "certificates/" — machine-readable verification outputs where appropriate.
- "reports/" — human-readable audit reports.

Verification contract

A verifier should:

1. reconstruct or parse the defined input;
2. recompute the relevant result;
3. check explicit invariants;
4. compare against the claimed result where applicable;
5. emit "PASS" or "FAIL" from computation;
6. preserve metadata for reproduction.

Expected values may be fixtures.

They must not replace recomputation.

Independence

Where independent verification is claimed, the verifier must not silently depend on the implementation it is intended to check.

Negative controls

Mature verifiers should include deliberate failures such as:

- wrong hashes;
- forged PASS results;
- stale roots;
- missing execution;
- self-comparison;
- malformed fixtures;
- altered inputs;
- incorrect parameters.

Relationship to proof

"VERIFICATION" is not "MATHEMATICAL PROOF".

Exhaustive verification over a declared finite domain establishes evidence for that domain. It does not automatically establish a universal theorem outside it.

Status

DOCUMENTED — extraction from existing AQARION verification systems is the next implementation stage.
