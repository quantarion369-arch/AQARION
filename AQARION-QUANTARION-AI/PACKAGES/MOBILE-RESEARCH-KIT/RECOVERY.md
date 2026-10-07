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



# Quadratic Atlas Technical Handoff

This report documents the completed quadratic-atlas experiment, saved-evidence verifier, corruption regression tests, and fixture-backed test integration. It is based on commands and terminal output supplied during this session—not direct inspection of the repository by the assistant.

## 1. Project and scope

| Item | Detail |
|---|---|
| Session date | October 7, 2026 |
| Environment | Termux on Android |
| Repository directory | `~/mobile-research-kit.Y2rXSF` |
| Absolute repository path | `/data/data/com.termux/files/home/mobile-research-kit.Y2rXSF` |
| Experiment | Quadratic Contract Atlas |
| Reference polynomial | $$x^2+x$$ |
| Candidate form | $$cx^2+ax+b$$ |
| Coefficient bound | 3; each coefficient ranges from −3 through 3 |
| Moduli | 2, 3, 4, 5, 6, 8 |
| Candidates per modulus | 343 |
| Total candidate–modulus cases | 2,058 |

The experiment compares complete residue enumeration, exact quadratic conditions, and evaluation at three points.

Strict coefficient matching is a deliberately adversarial comparison rule. Its false rejections are expected findings, not harness failures.

The report explicitly disclaims being a general polynomial classifier or formal certification.

## 2. Experiment results and provenance

### Atlas results

| Modulus | Candidates | Accepted | Primary disagreements | Strict false rejects | Strict false accepts | Failed replays |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 343 | 75 | 0 | 27 | 0 | 0 |
| 3 | 343 | 12 | 0 | 0 | 0 | 0 |
| 4 | 343 | 8 | 0 | 4 | 0 | 0 |
| 5 | 343 | 1 | 0 | 0 | 0 | 0 |
| 6 | 343 | 2 | 0 | 1 | 0 | 0 |
| 8 | 343 | 2 | 0 | 1 | 0 | 0 |
| Total | 2,058 | 100 | 0 | 33 | 0 | 0 |

All three primary routes agreed throughout the tested grid. Strict coefficient matching rejected 33 candidates that complete enumeration accepted.

Every tested even modulus had strict false rejections; neither tested odd modulus did. This is a finding for this grid, not a claim about arbitrary polynomial families.

### Representative saved evidence

These candidates produced the same residue outputs as $$x^2+x$$, despite failing strict coefficient matching:

| Modulus | Candidate | Shared residue sequence |
|---:|---|---|
| 2 | $$-2x^2-2x-2$$ | `[0, 0]` |
| 4 | $$-x^2-x$$ | `[0, 2, 2, 0]` |
| 6 | $$-2x^2-2x$$ | `[0, 2, 0, 0, 2, 0]` |
| 8 | $$-3x^2-3x$$ | `[0, 2, 6, 4, 4, 6, 2, 0]` |

### Recorded atlas workflow

Command executed:

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 examples/quadratic_contract_atlas.py --moduli 2 3 4 5 6 8 --bound 3 --output-dir reports/quadratic-atlas-001
```

Observed status:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
QUADRATIC_ATLAS_WORKFLOW_EXIT=0
```

Repository-relative artifacts:

```text
reports/quadratic-atlas-001/atlas.md
reports/quadratic-atlas-001/atlas.json

reports/workflow-bsy9838l/inventory.json
reports/workflow-bsy9838l/runs/run-5xpnje47/receipt.json
reports/workflow-bsy9838l/viewer.html
```

## 3. Saved-evidence verifier

### New verifier

```text
tools/verify_quadratic_atlas.py
```

The verifier uses the Python standard library and does not import the atlas generator.

It reads saved JSON and checks:

- Report kind, coefficient bound, and moduli.
- Modulus-group correspondence.
- Complete coefficient-grid coverage without duplicate candidates.
- Recomputed reference and candidate outputs over every residue input.
- Complete acceptance and three-point acceptance.
- Saved exact-route acceptance against complete enumeration.
- Strict coefficient acceptance and false-rejection/false-acceptance flags.
- First counterexample and saved replay status.
- Complete equivalence comparisons for strict false rejections.
- Summary counts against recomputed results.

Important distinction: the verifier does not independently implement the exact route’s algebraic conditions. It checks that route’s saved acceptance flag against recomputed complete enumeration.

Successful full-report replay produced:

```text
CASES_RECOMPUTED=2058
ACCEPTED_CASES=100
REJECTION_WITNESSES_REPLAYED=1958
EQUIVALENCE_COMPARISONS_REPLAYED=33
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
```

Here, `EQUIVALENCE_COMPARISONS_REPLAYED=33` counts candidate cases containing complete comparison lists, not individual input comparisons.

### Recorded verifier workflow

Command executed:

```sh
python3 tools/run_workflow.py --timeout 30 --output-root reports -- python3 tools/verify_quadratic_atlas.py reports/quadratic-atlas-001/atlas.json
```

Observed status:

```text
STATUS=completed
RECORDER_EXIT=0
WORKFLOW_RECORDER_EXIT=0
WORKFLOW_STATUS=reports_created
WORKFLOW_EXIT=0
SAVED_EVIDENCE_WORKFLOW_EXIT=0
```

Repository-relative artifacts:

```text
reports/workflow-peo6vad3/inventory.json
reports/workflow-peo6vad3/runs/run-d38iecjz/receipt.json
reports/workflow-peo6vad3/viewer.html
```

### Resolved implementation issue

The saved verifier initially contained a string split across physical lines 159–160, causing an unterminated f-string syntax error.

A targeted repair replaced it with:

```python
parser.exit(1, "VERIFICATION_FAILED: " + str(error) + chr(10))
```

Compilation, verification, and regression tests subsequently succeeded. The repair command created a backup named:

```text
tools/verify_quadratic_atlas.py.before-string-fix
```

## 4. Regression tests and fixture

### New test module

```text
tests/test_quadratic_atlas_saved_evidence.py
```

Six tests were added:

| Test | Expected behavior |
|---|---|
| `test_original_report_passes` | Accept the unmodified fixture with expected totals |
| `test_corrupted_recorded_output_fails` | Reject a modified candidate output in a counterexample |
| `test_missing_rejection_witness_fails` | Reject removal of a required counterexample |
| `test_corrupted_equivalence_comparison_fails` | Reject a modified candidate residue in an equivalence comparison |
| `test_corrupted_summary_fails` | Reject an altered acceptance count |
| `test_duplicate_candidate_fails` | Reject a duplicate candidate replacing another grid entry |

Corruptions are applied to in-memory copies. Tests do not modify the source report.

### Repository-local fixture

The tests initially depended on the generated six-modulus report. A reduced modulus-2 fixture was then created:

```text
tests/fixtures/quadratic_atlas_q2.json
```

Confirmed fixture size: 223,091 bytes.

The fixture was derived from the validated original report by retaining the modulus-2 group and summary. It was verified before being used for test integration.

Observed fixture verification:

```text
CASES_RECOMPUTED=343
ACCEPTED_CASES=75
REJECTION_WITNESSES_REPLAYED=268
EQUIVALENCE_COMPARISONS_REPLAYED=27
SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
FIXTURE_VERIFIER_EXIT=0
```

A guarded patch was supplied to switch the test path and expected totals to this fixture. The subsequent full suite passed. The patch’s success marker and final file contents were not pasted, so another tool should inspect the test module to confirm its current path directly.

### Test history

| Checkpoint | Tests | Duration | Result |
|---|---:|---:|---|
| Original baseline | 60 | 8.327 seconds | `OK`; explicit exit 0 |
| New regression tests after repair | 6 | 0.427 seconds | `OK` |
| Repeated regression run | 6 | 0.443 seconds | `OK`; explicit exit 0 |
| First integrated full suite | 66 | 9.147 seconds | `OK` |
| Subsequent full suite | 66 | 8.568 seconds | `OK` |
| Latest suite after fixture-switch instructions | 66 | 8.568 seconds | `OK` |

The latest `FIXTURE_BACKED_FULL_SUITE_EXIT` command was shown, but its output was not included. Therefore, the latest test result is confirmed as `OK`; its separate echoed exit value is not visible.

## 5. Handoff limits and next checks

### What is established

- The bounded six-modulus experiment completed successfully.
- All primary routes agreed across 2,058 tested cases.
- Saved evidence was recomputed by a separate report consumer.
- Five specific corruption scenarios were rejected by regression tests.
- A reduced local fixture was created and verified.
- The expanded 66-test suite passed.

### What is not established

- Formal mathematical certification.
- General polynomial classification.
- Independent-language replication.
- A security-grade validator for arbitrary untrusted JSON.
- Detection of every possible corruption.
- Clean-checkout portability of the entire project.
- Git staging, commits, or publication of the new files.
- Direct inspection of receipts or viewers beyond their reported creation.

The fixture is derived from this experiment, not an independently authored oracle. The verifier shares Python arithmetic with the experiment.

### Useful checks for the next tool

Run from the repository root:

```sh
git status --short
```

Confirm the test’s fixture path:

```sh
grep -n '^REPORT =' tests/test_quadratic_atlas_saved_evidence.py
```

Reverify the fixture:

```sh
python3 tools/verify_quadratic_atlas.py tests/fixtures/quadratic_atlas_q2.json
```

Run the full suite:

```sh
python3 -m unittest discover -s tests -v
```

Collaboration preference: the user works third shift, has no deadline for this exploration, and prefers iterative progress based on actual terminal output. Use clearly labeled paste blocks, avoid confusing code examples with shell commands, and use simple `echo` status checks where practical.

CASES_RECOMPUTED=2058
ACCEPTED_CASES=100
REJECTION_WITNESSES_REPLAYED=1958
EQUIVALENCE_COMPARISONS_REPLAYED=33                                                                         | q | c | a | b | Reference residues | Candidate residues |
|---:|---:|---:|---:|---|---|                         | 2 | -2 | -2 | -2 | [0, 0] | [0, 0] |
| 4 | -1 | -1 | 0 | [0, 2, 2, 0] | [0, 2, 2, 0] |     | 6 | -2 | -2 | 0 | [0, 2, 0, 0, 2, 0] | [0, 2, 0, 0, 2, 0] |
| 8 | -3 | -3 | 0 | [0, 2, 6, 4, 4, 6, 2, 0] | [0, 2, 6, 4, 4, 6, 2, 0] |
                                                      SAVED_QUADRATIC_EVIDENCE_REPLAY_OK
~/mobile-research-kit.Y2rXSF $

The saved-evidence replay succeeded: **all 2,058 cases were recomputed**, including 1,958 rejection witnesses and 33 complete comparisons for equivalent candidates rejected by the strict rule.

That closes an important gap: we checked the saved report using a separate consumer that did not import the atlas module.

## Concrete equivalence examples

These are your replayed results:

| Modulus | Candidate | Reference and candidate residues |
|---:|---|---|
| 2 | $$-2x^2-2x-2$$ | `[0, 0]` |
| 4 | $$-x^2-x$$ | `[0, 2, 2, 0]` |
| 6 | $$-2x^2-2x$$ | `[0, 2, 0, 0, 2, 0]` |
| 8 | $$-3x^2-3x$$ | `[0, 2, 6, 4, 4, 6, 2, 0]` |

In every row, the candidate’s coefficients differ from the reference $$x^2+x$$ modulo the selected modulus, yet the recorded residue outputs match completely.

## What is now established

| Evidence layer | Result |
|---|---|
| Full development suite | 60 tests passed |
| Recorded quadratic run | Completed; workflow exit 0 |
| Three primary routes | Agreed across all 2,058 cases |
| Strict coefficient rule | 33 false rejections; no false acceptances |
| Saved rejection witnesses | 1,958 recomputed successfully |
| Saved equivalence comparisons | 33 recomputed successfully |
| Report summaries | Matched the recomputed results |

This is implementation and report-consistency evidence from your local runs. It is not an independent-language replication or formal certification.

## Next step: make replay reusable

The replay currently exists as a terminal block. I’ll turn it into a saved command-line tool with regression tests, so future reports can be checked without copying a long script.

Its tests will deliberately tamper with:

- A recorded polynomial output.
- A rejection witness.
- An equivalence comparison.
- A summary count.
- The candidate grid.

The verifier must reject each corrupted report. That turns today’s successful replay into a repeatable capability—and gives your shell workflow a useful new command rather than another one-off check.

Citations:
[1] https://www.math.columbia.edu/~goldfeld/RAMANUJAN.pdf
[2] https://arxiv.org/pdf/2003.06908.pdf
[3] [PDF] Random mapping statistics - HAL-Inria https://inria.hal.science/inria-00075445/file/RR-1114.pdf

Citations:
[1] https://www.math.columbia.edu/~goldfeld/RAMANUJAN.pdf
[2] https://arxiv.org/pdf/2003.06908.pdf
[3] https://inria.hal.science/inria-00075445/file/RR-1114.pdf
