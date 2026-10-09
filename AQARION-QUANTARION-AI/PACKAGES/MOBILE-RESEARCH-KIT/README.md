# Mobile Research Kit

### Built on a phone. Executed locally. Reported within the evidence.

Mobile Research Kit is a Python toolkit developed through an Android /
Termux workflow. It combines environment inspection, command recording,
local HTML reporting, polynomial contract experiments, saved-evidence
checking, and package regression tools.

The project distinguishes four things:

- What the source implements.
- What a recorded execution reports.
- What saved evidence can be checked for consistency.
- What has actually been reproduced from a specific package artifact.

A passing test, a generated report, and a published repository are not
interchangeable forms of evidence.

## Current status

Documentation checkpoint: 2026-10-07.

Current phase: packaging hardening and oracle separation.

The supplied local inventory contains:

- Seven tool scripts.
- Four example scripts.
- Eighteen Python test modules.
- One quadratic atlas JSON fixture.
- Root documentation and a SHA-256 manifest.
- Two historical documents under `docs/history/`.

These are inventory counts, not test-execution results or a verified
GitHub inventory.

The user reported that the source, tests, root documentation, and
metadata were pushed, and then proceeded to transfer the two historical
documents. This README does not independently establish the resulting
repository contents.

A supplied external audit reports a 91-test working-directory result.
That result has not been reproduced in this documentation update, and
must not be interpreted as proof that GitHub or a freshly extracted
archive contains the same tested bytes.

The package is not yet documented as a sealed, replay-verified release.

## Tools

| Tool | Purpose |
|---|---|
| `tools/inspect_environment.py` | Save an environment snapshot |
| `tools/record_run.py` | Record an explicit command and its execution outcome |
| `tools/view_report.py` | Render supplied inventory and receipt JSON as local HTML |
| `tools/run_workflow.py` | Coordinate inspection, recording, and report generation |
| `tools/verify_package.py` | Check listed files against an existing SHA-256 manifest |
| `tools/run_regression.py` | Verify the package, then discover and run its unittest suite |
| `tools/verify_quadratic_atlas.py` | Check saved quadratic atlas evidence |

The environment inspector, recorder, and viewer can be used separately.
The workflow invokes them as separate Python processes.

The saved quadratic-evidence verifier has an oracle-independence
limitation described below.

## Connected workflow

Run from the package root:

```sh
python3 tools/run_workflow.py \
  --timeout 5 \
  --output-root reports \
  -- python3 -c "print('Connected workflow works')"
```

The workflow identifies its artifacts using terminal fields including:

```text
WORKFLOW_DIRECTORY
INVENTORY_FILE
RUN_DIRECTORY
WORKFLOW_RECORDER_EXIT
RECEIPT_FILE
VIEWER_FILE
WORKFLOW_STATUS
WORKFLOW_EXIT
```

Each invocation creates a separate workflow directory:

```text
reports/
└── workflow-.../
    ├── inventory.json
    ├── viewer.html
    └── runs/
        └── run-.../
            ├── receipt.json
            ├── stdout.txt
            └── stderr.txt
```

The command is launched directly, without an implicit shell.
Use an explicit shell when shell syntax is required.

The timeout applies to the recorded child execution, not to the entire
multi-stage workflow.

`WORKFLOW_STATUS=reports_created` means report generation finished.
It does not mean that the child command succeeded.

When report generation succeeds, the workflow returns the recorder's
exit result. A failed or timed-out child can therefore still produce a
viewer page.

Orchestration failures return 125 and print:

```text
WORKFLOW_STATUS=orchestration_failed
WORKFLOW_EXIT=125
```

A child can itself return 125. Interpret the status and receipt alongside
the exit number.

Artifacts created before a failure may remain.

## Standalone tools

### Environment inventory

Prepare the parent directory and use a new destination:

```sh
mkdir -p reports
python3 tools/inspect_environment.py reports/inventory.json
```

The inspector records environment classification, architecture, Python
version, available Termux and Android details, selected memory readings,
home-filesystem capacity, and selected command locations.

Interpretation boundaries:

- A command location establishes PATH discovery, not successful execution.
- Memory readings are snapshots, not workload allowances.
- Storage readings are snapshots, not performance measurements.
- Native-shell inspection does not establish Ubuntu tool availability.
- Environment details do not establish research correctness.

### Command recording

```sh
python3 tools/record_run.py \
  --timeout 5 \
  --output-root reports \
  -- python3 -c "print('hello')"
```

Each run directory contains `receipt.json`, `stdout.txt`, and `stderr.txt`.

| Receipt status | Meaning |
|---|---|
| `started` | Completion has not been recorded |
| `completed` | Child finished; inspect its return code |
| `timed_out` | Recorder handled its timeout |
| `interrupted` | Recorder handled keyboard interruption |
| `launch_failed` | Command could not be launched |
| `recorder_error` | A handled operating-system error occurred after launch |

A completed command can have a nonzero return code.

The recorder uses 124 for timeout, 127 for launch or handled
operating-system errors, and 130 for handled keyboard interruption.
Negative child return codes are mapped to 128 plus the signal number.

A child can itself return those numbers. The receipt status distinguishes
the recorded outcome.

An abrupt termination can leave a `started` receipt. That does not
establish whether the child is still running.

### HTML viewer

```sh
python3 tools/view_report.py \
  --receipt PATH_TO_RECEIPT_JSON \
  --inventory PATH_TO_INVENTORY_JSON \
  --output PATH_TO_NEW_HTML_FILE
```

Replace the placeholders with local paths. The output must be a new file.

The viewer displays supplied execution fields, environment fields, and
raw JSON. It does not authenticate, reproduce, or certify the run, and
does not prove that its two input files belong to the same execution.

## Polynomial contract experiments

| Example | Role |
|---|---|
| `examples/coefficient_sweep.py` | Coefficient-sweep experiment |
| `examples/contract_collision_lab.py` | Contract-collision experiment |
| `examples/modular_contract_atlas.py` | Compare modular coefficient classification with complete-residue observation |
| `examples/quadratic_contract_atlas.py` | Compare quadratic contract-equivalence routes |

The atlases concern selected polynomial families. They are not general
polynomial classifiers or machine-checked formal proofs.

### Modular family

The reference is:

```text
x*x + x
```

The candidate is:

```text
x*x + a*x + b
```

Their difference is:

```text
(a - 1)*x + b
```

For modulus `q >= 2`, equivalence for every integer input requires and is
characterized by:

```text
(a - 1) % q == 0
b % q == 0
```

The modular atlas compares that classifier with evaluation over every
residue class. Sampled acceptance is reported separately.

Example:

```sh
python3 examples/modular_contract_atlas.py \
  --moduli 2 3 4 5 6 \
  --bound 5 \
  --sample-radius 0 \
  --output-dir reports/modular-atlas-001
```

Use a new output directory.

A sample radius of zero checks only `x = 0`. It is not an empty sample
and does not establish complete equivalence.

### Quadratic family

For the candidate:

```text
c*x*x + a*x + b
```

the difference from the reference is:

```text
h(x) = (c - 1)*x*x + (a - 1)*x + b
```

The supplied mathematical audit gives the exact criterion:

```text
b % q == 0
(c + a - 2) % q == 0
(2 * (c - 1)) % q == 0
```

Writing `A = c - 1` and `B = a - 1` gives:

```text
h(x) = A*x*(x - 1) + (A + B)*x + b
```

The audit derives necessity from `h(0)`, `h(1) - h(0)`, and
`h(2) - 2*h(1) + h(0)`. Sufficiency follows because `x*(x - 1)` is even.

For this degree-two integer polynomial family, checking `h(0)`,
`h(1)`, and `h(2)` modulo `q` is an exact mathematical criterion, not
merely a sampling heuristic.

This mathematical statement does not by itself establish that a saved
file, generator implementation, or repository revision is correct.

### Why even moduli matter

For odd `q`, the audit explains that the exact criterion reduces to
coefficient-wise equivalence.

For even `q`, coefficient-wise equivalence can be unnecessarily strict.

The canonical witness is:

```text
q = 4
c = 3
a = -1
b = 0
```

Its difference is:

```text
h(x) = 2*x*(x - 1)
```

It vanishes modulo 4 for every integer input, although `c - 1 = 2` is
not divisible by 4.

The distinction is whether 2 is invertible modulo `q`, not simply
whether `q` is prime or composite.

## Oracle separation

The supplied audit reports that the quadratic generator independently
computes:

```text
complete_acceptance
exact_acceptance
three_point_acceptance
```

It also reports that the saved-evidence verifier reconstructs the
expected `exact_acceptance` flag from complete-residue acceptance,
rather than independently implementing the algebraic criterion.

Accordingly, the claims must remain separate:

- The generator compares its complete-residue, exact-classifier, and three-point routes.
- The saved-evidence verifier checks consistency of saved observations, three-point evidence, witnesses, controls, and summaries.
- The verifier does not currently provide an independent algebraic oracle for the exact criterion.

The supplied verifier audit has not been independently reproduced in
this documentation update. It is an open finding to confirm against the
frozen source revision.

Planned hardening includes independently checking the exact criterion
and adding mutation-sensitive regression evidence.

The canonical proposed mutation replaces:

```python
(2 * (c - 1)) % q == 0
```

with:

```python
(c - 1) % q == 0
```

The mod-4 witness above must distinguish the correct criterion from this
overly strict mutation.

No mutation execution is claimed here.

## Verification and tests

From the package root:

```sh
python3 tools/verify_package.py --root .
```

The package verifier checks only files listed in the manifest.
It does not verify unlisted files or establish software correctness.

Run the package regression entry point with:

```sh
python3 tools/run_regression.py
```

That entry point verifies the package before running unittest discovery.
A manifest failure stops the regression workflow.

For direct test discovery without the manifest gate:

```sh
python3 -m unittest discover -s tests -v
```

Direct test execution does not replace package-integrity verification.

Report the discovered test count, exit code, skipped tests, source
revision, and execution location from the actual run. Do not assume that
a prior reported count describes the current repository.

The inspected local checkout contains eighteen test modules. The supplied
audit discusses an earlier fourteen-module state and a reported 91-test
result. Those descriptions must be reconciled against a frozen revision.

## Packaging closure

The intended evidence sequence is:

```text
Frozen working tree
        ↓
Manifest tied to selected source bytes
        ↓
Archive
        ↓
Fresh extraction
        ↓
Extracted manifest verification
        ↓
Extracted regression execution
        ↓
Extracted quadratic fixture replay
        ↓
Archive receipt
```

A closure receipt should record actual values for:

```text
source revision or explicit source identity
archive filename
archive byte size
archive SHA-256
manifest SHA-256
archive entry count
manifest entry count
extracted manifest verification outcome
discovered test count
test exit code
skipped test count
fixture-verification exit code
execution timestamp
execution environment
```

Do not populate a receipt with invented values, placeholders presented
as results, or an `EXECUTED` status before the commands run.

Manifest regeneration after edits creates a new integrity baseline.
It does not prove that the edited files match an earlier artifact.

## Evidence and limitations

Historical 25-test evidence is preserved in:

```text
docs/history/CHECKPOINT-25tests.md
docs/history/README-25tests.md
```

Those documents describe earlier states. Their counts and publication
language do not define the current package.

The current checkpoint separates reported evidence from pending
verification. This README does not claim independent reproduction of
the reported 91-test result.

Current boundaries include:

- No established sealed GitHub/archive equivalence.
- No claimed independent exact-algebraic verification by the saved-evidence verifier.
- No claimed execution of the proposed classifier mutations.
- No claimed implementation of an empty-sample `no_evidence` policy.
- No command sandbox.
- No output-size limit in the supplied recorder.
- No guaranteed recorder timeout after the recorder itself is killed.
- No authenticated binding between viewer inputs.
- No established sustained Android workload stability.
- No complete security audit or formal certification.

Termux session resets remain unexplained in the supplied historical
evidence.

## Privacy, requirements, and publication

The supplied workflow tools use Python's standard library.
The recorder's process-group handling requires a POSIX environment.

Previously reported development environment:

- Samsung SM-A156U.
- Android 16.
- AArch64.
- Google Play Termux 2026.06.21.
- Python 3.13.13.

These are historical environment reports, not a current compatibility
matrix.

Commands, paths, device details, stdout, and stderr can contain private
information. Review artifacts before sharing.

Raw reports, generated HTML, caches, backups, and archives are outside
the intended source transfer unless deliberately reviewed and selected.

Repository publication does not by itself establish release integrity,
test reproduction, or a software license. License selection has not
been established by the material supplied for this update.

Ubuntu / Lean research and PB-006 remain separate from this Python
package's closure evidence.

---

Inspect what is available.
Record what ran.
Separate the oracles.
Replay the artifact.
Keep the claims within the evidence.
