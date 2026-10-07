# Mobile Research Kit — Packaging and Oracle-Separation Gate

Date: 2026-10-07
Phase: packaging hardening and oracle separation.
State: current inventory documented; package closure not yet established.
Release seal: not established.

This is the current checkpoint, not a concatenation of previous
checkpoints.

It separates source inventory, user-reported activity, supplied audit
findings, and evidence still required for closure.

## 1. Source basis

This checkpoint is based on:

- User-supplied terminal listings and source excerpts.
- User-reported GitHub pushes.
- A supplied external GPT audit.
- Historical 25-test documentation supplied in this conversation.

No independent GitHub checkout, archive extraction, regression run,
fixture replay, or mutation execution was performed as part of this
documentation update.

The audit's repository findings remain attributed findings until
confirmed against the selected source revision.

## 2. Current local inventory

The supplied local listing contains seven tools:

- `tools/inspect_environment.py`
- `tools/record_run.py`
- `tools/view_report.py`
- `tools/run_workflow.py`
- `tools/run_regression.py`
- `tools/verify_package.py`
- `tools/verify_quadratic_atlas.py`

It contains four examples:

- `examples/coefficient_sweep.py`
- `examples/contract_collision_lab.py`
- `examples/modular_contract_atlas.py`
- `examples/quadratic_contract_atlas.py`

It contains fifteen Python test modules:

- `tests/test_coefficient_sweep.py`
- `tests/test_contract_collision_lab.py`
- `tests/test_contract_evidence.py`
- `tests/test_contract_selection.py`
- `tests/test_inspect_environment.py`
- `tests/test_modular_contract_atlas.py`
- `tests/test_quadratic_atlas_saved_evidence.py`
- `tests/test_quadratic_contract_atlas.py`
- `tests/test_record_run.py`
- `tests/test_run_regression.py`
- `tests/test_run_workflow.py`
- `tests/test_verify_package.py`
- `tests/test_view_report.py`
- `tests/test_workflow_failures.py`
- `tests/test_workflow_os_errors.py`

Saved fixture:

- `tests/fixtures/quadratic_atlas_q2.json`

Root files:

- `.gitignore`
- `README.md`
- `CHECKPOINT.md`
- `FILETREE.md`
- `manifest.json`

Historical documents:

- `docs/history/CHECKPOINT-25tests.md`
- `docs/history/README-25tests.md`

The listing also contains generated caches and workflow reports.
Their presence locally does not establish that they belong in the
selected source package.

Inventory counts do not establish a frozen source revision or a
successful test run.

## 3. Transfer status

The user reported that the five newly handled files were pushed:

- `examples/modular_contract_atlas.py`
- `tools/inspect_environment.py`
- `tools/record_run.py`
- `tools/run_workflow.py`
- `tools/view_report.py`

The user subsequently confirmed that these tools were already present:

- `tools/run_regression.py`
- `tools/verify_package.py`
- `tools/verify_quadratic_atlas.py`

The user reported that everything except `docs/` had been transferred,
then supplied both historical documents for transfer.

The final push of both historical documents has not been independently
verified here.

The replacement root README and checkpoint constitute a new
documentation state. Their publication and correspondence with a
manifest or archive must be checked after the update.

## 4. Evidence ledger

| Evidence item | Current interpretation |
|---|---|
| Historical 25-test result | User-reported historical evidence: 25 tests in 5.674 seconds, OK, exit 0 |
| Historical connected workflow | User-reported inventory, receipt, and viewer creation with workflow exit 0 |
| Later 66-test state | Earlier state described in the supplied audit; not the current acceptance baseline |
| Later 91-test result | Working-directory result reported by the supplied audit; not reproduced here |
| Fifteen local test modules | Established by the supplied file listing; not an executed test count |
| GitHub source transfer | User-reported; exact repository bytes not checked here |
| Extracted archive regression | No current artifact-linked successful execution established here |
| Quadratic fixture replay | No current extracted-artifact execution established here |
| Classifier mutation checks | Proposed; execution not established |
| PB-006 mutation gate | Separate proposed research gate; execution not established |

The supplied audit discusses a fourteen-test-module state, while the
later local listing contains fifteen test modules.

The final discovered test count must come from an actual execution
against the frozen source revision. Neither 91 nor any historical count
is assumed in advance.

## 5. Documentation drift finding

The supplied audit reports that the previous root documentation mixed
successive implementation and packaging states, including:

- Five-tool / twelve-module descriptions.
- Seven-tool / fourteen-module descriptions.
- Historical 66-test and later 91-test claims.
- Archive-pending and archive-complete language without one clear artifact identity.

This replacement checkpoint removes those states from the current
acceptance narrative.

Historical records must remain identifiable as historical records.
Replacing this document does not itself establish that every superseded
checkpoint has been archived.

Before replacement, preserve any earlier root material that must remain
auditable in a dated history record or an identifiable repository
revision.

Do not describe historical migration as complete until it is confirmed.

## 6. Mathematical scope

Reference:

```text
f(x) = x*x + x
```

Modular-family candidate:

```text
g(x) = x*x + a*x + b
```

The supplied classifier checks:

```text
(a - 1) % q == 0
b % q == 0
```

Complete-residue observation and sampled observation are separate
outputs.

Quadratic-family candidate:

```text
g(x) = c*x*x + a*x + b
```

The supplied audit derives equivalence for every integer input from:

```text
b % q == 0
(c + a - 2) % q == 0
(2 * (c - 1)) % q == 0
```

It also derives the exact three-point condition for this degree-two
integer polynomial family:

```text
h(0) % q == 0
h(1) % q == 0
h(2) % q == 0
```

where:

```text
h(x) = g(x) - f(x)
```

These are scoped mathematical statements. They do not certify an
implementation, a saved fixture, or a published artifact.

A general finite-difference contract theorem remains future work and
is not claimed as implemented or formally verified.

## 7. Oracle-independence finding

The supplied audit reports that the quadratic generator separately
computes complete-residue, exact-classifier, and three-point acceptance.

It reports that the saved-evidence verifier assigns expected
`exact_acceptance` from complete-residue acceptance rather than
independently evaluating the exact algebraic criterion.

Until confirmed or corrected, describe the verifier as checking saved
evidence consistency, not as supplying an independent algebraic oracle.

Required next steps:

- Confirm the finding against the frozen verifier source.
- Implement or otherwise establish a separately checked exact criterion.
- Add tests that detect corruption of the generator-side exact classifier.
- Preserve the distinction between generator agreement and fixture-verifier independence.

No correction or mutation execution is recorded by this checkpoint.

## 8. Required adversarial witnesses

### Exact-classifier mutation

Proposed correct condition:

```python
(2 * (c - 1)) % q == 0
```

Proposed faulty replacement:

```python
(c - 1) % q == 0
```

Canonical witness:

```text
q = 4
c = 3
a = -1
b = 0
h(x) = 2*x*(x - 1)
```

Expected mathematical distinction:

- Correct functional-equivalence criterion accepts.
- Overly strict coefficient-style mutation rejects.

The gate must demonstrate that the relevant test detects the mutation.
A documented witness alone is not a mutation receipt.

### Strict-coefficient control

Replay the even-modulus witness against the strict coefficient rule.

Distinguish a deliberately faulty control from a corrupted production
classifier. Record which code path was exercised.

### Modular witness

Select and record a concrete witness distinguishing sampled acceptance
from complete equivalence.

Record the coefficients, modulus, sampled inputs, and counterexample.
No successful replay is claimed here.

### Empty-sample semantics

Target policy:

```text
empty sample = no_evidence
```

The supplied modular `observe()` implementation currently returns
`accepted_on_checked_domain=True` when given an empty iterable, because
no failure is encountered.

That behavior must not be described as an implemented `no_evidence`
policy.

Its CLI with `sample_radius=0` checks `[0]`, which is not an empty sample.

Any policy change requires an explicit implementation and regression
tests, including preservation of the nonempty zero-radius case.

## 9. Packaging closure sequence

Required sequence:

1. Select and freeze the source revision.
2. Reconcile README, checkpoint, file tree, and actual inventory.
3. Preserve superseded checkpoint material.
4. Finalize oracle-separation changes and tests.
5. Generate or update the manifest for the final selected bytes.
6. Verify that manifest against the selected working tree.
7. Create the archive.
8. Record archive byte size, SHA-256, and entry count.
9. Extract into a fresh location.
10. Verify the extracted manifest.
11. Execute the extracted regression suite.
12. Execute the extracted quadratic fixture verification.
13. Replay the required witnesses and mutations at their declared scope.
14. Record an artifact-linked closure receipt.

The receipt must distinguish the frozen repository revision, working
directory, archive, and extraction directory.

No current archive is designated as sealed by this checkpoint.

## 10. Acceptance checklist

- [ ] Frozen source identity recorded.
- [ ] Current inventory reconciled.
- [ ] Both historical documents confirmed in the repository.
- [ ] Superseded checkpoint material preserved.
- [ ] README and FILETREE match the selected source.
- [ ] Exact-verifier independence finding confirmed.
- [ ] Independent exact-criterion checking established.
- [ ] Exact-classifier mutation detected.
- [ ] Strict-coefficient control replayed.
- [ ] Empty-sample policy implemented and tested.
- [ ] Modular witness replayed.
- [ ] Quadratic witness replayed.
- [ ] Manifest tied to final selected source bytes.
- [ ] Working-tree manifest verification passed.
- [ ] Archive created and identified.
- [ ] Archive SHA-256 and byte size recorded.
- [ ] Archive and manifest entry counts recorded.
- [ ] Fresh extraction completed.
- [ ] Extracted manifest verification passed.
- [ ] Extracted regression result recorded.
- [ ] Actual discovered test count and skips recorded.
- [ ] Extracted quadratic fixture verification passed.
- [ ] Artifact-linked closure receipt recorded.

Unchecked means not established by the evidence collected for this
checkpoint. It does not necessarily mean the activity has never occurred.

## 11. Closure receipt requirements

Populate only from actual execution:

```text
source_identity
recorded_at_utc
execution_environment
archive_file
archive_bytes
archive_sha256
manifest_sha256
archive_entries
manifest_entries
extraction_directory
extracted_manifest_exit
discovered_tests
skipped_tests
test_exit
fixture_exit
witness_results
mutation_results
status
```

Do not write `EXECUTED`, `VERIFIED`, or `SEALED` solely because a planned
command or expected outcome has been documented.

A newly regenerated manifest establishes a new selected-byte baseline.
It does not establish equivalence to an earlier archive.

## 12. Separate PB-006 research gate

PB-006 is outside the Python package's acceptance checklist.

The supplied audit proposes a semantic mutation replacing:

```text
listGcd b
```

with:

```text
b.foldl Nat.lcm 1
```

The intended evidence must distinguish:

- Baseline build.
- Whether the mutation itself compiles.
- Whether a semantic theorem or value check detects the mutation.
- Restoration of the original implementation.
- Restored build.
- The actual theorem's `#print axioms` output.

The proposed `9 -> 13` witness remains an audit-supplied target until
replayed.

If the mutation compiles but the semantic check fails, record those
outcomes separately. Do not label a successful mutation compilation as
a failed build.

No PB-006 execution receipt or Lean axiom result is established here.

## 13. Limitations and privacy

This checkpoint does not establish:

- Independent reproduction of the reported 91-test result.
- GitHub/archive byte equivalence.
- Current archive closure.
- General polynomial classification.
- Machine-checked proof of the mathematical criteria.
- Complete security coverage.
- Sustained Android workload stability.
- Cause of Termux session resets.
- Authentication of viewer inputs or execution receipts.
- A selected software license.

The recorder is not a sandbox. Output files are not size-limited.
A timeout cannot be assumed after the recorder is killed.

Review commands, paths, device details, stdout, stderr, and generated
reports before sharing.

## 14. Next priority

First: close packaging and oracle-separation evidence for a specific
source revision and archive.

Second: execute the separate PB-006 semantic mutation gate.

Further atlas development and general finite-difference theory remain
deferred work, not part of the current closure claim.

---

Current state: documented, not sealed.
Next state requires execution evidence, not another appended claim.
