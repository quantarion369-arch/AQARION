#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REQUIRED_FILES = (
    "README.md",
    "manifest.json",
    "zip-clone.md",
    "claims.jsonl",
    "evidence.jsonl",
    "reproduce.sh",
)

REQUIRED_DIRS = (
    "fixtures",
    "negative-controls",
    "receipts",
    "docs",
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        fail(f"cannot parse {path.name}: {exc}")


def load_jsonl(path: Path):
    records = []

    try:
        with path.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()

                if not line:
                    continue

                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    fail(
                        f"{path.name}:{line_number}: invalid JSON: {exc}"
                    )

    except OSError as exc:
        fail(f"cannot read {path.name}: {exc}")

    return records


def main() -> int:
    print("AQARION JOIN-STABILITY verifier")
    print("--------------------------------")

    for filename in REQUIRED_FILES:
        path = ROOT / filename

        if not path.is_file():
            fail(f"required file missing: {filename}")

    for dirname in REQUIRED_DIRS:
        path = ROOT / dirname

        if not path.is_dir():
            fail(f"required directory missing: {dirname}")

    manifest = load_json(ROOT / "manifest.json")
    claims = load_jsonl(ROOT / "claims.jsonl")
    evidence = load_jsonl(ROOT / "evidence.jsonl")

    if not isinstance(manifest, dict):
        fail("manifest.json must contain an object")

    if not claims:
        fail("claims.jsonl contains no claims")

    if not evidence:
        fail("evidence.jsonl contains no evidence records")

    claim_ids = set()

    for record in claims:
        claim_id = record.get("claim_id")

        if not isinstance(claim_id, str) or not claim_id:
            fail("claim without valid claim_id")

        if claim_id in claim_ids:
            fail(f"duplicate claim_id: {claim_id}")

        claim_ids.add(claim_id)

        if "statement" not in record:
            fail(f"{claim_id}: missing statement")

        if "mathematical_status" not in record:
            fail(f"{claim_id}: missing mathematical_status")

        if "evidence_class" not in record:
            fail(f"{claim_id}: missing evidence_class")

    evidence_ids = set()

    for record in evidence:
        evidence_id = record.get("evidence_id")

        if not isinstance(evidence_id, str) or not evidence_id:
            fail("evidence without valid evidence_id")

        if evidence_id in evidence_ids:
            fail(f"duplicate evidence_id: {evidence_id}")

        evidence_ids.add(evidence_id)

        claim_id = record.get("claim_id")

        if claim_id not in claim_ids:
            fail(
                f"{evidence_id}: references unknown claim_id {claim_id!r}"
            )

        if "class" not in record:
            fail(f"{evidence_id}: missing evidence class")

    # The verifier deliberately does NOT manufacture mathematical PASS.
    # Mathematical verification will be added when declared finite fixtures
    # and the independent JOIN-STABILITY computation are present.

    print(f"Manifest: OK")
    print(f"Claims: {len(claims)}")
    print(f"Evidence records: {len(evidence)}")
    print("Package structure: OK")
    print("Claim/evidence references: OK")
    print()
    print("STATUS: PACKAGE_VALID")
    print()
    print(
        "NOTE: PACKAGE_VALID is not a mathematical proof "
        "and is not a theorem certification."
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
