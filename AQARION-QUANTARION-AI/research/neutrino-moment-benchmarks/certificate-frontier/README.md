# Neutrino moment-certificate frontier

## Scope
Compare 38 explicit nonnegative polynomial weights for
G(mu)=1/10-3*mu/10+mu^3/2 on [-1,1].
Three declared moment-error profiles are compared at budgets
11, 13, 20, and 37. These are illustrative error models,
not measured instrument noise.

## Evidence
The user reported a successful Ubuntu/Termux Python-FLINT 0.9.0
run with 321 checks and exit status zero.
receipts/user-reported-frontier.json is a structured transcription
from the supplied chat output, not an original captured log.

frontier_check.py is a replay implementation assembled from the
accepted chat command. It is syntax-checked during preparation,
and a file-bound replay has now been attempted; see receipts/file-bound-replay.json for its status.
No execution-time source hash was recorded in the earlier run.

## Reproduction
Use a Python environment containing python-flint.
Run: python -B -I frontier_check.py
The previously successful interpreter was:
  /root/.venvs/aqarion-flint-090/bin/python
That path is environment-specific, not a portable requirement.

## Interpretation
Thresholds require strict inequality.
Nonnegativity follows from the explicit factored constructions.
The best candidate depends on both the moment budget and error profile.
Best in this finite catalog does not mean globally optimal.

This package does not establish nonlinear neutrino evolution,
physical-unit growth rates, interval-certified dispersion roots,
a Lean proof, or novelty of positive-polynomial crossing tests.

## Literature
Johns and Nagakura, Fast flavor instabilities and the search for
neutrino angular crossings:
https://arxiv.org/abs/2104.04106

## Preservation
SHA256SUMS fingerprints the files prepared in this package.
It does not retrospectively authenticate the earlier execution.
No RAG integration, Lean integration, staging, commit, or push
is performed by the preparation command.

## File-bound replay
The saved source bytes were supplied to Ubuntu Python on stdin.
The source hash, raw stdout/stderr hashes, exit code, and comparison
status are preserved in receipts/file-bound-replay.json.
The earlier chat transcription remains separately labeled.
