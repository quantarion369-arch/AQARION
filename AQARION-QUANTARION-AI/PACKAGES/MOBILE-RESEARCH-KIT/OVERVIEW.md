MOBILE RESEARCH KIT
James Aaron | AQARION & QUANTARION_AI
===============================================================

PURPOSE
-------
Run bounded experiments.
Expose differences between contracts.
Preserve inspectable evidence.
Test implementations and failure behavior.
Keep execution success separate from mathematical meaning.


                         YOU
                          |
                          | choose an experiment or check
                          v
                +--------------------+
                | WORKING PACKAGE    |
                | Phone / Termux     |
                +--------------------+
                          |
             +------------+-------------+
             |                          |
             v                          v
   +-------------------+      +----------------------+
   | EXPERIMENT PATH   |      | REGRESSION PATH      |
   | Generate evidence |      | Check implementation |
   +-------------------+      +----------------------+
             |                          |
             v                          v
   examples/*.py              tools/run_regression.py
             |                          |
             |                          v
             |                tools/verify_package.py
             |                          |
             |                 read manifest.json
             |                          |
             |                 compare listed files
             |                 - path safety
             |                 - byte sizes
             |                 - SHA-256 hashes
             |                          |
             |                 +--------+--------+
             |                 |                 |
             |               FAIL              PASS
             |                 |                 |
             |                 v                 v
             |               STOP       discover test modules
             |                                   |
             |                          +--------+--------+
             |                          |                 |
             |                    discovery error     tests found
             |                    or zero tests           |
             |                          |                 v
             |                          v           execute suite
             |                        STOP                |
             |                                  +--------+--------+
             |                                  |                 |
             |                                FAIL              PASS
             |                                  |                 |
             |                                  v                 v
             |                         inspect failure     REGRESSION_OK
             |                                             report skips
             v
   +----------------------+
   | EXPERIMENT OUTPUTS   |
   | Reports / evidence   |
   +----------------------+
             |
             v
   +------------------------------+
   | EVIDENCE INTERPRETATION      |
   | What domain was checked?     |
   | What contract was tested?    |
   | What witnesses were saved?   |
   | What remains unestablished?  |
   +------------------------------+
```

The regression path is grounded in the code and execution results supplied in this conversation. The experiment and workflow outputs need source inspection before we prescribe new exact commands or fields.

## Experimental evidence flow

```text
TRACK A: CONTRACT DISCRIMINATION
===============================================================

coefficient_sweep.py
        |
        v
Examine a bounded coefficient family
        |
        v
Record classification outcomes


contract_collision_lab.py
        |
        v
Exercise supported contracts and counterexamples
        |
        v
Keep distinct contracts from being silently conflated


modular_contract_atlas.py
        |
        +--------------------------+
        |                          |
        v                          v
Sample-based evaluation     Complete residue evaluation
        |                          |
        +------------+-------------+
                     |
                     v
             Compare classifications
                     |
                     v
       Save disagreements / false accepts / witnesses


TRACK B: QUADRATIC FUNCTIONAL EQUIVALENCE
===============================================================

quadratic_contract_atlas.py
        |
        +------------------+-------------------+
        |                  |                   |
        v                  v                   v
Residue evaluation    Exact criterion     Strict coefficient
                                          matching control
        |                  |                   |
        +------------------+-------------------+
                           |
                           v
                 Compare route outcomes
                           |
                           v
                 Save inspectable evidence
                           |
                           v
              verify_quadratic_atlas.py
                           |
                           v
             Check recorded mathematical evidence


IMPORTANT SEPARATION
===============================================================

verify_package.py
    "Do listed file bytes match the manifest?"

verify_quadratic_atlas.py
    "Does saved quadratic evidence survive its verifier?"

run_regression.py
    "Do integrity verification and discovered tests pass?"

These are three different questions.
A PASS on one does not automatically answer the others.
```

Your supplied historical audit reported the modular and quadratic counts. Those are retained evidence claims—not a new atlas run performed in this response.

## Recorded workflow extension

You already have `run_workflow.py`, `record_run.py`, `inspect_environment.py`, and `view_report.py`. **We should reuse them first.**

```text
PROPOSED NEXT BUILD: RECORDED REGRESSION WORKFLOW
===============================================================

You request a new recorded run
        |
        v
Existing workflow entry point
        |
        +--> Inspect execution environment
        |
        +--> Record execution of:
        |        tools/run_regression.py
        |                  |
        |                  +--> Verify selected package files
        |                  |
        |                  +--> Discover and execute tests
        |
        +--> Preserve stdout / stderr / execution outcome
        |
        +--> Generate the existing report view
        |
        v
A run directory that can be inspected afterward


DESIRED RECORD
---------------------------------------------------------------
Actual command
Actual working directory
Python / environment information
Start and completion information
Recorded exit status
Captured test output
Manifest identity for the run
Clear indication of missing or failed stages

These are proposed requirements.
We must inspect the existing schemas before adding fields.


FAILURE BEHAVIOR
---------------------------------------------------------------
Integrity failure:
    Record the failure.
    Do not run the test suite.

Test failure:
    Preserve failure output.
    Do not label the experiment or package successful.

Timeout:
    Preserve whatever the recorder supports.
    Mark execution incomplete or timed out.

Report-view failure:
    Preserve the underlying execution record.
    Do not replace the execution outcome with viewer success.

Recording failure:
    Do not claim a complete recorded run.
```

A later GitHub workflow could retain these logs and results as downloadable workflow artifacts. GitHub explicitly supports preserving test output and other files after a job finishes. That is optional automation—not the next prerequisite for your Termux build.[1]

## Development and release flow

```text
ONE WORKING PACKAGE, CONTROLLED CHANGES
===============================================================

Choose one bounded feature
        |
        v
Inspect relevant existing code
        |
        v
Implement a focused change
        |
        v
Add regression tests
        |
        v
Review changed files
        |
        v
Update only approved manifest entries
        |
        v
Run the regression runner
        |
        +--> FAIL: investigate; do not erase mismatches
        |
        +--> PASS: record the actual result
                       |
                       v
              Select GitHub deliverables
                       |
                       v
              Transfer exact file contents
                       |
                       v
              Verify the transferred copy
                       |
                       v
              Package / extract / test release
                       |
                       v
              Describe only verified outcomes


AI COLLABORATION
===============================================================

Builder:
    Produce a small implementation and tests.

Reviewer:
    Challenge the implementation with concrete failing cases.

Perplexity:
    Reconcile findings.
    Clean and finalize deliverables.
    Provide precisely labeled mobile commands.

James:
    Execute the actual phone package.
    Approve changes and publication scope.

Multiple agreeing explanations are not a substitute for a run.
```

Current supplied checkpoint: **91 tests passed in 11.375 seconds, zero skips**. We have not established a verified GitHub copy or whole-package extracted release.

## Start the real workflow build

The next step is source inspection, not another speculative script. This **Termux command** displays the existing workflow interfaces and orchestration code without creating a run:

```sh
cd /storage/emulated/0/Download/Mobile-Research-Kit-Deliverables && python - <<'PY'
from pathlib import Path
import subprocess
import sys

for name in ("run_workflow.py", "record_run.py"):
    print()
    print("===== HELP: " + name + " =====", flush=True)
    subprocess.run(
        [sys.executable, str(Path("tools") / name), "--help"],
        check=False,
    )

print()
print("===== SOURCE: tools/run_workflow.py =====")
print(Path("tools/run_workflow.py").read_text(encoding="utf-8"))
PY
```

**Paste that output.** Then we’ll connect your already-tested regression runner to the existing recording workflow, using its actual arguments and preserving the package’s current structure.

Citations:
[1] Workflow artifacts - GitHub Docs https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts
[2] https://docs.python.org/3.2/library/subprocess.html https://docs.python.org/3.2/library/subprocess.html
[3] Store and share data with workflow artifacts - GitHub Docs https://docs.github.com/en/actions/tutorials/store-and-share-data
[4] monty.subprocess — monty 1.0.0 documentation - Pythonhosted.org https://pythonhosted.org/monty/_modules/monty/subprocess.html
[5] Subprocesses - Python 3.12.0a0 documentation https://pradyunsg-cpython-lutra-testing.readthedocs.io/en/latest/library/asyncio-subprocess.html
[6] Publish Test Results · Actions · GitHub Marketplace https://github.com/marketplace/actions/publish-test-results
[7] Subprocess timeout causes output to be returned as bytes in text mode https://github.com/python/cpython/issues/87597
[8] Actions · GitHub Marketplace - Test Reporter https://github.com/marketplace/actions/test-reporter
[9] How to Use subprocess to Run External Programs in Python 3 https://mangohost.net/blog/how-to-use-subprocess-to-run-external-programs-in-python-3/
[10] proc communicate not exiting on python subprocess timeout using ... https://github.com/python/cpython/issues/75628
[11] python - How to forcefully timeout a process that spawns subprocesses https://stackoverflow.com/questions/53685143/how-to-forcefully-timeout-a-process-that-spawns-subprocesses
[12] Source code for subprocess - Tornado Web Server https://www.tornadoweb.org/en/branch6.3/_modules/subprocess.html
[13] Subprocess.Popen get output even in case of timeout - Stack Overflow https://stackoverflow.com/questions/44335403/subprocess-popen-get-output-even-in-case-of-timeout
[14] [Feature Request] Native Test Results Dashboard for GitHub Actions ... https://github.com/orgs/community/discussions/163123
[15] https://github.com/quantarion369-arch/AQARION/tree/main/AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT
