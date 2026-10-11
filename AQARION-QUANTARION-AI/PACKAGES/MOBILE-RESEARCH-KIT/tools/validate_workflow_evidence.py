#!/usr/bin/env python3
"""Validate Mobile Research Kit execution evidence.

Public API:
    validate_evidence(evidence_root, environment) -> metadata

Writes run-metadata.json at the evidence root.
Evidence validity is separate from child-command success.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping

REQUIRED_ENV = (
    "GITHUB_REPOSITORY",
    "GITHUB_SHA",
    "GITHUB_REF",
    "GITHUB_WORKFLOW",
    "GITHUB_EVENT_NAME",
    "GITHUB_RUN_ID",
    "GITHUB_RUN_ATTEMPT",
    "GITHUB_SERVER_URL",
)

TERMINAL_STATUSES = frozenset({
    "completed",
    "timed_out",
    "interrupted",
    "recorder_error",
    "launch_failed",
})


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_metadata(path, metadata):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".run-metadata-",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(metadata, handle, indent=2, sort_keys=True)
            handle.write(chr(10))
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def validate_evidence(
    evidence_root,
    environment: Mapping[str, str],
):
    root = Path(evidence_root)
    failures = []
    metadata = {
        "schema_version": "1.0",
        "validated_at_utc": datetime.now(timezone.utc).isoformat(),
        "acceptance_passed": False,
        "acceptance_failures": failures,
        "theorem_proved": False,
        "formal_kernel_accepted": False,
        "independently_certified": False,
    }

    bindings = {}
    for name in REQUIRED_ENV:
        value = environment.get(name)
        if not isinstance(value, str) or not value.strip():
            failures.append("missing GitHub run-binding field: " + name)
        else:
            bindings[name] = value.strip()

    fields = {
        "repository": "GITHUB_REPOSITORY",
        "commit_sha": "GITHUB_SHA",
        "ref": "GITHUB_REF",
        "workflow": "GITHUB_WORKFLOW",
        "event_name": "GITHUB_EVENT_NAME",
        "run_id": "GITHUB_RUN_ID",
        "run_attempt": "GITHUB_RUN_ATTEMPT",
    }
    for field, variable in fields.items():
        metadata[field] = bindings.get(variable)

    if all(name in bindings for name in (
        "GITHUB_SERVER_URL", "GITHUB_REPOSITORY", "GITHUB_RUN_ID"
    )):
        metadata["run_url"] = (
            bindings["GITHUB_SERVER_URL"].rstrip("/")
            + "/" + bindings["GITHUB_REPOSITORY"]
            + "/actions/runs/" + bindings["GITHUB_RUN_ID"]
        )
        if "GITHUB_RUN_ATTEMPT" in bindings:
            metadata["run_attempt_url"] = (
                metadata["run_url"]
                + "/attempts/" + bindings["GITHUB_RUN_ATTEMPT"]
            )

    if not root.is_dir():
        failures.append("evidence root is not an existing directory")
        return metadata

    def unique(pattern, label):
        paths = sorted(root.glob(pattern))
        if len(paths) != 1:
            failures.append(
                "expected exactly one " + label
                + "; found " + str(len(paths))
            )
            return None
        path = paths[0]
        if path.is_symlink() or not path.is_file():
            failures.append(label + " is not a regular evidence file")
            return None
        try:
            path.resolve().relative_to(root.resolve())
        except ValueError:
            failures.append(label + " escapes evidence root")
            return None
        return path

    def load_object(path, label):
        if path is None:
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            failures.append(
                label + " is not readable valid JSON: " + str(exc)
            )
            return None
        if not isinstance(value, dict) or not value:
            failures.append(label + " must be a nonempty JSON object")
            return None
        return value

    receipt_path = unique(
        "workflow-*/runs/run-*/receipt.json", "receipt"
    )
    viewer_path = unique("workflow-*/viewer.html", "viewer")
    inventory_path = unique("workflow-*/inventory.json", "inventory")

    if receipt_path and viewer_path and inventory_path:
        workflow_dir = receipt_path.parent.parent.parent
        if (
            viewer_path.parent != workflow_dir
            or inventory_path.parent != workflow_dir
        ):
            failures.append("evidence files belong to different workflows")

    receipt = load_object(receipt_path, "execution receipt")
    load_object(inventory_path, "environment inventory")

    if viewer_path:
        try:
            if viewer_path.stat().st_size == 0:
                failures.append("viewer is empty")
        except OSError as exc:
            failures.append("cannot inspect viewer: " + str(exc))

    output_paths = {}

    if receipt is not None:
        if receipt.get("kind") != "command_execution":
            failures.append("receipt kind is not command_execution")

        status = receipt.get("status")
        if status not in TERMINAL_STATUSES:
            failures.append("receipt was not finalized")
        metadata["receipt_status"] = status

        ended = receipt.get("ended_at_utc")
        if not isinstance(ended, str) or not ended.strip():
            failures.append("receipt has no ended_at_utc")
        else:
            try:
                timestamp = datetime.fromisoformat(ended)
                if timestamp.utcoffset() is None:
                    raise ValueError("timezone is missing")
            except ValueError:
                failures.append("receipt ended_at_utc is invalid")

        exit_code = receipt.get("recorder_exit")
        if isinstance(exit_code, bool) or not isinstance(exit_code, int):
            failures.append("receipt recorder_exit must be an integer")
        else:
            metadata["recorder_exit"] = exit_code
            metadata["child_command_succeeded"] = (
                status == "completed" and exit_code == 0
            )

        command = receipt.get("command")
        if (
            not isinstance(command, list)
            or not command
            or any(not isinstance(item, str) for item in command)
        ):
            failures.append("receipt command must be a nonempty string list")

        for field in ("stdout_file", "stderr_file"):
            name = receipt.get(field)
            if (
                not isinstance(name, str)
                or not name.strip()
                or name in {".", ".."}
                or "/" in name
                or "\\" in name
                or chr(0) in name
            ):
                failures.append("unsafe recorded output filename: " + field)
                continue

            path = receipt_path.parent / name
            if path.is_symlink() or not path.is_file():
                failures.append(
                    "missing or empty recorded output file: " + field
                    + " (file missing or not regular)"
                )
                continue

            # Empty stdout and stderr are valid process output.
            output_paths[field] = path

        if (
            "stdout_file" in output_paths
            and "stderr_file" in output_paths
            and output_paths["stdout_file"] == output_paths["stderr_file"]
        ):
            failures.append("stdout and stderr must be distinct files")

    hash_paths = {
        "receipt": receipt_path,
        "viewer": viewer_path,
        "inventory": inventory_path,
        "stdout": output_paths.get("stdout_file"),
        "stderr": output_paths.get("stderr_file"),
    }
    for label, path in hash_paths.items():
        if path is None:
            continue
        try:
            metadata[label + "_sha256"] = sha256_file(path)
            metadata[label + "_path"] = str(path.relative_to(root))
            metadata[label + "_size_bytes"] = path.stat().st_size
        except OSError as exc:
            failures.append("cannot hash " + label + ": " + str(exc))

    metadata["acceptance_passed"] = not failures

    try:
        write_metadata(root / "run-metadata.json", metadata)
    except OSError as exc:
        failures.append("cannot write run-metadata.json: " + str(exc))
        metadata["acceptance_passed"] = False

    return metadata


def main():
    value = os.environ.get("EVIDENCE_ROOT")
    if not value or not value.strip():
        print("ERROR: EVIDENCE_ROOT is required.", file=sys.stderr)
        return 2

    try:
        metadata = validate_evidence(value, os.environ)
    except Exception as exc:
        print("ERROR: evidence validation failed: " + str(exc), file=sys.stderr)
        return 2

    print(json.dumps(metadata, indent=2, sort_keys=True))
    return 0 if metadata["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
