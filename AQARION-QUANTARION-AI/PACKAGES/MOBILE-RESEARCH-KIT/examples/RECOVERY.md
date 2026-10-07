# AQ-QUADRATIC-CONTRACT-ATLAS — Recovery Receipt

Date: 2026-10-07

## Original source recovered

examples/quadratic_contract_atlas.py

Recovered consecutively from Termux output:
- Lines 1–240.
- Final entry point at lines 241–242.
- Terminal prompts and duplicate pasted output removed.
- Formatting normalized.
- Original supplied logic preserved.
- No execution performed during this recovery.
- Byte-for-byte identity and original hashes not verified.

## Source-defined experiment

Reference:
    f(x) = x*x + x

Candidate:
    g(x) = c*x*x + a*x + b

Default moduli:
    2, 3, 4, 5, 6, 8

Default coefficient bound:
    3

Candidate coefficients:
    c, a, b each range from -bound through +bound.

Compared routes:
- Complete residue-domain evaluation.
- Algebraic classifier.
- Evaluation at inputs 0, 1, 2.
- Strict coefficient classifier.

Saved row evidence:
- Acceptance flags.
- Primary-route agreement.
- Strict false-rejection and false-acceptance flags.
- First counterexample.
- Counterexample replay result.
- Full residue comparison certificate for accepted-not-strict cases.

Outputs:
- atlas.json
- atlas.md

Exit codes:
- 0: primary routes agree and consistency checks pass.
- 1: disagreement or consistency failure.
- 2: invalid input or output failure.

Output directory:
- Must not already exist.
- The program does not overwrite an existing directory.

## Saved evidence fragments recovered

Candidate (c, a, b) = (0, 2, 0):
- Complete acceptance: true.
- Exact acceptance: true.
- Three-point acceptance: true.
- Strict acceptance: false.
- Strict false rejection: true.
- Certificate includes matching residues at inputs 0 and 1.

Candidate (c, a, b) = (0, 2, 2):
- Complete acceptance: true.
- Exact acceptance: true.
- Three-point acceptance: true.
- Strict acceptance: false.
- Strict false rejection: true.
- Certificate includes matching residues at inputs 0 and 1.

Candidate (c, a, b) = (0, 3, 0):
- Complete acceptance: false.
- Exact acceptance: false.
- Three-point acceptance: false.
- Strict acceptance: false.
- First counterexample input: 1.
- Reference output: 2.
- Candidate output: 3.
- Reference residue: 0.
- Candidate residue: 1.
- Witness replay recorded as true.

These are transcribed saved records, not newly executed results.

## Remaining recovery

Original contents not yet recovered:
- examples/coefficient_sweep.py
- tools/verify_quadratic_atlas.py
- tests/test_quadratic_atlas_saved_evidence.py
- Complete tests/fixtures/quadratic_atlas_q2.json
- manifest.json
- Original README.md and CHECKPOINT.md

The pasted consolidated report describes these artifacts but does not
supply their complete original source or establish a completed replay.

## Corpus correction

The supplied directory listing contains:
- 28 files per directory.
- 56 listed file paths across both directories.
- 4 example Python files.
- 5 tool Python files.
- 12 test Python files.
- 21 Python files per directory in total.

Matching relative filenames were shown.
Byte-identical mirror contents were not established.

## Governance carried from the supplied report

C3: OPEN
C4: BLOCKED
Publication: BLOCKED
Promotion: FALSE

No new certification or promotion claimed.
