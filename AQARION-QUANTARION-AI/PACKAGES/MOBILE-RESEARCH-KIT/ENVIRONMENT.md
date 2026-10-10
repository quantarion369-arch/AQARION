Mobile Research Kit — Python and Environment Requirements

Repository: "quantarion369-arch/AQARION"
Package path: "AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT"
Branch audited: "main"
Environment declaration: "manifest.json"
Audit scope: published source, manifest-listed Python modules, regression entry point, package verifier, and existing GitHub Actions workflow.

1. Confirmed environment specification

Item| Finding| Evidence boundary
Declared Python version| "3.13.13"| "manifest.json", field "packaging_python"
CI Python version| "3.13.13"| Existing workflow's "actions/setup-python" configuration
Regression entry point| "tools/run_regression.py"| Existing package source
Package integrity checker| "tools/verify_package.py"| Existing package source
Third-party Python imports| None found in the 29 inspected, manifest-listed Python modules| Import audit of the selected published source
Python dependency lockfile| Not found in the inspected package root| No "requirements.txt", "pyproject.toml", or "setup.py" found at the tested paths
OS compatibility| POSIX-specific process-group behavior exists| Does not establish compatibility across all POSIX systems
Windows compatibility| Not established| Do not claim support without platform-specific testing
Termux suitability| Consistent with the documented Android/Termux workflow| Does not establish compatibility with every Termux installation
Package integrity scope| 35 manifest-listed files| Unlisted files are outside the manifest verification scope

The declared Python version is the project's explicit tested target. This does not establish that it is the only version capable of running the code.

2. Python version policy

The package manifest declares:

"packaging_python": "3.13.13"

The existing GitHub Actions workflow also configures Python "3.13.13" and invokes the package's established regression entry point.

The package verifier uses "Path.is_relative_to()", an API introduced in Python 3.9. This establishes a lower bound for that API only; it is not a complete compatibility proof for the package.

Recommended policy:

- Preserve Python "3.13.13" as the current declared test target until a version change is deliberately approved.
- Treat a different Python version as a separate compatibility target.
- If updating the patch version, update the environment declaration and workflow configuration together, then rerun the complete regression.
- Record the actual interpreter version and executable path in the execution evidence.
- Do not infer a compatibility matrix from one successful run.

Python 3.13.16 was listed as released on September 30, 2026, by the official Python release page. The project's "3.13.13" pin is therefore a reproducibility choice, not the latest patch-version claim.

3. Python dependencies

The import audit covered the 29 Python modules listed by the current manifest:

- Four files under "examples/".
- Seven files under "tools/".
- Eighteen files under "tests/".

The imported modules belong to the Python standard library or to the package itself. No third-party Python package imports were identified in those files.

Representative standard-library modules include:

argparse
contextlib
datetime
hashlib
html
importlib
io
json
math
os
pathlib
platform
re
shutil
signal
subprocess
sys
tempfile
time
unittest
unittest.mock

This finding supports the statement:

«No third-party Python package dependency was identified in the audited manifest-listed Python source.»

It does not prove that every operating-system capability is built into Python or that arbitrary commands launched by the recorder require no external software. "tools/record_run.py" executes a caller-supplied command; dependencies of that command belong to the command being run, not necessarily to the Mobile Research Kit itself.

No package installer or dependency resolver is required by the inspected regression entry point.

4. Operating-system requirements

The package is documented as an Android/Termux-oriented research toolkit. The existing CI workflow runs on "ubuntu-latest".

The source contains POSIX-specific process handling in "tools/record_run.py", including:

subprocess.Popen(
    ...,
    start_new_session=True,
)

and process-group termination using:

os.killpg(process.pid, signal.SIGKILL)

These operations are relevant to timeout and process cleanup. They mean that full recorder behavior cannot be assumed to work unchanged on Windows.

The current evidence supports:

- Linux CI execution.
- The documented Android/Termux development workflow.
- POSIX-specific process handling in the recorder.

It does not establish:

- Universal POSIX portability.
- Native Windows compatibility.
- Android compatibility for every Python distribution or device.
- Long-duration stability, memory limits, or performance guarantees on mobile hardware.

5. Canonical regression command

Run the following from the package directory:

python tools/run_regression.py

Repository-relative working directory:

AQARION-QUANTARION-AI/PACKAGES/MOBILE-RESEARCH-KIT

The runner:

1. Resolves its package root from its own source location.
2. Checks that the verifier and tests directory exist.
3. Invokes "tools/verify_package.py".
4. Stops if package integrity verification fails.
5. Discovers tests matching "test*.py" under "tests/".
6. Runs the discovered "unittest" suite.
7. Returns a nonzero status if verification, discovery, or testing fails.

A successful package-integrity check is necessary for this entry point to proceed to the test suite, but it is not sufficient to establish that the software is correct.

6. Package-integrity command

Run from the package directory:

python tools/verify_package.py --root .

The verifier checks the files selected by "manifest.json", including their byte sizes and SHA-256 hashes. It also rejects unsafe manifest paths and symbolic links along the listed paths.

A successful result means the selected listed files match the declared manifest values at verification time.

It does not establish:

- Integrity of unlisted files.
- Authenticity of the manifest itself.
- Identity with an independently obtained archive.
- Correctness of the source logic.
- Reproducibility of a previous execution.
- Formal mathematical verification.

The manifest is an integrity baseline, not an independent trust anchor.

7. Evidence required for a reproducible run

For every release or audit run, preserve:

Repository and package path
Git commit SHA
Python version
Python executable path
Operating system and architecture
Manifest SHA-256
Package-verification exit code
Discovered test count
Passed test count
Failed test count
Skipped test count
Regression exit code
Standard output and standard error
Execution timestamp
Execution environment

Record observed values only. Do not copy an earlier test count into a new receipt unless the current run actually reports that count.

A successful regression is evidence about the source revision and environment that were executed. It should not automatically be attributed to a different commit, a local working tree, or an archive that was not tested.

8. Recommended release-closure sequence

Freeze a source revision
        |
        v
Verify the package manifest
        |
        v
Run the canonical regression
        |
        v
Create the selected archive
        |
        v
Record archive size and SHA-256
        |
        v
Extract into a fresh directory
        |
        v
Verify the extracted package
        |
        v
Run the regression from the extraction
        |
        v
Preserve the receipt and logs

The sequence is a recommended procedure, not a claim that every stage has already been performed.

A release should not be called independently reproduced or sealed until the relevant archive and fresh-extraction checks have actually completed.

9. Current status and limitations

The inspected repository contains a declared Python target, an established package verifier, a canonical regression entry point, and an existing CI workflow.

The published workflow has reported a successful regression of 117 tests with zero skips for the previously inspected commit. That result is tied to that run and revision; it is not automatically a result for future source changes.

The following remain separate claims requiring separate evidence:

- Compatibility with other Python versions.
- Native Windows support.
- Complete dependency closure for arbitrary user-supplied commands.
- Archive-to-source byte identity.
- Fresh-extraction reproducibility.
- Formal proof or mathematical certification of the research results.

10. References

- Package manifest: "manifest.json"
- Regression entry point: "tools/run_regression.py"
- Package verifier: "tools/verify_package.py"
- Process recorder: "tools/record_run.py"
- Package documentation: "README.md"
- Existing workflow: repository-root ".github/workflows/mobile-research-kit.yml"
- Python 3.13 documentation: https://docs.python.org/3.13/
- Python release versions: https://www.python.org/doc/versions/
- SLSA provenance specification: https://slsa.dev/spec/v1.2/provenance

Evidence rule: distinguish what the source declares, what the test runner executes, what the logs report, and what has been independently reproduced. Do not promote one category into another without additional evidence.
