#!/usr/bin/env python3
"""Fail-closed structural verifier for JOIN-STABILITY."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

CLAIM_FIELDS = {
    "claim_id", "version", "statement", "mathematical_status",
    "evidence_class", "domain", "dependencies", "proof_artifact",
}
EVIDENCE_FIELDS = {
    "evidence_id", "claim_id", "class", "type", "artifact",
    "status", "description",
}
ALLOWED_CLASSES = {"[D]", "[P]", "[V]", "[PV]", "[C]", "[R]", "[CE]"}
ALLOWED_STATUSES = {
    "DEFINITION",
    "PROVED_MATHEMATICALLY",
    "PROVED_MATHEMATICALLY_LEAN_OPEN",
    "REFUTED",
    "IMPLEMENTATION_SCOPE_ONLY",
    "COMPUTATIONAL_TARGET_NOT_YET_REPRODUCED_IN_PACKAGE",
}


class VerificationError(Exception):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise VerificationError(f"missing file: {path.relative_to(ROOT)}") from exc
    except json.JSONDecodeError as exc:
        raise VerificationError(
            f"invalid JSON in {path.relative_to(ROOT)}: {exc}"
        ) from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise VerificationError(f"missing file: {path.relative_to(ROOT)}") from exc

    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise VerificationError(
                f"{path.name}:{line_no}: invalid JSON: {exc}"
            ) from exc
        require(
            isinstance(value, dict),
            f"{path.name}:{line_no}: each JSONL record must be an object",
        )
        records.append(value)
    return records



# Explicit JSON-type boundaries. These do not alter promotion gates.

def _jt_object(value, location):
    require(
        isinstance(value, dict),
        f"TYPE_ERROR: {location}: object required",
    )

def _jt_text(value, location):
    require(
        isinstance(value, str) and bool(value) and "\0" not in value,
        f"TYPE_ERROR: {location}: nonempty NUL-free string required",
    )

def _jt_records(records, kind):
    require(
        isinstance(records, list),
        f"TYPE_ERROR: {kind}_records: array required",
    )
    for index, record in enumerate(records, 1):
        location = f"{kind}[{index}]"
        _jt_object(record, location)

        fields = (
            ("evidence_class", "mathematical_status")
            if kind == "claim"
            else ("claim_id", "class", "artifact")
        )

        for field in fields:
            if field in record:
                _jt_text(record[field], f"{location}.{field}")

        if kind == "claim" and "proof_artifact" in record:
            artifact = record["proof_artifact"]
            if artifact is not None:
                _jt_text(artifact, f"{location}.proof_artifact")

def _jt_manifest(manifest):
    _jt_object(manifest, "manifest")

    for field in ("verification_policy", "audit", "promotion"):
        if field in manifest:
            _jt_object(manifest[field], f"manifest.{field}")

    for field in (
        "status", "source_revision", "claim_registry",
        "evidence_registry",
    ):
        if field in manifest:
            _jt_text(manifest[field], f"manifest.{field}")

    for field in ("required_artifacts", "required_directories"):
        if field not in manifest:
            continue

        require(
            isinstance(manifest[field], list),
            f"TYPE_ERROR: manifest.{field}: array required",
        )

        for index, value in enumerate(manifest[field]):
            _jt_text(value, f"manifest.{field}[{index}]")

    policy = manifest.get("verification_policy", {})

    for field in (
        "fail_closed", "allow_automatic_manifest_generation",
        "reject_unknown_record_fields", "require_source_revision_match",
        "require_independent_audit", "require_negative_controls",
    ):
        if field in policy:
            require(
                type(policy[field]) is bool,
                f"TYPE_ERROR: manifest.verification_policy.{field}: boolean required",
            )

    for field in ("lean_status", "mathematical_verification_status"):
        if field in policy:
            _jt_text(
                policy[field],
                f"manifest.verification_policy.{field}",
            )

def _jt_audit(manifest):
    _jt_object(manifest, "manifest")

    if "audit" not in manifest:
        return

    audit = manifest["audit"]
    _jt_object(audit, "manifest.audit")

    if "expected" not in audit:
        return

    expected = audit["expected"]
    _jt_object(expected, "manifest.audit.expected")

    for key, pair in expected.items():
        require(
            isinstance(pair, list)
            and len(pair) == 2
            and all(type(value) is int for value in pair),
            f"TYPE_ERROR: manifest.audit.expected.{key}: integer pair required",
        )


def validate_claims(
    records: list[dict[str, Any]],
    reject_unknown: bool = True,
) -> set[str]:
    _jt_records(records, 'claim')
    seen: set[str] = set()

    for index, record in enumerate(records, start=1):
        require(
            CLAIM_FIELDS.issubset(record),
            f"claim record {index} is missing required fields",
        )
        if reject_unknown:
            require(
                set(record).issubset(CLAIM_FIELDS),
                f"claim record {index} has unknown fields",
            )

        claim_id = record["claim_id"]
        require(
            isinstance(claim_id, str) and claim_id.strip(),
            f"claim record {index} has invalid claim_id",
        )
        require(claim_id not in seen, f"duplicate claim_id: {claim_id}")
        seen.add(claim_id)

        require(
            record["evidence_class"] in ALLOWED_CLASSES,
            f"{claim_id}: invalid evidence_class",
        )
        require(
            record["mathematical_status"] in ALLOWED_STATUSES,
            f"{claim_id}: invalid mathematical_status",
        )
        require(
            isinstance(record["dependencies"], list)
            and all(isinstance(x, str) for x in record["dependencies"]),
            f"{claim_id}: dependencies must be a list of strings",
        )

    for record in records:
        claim_id = record["claim_id"]
        for dependency in record["dependencies"]:
            require(
                dependency in seen,
                f"{claim_id}: unresolved dependency {dependency}",
            )
            require(
                dependency != claim_id,
                f"{claim_id}: self-dependency is not allowed",
            )

    return seen


def validate_evidence(
    records: list[dict[str, Any]],
    claim_ids: set[str],
    reject_unknown: bool = True,
) -> set[str]:
    _jt_records(records, 'evidence')
    seen: set[str] = set()

    for index, record in enumerate(records, start=1):
        require(
            EVIDENCE_FIELDS.issubset(record),
            f"evidence record {index} is missing required fields",
        )
        if reject_unknown:
            require(
                set(record).issubset(EVIDENCE_FIELDS),
                f"evidence record {index} has unknown fields",
            )

        evidence_id = record["evidence_id"]
        require(
            isinstance(evidence_id, str) and evidence_id.strip(),
            f"evidence record {index} has invalid evidence_id",
        )
        require(
            evidence_id not in seen,
            f"duplicate evidence_id: {evidence_id}",
        )
        seen.add(evidence_id)

        require(
            record["claim_id"] in claim_ids,
            f"{evidence_id}: unresolved claim {record['claim_id']}",
        )
        require(
            record["class"] in ALLOWED_CLASSES,
            f"{evidence_id}: invalid evidence class",
        )
        require(
            isinstance(record["artifact"], str) and record["artifact"],
            f"{evidence_id}: artifact must be a nonempty path",
        )

    return seen


def safe_package_path(relative: str) -> Path:
    _jt_text(relative, 'package_path')
    path = Path(relative)
    require(not path.is_absolute(), f"absolute package path rejected: {relative}")
    resolved = (ROOT / path).resolve()
    require(
        resolved == ROOT or ROOT in resolved.parents,
        f"path escapes package root: {relative}",
    )
    return resolved


def check_manifest_shape(manifest: dict[str, Any]) -> None:
    _jt_manifest(manifest)
    required = {
        "schema_version", "package_id", "package_version", "status",
        "source_revision", "claim_registry", "evidence_registry",
        "required_artifacts", "required_directories",
        "verification_policy", "audit", "promotion",
    }
    require(required.issubset(manifest), "manifest is missing required fields")
    require(manifest["package_id"] == "JOIN-STABILITY", "wrong package_id")
    require(
        manifest["status"] == "BLOCKED_PENDING_REPRODUCTION",
        "release status must remain blocked until promotion gates are reviewed",
    )
    require(
        isinstance(manifest["source_revision"], str)
        and SHA_RE.fullmatch(manifest["source_revision"]) is not None,
        "source_revision must be a full lowercase 40-character Git SHA",
    )
    require(
        isinstance(manifest["required_artifacts"], list),
        "required_artifacts must be a list",
    )
    require(
        isinstance(manifest["required_directories"], list),
        "required_directories must be a list",
    )
    require(
        manifest["verification_policy"].get("fail_closed") is True,
        "fail_closed must be true",
    )
    require(
        manifest["verification_policy"].get("lean_status") == "OPEN",
        "Lean status must remain OPEN until formally verified",
    )

    promotion = manifest["promotion"]
    require(isinstance(promotion, dict), "promotion must be an object")
    for key in (
        "reproduction_verified", "proof_reviewed",
        "lean_verified", "publication_approved",
    ):
        require(promotion.get(key) is False, f"promotion.{key} must remain false")


def check_revision(source_baseline: str) -> str:
    expected = os.environ.get("AQ_EXPECTED_TESTED_REVISION", "")
    require(
        SHA_RE.fullmatch(expected) is not None,
        "AQ_EXPECTED_TESTED_REVISION must be supplied externally as a full Git SHA",
    )

    try:
        actual = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except Exception as exc:
        raise VerificationError(
            "cannot determine tested revision; run from a Git checkout"
        ) from exc

    require(
        actual == expected,
        f"tested revision mismatch: expected {expected}, got {actual}",
    )

    try:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", source_baseline, actual],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except Exception as exc:
        raise VerificationError("cannot verify source-baseline ancestry") from exc

    require(
        result.returncode == 0,
        "source_revision is not an ancestor of the tested commit",
    )

    print(f"Source baseline: {source_baseline}")
    print(f"Tested revision: {actual}")
    return actual


def check_audit_contract(manifest: dict[str, Any]) -> None:
    _jt_audit(manifest)
    audit = manifest["audit"]
    require(
        audit.get("script") == "join_stability_independent_audit.py",
        "unexpected audit script",
    )
    expected = audit.get("expected")
    require(isinstance(expected, dict), "audit.expected must be an object")

    required = {
        "1": [1, 0],
        "2": [10, 0],
        "3": [117, 0],
        "4": [1960, 0],
        "5": [40385, 0],
        "6": [1016496, 0],
    }
    require(expected == required, "audit expected-count contract is incorrect")


def check_package() -> None:
    manifest_path = ROOT / "manifest.json"
    manifest = load_json(manifest_path)
    require(isinstance(manifest, dict), "manifest must be an object")
    check_manifest_shape(manifest)

    for relative in manifest["required_artifacts"]:
        path = safe_package_path(relative)
        require(path.is_file(), f"required artifact missing: {relative}")

    for relative in manifest["required_directories"]:
        path = safe_package_path(relative)
        require(path.is_dir(), f"required directory missing: {relative}")

    claims_path = safe_package_path(manifest["claim_registry"])
    evidence_path = safe_package_path(manifest["evidence_registry"])

    claims = load_jsonl(claims_path)
    evidence = load_jsonl(evidence_path)
    claim_ids = validate_claims(
        claims,
        reject_unknown=manifest["verification_policy"].get(
            "reject_unknown_record_fields", True
        ),
    )
    validate_evidence(
        evidence,
        claim_ids,
        reject_unknown=manifest["verification_policy"].get(
            "reject_unknown_record_fields", True
        ),
    )

    for record in claims:
        artifact = record.get("proof_artifact")
        if artifact:
            require(
                safe_package_path(artifact).is_file(),
                f"{record['claim_id']}: proof artifact missing: {artifact}",
            )

    for record in evidence:
        artifact = record["artifact"]
        require(
            safe_package_path(artifact).is_file(),
            f"{record['evidence_id']}: evidence artifact missing: {artifact}",
        )

    check_audit_contract(manifest)
    tested_revision = check_revision(manifest["source_revision"])

    print(f"Claims: {len(claims)}")
    print(f"Evidence records: {len(evidence)}")
    print(f"Tested revision: {tested_revision}")
    print("STRUCTURAL_RESULT=PASS")
    print("MATHEMATICAL_PROOF=NOT_ESTABLISHED_BY_THIS_VERIFIER")
    print("LEAN_STATUS=OPEN")


def run_negative_control_self_tests() -> None:
    """Run focused in-memory tests of registry and manifest validators."""
    base_claim = {
        "claim_id": "A",
        "version": "1.0.0",
        "statement": "test",
        "mathematical_status": "DEFINITION",
        "evidence_class": "[D]",
        "domain": "test",
        "dependencies": [],
        "proof_artifact": None,
    }
    base_evidence = {
        "evidence_id": "EV-A",
        "claim_id": "A",
        "class": "[R]",
        "type": "test",
        "artifact": "README.md",
        "status": "TEST",
        "description": "test",
    }

    tests: list[tuple[str, Any]] = []

    tests.append((
        "duplicate_claim_id",
        lambda: validate_claims(
            [dict(base_claim), dict(base_claim)]
        ),
    ))

    missing_dependency = dict(base_claim, claim_id="B", dependencies=["MISSING"])
    tests.append((
        "unresolved_dependency",
        lambda: validate_claims([dict(base_claim), missing_dependency]),
    ))

    missing_field = dict(base_claim)
    missing_field.pop("statement")
    tests.append((
        "missing_claim_field",
        lambda: validate_claims([missing_field]),
    ))

    unknown_field = dict(base_claim, unexpected=True)
    tests.append((
        "unknown_claim_field",
        lambda: validate_claims([unknown_field]),
    ))

    tests.append((
        "unresolved_evidence_claim",
        lambda: validate_evidence(
            [dict(base_evidence, claim_id="MISSING")], {"A"}
        ),
    ))

    tests.append((
        "duplicate_evidence_id",
        lambda: validate_evidence(
            [dict(base_evidence), dict(base_evidence)], {"A"}
        ),
    ))

    malformed_status = dict(base_claim, mathematical_status="PASS_EVERYTHING")
    tests.append((
        "invalid_claim_status",
        lambda: validate_claims([malformed_status]),
    ))

    malformed_class = dict(base_claim, evidence_class="[UNKNOWN]")
    tests.append((
        "invalid_evidence_class",
        lambda: validate_claims([malformed_class]),
    ))

    tests.append((
        "absolute_path",
        lambda: safe_package_path("/etc/passwd"),
    ))

    tests.append((
        "path_traversal",
        lambda: safe_package_path("../../outside"),
    ))

    require(
        validate_claims([dict(base_claim)]) == {"A"},
        "valid claim positive control failed",
    )
    require(
        validate_evidence([dict(base_evidence)], {"A"}) == {"EV-A"},
        "valid evidence positive control failed",
    )
    print("POSITIVE_CONTROLS=2/2")

    expected_errors = {
        "duplicate_claim_id": "duplicate claim_id: A",
        "unresolved_dependency": "B: unresolved dependency MISSING",
        "missing_claim_field": "claim record 1 is missing required fields",
        "unknown_claim_field": "claim record 1 has unknown fields",
        "unresolved_evidence_claim": "EV-A: unresolved claim MISSING",
        "duplicate_evidence_id": "duplicate evidence_id: EV-A",
        "invalid_claim_status": "A: invalid mathematical_status",
        "invalid_evidence_class": "A: invalid evidence_class",
        "absolute_path": "absolute package path rejected: /etc/passwd",
        "path_traversal": "path escapes package root: ../../outside",
    }
    require(
        len(tests) == len(expected_errors)
        and {name for name, _ in tests} == set(expected_errors),
        "negative-control expectation inventory differs",
    )

    passed = 0
    for name, action in tests:
        try:
            action()
        except VerificationError as exc:
            require(
                str(exc) == expected_errors[name],
                f"negative control wrong rejection reason: {name}: {exc}",
            )
            print(f"NEGATIVE_CONTROL={name}:REJECTED")
            passed += 1
        except Exception as exc:
            raise VerificationError(
                f"negative control raised unexpected exception: {name}"
            ) from exc
        else:
            print(f"NEGATIVE_CONTROL={name}:UNEXPECTED_ACCEPT")
            raise VerificationError(
                f"negative control failed to reject invalid input: {name}"
            )

    print(f"NEGATIVE_CONTROLS={passed}/{len(tests)}")
    print("NEGATIVE_CONTROL_SCOPE=IN_MEMORY_VALIDATOR_TESTS_ONLY")


def main() -> int:
    try:
        if "--self-test-negative-controls" in sys.argv[1:]:
            run_negative_control_self_tests()
        else:
            check_package()
        return 0
    except VerificationError as exc:
        print(f"VERIFY_ERROR={exc}", file=sys.stderr)
        print("STRUCTURAL_RESULT=FAIL", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
