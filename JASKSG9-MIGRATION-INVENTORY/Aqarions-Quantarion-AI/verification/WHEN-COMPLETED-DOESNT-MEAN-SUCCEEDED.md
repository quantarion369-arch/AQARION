Public community case study · 11 October 2026 · Draft, not published

# When “Completed” Doesn’t Mean “Succeeded”

*A transparent debugging case study from AQARION*

## The question

Can an execution receipt pass validation while contradicting the command outcome it records?

In the implementation examined during this investigation, yes. Adversarial tests exposed validation gaps, including a receipt that reported recorder exit code `0` while the child command returned `7`.

That is not a cosmetic reporting problem. An execution receipt is supposed to preserve what happened, including failure. If a checker accepts internally inconsistent evidence—or crashes on malformed input—it cannot reliably distinguish a valid failure record from an invalid receipt.

Our objective was not to make the dashboard green. It was to make the validator enforce explicit rules, reject contradictions, and preserve truthful evidence of failed commands.

## What the adversarial tests examined

The regression cases targeted several independent failure modes:

- **Contradictory exit codes:** reject a receipt whose recorder reports success while the recorded child outcome is inconsistent with the declared execution contract.
- **Missing child outcome:** reject a completed-command receipt that omits the child return code.
- **Boolean return codes:** reject `true` and `false` where an integer process return code is required. In Python, `bool` is a subclass of `int`, so an ordinary integer type check is insufficient.
- **Invalid timestamps:** require a timezone-aware start timestamp and reject an end timestamp earlier than the start.
- **Malformed status values:** reject unsupported status types cleanly rather than allowing validation to raise an unexpected exception.
- **Signal-normalized failures:** retain valid failure evidence when a process terminates because of a signal and the runner records the outcome using its documented normalization rules.

These cases test different invariants. Passing one does not imply that the others are enforced.

## A small type-checking bug with a large lesson

The original status validation included this check:

```python
if status not in TERMINAL_STATUSES:
```

When `TERMINAL_STATUSES` is a set, an unhashable value such as a list or dictionary can raise `TypeError` during membership testing. The validator may crash instead of returning a controlled rejection.

The corrected validation order is conceptually:

```python
if not isinstance(status, str):
    reject("status must be a string")

if status not in TERMINAL_STATUSES:
    reject("unsupported terminal status")
```

This example illustrates a general defensive-programming rule: validate a value's type before performing operations whose behavior depends on that type.

A robust checker should reject malformed input through its documented error path, not rely on callers to supply well-typed values.

## The failed intermediate revision

The investigation included an intermediate commit:

`d191b558851c60f0203fe7598f445f21f464b1c8`

The accompanying report identifies GitHub Actions run **62** as a failed hosted regression. The adversarial tests existed, but the validator had not yet implemented all the checks those tests required.

Initially, the available summary showed the recorder's exit result without the detailed test failures. An access-enabled inspection subsequently retrieved the workflow logs and evidence artifact, allowing the discrepancy to be investigated more directly.

This is an important part of the debugging record: the root cause was not established by the first summary. Early explanations were hypotheses until the more detailed evidence became available.

## The later revision

The report identifies this subsequent commit:

`b4440305f63be59a8036cedf3ac394f8dafc9d9e`

It reports that GitHub Actions run **64** passed the original acceptance tests, recorded regression, evidence validation, and artifact upload.

The reported acceptance metadata was:

```text
acceptance_passed = true
acceptance_failures = []
child_command_succeeded = true
recorder_exit = 0
```

The report also records 135 discovered tests in the successful hosted regression and a local run of 135 tests executed with zero skipped.

Those are separate observations. A hosted discovery count does not, by itself, establish that every test executed successfully. The local result is a distinct piece of evidence, but its strength depends on the actual test command, environment, and captured output.

These historical run results are attributed to the access-enabled inspection report. This document does not claim that the commits or workflow logs were independently re-fetched and re-executed for this publication draft.

## A failed command can produce valid evidence

Consider the following reported failure receipt:

```text
child_returncode = 1
recorder_exit = 1
acceptance_passed = true
child_command_succeeded = false
```

These fields can be mutually consistent.

The child command failed. The recorder accurately reported that failure. The acceptance process accepted the evidence because it correctly described the failed execution and satisfied the applicable validation rules.

The distinction is fundamental:

| Question | Meaning |
|---|---|
| Did the child command succeed? | The outcome of the command that was executed. |
| Was the receipt accepted? | Whether the evidence satisfied the validator's rules. |
| Is the receipt internally consistent? | Whether its fields agree under the declared execution contract. |
| Is the receipt authentic? | Whether its origin and integrity are established by adequate provenance controls. |

A valid receipt may describe failure. An accepted receipt is not necessarily proof of successful execution, and neither acceptance nor internal consistency alone establishes authenticity.

## What this investigation establishes—and what it does not

The reported tests and revisions concern specific receipt-validation behaviors. They do not establish that the validator is infallible.

This case study does not claim:

- a mathematical theorem or formal-kernel acceptance;
- authenticated provenance merely because a receipt parses or passes validation;
- independent certification of the entire execution environment;
- that every possible malformed receipt has been covered;
- that a passing workflow proves the absence of defects;
- or that the separate JOIN-STABILITY workstream has been repaired.

The evidence supports a narrower engineering lesson: explicit invariants and adversarial regression tests can expose inconsistencies that ordinary happy-path tests may miss.

## Invitation to the community

We invite reviewers to find a receipt the validator handles incorrectly.

A useful report should include:

1. **Minimal reproducer:** the smallest receipt or evidence bundle that triggers the behavior.
2. **Expected outcome:** accept or reject, with the violated or satisfied rule.
3. **Observed outcome:** the actual validator result, including any exception or exit code.
4. **Regression test:** a test that reproduces the defect and protects against its return.
5. **Evidence:** the exact revision and command used, plus relevant output.

Please avoid publishing secrets, private execution data, credentials, or sensitive environment variables in reproduction bundles.

The goal is not to claim that the checker is now infallible. It is to make defects reproducible, repairs inspectable, and claims proportional to the evidence.

## Publication status

This document is a community-facing draft. It is not a GitHub publication, release announcement, or independent certification. The commit identifiers, run numbers, and test counts above are attributed to the inspection report; they should be checked against the repository and retained workflow artifacts before the document is presented as independently revalidated.

**AQARION principle:** record what happened, validate what the evidence actually establishes, and never turn a successful checker exit into an unsupported claim of success.
