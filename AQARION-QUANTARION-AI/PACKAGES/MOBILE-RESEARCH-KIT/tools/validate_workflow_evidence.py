#!/usr/bin/env python3
"""Validate and bind Mobile Research Kit GitHub Actions evidence.

This validator checks that a workflow execution produced a complete,
internally consistent evidence bundle. It writes run_metadata.json only
after validation has completed.

Expected evidence layout beneath EVIDENCE_ROOT:

    workflow-*/
        viewer.html
        inventory.json
        runs/
            run-*/
                receipt.json
                stdout.txt
                stderr.txt

The receipt must describe a finalized command execution and bind its
stdout/stderr filenames. Empty stdout or stderr files are valid.

Required GitHub Actions environment variables:

    GITHUB_REPOSITORY
    GITHUB_SHA
    GITHUB_REF
    GITHUB_WORKFLOW
    GITHUB_EVENT_NAME
    GITHUB_RUN_ID
    GITHUB_RUN_ATTEMPT
    GITHUB_SERVER_URL

Exit codes:
    0  Evidence validated and metadata written.
    1  Evidence validation failed.
    2  Configuration, filesystem, or unexpected execution error.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


METADATA_FILENAME = "run_metadata.json"
RECEIPT_FILENAME = "receipt.json"
VIEWER_FILENAME = "viewer.html"
INVENTORY_FILENAME = "inventory.json"

REQUIRED_GITHUB_ENV = (
    "GITHUB_REPOSITORY",
    "GITHUB_SHA",
    "GITHUB_REF",
    "GITHUB_WORKFLOW",
    "GITHUB_EVENT_NAME",
    "GITHUB_RUN_ID",
    "GITHUB_RUN_ATTEMPT",
    "GITHUB_SERVER_URL",
)

# These are terminal states accepted by this validator. If the recorder
# uses a different documented terminal status, update this set to match
# the recorder's actual schema before deployment.
FINAL_RECEIPT_STATUSES = frozenset(
    {
        "completed",
        "success",
        "succeeded",
        "failed",
        "error",
        "timeout",
        "timed_out",
        "cancelled",
        "canceled",
    }
)


class EvidenceValidationError(Exception):
    """Raised when the evidence bundle fails an acceptance check."""


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file without loading it all at once."""
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_json(path: Path) -> Any:
    """Load a UTF-8 JSON file, reporting a useful validation error."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(
            f"Cannot read valid JSON from {path}: {exc}"
        ) from exc


def require_nonempty_string(
    value: Any,
    field_name: str,
) -> str:
    """Require a nonempty string and return its stripped value."""
    if not isinstance(value, str) or not value.strip():
        raise EvidenceValidationError(
            f"Required field must be a nonempty string: {field_name}"
        )

    return value.strip()


def require_github_environment() -> dict[str, str]:
    """Read and validate the required GitHub Actions environment bindings."""
    bindings: dict[str, str] = {}
    missing: list[str] = []

    for name in REQUIRED_GITHUB_ENV:
        value = os.environ.get(name)

        if value is None or not value.strip():
            missing.append(name)
        else:
            bindings[name] = value.strip()

    if missing:
        raise EvidenceValidationError(
            "Missing required GitHub Actions environment variables: "
            + ", ".join(missing)
        )

    return bindings


def safe_evidence_filename(value: Any, field_name: str) -> str:
    """Accept a simple filename, rejecting paths and traversal."""
    filename = require_nonempty_string(value, field_name)

    if filename in {".", ".."}:
        raise EvidenceValidationError(
            f"Unsafe evidence filename in {field_name}: {filename!r}"
        )

    if Path(filename).name != filename:
        raise EvidenceValidationError(
            f"{field_name} must be a filename, not a path: {filename!r}"
        )

    if "/" in filename or "\\" in filename:
        raise EvidenceValidationError(
            f"Path separators are forbidden in {field_name}: {filename!r}"
        )

    return filename


def collect_evidence(
    evidence_root: Path,
) -> tuple[Path, Path, Path, Path, Path, Path, dict[str, Any]]:
    """Locate one evidence bundle and validate its core files.

    Returns:
        workflow_dir, run_dir, receipt_path, viewer_path, inventory_path,
        stdout_path, receipt

    The stderr path is checked separately from the receipt-bound filename.
    """
    if not evidence_root.exists():
        raise EvidenceValidationError(
            f"Evidence root does not exist: {evidence_root}"
        )

    if not evidence_root.is_dir():
        raise EvidenceValidationError(
            f"Evidence root is not a directory: {evidence_root}"
        )

    workflow_dirs = sorted(
        path
        for path in evidence_root.glob("workflow-*")
        if path.is_dir()
    )

    if len(workflow_dirs) != 1:
        raise EvidenceValidationError(
            "Expected exactly one workflow-* directory; found "
            f"{len(workflow_dirs)} beneath {evidence_root}"
        )

    workflow_dir = workflow_dirs[0]

    viewer_path = workflow_dir / VIEWER_FILENAME
    inventory_path = workflow_dir / INVENTORY_FILENAME

    if not viewer_path.is_file():
        raise EvidenceValidationError(
            f"Required viewer file is missing: {viewer_path}"
        )

    if viewer_path.stat().st_size == 0:
        raise EvidenceValidationError(
            f"Viewer file is empty: {viewer_path}"
        )

    if not inventory_path.is_file():
        raise EvidenceValidationError(
            f"Required inventory file is missing: {inventory_path}"
        )

    inventory = load_json(inventory_path)

    if not isinstance(inventory, dict) or not inventory:
        raise EvidenceValidationError(
            "Inventory must be a nonempty JSON object."
        )

    runs_dir = workflow_dir / "runs"

    if not runs_dir.is_dir():
        raise EvidenceValidationError(
            f"Required runs directory is missing: {runs_dir}"
        )

    run_dirs = sorted(
        path
        for path in runs_dir.glob("run-*")
        if path.is_dir()
    )

    if len(run_dirs) != 1:
        raise EvidenceValidationError(
            "Expected exactly one run-* directory; found "
            f"{len(run_dirs)} beneath {runs_dir}"
        )

    run_dir = run_dirs[0]
    receipt_path = run_dir / RECEIPT_FILENAME

    if not receipt_path.is_file():
        raise EvidenceValidationError(
            f"Required execution receipt is missing: {receipt_path}"
        )

    receipt = load_json(receipt_path)

    if not isinstance(receipt, dict):
        raise EvidenceValidationError(
            "Execution receipt must be a JSON object."
        )

    return (
        workflow_dir,
        run_dir,
        receipt_path,
        viewer_path,
        inventory_path,
        receipt,
    )


def validate_receipt_and_outputs(
    run_dir: Path,
    receipt: dict[str, Any],
) -> tuple[Path, Path]:
    """Validate receipt semantics and the files bound by that receipt."""
    receipt_kind = require_nonempty_string(
        receipt.get("kind"),
        "receipt.kind",
    )

    if receipt_kind != "command_execution":
        raise EvidenceValidationError(
            "receipt.kind must equal 'command_execution'; "
            f"received {receipt_kind!r}"
        )

    status = require_nonempty_string(
        receipt.get("status"),
        "receipt.status",
    ).lower()

    if status == "started":
        raise EvidenceValidationError(
            "Execution receipt is not finalized: status='started'."
        )

    if status not in FINAL_RECEIPT_STATUSES:
        raise EvidenceValidationError(
            "Unrecognized or nonterminal receipt.status: "
            f"{status!r}. Accepted terminal statuses: "
            f"{', '.join(sorted(FINAL_RECEIPT_STATUSES))}"
        )

    recorder_exit = receipt.get("recorder_exit")

    if (
        isinstance(recorder_exit, bool)
        or not isinstance(recorder_exit, int)
    ):
        raise EvidenceValidationError(
            "receipt.recorder_exit must be an integer, not a boolean."
        )

    require_nonempty_string(
        receipt.get("ended_at_utc"),
        "receipt.ended_at_utc",
    )

    stdout_name = safe_evidence_filename(
        receipt.get("stdout_file"),
        "receipt.stdout_file",
    )

    stderr_name = safe_evidence_filename(
        receipt.get("stderr_file"),
        "receipt.stderr_file",
    )

    stdout_path = run_dir / stdout_name
    stderr_path = run_dir / stderr_name

    if not stdout_path.is_file():
        raise EvidenceValidationError(
            f"Receipt-bound stdout file is missing: {stdout_path}"
        )

    if not stderr_path.is_file():
        raise EvidenceValidationError(
            f"Receipt-bound stderr file is missing: {stderr_path}"
        )

    # Empty stdout and stderr are permitted. Existence and hashes establish
    # the files' presence; their contents need not be nonempty.
    return stdout_path, stderr_path


def validate_and_build_metadata(
    evidence_root: Path,
) -> tuple[dict[str, Any], list[str]]:
    """Validate all evidence and build metadata without writing it."""
    failures: list[str] = []

    try:
        bindings = require_github_environment()

        (
            workflow_dir,
            run_dir,
            receipt_path,
            viewer_path,
            inventory_path,
            receipt,
        ) = collect_evidence(evidence_root)

        stdout_path, stderr_path = validate_receipt_and_outputs(
            run_dir,
            receipt,
        )

        run_id = bindings["GITHUB_RUN_ID"]
        run_attempt = bindings["GITHUB_RUN_ATTEMPT"]

        metadata: dict[str, Any] = {
            "schema_version": 1,
            "evidence_type": "mobile_research_kit_workflow",
            "validated_at_utc": datetime.now(timezone.utc).isoformat(),
            "repository": bindings["GITHUB_REPOSITORY"],
            "commit_sha": bindings["GITHUB_SHA"],
            "ref": bindings["GITHUB_REF"],
            "workflow": bindings["GITHUB_WORKFLOW"],
            "event_name": bindings["GITHUB_EVENT_NAME"],
            "run_id": run_id,
            "run_attempt": run_attempt,
            "run_url": (
                f"{bindings['GITHUB_SERVER_URL'].rstrip('/')}/"
                f"{bindings['GITHUB_REPOSITORY']}/actions/runs/{run_id}"
                f"/attempts/{run_attempt}"
            ),
            "evidence_root": str(evidence_root.resolve()),
            "workflow_directory": str(workflow_dir.resolve()),
            "run_directory": str(run_dir.resolve()),
            "receipt": {
                "path": str(receipt_path.resolve()),
                "sha256": sha256_file(receipt_path),
                "kind": receipt["kind"],
                "status": receipt["status"],
                "recorder_exit": receipt["recorder_exit"],
                "ended_at_utc": receipt["ended_at_utc"],
            },
            "viewer": {
                "path": str(viewer_path.resolve()),
                "sha256": sha256_file(viewer_path),
                "size_bytes": viewer_path.stat().st_size,
            },
            "inventory": {
                "path": str(inventory_path.resolve()),
                "sha256": sha256_file(inventory_path),
                "size_bytes": inventory_path.stat().st_size,
            },
            "stdout": {
                "path": str(stdout_path.resolve()),
                "sha256": sha256_file(stdout_path),
                "size_bytes": stdout_path.stat().st_size,
            },
            "stderr": {
                "path": str(stderr_path.resolve()),
                "sha256": sha256_file(stderr_path),
                "size_bytes": stderr_path.stat().st_size,
            },
            "acceptance": {
                "passed": True,
                "failures": [],
            },
            "interpretation": {
                "evidence_bundle_valid": True,
                "child_command_succeeded": (
                    receipt["recorder_exit"] == 0
                ),
                "theorem_proved": False,
                "formal_kernel_accepted": False,
                "independently_certified": False,
            },
        }

        return metadata, failures

    except EvidenceValidationError as exc:
        failures.append(str(exc))
    except OSError as exc:
        failures.append(f"Filesystem error: {exc}")
    except (KeyError, TypeError, ValueError) as exc:
        failures.append(f"Malformed evidence metadata: {exc}")

    return {}, failures


def write_json_atomically(destination: Path, payload: dict[str, Any]) -> None:
    """Write JSON via a temporary file followed by an atomic replacement."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=destination.parent,
            prefix=f".{destination.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary_path = Path(handle.name)
            json.dump(
                payload,
                handle,
                indent=2,
                sort_keys=True,
                ensure_ascii=False,
            )
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary_path, destination)
        temporary_path = None

    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def main() -> int:
    """Run validation and emit a machine-readable acceptance result."""
    evidence_root_value = os.environ.get("EVIDENCE_ROOT")

    if not evidence_root_value or not evidence_root_value.strip():
        print(
            "ERROR: EVIDENCE_ROOT environment variable is required.",
            file=sys.stderr,
        )
        return 2

    evidence_root = Path(evidence_root_value).expanduser()
    metadata_path = evidence_root / METADATA_FILENAME

    metadata, failures = validate_and_build_metadata(evidence_root)

    if failures:
        result = {
            "acceptance": {
                "passed": False,
                "failures": failures,
            }
        }

        print(json.dumps(result, indent=2, sort_keys=True), file=sys.stderr)
        return 1

    metadata["acceptance"] = {
        "passed": True,
        "failures": [],
    }

    try:
        write_json_atomically(metadata_path, metadata)
    except OSError as exc:
        print(
            json.dumps(
                {
                    "acceptance": {
                        "passed": False,
                        "failures": [
                            f"Could not write {metadata_path}: {exc}"
                        ],
                    }
                },
                indent=2,
                sort_keys=True,
            ),
            file=sys.stderr,
        )
        return 2

    print(
        json.dumps(
            {
                "acceptance": {
                    "passed": True,
                    "failures": [],
                },
                "metadata_path": str(metadata_path.resolve()),
                "child_command_succeeded": metadata["interpretation"][
                    "child_command_succeeded"
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )

    # Evidence validity and command success are distinct. A failed child
    # command can still have a valid, complete evidence bundle; the workflow
    # must separately preserve and report the child command's exit status.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
