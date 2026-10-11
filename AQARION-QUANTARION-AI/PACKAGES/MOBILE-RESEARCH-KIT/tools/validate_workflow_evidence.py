"""Validate and bind Mobile Research Kit workflow evidence.

This validates the presence and internal consistency of captured process
evidence. It does not prove that the recorded command is mathematically
correct, authenticate the GitHub runner, or certify the repository.
"""

import hashlib
import json
import os
import sys
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def load_json(path, failures, description):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        failures.append(f"{description} is not readable valid JSON: {exc}")
        return None


def nonempty_file(path):
    try:
        return path.is_file() and path.stat().st_size > 0
    except OSError:
        return False


def collect_evidence(root):
    """Find the one expected workflow's receipt, viewer, and inventory."""
    receipts = sorted(root.glob("workflow-*/runs/run-*/receipt.json"))
    viewers = sorted(root.glob("workflow-*/viewer.html"))
    inventories = sorted(root.glob("workflow-*/inventory.json"))

    failures = []

    if len(receipts) != 1:
        failures.append(
            f"expected exactly one receipt; found {len(receipts)}"
        )

    if len(viewers) != 1:
        failures.append(
            f"expected exactly one viewer; found {len(viewers)}"
        )

    if len(inventories) != 1:
        failures.append(
            f"expected exactly one inventory; found {len(inventories)}"
        )

    receipt = receipts[0] if len(receipts) == 1 else None
    viewer = viewers[0] if len(viewers) == 1 else None
    inventory = inventories[0] if len(inventories) == 1 else None

    return receipt, viewer, inventory, failures


def validate_evidence(root, environment=None):
    """Validate files, write run-metadata.json, and return metadata.

    `environment` is injectable so acceptance behavior can be unit-tested
    outside GitHub Actions. In CI, pass os.environ.
    """
    root = Path(root).resolve()
    env = os.environ if environment is None else environment
    root.mkdir(parents=True, exist_ok=True)

    receipt, viewer, inventory, failures = collect_evidence(root)

    required_binding_fields = (
        "GITHUB_REPOSITORY",
        "GITHUB_SHA",
        "GITHUB_REF",
        "GITHUB_WORKFLOW",
        "GITHUB_EVENT_NAME",
        "GITHUB_RUN_ID",
        "GITHUB_RUN_ATTEMPT",
        "GITHUB_SERVER_URL",
    )

    for key in required_binding_fields:
        if not env.get(key):
            failures.append(f"missing GitHub run-binding field: {key}")

    receipt_record = None
    inventory_record = None

    if receipt is not None:
        receipt_record = load_json(
            receipt, failures, "execution receipt"
        )

        if isinstance(receipt_record, dict):
            if receipt_record.get("kind") != "command_execution":
                failures.append("receipt kind mismatch")

            if receipt_record.get("status") == "started":
                failures.append("receipt was not finalized")

            if not isinstance(receipt_record.get("recorder_exit"), int) \
                    or isinstance(receipt_record.get("recorder_exit"), bool):
                failures.append("receipt has no integer recorder_exit")

            if not receipt_record.get("ended_at_utc"):
                failures.append("receipt has no ended_at_utc")

            for key in ("stdout_file", "stderr_file"):
                filename = receipt_record.get(key)

                # Output names must be simple filenames inside the receipt
                # directory, not absolute paths or paths containing "..".
                if (
                    not isinstance(filename, str)
                    or not filename
                    or Path(filename).name != filename
                    or filename in {".", ".."}
                ):
                    failures.append(
                        f"invalid recorded output filename: {key}"
                    )
                    continue

                output_path = receipt.parent / filename

                if not nonempty_file(output_path):
                    failures.append(
                        f"missing or empty recorded output file: {key}"
                    )

    if viewer is not None and not nonempty_file(viewer):
        failures.append("viewer.html is missing or empty")

    if inventory is not None:
        if not nonempty_file(inventory):
            failures.append("inventory.json is missing or empty")
        else:
            inventory_record = load_json(
                inventory, failures, "environment inventory"
            )

            if not isinstance(inventory_record, dict):
                failures.append("inventory JSON root must be an object")

    run_url = None
    if env.get("GITHUB_SERVER_URL") and env.get("GITHUB_REPOSITORY") \
            and env.get("GITHUB_RUN_ID"):
        run_url = (
            f'{env["GITHUB_SERVER_URL"].rstrip("/")}/'
            f'{env["GITHUB_REPOSITORY"]}/actions/runs/'
            f'{env["GITHUB_RUN_ID']}'
        )

    def relative_path(path):
        return str(path.relative_to(root)) if path is not None else None

    metadata = {
        "schema_version": "1.0.0",
        "repository": env.get("GITHUB_REPOSITORY"),
        "commit_sha": env.get("GITHUB_SHA"),
        "ref": env.get("GITHUB_REF"),
        "workflow": env.get("GITHUB_WORKFLOW"),
        "event": env.get("GITHUB_EVENT_NAME"),
        "run_id": env.get("GITHUB_RUN_ID"),
        "run_attempt": env.get("GITHUB_RUN_ATTEMPT"),
        "run_url": run_url,
        "receipt_path": relative_path(receipt),
        "receipt_sha256": (
            sha256_file(receipt) if receipt is not None else None
        ),
        "viewer_path": relative_path(viewer),
        "viewer_sha256": (
            sha256_file(viewer) if viewer is not None else None
        ),
        "inventory_path": relative_path(inventory),
        "inventory_sha256": (
            sha256_file(inventory) if inventory is not None else None
        ),
        "receipt_status": (
            receipt_record.get("status")
            if isinstance(receipt_record, dict)
            else None
        ),
        "recorder_exit": (
            receipt_record.get("recorder_exit")
            if isinstance(receipt_record, dict)
            else None
        ),
        "acceptance_failures": failures,
        "acceptance_passed": not failures,
        "interpretation": (
            "Process-evidence integrity only; not mathematical proof "
            "or independent certification."
        ),
    }

    metadata_path = root / "run-metadata.json"
    temporary_path = root / "run-metadata.json.tmp"

    temporary_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary_path.replace(metadata_path)

    return metadata


def main():
    root_value = os.environ.get("EVIDENCE_ROOT")

    if not root_value:
        print("ACCEPTANCE_ERROR: EVIDENCE_ROOT is unset", file=sys.stderr)
        return 2

    try:
        metadata = validate_evidence(Path(root_value), os.environ)
    except OSError as exc:
        print(f"ACCEPTANCE_ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(metadata, indent=2, sort_keys=True))

    if metadata["acceptance_failures"]:
        print("EVIDENCE_ACCEPTANCE=FAIL")
        return 1

    print("EVIDENCE_ACCEPTANCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
