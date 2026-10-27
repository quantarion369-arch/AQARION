"""Isolated wrapper tests; synthetic scripts, never the real census."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "receipt_runner", Path(__file__).with_name("reproduction.py")
)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

def actual_validator():
    spec = importlib.util.spec_from_file_location(
        "actual_join_validator",
        Path(__file__).with_name("verify.py"),
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "checkout"
        self.repo.mkdir()
        self.package = self.repo / "pkg"
        self.package.mkdir()
        self.env = dict(
            os.environ,
            GIT_AUTHOR_NAME="Fixture",
            GIT_AUTHOR_EMAIL="",
            GIT_COMMITTER_NAME="Fixture",
            GIT_COMMITTER_EMAIL="",
        )
        self.g("init", "-q")
        self.g(
            "remote", "add", "origin",
            "https://example.invalid/fixture.git"
        )
        self.g(
            "commit", "-q", "--allow-empty",
            "-m", "synthetic baseline"
        )
        self.baseline = self.g("rev-parse", "HEAD").strip()

    def g(self, *args):
        return subprocess.check_output(
            ["git", "-c", "core.hooksPath=/dev/null",
             "-C", str(self.repo), *args],
            env=self.env,
            stderr=subprocess.PIPE,
        ).decode()

    def fixture(
        self, verify="print('verify fixture')\n",
        baseline=None, tracked_runner=True
    ):
        files = {
            "verify.py": verify,
            "join_stability_independent_audit.py":
                "print('synthetic audit; no census')\n",
            "reproduce.sh": "#!/bin/sh\nexit 0\n",
            "reproduction.py": "# tracked fixture entry point\n",
            "claims.jsonl": "{}\n",
            "evidence.jsonl": "{}\n",
            "proof.md": "synthetic proof placeholder\n",
            "source.lean": "-- synthetic Lean placeholder\n",
        }
        manifest = {
            "package_id": "JOIN-STABILITY",
            "package_version": "fixture",
            "source_revision": baseline or self.baseline,
            "claim_registry": "claims.jsonl",
            "evidence_registry": "evidence.jsonl",
            "required_artifacts": list(files),
        }
        files["manifest.json"] = json.dumps(manifest)
        for name, text in files.items():
            (self.package / name).write_text(text)
            if name != "reproduction.py" or tracked_runner:
                self.g("add", "--", "pkg/" + name)
        self.g("commit", "-q", "-m", "synthetic package")
        return self.g("rev-parse", "HEAD").strip()

    def run_case(self, expected):
        rc, output = R.run(
            self.package, self.root, expected, io.BytesIO()
        )
        path = output / "receipt.json"
        report = (
            json.loads(path.read_text()) if path.exists() else None
        )
        return rc, output, report

    def test_success_complete_receipt(self):
        rc, out, report = self.run_case(self.fixture())
        self.assertEqual(rc, 0)
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(
            [x["exit_code"] for x in report["commands"]],
            [0, 0, 0],
        )
        self.assertEqual(
            report["source_sha256_before"],
            report["source_sha256_after"],
        )
        self.assertTrue(
            report["tracked_sources_and_revision_unchanged"]
        )
        self.assertEqual(report["lean"]["result"], "NOT_RUN")
        self.assertIn(
            "pkg/manifest.json", report["source_sha256_before"]
        )
        self.assertIn(
            "reproduction.log", report["output_sha256"]
        )
        self.assertTrue(report["finished_at_utc"])

    def test_producer_failure_preserved(self):
        rev = self.fixture(
            "import sys\n"
            "print('producer error', file=sys.stderr)\n"
            "sys.exit(7)\n"
        )
        rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 1)
        self.assertEqual(
            report["commands"][0]["exit_code"], 7
        )
        self.assertEqual(
            report["commands"][1]["result"], "NOT_RUN"
        )
        self.assertIn(
            "producer error",
            (out / "verify.stderr").read_text(),
        )

    def test_logging_failure_cannot_pass(self):
        rev = self.fixture()
        original = R.write_checked
        def fail_log(handle, data):
            if str(getattr(handle, "name", "")).endswith(
                "verify.stdout"
            ):
                raise OSError("injected log failure")
            return original(handle, data)
        with patch.object(R, "write_checked", fail_log):
            rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 90)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(
            report["commands"][0]["logging_exit"], 90
        )
        self.assertEqual(
            report["commands"][1]["result"], "NOT_RUN"
        )

    def test_interruption_cannot_pass(self):
        rev = self.fixture()
        original = R.write_checked
        def interrupt_log(handle, data):
            if str(getattr(handle, "name", "")).endswith(
                "verify.stdout"
            ):
                raise KeyboardInterrupt()
            return original(handle, data)
        with patch.object(R, "write_checked", interrupt_log):
            rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 130)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(
            report["commands"][1]["result"], "NOT_RUN"
        )

    def test_receipt_failure_is_nonzero(self):
        rev = self.fixture()
        with patch.object(
            R, "atomic_receipt",
            side_effect=OSError("injected receipt failure")
        ), contextlib.redirect_stderr(io.StringIO()):
            rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 93)
        self.assertIsNone(report)

    def test_unstaged_source_rejected(self):
        rev = self.fixture()
        (self.package / "proof.md").write_text("dirty\n")
        rc, out, report = self.run_case(rev)
        self.assertNotEqual(rc, 0)
        self.assertEqual(report["preflight"], "BLOCKED")
        self.assertTrue(all(
            x["result"] == "NOT_RUN" for x in report["commands"]
        ))

    def test_staged_source_rejected(self):
        rev = self.fixture()
        (self.package / "proof.md").write_text("dirty\n")
        self.g("add", "--", "pkg/proof.md")
        self.assertNotEqual(self.run_case(rev)[0], 0)

    def test_wrong_revision_rejected(self):
        self.fixture()
        rc, out, report = self.run_case("f"*40)
        self.assertNotEqual(rc, 0)
        self.assertEqual(report["preflight"], "BLOCKED")

    def test_missing_baseline_object_rejected(self):
        rev = self.fixture(baseline="f"*40)
        rc, out, report = self.run_case(rev)
        self.assertNotEqual(rc, 0)
        self.assertEqual(report["preflight"], "BLOCKED")

    def test_source_mutation_stops_next_command(self):
        rev = self.fixture(
            "from pathlib import Path\n"
            "Path('proof.md').write_text("
            "'changed during execution')\n"
        )
        rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 94)
        self.assertEqual(
            report["commands"][1]["result"], "NOT_RUN"
        )
        self.assertFalse(
            report["tracked_sources_and_revision_unchanged"]
        )

    def test_untracked_entrypoint_rejected(self):
        rev = self.fixture(tracked_runner=False)
        rc, out, report = self.run_case(rev)
        self.assertNotEqual(rc, 0)
        self.assertIn("not tracked", report["error"])

    def test_unique_outputs(self):
        rev = self.fixture()
        a = self.run_case(rev)
        b = self.run_case(rev)
        self.assertEqual((a[0], b[0]), (0, 0))
        self.assertNotEqual(a[1], b[1])

    def test_output_inside_repository_rejected(self):
        rev = self.fixture()
        with self.assertRaises(RuntimeError):
            R.run(self.package, self.repo, rev, io.BytesIO())


    def test_existing_nonancestor_rejected(self):
        tree = self.g(
            "rev-parse", self.baseline + "^{tree}"
        ).strip()
        unrelated = self.g(
            "commit-tree", tree,
            "-m", "existing unrelated root"
        ).strip()
        self.g("cat-file", "-e", unrelated + "^{commit}")
        rev = self.fixture(baseline=unrelated)
        ancestry = subprocess.run(
            ["git", "-C", str(self.repo), "merge-base",
             "--is-ancestor", unrelated, rev],
            capture_output=True,
        )
        self.assertEqual(ancestry.returncode, 1)
        rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 2)
        self.assertEqual(report["preflight"], "BLOCKED")
        self.assertEqual(report["source_baseline"], unrelated)
        self.assertTrue(all(
            x["result"] == "NOT_RUN"
            for x in report["commands"]
        ))

    def test_atomic_temporary_write_failure(self):
        rev = self.fixture()
        original = R.write_checked
        def fail_temporary(handle, data):
            if str(getattr(handle, "name", "")).endswith(
                ".json.tmp"
            ):
                raise OSError("injected temporary receipt write")
            return original(handle, data)
        with patch.object(
            R, "write_checked", fail_temporary
        ), contextlib.redirect_stderr(io.StringIO()):
            rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 93)
        self.assertIsNone(report)
        self.assertFalse((out / "receipt.json").exists())
        self.assertFalse((out / "receipt.json.tmp").exists())

    def test_atomic_replacement_failure(self):
        rev = self.fixture()
        with patch.object(
            R.os, "replace",
            side_effect=OSError("injected atomic replacement")
        ), contextlib.redirect_stderr(io.StringIO()):
            rc, out, report = self.run_case(rev)
        self.assertEqual(rc, 93)
        self.assertIsNone(report)
        self.assertFalse((out / "receipt.json").exists())
        self.assertFalse((out / "receipt.json.tmp").exists())

    def test_short_write_rejected(self):
        class ShortWriter:
            def write(self, data):
                return len(data) - 1
            def flush(self):
                pass
        with self.assertRaisesRegex(OSError, "Short output write"):
            R.write_checked(ShortWriter(), b"abc")

    def test_actual_validator_positive_and_negative_controls(self):
        validator = actual_validator()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            validator.run_negative_control_self_tests()
        text = output.getvalue()
        self.assertIn("POSITIVE_CONTROLS=2/2", text)
        self.assertIn("NEGATIVE_CONTROLS=10/10", text)
        self.assertEqual(text.count("NEGATIVE_CONTROL="), 10)

    def test_validator_wrong_errors_cannot_pass(self):
        for kind in ("wrong_reason", "unexpected_exception"):
            with self.subTest(kind=kind):
                validator = actual_validator()
                if kind == "wrong_reason":
                    error = validator.VerificationError("unrelated reason")
                    expected = "wrong rejection reason"
                else:
                    error = OSError("unrelated IO failure")
                    expected = "unexpected exception"
                with patch.object(
                    validator, "validate_claims",
                    side_effect=[{"A"}, error],
                ), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaisesRegex(
                        validator.VerificationError, expected
                    ):
                        validator.run_negative_control_self_tests()

    def test_validator_acceptance_mutant_detected(self):
        validator = actual_validator()
        with patch.object(
            validator, "validate_claims",
            side_effect=[{"A"}, {"A"}],
        ), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(
                validator.VerificationError,
                "failed to reject invalid input",
            ):
                validator.run_negative_control_self_tests()

if __name__ == "__main__":
    unittest.main(verbosity=2)
