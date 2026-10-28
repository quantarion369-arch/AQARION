from pathlib import Path
import hashlib
import json
import shutil
import sys

repo, review, prior, out = map(Path, sys.argv[1:])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_manifest(folder):
    manifest = folder / "SHA256SUMS"
    require(manifest.is_file(), "Missing manifest: " + str(folder))
    entries = {}

    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        require(Path(name).name == name, "Unexpected manifest path")
        path = folder / name
        require(path.is_file(), "Missing evidence file: " + str(path))
        require(digest(path) == expected, "Checksum mismatch: " + str(path))
        entries[name] = expected

    return entries


review_entries = checked_manifest(review)
prior_entries = checked_manifest(prior)

require("receipt_review.json" in review_entries, "Review receipt unbound")
require("results.json" in prior_entries, "Census results unbound")
require("census.py" in prior_entries, "Census source unbound")
require("exit.txt" in prior_entries, "Census exit unbound")

review_data = json.loads(
    (review / "receipt_review.json").read_text(encoding="utf-8")
)
result = json.loads(
    (prior / "results.json").read_text(encoding="utf-8")
)

require(review_data["status"] == "PASS", "Review receipt not PASS")
require(
    Path(review_data["prior_run"]).resolve() == prior.resolve(),
    "Review references a different prior run",
)
require(
    review_data["prior_manifest_sha256"] == digest(prior / "SHA256SUMS"),
    "Prior manifest changed since review",
)
require(
    review_data["verified_prior_files"] == prior_entries,
    "Prior evidence set changed since review",
)
require(result["execution_status"] == "PASS", "Census status mismatch")
require(result["primitive_necklaces"] == 4080, "Necklace count mismatch")
require(result["full_rank_degree_3"] == 4080, "Rank count mismatch")
require(result["deficient_degree_3"] == 0, "Defect count mismatch")
require(result["prefix_good_total"] == 16, "Prefix count mismatch")
require(
    (prior / "exit.txt").read_text().strip() == "0",
    "Census exit was not zero",
)

evidence = out / "evidence"
evidence.mkdir()

for source, label, entries in (
    (review, "proof-review", review_entries),
    (prior, "cycle16", prior_entries),
):
    destination = evidence / label
    destination.mkdir()

    for name, expected in entries.items():
        shutil.copy2(source / name, destination / name)
        require(
            digest(destination / name) == expected,
            "Copied evidence checksum mismatch: " + name,
        )

    shutil.copy2(
        source / "SHA256SUMS",
        destination / "SHA256SUMS",
    )
    checked_manifest(destination)

source_snapshots = {}

for relative, expected in review_data["local_source_hashes"].items():
    relative_path = Path(relative)
    require(
        not relative_path.is_absolute() and ".." not in relative_path.parts,
        "Unsafe source snapshot path",
    )
    source = repo / relative_path
    require(source.is_file(), "Local source missing: " + relative)
    require(
        digest(source) == expected,
        "Local source changed since proof review: " + relative,
    )

    destination = evidence / "source-snapshots" / relative_path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    require(digest(destination) == expected, "Source snapshot copy mismatch")
    source_snapshots[relative] = expected

provenance = {
    "status": "PASS",
    "purpose": "Local working manuscript and preserved evidence",
    "proof_review_origin": str(review),
    "cycle16_origin": str(prior),
    "recorded_repository_HEAD": review_data["repository_HEAD"],
    "proof_review_manifest_sha256": digest(review / "SHA256SUMS"),
    "cycle16_manifest_sha256": digest(prior / "SHA256SUMS"),
    "source_snapshots": source_snapshots,
    "census_rerun": False,
    "new_rank_computations": False,
    "public_archive_status": "Not published by this preparation",
    "proof_status": "Written derivation under external theorem; review draft",
    "submission_authorized": False,
    "application_sources_modified": False,
    "stage_commit_fetch_push": "NONE",
}

(out / "PROVENANCE.json").write_text(
    json.dumps(provenance, indent=2) + "\n",
    encoding="utf-8",
)

print("PROOF_REVIEW_RECEIPT_BOUND=PASS")
print("CYCLE16_RECEIPT_BOUND=PASS")
print("EVIDENCE_COPIES_VERIFIED=PASS")
print("SOURCE_SNAPSHOTS_VERIFIED=PASS")
print("EXPERIMENTS_RERUN=NO")
print("MANUSCRIPT_STATUS=COMPLETE_WORKING_DRAFT")
print("SUBMISSION_STATUS=WAIT_FOR_REVIEW")
