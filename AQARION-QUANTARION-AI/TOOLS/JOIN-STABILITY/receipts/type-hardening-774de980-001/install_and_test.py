import ast
import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import traceback
import unittest

repo = Path(sys.argv[1]).resolve()
source_run = Path(sys.argv[2]).resolve()
run = Path(sys.argv[3]).resolve()

prefix = Path("AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY")
package = repo / prefix
pb_relative = Path("AQARION-QUANTARION-AI/PB_001.md")
workflow_relative = Path(".github/workflows/join-stability.yml")
test_relative = prefix / "test_validator_types.py"

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(repo), *args],
        stderr=subprocess.PIPE,
    ).decode()

def atomic_write(path, data, mode):
    descriptor, temporary = tempfile.mkstemp(
        prefix=".aqarion-install-",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

report = {
    "status": "FAIL",
    "installation_started": False,
    "source_run": str(source_run),
    "repository": str(repo),
    "finite_census": "NOT_RUN",
    "lean": "NOT_RUN",
    "git_stage_commit_push": "NONE",
}

try:
    # Verify the complete preserved candidate-run archive.
    manifest_lines = (
        source_run / "SHA256SUMS"
    ).read_text(encoding="utf-8").splitlines()

    for line in manifest_lines:
        expected, name = line.split("  ", 1)
        path = (source_run / name).resolve()

        require(
            source_run in path.parents,
            "Unsafe saved-artifact path",
        )
        require(path.is_file(), f"Missing saved artifact: {name}")
        require(
            sha(path.read_bytes()) == expected,
            f"Saved-artifact hash mismatch: {name}",
        )

    previous = json.loads(
        (source_run / "results.json").read_text(encoding="utf-8")
    )

    require(previous["status"] == "PASS", "Candidate run was not PASS")

    revision = git("rev-parse", "HEAD").strip()
    require(
        revision == previous["tested_local_revision"],
        "HEAD differs from the tested candidate baseline",
    )
    report["parent_revision"] = revision

    original_targets = {
        "verify.py": package / "verify.py",
        "PB_001.md": repo / pb_relative,
        "manifest.json": package / "manifest.json",
        "claims.jsonl": package / "claims.jsonl",
        "evidence.jsonl": package / "evidence.jsonl",
    }

    for name, path in original_targets.items():
        require(
            path.read_bytes()
            == (source_run / "baseline" / name).read_bytes(),
            f"Local baseline changed: {name}",
        )

    require(
        not (repo / test_relative).exists(),
        "test_validator_types.py already exists; refusing overwrite",
    )

    workflow_path = repo / workflow_relative
    workflow_before = workflow_path.read_text(encoding="utf-8")

    marker = "      - name: Preserve diagnostics even on test failure\n"

    require(
        workflow_before.count(marker) == 1,
        "Workflow differs from the expected reviewed structure",
    )
    require(
        "Run validator type regression tests" not in workflow_before,
        "Workflow already contains the new regression step",
    )

    # Preserve the tested fixtures verbatim as standalone tests.
    driver = (
        source_run / "prepare_and_test.py"
    ).read_text(encoding="utf-8")

    positive_start = driver.index("def positives(module):")
    positive_end = driver.index("\nbefore_positive =", positive_start)
    positive_function = driver[positive_start:positive_end]

    fixture_start = driver.index("base_claim = {")
    fixture_end = driver.index("\nresults = []", fixture_start)
    fixtures = driver[fixture_start:fixture_end]

    test_header = '''
"""Maintained malformed-type regressions for JOIN-STABILITY.

Fixtures originate from the source-bound candidate verification.
No temporary run directory is required to execute these tests.
"""

import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location(
    "_join_type_test_verifier", ROOT / "verify.py"
)
V = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = V
spec.loader.exec_module(V)
V.ROOT = ROOT

manifest = json.loads(
    (ROOT / "manifest.json").read_text(encoding="utf-8")
)

def read_records(name):
    return [
        json.loads(line)
        for line in (ROOT / name).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

claims = read_records("claims.jsonl")
evidence = read_records("evidence.jsonl")

'''

    test_footer = '''
if len(cases) != 15 or len({name for name, _, _ in cases}) != 15:
    raise RuntimeError("Expected fifteen unique malformed-type controls")


class TypeBoundaryTests(unittest.TestCase):
    def test_actual_manifest_and_registries(self):
        actual = positives(V)
        expected = (
            sorted(record["claim_id"] for record in claims),
            sorted(record["evidence_id"] for record in evidence),
        )
        self.assertEqual(actual, expected)

    def test_existing_in_memory_controls(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            V.run_negative_control_self_tests()
        text = stream.getvalue()
        self.assertIn("POSITIVE_CONTROLS=2/2", text)
        self.assertIn("NEGATIVE_CONTROLS=10/10", text)


def make_type_test(location, action):
    def test(self):
        first = outcome(V, action)
        second = outcome(V, action)
        self.assertEqual(first["exception"], "VerificationError")
        self.assertTrue(first["controlled"])
        self.assertTrue(
            first["message"].startswith(
                f"TYPE_ERROR: {location}:"
            ),
            first["message"],
        )
        self.assertEqual(first, second)
    return test


for name, location, action in cases:
    setattr(
        TypeBoundaryTests,
        "test_type_" + name,
        make_type_test(location, action),
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''

    test_source = (
        test_header
        + positive_function
        + "\n\n"
        + fixtures
        + "\n\n"
        + test_footer
    )

    ast.parse(test_source)
    compile(test_source, str(test_relative), "exec")

    workflow_step = '''      - name: Run validator type regression tests
        env:
          CI_EVIDENCE_DIR: ${{ runner.temp }}/join-stability-contract
        shell: python
        run: |
          import json
          import os
          from pathlib import Path
          import subprocess
          import sys

          output = Path(os.environ["CI_EVIDENCE_DIR"])
          output.mkdir(parents=True, exist_ok=True)
          script = (
              Path(os.environ["GITHUB_WORKSPACE"])
              / "AQARION-QUANTARION-AI/TOOLS/JOIN-STABILITY"
              / "test_validator_types.py"
          )
          result = subprocess.run(
              [sys.executable, "-I", str(script)],
              stdout=subprocess.PIPE,
              stderr=subprocess.STDOUT,
              text=True,
          )
          (output / "validator-types.log").write_text(
              result.stdout, encoding="utf-8"
          )
          (output / "validator-types-execution.json").write_text(
              json.dumps({
                  "status": "PASS" if result.returncode == 0 else "FAIL",
                  "expected_tests": 17,
                  "exit_code": result.returncode,
                  "scope": "TYPE_BOUNDARIES_AND_VALIDATOR_CONTROLS_ONLY",
                  "finite_census": "NOT_RUN",
                  "lean": "NOT_RUN",
                  "promotion_changed": False,
              }, indent=2) + "\\n",
              encoding="utf-8",
          )
          print(result.stdout, end="")
          raise SystemExit(result.returncode)
'''

    workflow_candidate = workflow_before.replace(
        marker, workflow_step + marker, 1
    )

    replacements = {
        prefix / "verify.py":
            (source_run / "candidate" / "verify.py").read_bytes(),
        pb_relative:
            (source_run / "candidate" / "PB_001.md").read_bytes(),
        test_relative:
            test_source.encode("utf-8"),
        workflow_relative:
            workflow_candidate.encode("utf-8"),
    }

    for relative in replacements:
        require(
            not git("diff", "--cached", "--name-only", "--", str(relative)).strip(),
            f"Target already has staged changes: {relative}",
        )

    backup = run / "before"
    backup.mkdir()

    for relative in replacements:
        path = repo / relative
        if path.exists():
            target = backup / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())

    preserved_manifest = (package / "manifest.json").read_bytes()
    preserved_claims = (package / "claims.jsonl").read_bytes()
    preserved_evidence = (package / "evidence.jsonl").read_bytes()

    report["installation_started"] = True
    report["installed_paths"] = [str(p) for p in replacements]

    for relative, data in replacements.items():
        path = repo / relative
        mode = (path.stat().st_mode & 0o777) if path.exists() else 0o644
        atomic_write(path, data, mode)

    installed_hashes = {
        str(relative): sha((repo / relative).read_bytes())
        for relative in replacements
    }

    # Use the same explicit ReceiptTests collection as existing CI.
    log = io.StringIO()

    with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
        wrapper_namespace = runpy.run_path(
            str(package / "test_reproduction.py")
        )
        type_namespace = runpy.run_path(
            str(package / "test_validator_types.py")
        )

        wrapper_suite = unittest.defaultTestLoader.loadTestsFromTestCase(
            wrapper_namespace["ReceiptTests"]
        )
        type_suite = unittest.defaultTestLoader.loadTestsFromTestCase(
            type_namespace["TypeBoundaryTests"]
        )

        require(
            wrapper_suite.countTestCases() == 20,
            "Expected exactly twenty existing wrapper tests",
        )
        require(
            type_suite.countTestCases() == 17,
            "Expected exactly seventeen type-regression tests",
        )

        suite = unittest.TestSuite([wrapper_suite, type_suite])
        result = unittest.TextTestRunner(
            stream=log, verbosity=2
        ).run(suite)

    (run / "tests.log").write_text(log.getvalue(), encoding="utf-8")
    print(log.getvalue(), end="")

    report.update({
        "expected_wrapper_tests": 20,
        "expected_type_tests": 17,
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "skipped": len(result.skipped),
    })

    require(
        result.testsRun == 37
        and result.wasSuccessful()
        and not result.skipped,
        "Required tests failed, errored, skipped, or were not all run",
    )

    for relative, expected in installed_hashes.items():
        require(
            sha((repo / relative).read_bytes()) == expected,
            f"Installed source changed during tests: {relative}",
        )

    require(
        (package / "manifest.json").read_bytes() == preserved_manifest,
        "Manifest changed during tests",
    )
    require(
        (package / "claims.jsonl").read_bytes() == preserved_claims,
        "Claims registry changed during tests",
    )
    require(
        (package / "evidence.jsonl").read_bytes() == preserved_evidence,
        "Evidence registry changed during tests",
    )
    require(
        git("rev-parse", "HEAD").strip() == revision,
        "HEAD changed during execution",
    )

    (run / "changes.diff").write_text(
        git("diff", "--", *[str(p) for p in replacements]),
        encoding="utf-8",
    )
    (run / "new_test_validator_types.py").write_bytes(
        (repo / test_relative).read_bytes()
    )
    (run / "git-status.txt").write_text(
        git("status", "--short"), encoding="utf-8"
    )

    report["installed_source_sha256"] = installed_hashes
    report["manifest_and_registries_unchanged"] = True
    report["head_unchanged"] = True
    report["status"] = "PASS"

except BaseException:
    report["error"] = traceback.format_exc()
    print(report["error"], file=sys.stderr)

finally:
    (run / "execution.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

print("INSTALLATION_STARTED=" + str(report["installation_started"]))
print("RESULT=" + report["status"])

if report["status"] == "PASS":
    print("WRAPPER_TESTS=20/20")
    print("TYPE_REGRESSION_TESTS=17/17")
    print("TOTAL_TESTS=37/37")
    print("TYPE_TESTS_WIRED_INTO_CI=YES")
    print("EXISTING_CI_20_TEST_CONTRACT=UNCHANGED")
    print("MANIFEST_AND_REGISTRIES_UNCHANGED=YES")
    print("FULL_CENSUS_AND_LEAN=NOT_RUN")
    print("GIT_STAGE_COMMIT_PUSH=NONE")
else:
    print("NO_AUTOMATIC_ROLLBACK_OR_COMMIT")
    print("PRESERVED_BACKUPS_AND_REPORT=" + str(run))

raise SystemExit(0 if report["status"] == "PASS" else 1)
