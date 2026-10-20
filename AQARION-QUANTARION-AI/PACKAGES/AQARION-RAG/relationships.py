"""Revision-pinned relationship lookup; validation is not review approval."""
import hashlib
import subprocess
import json
from pathlib import Path

import context
import retrieve

REGISTRY = Path(__file__).resolve().with_name("relationships.json")


class RelationshipError(ValueError):
    pass


def identity(item):
    return (
        item["path"], item["commit_sha"],
        item["char_start"], item["char_end"],
    )


def validate_anchor(anchor):
    if not isinstance(anchor, dict):
        raise RelationshipError("Anchor must be an object")
    required = {
        "path", "commit_sha", "char_start", "char_end", "passage_sha256"
    }
    if not required.issubset(anchor):
        raise RelationshipError("Anchor is missing required fields")

    start, end = anchor["char_start"], anchor["char_end"]
    if type(start) is not int or type(end) is not int:
        raise RelationshipError("Offsets must be integers")
    if start < 0 or end <= start:
        raise RelationshipError("Invalid offset range")
    if not isinstance(anchor["passage_sha256"], str):
        raise RelationshipError("Passage hash must be a string")

    entries = [
        entry for entry in retrieve.load_manifest()
        if entry["path"] == anchor["path"]
        and entry["sha"] == anchor["commit_sha"]
    ]
    if len(entries) != 1:
        raise RelationshipError("Anchor is not uniquely pinned in the manifest")

    text = retrieve.load_at_sha(anchor["path"], anchor["commit_sha"])
    if end > len(text):
        raise RelationshipError("Offsets exceed pinned source")

    matches = [
        item for item in context._paragraphs(entries[0], text)
        if item["char_start"] == start and item["char_end"] == end
    ]
    if len(matches) != 1:
        raise RelationshipError("Anchor must identify one complete paragraph")

    item = matches[0]
    digest = hashlib.sha256(item["passage"].encode("utf-8")).hexdigest()
    if digest != anchor["passage_sha256"]:
        raise RelationshipError("Pinned passage hash mismatch")
    return {**item, "passage_sha256": digest}


def load_relationships():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RelationshipError("Registry must be an object")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise RelationshipError("Unsupported relationship schema")
    records = data.get("relationships")
    if not isinstance(records, list):
        raise RelationshipError("Relationships must be a list")
    ids = [item.get("id") for item in records if isinstance(item, dict)]
    if len(ids) != len(records) or any(
        not isinstance(value, str) or not value for value in ids
    ) or len(ids) != len(set(ids)):
        raise RelationshipError("Relationship IDs must be unique nonempty strings")
    return records


def resolve_related(passages, records=None):
    """Return direct relationships only; never alter retrieval or claim status."""
    wanted = {identity(item) for item in passages}
    related, diagnostics = [], []
    if records is None:
        try:
            records = load_relationships()
        except (RelationshipError, OSError, ValueError, TypeError,
                subprocess.SubprocessError) as error:
            return {
                "related_evidence": [],
                "relationship_diagnostics": [{
                    "relationship_id": "registry",
                    "status": "unavailable_or_invalid",
                    "reason": type(error).__name__ + ": " + str(error),
                }],
            }

    if not isinstance(records, list):
        return {
            "related_evidence": [],
            "relationship_diagnostics": [{
                "relationship_id": "registry",
                "status": "invalid",
                "reason": "Relationships must be a list",
            }],
        }

    for record in records:
        if not isinstance(record, dict):
            diagnostics.append({
                "relationship_id": "unknown",
                "status": "invalid",
                "reason": "Relationship record must be an object",
            })
            continue
        try:
            if record.get("relation") != "qualifies_provenance":
                raise RelationshipError("Unsupported relationship type")
            if record.get("source_basis") != "explicit_documented_correction":
                raise RelationshipError("Unsupported source basis")
            if record.get("review_status") not in ("pending", "approved"):
                raise RelationshipError("Unsupported review status")
            if record["review_status"] == "approved":
                if not record.get("reviewer") or not record.get("reviewed_at"):
                    raise RelationshipError("Approved record lacks review metadata")

            subject = validate_anchor(record["subject"])
            object_ = validate_anchor(record["object"])
            supporting = [
                {
                    "role": item["role"],
                    "citation": validate_anchor(item["anchor"]),
                }
                for item in record.get("supporting_evidence", [])
            ]

            directions = []
            if identity(object_) in wanted:
                directions.append("correction_for_returned_statement")
            if identity(subject) in wanted:
                directions.append("original_statement_for_returned_correction")
            if not directions:
                continue

            related.append({
                "id": record["id"],
                "relation": record["relation"],
                "source_basis": record["source_basis"],
                "review_status": record["review_status"],
                "review_note": record.get("review_note", ""),
                "locator_validation": "passed",
                "match_directions": directions,
                "subject": subject,
                "object": object_,
                "supporting_evidence": supporting,
                "scope_note": record.get("scope_note", ""),
            })
        except (RelationshipError, KeyError, TypeError, ValueError,
                OSError, subprocess.SubprocessError) as error:
            diagnostics.append({
                "relationship_id": record.get("id", "unknown"),
                "status": "invalid",
                "reason": str(error),
            })

    return {
        "related_evidence": related,
        "relationship_diagnostics": diagnostics,
    }
