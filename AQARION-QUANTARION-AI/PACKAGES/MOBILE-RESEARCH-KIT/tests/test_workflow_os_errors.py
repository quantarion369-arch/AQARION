import contextlib
import importlib.util
import io
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
    "workflow_os_errors_under_test",
    SOURCE,
)
WORKFLOW = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKFLOW)


class WorkflowOSErrorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.output_root = Path(self.temporary.name) / "output"

    def run_case(self, invoke_error):
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
                side_effect=invoke_error,
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

    def test_tool_invocation_os_error(self):
        stdout, stderr, invoked = self.run_case(
            OSError("synthetic subprocess launch failure")
        )
        self.assertEqual(invoked.call_count, 1)
        self.assertIn(
            "synthetic subprocess launch failure",
            stderr,
        )
        self.assertNotIn("WORKFLOW_RECORDER_EXIT=", stdout)

        directories = list(
            self.output_root.glob("workflow-*")
        )
        self.assertEqual(len(directories), 1)
        self.assertFalse(
            (directories[0] / "viewer.html").exists()
        )

    def test_output_root_cannot_be_a_file(self):
        original = b"existing file must remain unchanged"
        self.output_root.write_bytes(original)

        stdout, _, invoked = self.run_case(
            AssertionError("No tool should start")
        )
        invoked.assert_not_called()
        self.assertEqual(
            self.output_root.read_bytes(),
            original,
        )
        self.assertNotIn("WORKFLOW_DIRECTORY=", stdout)


if __name__ == "__main__":
    unittest.main()
