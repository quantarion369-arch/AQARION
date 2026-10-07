import argparse
import json
import math
import os
import signal
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def write_receipt(path, record):
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        print(json.dumps(record, indent=2), file=handle)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def stop_group(process):
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def main():
    parser = argparse.ArgumentParser()
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

    args.output_root.mkdir(parents=True, exist_ok=True)
    directory = Path(tempfile.mkdtemp(
        prefix="run-", dir=args.output_root
    )).resolve()

    receipt = directory / "receipt.json"
    record = {
        "schema_version": "0.1.0",
        "kind": "command_execution",
        "status": "started",
        "started_at_utc": utc_now(),
        "command": command,
        "working_directory": str(Path.cwd()),
        "timeout_seconds": args.timeout,
        "stdout_file": "stdout.txt",
        "stderr_file": "stderr.txt",
        "interpretation": "Process evidence only; no mathematical verdict.",
    }
    write_receipt(receipt, record)
    print("RUN_DIRECTORY=" + str(directory), flush=True)

    started = time.monotonic()
    process = None
    recorder_exit = 127

    with (directory / "stdout.txt").open("wb") as stdout:
        with (directory / "stderr.txt").open("wb") as stderr:
            try:
                process = subprocess.Popen(
                    command,
                    stdout=stdout,
                    stderr=stderr,
                    start_new_session=True,
                )
                record["process_id"] = process.pid
                write_receipt(receipt, record)
                code = process.wait(timeout=args.timeout)
                record["status"] = "completed"
                recorder_exit = code if code >= 0 else 128 - code
            except subprocess.TimeoutExpired:
                stop_group(process)
                record["status"] = "timed_out"
                recorder_exit = 124
            except KeyboardInterrupt:
                if process is not None:
                    stop_group(process)
                record["status"] = "interrupted"
                recorder_exit = 130
            except OSError as error:
                if process is not None:
                    stop_group(process)
                    record["status"] = "recorder_error"
                else:
                    record["status"] = "launch_failed"
                record["error"] = str(error)
                recorder_exit = 127

    record["child_returncode"] = (
        process.returncode if process is not None else None
    )
    record["recorder_exit"] = recorder_exit
    record["ended_at_utc"] = utc_now()
    record["elapsed_seconds"] = round(time.monotonic() - started, 6)
    write_receipt(receipt, record)

    print("STATUS=" + record["status"])
    print("RECORDER_EXIT=" + str(recorder_exit))
    return recorder_exit


if __name__ == "__main__":
    raise SystemExit(main())
