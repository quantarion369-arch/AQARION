import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "tools"
    / "run_workflow.py"
)
SPEC = importlib.util.spec_from_file_location(
    "workflow_under_test",
    SOURCE,
)
WORKFLOW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKFLOW)


class WorkflowFailureTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output_root = Path(self.temporary.name) / "output"

    def result(self, code=0, stderr=""):
        return subprocess.CompletedProcess(
            args=["simulated-tool"],
            returncode=code,
            stdout="",
            stderr=stderr,
        )

    def inventory_ok(self, arguments):
        Path(arguments[0]).write_text(
            json.dumps({"kind": "environment_snapshot"}),
            encoding="utf-8",
        )
        return self.result()

    def write_receipt(self, arguments, record):
        runs = Path(
            arguments[arguments.index("--output-root") + 1]
        )
        run = runs / "run-synthetic"
        run.mkdir(parents=True)
        (run / "receipt.json").write_text(
            json.dumps(record),
            encoding="utf-8",
        )

    def recorder_ok(self, arguments, code=0):
        self.write_receipt(
            arguments,
            {
                "kind": "command_execution",
                "status": "completed",
                "child_returncode": code,
                "recorder_exit": code,
            },
        )
        return self.result(code)

    def run_case(self, behavior):
        argv = [
            str(SOURCE),
            "--timeout",
            "5",
            "--output-root",
            str(self.output_root),
            "--",
            sys.executable,
            "-c",
            "print('synthetic')",
        ]
        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(sys, "argv", argv):
            with patch.object(
                WORKFLOW,
                "invoke",
                side_effect=behavior,
            ) as invoked:
                with contextlib.redirect_stdout(stdout):
                    with contextlib.redirect_stderr(stderr):
                        code = WORKFLOW.main()

        self.assertEqual(code, 125)
        self.assertIn(
            "WORKFLOW_STATUS=orchestration_failed",
            stdout.getvalue(),
        )
        self.assertIn("WORKFLOW_EXIT=125", stdout.getvalue())
        self.assertIn("WORKFLOW_ERROR=", stderr.getvalue())

        return stdout.getvalue(), stderr.getvalue(), invoked

    def test_inventory_failure_stops_before_recording(self):
        def behavior(tool, arguments):
            self.assertEqual(tool, "inspect_environment.py")
            return self.result(1, "synthetic inventory failure")

        stdout, stderr, invoked = self.run_case(behavior)
        self.assertEqual(invoked.call_count, 1)
        self.assertIn("Inventory tool exited with 1", stderr)
        self.assertIn("synthetic inventory failure", stderr)
        self.assertNotIn("WORKFLOW_RECORDER_EXIT=", stdout)

    def test_missing_receipt_is_orchestration_failure(self):
        def behavior(tool, arguments):
            if tool == "inspect_environment.py":
                return self.inventory_ok(arguments)
            self.assertEqual(tool, "record_run.py")
            return self.result(127)

        stdout, stderr, invoked = self.run_case(behavior)
        self.assertEqual(invoked.call_count, 2)
        self.assertIn(
            "Expected exactly one execution receipt",
            stderr,
        )
        self.assertIn("WORKFLOW_RECORDER_EXIT=127", stdout)

    def test_malformed_receipt_is_orchestration_failure(self):
        def behavior(tool, arguments):
            if tool == "inspect_environment.py":
                return self.inventory_ok(arguments)

            self.assertEqual(tool, "record_run.py")
            runs = Path(
                arguments[arguments.index("--output-root") + 1]
            )
            run = runs / "run-synthetic"
            run.mkdir(parents=True)
            (run / "receipt.json").write_text(
                "not valid JSON",
                encoding="utf-8",
            )
            return self.result()

        _, _, invoked = self.run_case(behavior)
        self.assertEqual(invoked.call_count, 2)

    def test_inconsistent_receipts_are_rejected(self):
        records = [
            {
                "kind": "wrong-kind",
                "status": "completed",
                "recorder_exit": 0,
            },
            {
                "kind": "command_execution",
                "status": "started",
                "recorder_exit": 0,
            },
            {
                "kind": "command_execution",
                "status": "completed",
                "recorder_exit": 7,
            },
            [],
        ]

        for record in records:
            with self.subTest(record=record):
                def behavior(tool, arguments):
                    if tool == "inspect_environment.py":
                        return self.inventory_ok(arguments)
                    self.assertEqual(tool, "record_run.py")
                    self.write_receipt(arguments, record)
                    return self.result()

                _, stderr, invoked = self.run_case(behavior)
                self.assertEqual(invoked.call_count, 2)
                self.assertIn(
                    "Missing or inconsistent final receipt",
                    stderr,
                )

    def test_viewer_failure_preserves_recorded_result(self):
        def behavior(tool, arguments):
            if tool == "inspect_environment.py":
                return self.inventory_ok(arguments)
            if tool == "record_run.py":
                return self.recorder_ok(arguments, code=7)
            self.assertEqual(tool, "view_report.py")
            return self.result(1, "synthetic viewer failure")

        stdout, stderr, invoked = self.run_case(behavior)
        self.assertEqual(invoked.call_count, 3)
        self.assertIn("WORKFLOW_RECORDER_EXIT=7", stdout)
        self.assertIn("Viewer tool exited with 1", stderr)

        receipts = list(
            self.output_root.glob(
                "workflow-*/runs/run-*/receipt.json"
            )
        )
        self.assertEqual(len(receipts), 1)
        record = json.loads(receipts[0].read_text())
        self.assertEqual(record["child_returncode"], 7)
        self.assertEqual(record["recorder_exit"], 7)

    def test_viewer_success_without_output_is_rejected(self):
        def behavior(tool, arguments):
            if tool == "inspect_environment.py":
                return self.inventory_ok(arguments)
            if tool == "record_run.py":
                return self.recorder_ok(arguments)
            self.assertEqual(tool, "view_report.py")
            return self.result()

        _, stderr, invoked = self.run_case(behavior)
        self.assertEqual(invoked.call_count, 3)
        self.assertIn("Viewer output was not created", stderr)


if __name__ == "__main__":
    unittest.main()
