#!/usr/bin/env python3
"""External replay controller for AQARION.

Fail-closed stages:
  acquire -> archive -> inventory -> manifest -> fixtures
  -> test coverage -> execution -> mutation -> receipt

Downloaded code is never executed unless both:
  1. the policy permits execution; and
  2. --allow-exec is supplied.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


PASS = "PASS"
FAIL = "FAIL"
NOT_RUN = "NOT_RUN"
INCOMPLETE = "INCOMPLETE"

SUPPORTED_MUTATION_MODES = ("byte-flip-hash-must-change",)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        + "\n"
    ).encode()


def safe_rel(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))

    if path.is_absolute():
        raise ValueError(f"absolute path rejected: {value}")

    if ".." in path.parts:
        raise ValueError(f"path traversal rejected: {value}")

    if not path.parts:
        raise ValueError(f"empty path rejected: {value}")

    return str(path)


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as stream:
        value = json.load(stream)

    if not isinstance(value, dict):
        raise ValueError("JSON root must be an object")

    return value


def load_policy(path: Path) -> dict[str, Any]:
    policy = load_json(path)

    required_files = policy.get("required_files")

    if not isinstance(required_files, list) or not required_files:
        raise ValueError("policy.required_files must be a non-empty list")

    for item in required_files:
        if not isinstance(item, dict) or "path" not in item:
            raise ValueError(
                "policy.required_files entries must be objects with a path"
            )
        safe_rel(item["path"])

    for key in (
        "repository",
        "commit",
        "package_path",
        "archive",
        "required_tests",
        "execution",
        "mutations",
        "limits",
    ):
        if key not in policy:
            raise ValueError(f"policy missing required key: {key}")

    if policy["unexpected_files"] not in ("report", "reject"):
        raise ValueError(
            "policy.unexpected_files must be 'report' or 'reject'"
        )

    mode = policy["mutations"].get("mode")
    if mode not in SUPPORTED_MUTATION_MODES:
        raise ValueError(f"policy.mutations.mode unsupported: {mode!r}")

    return policy


def download_archive(
    repository: str,
    commit: str,
    destination: Path,
    maximum_bytes: int,
    maximum_seconds: int,
) -> str:
    url = f"https://github.com/{repository}/archive/{commit}.zip"

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "AQARION-REPLAY"},
    )

    digest = hashlib.sha256()
    total = 0
    started = time.monotonic()

    with urllib.request.urlopen(request, timeout=60) as response:
        with destination.open("wb") as output:
            while True:
                if time.monotonic() - started > maximum_seconds:
                    raise ValueError("archive download exceeded time limit")

                block = response.read(1024 * 1024)

                if not block:
                    break

                total += len(block)

                if total > maximum_bytes:
                    raise ValueError("archive exceeds byte limit")

                digest.update(block)
                output.write(block)

    return digest.hexdigest()


def extract_archive(
    archive: Path,
    destination: Path,
    maximum_files: int,
    maximum_file_bytes: int,
    maximum_total_bytes: int,
) -> None:
    destination.mkdir(parents=True, exist_ok=True)

    state = {"files": 0, "bytes": 0}

    def reserve_slot() -> None:
        if state["files"] + 1 > maximum_files:
            raise ValueError("archive exceeds file-count limit")

    def install(name: str, source) -> None:
        relative = safe_rel(name)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)

        reserve_slot()

        written = 0

        with target.open("wb") as output:
            for block in iter(
                lambda: source.read(1024 * 1024),
                b"",
            ):
                written += len(block)
                state["bytes"] += len(block)

                if written > maximum_file_bytes:
                    raise ValueError(
                        f"file exceeds byte limit: {relative}"
                    )

                if state["bytes"] > maximum_total_bytes:
                    raise ValueError(
                        "extracted data exceeds byte limit"
                    )

                output.write(block)

        state["files"] += 1

    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as source:
            for member in source.infolist():
                if member.is_dir():
                    safe_rel(member.filename)
                    continue

                with source.open(member) as stream:
                    install(member.filename, stream)

        return

    if tarfile.is_tarfile(archive):
        with tarfile.open(archive, "r:*") as source:
            for member in source.getmembers():

                safe_rel(member.name)

                if member.isdir():
                    continue

                if (
                    member.issym()
                    or member.islnk()
                    or member.isdev()
                ):
                    raise ValueError(
                        f"unsafe archive member: {member.name}"
                    )

                if not member.isfile():
                    raise ValueError(
                        f"unsupported archive member: {member.name}"
                    )

                stream = source.extractfile(member)

                if stream is None:
                    raise ValueError(
                        f"cannot read archive member: {member.name}"
                    )

                install(member.name, stream)

        return

    raise ValueError("unsupported archive format")


def inventory(root: Path) -> list[dict[str, Any]]:
    result = []

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue

        relative = path.relative_to(root).as_posix()

        result.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    return result


def inventory_hash(rows: list[dict[str, Any]]) -> str:
    return sha256_bytes(canonical_json(rows))


def manifest_check(
    rows: list[dict[str, Any]],
    required: list[dict[str, Any]],
    unexpected_policy: str,
) -> tuple[str, list[str]]:

    actual = {row["path"]: row for row in rows}
    findings = []

    for item in required:
        path = safe_rel(item["path"])

        if path not in actual:
            findings.append(f"EXPECTED_FILE_ABSENT:{path}")
            continue

        expected_hash = item.get("sha256")

        if (
            expected_hash is not None
            and actual[path]["sha256"] != expected_hash
        ):
            findings.append(f"EXPECTED_FILE_HASH_WRONG:{path}")

    expected_paths = {
        safe_rel(item["path"])
        for item in required
    }

    extras = sorted(set(actual) - expected_paths)

    if unexpected_policy == "reject":
        findings.extend(
            f"UNEXPECTED_FILE_PRESENT:{path}"
            for path in extras
        )
    elif extras:
        findings.append(
            f"UNEXPECTED_FILES_REPORTED:{len(extras)}"
        )

    fatal = any(
        item.startswith(
            (
                "EXPECTED_FILE_ABSENT:",
                "EXPECTED_FILE_HASH_WRONG:",
                "UNEXPECTED_FILE_PRESENT:",
            )
        )
        for item in findings
    )

    return (FAIL if fatal else PASS), findings


def fixture_check(
    root: Path,
    fixtures: list[dict[str, Any]],
) -> tuple[str, list[str]]:

    findings = []

    for item in fixtures:
        path = safe_rel(item["path"])
        target = root / path

        if not target.is_file():
            findings.append(f"FIXTURE_ABSENT:{path}")
            continue

        expected_hash = item.get("sha256")

        if (
            expected_hash is not None
            and sha256_file(target) != expected_hash
        ):
            findings.append(f"FIXTURE_HASH_WRONG:{path}")

        if path.endswith(".json"):
            try:
                with target.open("r", encoding="utf-8") as stream:
                    json.load(stream)
            except Exception as exc:
                findings.append(
                    f"FIXTURE_JSON_INVALID:{path}:"
                    f"{type(exc).__name__}"
                )

    return (PASS if not findings else FAIL), findings


def discover_tests(
    root: Path,
    required_tests: list[str],
) -> tuple[str, list[str], str]:

    findings = []
    identifiers = []

    for relative in required_tests:
        relative = safe_rel(relative)
        path = root / relative

        if not path.is_file():
            findings.append(
                f"REQUIRED_TEST_ABSENT:{relative}"
            )
            continue

        try:
            tree = ast.parse(
                path.read_text(encoding="utf-8"),
                filename=relative,
            )
        except Exception as exc:
            findings.append(
                f"TEST_PARSE_FAIL:{relative}:"
                f"{type(exc).__name__}"
            )
            continue

        for node in ast.walk(tree):
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            ) and node.name.startswith("test"):
                identifiers.append(
                    f"{relative}::{node.name}"
                )

            if isinstance(node, ast.ClassDef):
                if node.name.startswith("Test"):
                    identifiers.append(
                        f"{relative}::{node.name}"
                    )
                    for child in node.body:
                        if isinstance(
                            child,
                            (ast.FunctionDef, ast.AsyncFunctionDef),
                        ) and child.name.startswith("test"):
                            identifiers.append(
                                f"{relative}::{node.name}::{child.name}"
                            )

    identifiers = sorted(set(identifiers))

    return (
        PASS if not findings else FAIL,
        findings + identifiers,
        sha256_bytes(canonical_json(identifiers)),
    )


def execute_tests(
    root: Path,
    command: list[str],
    timeout_seconds: int,
    authorized: bool,
) -> tuple[str, str, int | None]:

    if not authorized:
        return (
            INCOMPLETE,
            "EXECUTION_NOT_AUTHORIZED",
            None,
        )

    try:
        result = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return INCOMPLETE, "TIMEOUT", None
    except KeyboardInterrupt:
        return INCOMPLETE, "INTERRUPTED", None
    except OSError as exc:
        return (
            FAIL,
            f"EXECUTION_ERROR:{type(exc).__name__}",
            None,
        )

    if result.returncode == 0:
        return PASS, "EXIT_0", 0

    return (
        FAIL,
        f"EXIT_{result.returncode}",
        result.returncode,
    )


def mutation_check(
    root: Path,
    fixture: str,
    mode: str,
) -> tuple[str, str]:

    if mode not in SUPPORTED_MUTATION_MODES:
        return FAIL, f"MUTATION_MODE_UNSUPPORTED:{mode}"

    relative = safe_rel(fixture)
    original = root / relative

    if not original.is_file():
        return (
            FAIL,
            f"MUTATION_FIXTURE_ABSENT:{relative}",
        )

    with tempfile.TemporaryDirectory(
        prefix="aqarion-replay-mutation-"
    ) as temporary:

        copy_root = Path(temporary) / "package"
        shutil.copytree(root, copy_root)

        target = copy_root / relative
        data = bytearray(target.read_bytes())

        if data:
            data[0] ^= 1
        else:
            data.extend(b"0")

        target.write_bytes(bytes(data))

        before = sha256_file(original)
        after = sha256_file(target)

        if before == after:
            return FAIL, "MUTATION_HASH_UNCHANGED"

    return PASS, "BYTE_FLIP_CHANGED_SHA256"


def overall_status(
    stages: dict[str, dict[str, Any]],
) -> str:

    required = [
        "archive",
        "inventory",
        "manifest",
        "fixtures",
        "tests",
        "mutations",
    ]

    if all(
        stages[name]["status"] == PASS
        for name in required
    ):
        return PASS

    if any(
        stages[name]["status"] == FAIL
        for name in required
    ):
        return FAIL

    return INCOMPLETE


def stage(
    status: str,
    reason: str,
    **extra: Any,
) -> dict[str, Any]:

    return {
        "status": status,
        "reason": reason,
        **extra,
    }


def write_receipt(path: Path, receipt: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def fail_receipt(
    policy: dict[str, Any],
    policy_hash: str,
    archive_hash: str,
    archive_status: str,
    archive_reason: str,
    inventory_status: str,
    inventory_reason: str,
) -> dict[str, Any]:
    return {
        "schema_version": "AQ-REPLAY-001/1",
        "target": {
            "repository": policy["repository"],
            "commit": policy["commit"],
            "package_path": policy["package_path"],
        },
        "policy": {
            "policy_id": policy.get("policy_id", ""),
            "sha256": policy_hash,
        },
        "source": {
            "archive_sha256": archive_hash,
            "inventory_sha256": "0" * 64,
            "inventory_count": 0,
        },
        "stages": {
            "archive": stage(archive_status, archive_reason),
            "inventory": stage(inventory_status, inventory_reason),
            "manifest": stage(NOT_RUN, "UPSTREAM_FAILURE"),
            "fixtures": stage(NOT_RUN, "UPSTREAM_FAILURE"),
            "tests": stage(NOT_RUN, "UPSTREAM_FAILURE"),
            "mutations": stage(NOT_RUN, "UPSTREAM_FAILURE"),
        },
        "overall_status": FAIL,
        "promotion": {"allowed": False},
    }


def main(argv: list[str] | None = None) -> int:

    parser = argparse.ArgumentParser(
        description="AQARION external replay controller"
    )

    parser.add_argument(
        "--policy",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--policy-sha256",
    )

    parser.add_argument(
        "--allow-exec",
        action="store_true",
    )

    parser.add_argument(
        "--archive",
        type=Path,
    )

    args = parser.parse_args(argv)

    started = time.time()

    try:
        policy = load_policy(args.policy)
    except Exception as exc:
        raise SystemExit(f"POLICY_LOAD_FAIL:{type(exc).__name__}:{exc}")

    policy_hash = sha256_file(args.policy)

    if (
        args.policy_sha256
        and args.policy_sha256.lower() != policy_hash
    ):
        raise SystemExit("POLICY_HASH_MISMATCH")

    repository = policy["repository"]
    commit = policy["commit"]
    package_path = safe_rel(policy["package_path"])

    archive_policy = policy["archive"]

    with tempfile.TemporaryDirectory(
        prefix="aqarion-replay-"
    ) as temporary:

        workspace = Path(temporary)
        archive = workspace / "source.zip"
        extracted = workspace / "extract"

        try:
            if args.archive:
                shutil.copyfile(args.archive, archive)

                if (
                    archive.stat().st_size
                    > archive_policy["max_bytes"]
                ):
                    raise ValueError(
                        "provided archive exceeds byte limit"
                    )

                archive_hash = sha256_file(archive)

            else:
                archive_hash = download_archive(
                    repository,
                    commit,
                    archive,
                    archive_policy["max_bytes"],
                    int(archive_policy.get("max_seconds", 600)),
                )

        except Exception as exc:

            receipt = fail_receipt(
                policy,
                policy_hash,
                "0" * 64,
                FAIL,
                f"ACQUIRE_FAIL:{type(exc).__name__}",
                NOT_RUN,
                "UPSTREAM_FAILURE",
            )

            write_receipt(args.output, receipt)
            return 1

        try:
            extract_archive(
                archive,
                extracted,
                archive_policy["max_files"],
                archive_policy["max_file_bytes"],
                policy["limits"]["extracted_bytes"],
            )

            roots = list(extracted.iterdir())

            if len(roots) == 1 and roots[0].is_dir():
                source_root = roots[0]
            else:
                source_root = extracted

            package_root = source_root / package_path

            if not package_root.is_dir():
                raise ValueError("PACKAGE_PATH_ABSENT")

        except Exception as exc:

            receipt = fail_receipt(
                policy,
                policy_hash,
                archive_hash,
                PASS,
                "ARCHIVE_HASHED",
                FAIL,
                f"ARCHIVE_REJECT:{type(exc).__name__}",
            )

            write_receipt(args.output, receipt)
            return 1

        rows = inventory(package_root)
        inventory_digest = inventory_hash(rows)

        manifest_status, manifest_findings = (
            manifest_check(
                rows,
                policy["required_files"],
                policy["unexpected_files"],
            )
        )

        fixture_paths = {
            safe_rel(item["path"])
            for item in policy["required_files"]
            if str(item["path"]).startswith("tests/fixtures/")
        }

        fixture_files = [
            item
            for item in policy["required_files"]
            if safe_rel(item["path"]) in fixture_paths
        ]

        fixture_status, fixture_findings = (
            fixture_check(
                package_root,
                fixture_files,
            )
        )

        coverage_status, coverage_data, test_ids_digest = (
            discover_tests(
                package_root,
                policy["required_tests"],
            )
        )

        authorized = (
            bool(policy["execution"]["allow_exec"])
            and args.allow_exec
        )

        test_status, test_reason, return_code = (
            execute_tests(
                package_root,
                policy["execution"]["command"],
                int(
                    policy["execution"][
                        "timeout_seconds"
                    ]
                ),
                authorized,
            )
        )

        if coverage_status != PASS:
            test_status = FAIL
            test_reason = "TEST_COVERAGE_FAIL"

        mutation_status, mutation_reason = (
            mutation_check(
                package_root,
                policy["mutations"]["fixture"],
                policy["mutations"]["mode"],
            )
        )

        test_ids = [
            value
            for value in coverage_data
            if "::" in value
        ]

        stages = {
            "archive": stage(
                PASS,
                "ARCHIVE_HASHED",
            ),
            "inventory": stage(
                PASS,
                "COMPLETE_INVENTORY",
            ),
            "manifest": stage(
                manifest_status,
                (
                    ";".join(manifest_findings)
                    if manifest_findings
                    else "REQUIRED_FILES_ACCEPTED"
                ),
            ),
            "fixtures": stage(
                fixture_status,
                (
                    ";".join(fixture_findings)
                    if fixture_findings
                    else "FIXTURES_ACCEPTED"
                ),
            ),
            "tests": stage(
                test_status,
                test_reason,
                discovered=len(test_ids),
                executed=(
                    len(test_ids)
                    if authorized
                    and test_status in (PASS, FAIL)
                    else 0
                ),
                failed=(
                    1
                    if test_status == FAIL
                    else 0
                ),
                skipped=0,
                ids_sha256=test_ids_digest,
                returncode=return_code,
                static_ids=test_ids,
            ),
            "mutations": stage(
                mutation_status,
                mutation_reason,
            ),
        }

        result = overall_status(stages)

        receipt = {
            "schema_version": "AQ-REPLAY-001/1",
            "target": {
                "repository": repository,
                "commit": commit,
                "package_path": package_path,
            },
            "policy": {
                "policy_id": policy.get(
                    "policy_id",
                    "",
                ),
                "sha256": policy_hash,
            },
            "source": {
                "archive_sha256": archive_hash,
                "inventory_sha256": inventory_digest,
                "inventory_count": len(rows),
            },
            "stages": stages,
            "overall_status": result,
            "promotion": {
                "allowed": False,
            },
            "elapsed_seconds": round(
                time.time() - started,
                3,
            ),
            "inventory": rows,
            "manifest_findings": manifest_findings,
            "fixture_findings": fixture_findings,
        }

        payload = (
            json.dumps(
                receipt,
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        if (
            len(payload.encode())
            > policy["limits"]["receipt_bytes"]
        ):
            raise SystemExit("RECEIPT_TOO_LARGE")

        write_receipt(args.output, receipt)

        if result == PASS:
            return 0

        if result == FAIL:
            return 1

        return 2


if __name__ == "__main__":
    raise SystemExit(main())
