import argparse
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path


TOOLS = Path(__file__).resolve().parent
WORKFLOW_ERROR = 125


def invoke(tool, arguments):
    return subprocess.run(
        [sys.executable, str(TOOLS / tool), *map(str, arguments)],
        capture_output=True,
        text=True,
    )


def show_errors(result):
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")


def main():
    parser = argparse.ArgumentParser(
        description="Inspect, record, and generate a local HTML report."
    )
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]

    if not command:
        parser.error("Supply a command after --")
    if not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("--timeout must be finite and positive")

    recorder_exit = None

    try:
        args.output_root.mkdir(parents=True, exist_ok=True)
        directory = Path(tempfile.mkdtemp(
            prefix="workflow-", dir=args.output_root
        )).resolve()

        inventory = directory / "inventory.json"
        runs = directory / "runs"
        viewer = directory / "viewer.html"

        print("WORKFLOW_DIRECTORY=" + str(directory), flush=True)

        inspected = invoke(
            "inspect_environment.py", [inventory]
        )
        show_errors(inspected)
        if inspected.returncode != 0:
            raise RuntimeError(
                "Inventory tool exited with "
                + str(inspected.returncode)
            )
        print("INVENTORY_FILE=" + str(inventory), flush=True)

        recorded = invoke("record_run.py", [
            "--timeout", args.timeout,
            "--output-root", runs,
            "--", *command,
        ])
        if recorded.stdout:
            print(recorded.stdout, end="", flush=True)
        show_errors(recorded)

        recorder_exit = recorded.returncode
        print(
            "WORKFLOW_RECORDER_EXIT=" + str(recorder_exit),
            flush=True,
        )

        receipts = list(runs.glob("run-*/receipt.json"))
        if len(receipts) != 1:
            raise RuntimeError("Expected exactly one execution receipt")

        receipt = receipts[0]
        record = json.loads(receipt.read_text(encoding="utf-8"))
        if (
            not isinstance(record, dict)
            or record.get("kind") != "command_execution"
            or record.get("status") == "started"
            or record.get("recorder_exit") != recorder_exit
        ):
            raise RuntimeError("Missing or inconsistent final receipt")

        print("RECEIPT_FILE=" + str(receipt), flush=True)

        viewed = invoke("view_report.py", [
            "--receipt", receipt,
            "--inventory", inventory,
            "--output", viewer,
        ])
        show_errors(viewed)
        if viewed.returncode != 0:
            raise RuntimeError(
                "Viewer tool exited with " + str(viewed.returncode)
            )
        if not viewer.is_file():
            raise RuntimeError("Viewer output was not created")

        print("VIEWER_FILE=" + str(viewer), flush=True)
        print("WORKFLOW_STATUS=reports_created", flush=True)
        print("WORKFLOW_EXIT=" + str(recorder_exit), flush=True)
        return recorder_exit

    except (OSError, ValueError, RuntimeError) as error:
        print("WORKFLOW_ERROR=" + str(error), file=sys.stderr)
        print("WORKFLOW_STATUS=orchestration_failed", flush=True)
        print("WORKFLOW_EXIT=" + str(WORKFLOW_ERROR), flush=True)
        return WORKFLOW_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
