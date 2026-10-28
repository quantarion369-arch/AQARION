from pathlib import Path
import hashlib
import json
import shutil
import sys

paper = Path(sys.argv[1])
out = Path(sys.argv[2])

EXPECTED = (
    "6c068e7944ffee836903415d198fdee2"
    "2d17aea79edcf14b5883679e161dc906"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manuscript = paper / "MANUSCRIPT.md"
manifest = paper / "SHA256SUMS"

require(manifest.is_file(), "Original manifest missing")
require(digest(manuscript) == EXPECTED, "Manuscript identity mismatch")

entries = {}

for line in manifest.read_text(encoding="utf-8").splitlines():
    expected, name = line.split("  ", 1)
    relative = Path(name)

    require(
        not relative.is_absolute() and ".." not in relative.parts,
        "Unsafe manifest path",
    )

    source = paper / relative
    require(source.is_file(), "Missing original file: " + name)
    require(digest(source) == expected, "Original checksum mismatch: " + name)
    entries[name] = expected

require(
    entries.get("MANUSCRIPT.md") == EXPECTED,
    "Manifest does not bind the expected manuscript",
)

lines = manuscript.read_text(encoding="utf-8").splitlines()

require(
    lines[125] == "## 4. The external support result used here",
    "Section-4 line anchor changed",
)
require(lines[160] == "Theorem 5.1.", "Theorem line anchor changed")
require(lines[259] == "Corollary 6.2.", "Counting line anchor changed")

copied = out / "paper-bundle"
copied.mkdir()

for name, expected in entries.items():
    destination = copied / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(paper / name, destination)

    require(
        digest(destination) == expected,
        "Copied artifact mismatch: " + name,
    )

shutil.copy2(manifest, copied / "SHA256SUMS")

audit_rows = [
    {
        "lines": "130-133,147-148",
        "claim": "Support lower bound",
        "basis": "Valyuzhenich Theorem 1; n_source=L, i=d, j=L",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "135-155",
        "claim": "Disjoint-block support and literal coordinates",
        "basis": "Theorem 2(1); k+ell=d; ell>=L-j=0",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "182-188",
        "claim": "Nonzero rational annihilator and spectral interval",
        "basis": "Injective itinerary map and low-degree character basis",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "190-192",
        "claim": "Equality on the entire itinerary support",
        "basis": "Support at least 2^d and contained in 2^d points",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "194-206",
        "claim": "First d observations form a bijective prefix",
        "basis": "Literal coordinate span dimension d+1; no-pause lemma",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "208-212",
        "claim": "Terminal is constant or literal",
        "basis": "The observation a_d is inside the window since L>=d+1",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "214-225",
        "claim": "Converse and complete Hilbert profile",
        "basis": "All future observations are literals; prefix supplies cube bits",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "248-257",
        "claim": "Unique parity obstruction up to scale",
        "basis": "Parity annihilation and rank 2^d-1",
        "disposition": "SUPPORTED",
    },
    {
        "lines": "260-283",
        "claim": "Labelled counting formula",
        "basis": "Prefix recovers encoding; terminal is then uniquely recovered",
        "disposition": "SUPPORTED",
    },
]

audit = {
    "review_type": "Assistant source-correspondence review",
    "independent_referee_report": False,
    "manuscript_version": "0.1",
    "manuscript_sha256": EXPECTED,
    "reviewed_lines": [126, 291],
    "external_source": {
        "identifier": "arXiv:2303.10995v1",
        "author": "Alexandr Valyuzhenich",
        "title": "Optimal functions with spectral constraints in hypercubes",
        "used_results": ["Lemma 4", "Theorem 1", "Theorem 2(1)"],
        "source_cube_dimension": "L",
        "source_lower_level": "d",
        "source_upper_level": "L",
    },
    "rows": audit_rows,
    "blocking_gap_identified_in_displayed_sections": False,
    "general_proof_machine_checked": False,
    "novelty_cleared": False,
    "independent_review_complete": False,
    "new_manuscript_version_created": False,
    "experiments_rerun": False,
}

(out / "SOURCE_CORRESPONDENCE.json").write_text(
    json.dumps(audit, indent=2) + "\n",
    encoding="utf-8",
)

numbered = "\n".join(
    f"{number:04d}: {line}"
    for number, line in enumerate(lines, 1)
    if 126 <= number <= 291
)

(out / "NUMBERED_REVIEWED_TEXT.txt").write_text(
    numbered + "\n", encoding="utf-8"
)

request = """# Request for independent mathematical review

## Artifact

Review paper-bundle/MANUSCRIPT.md, version 0.1.
The exact manuscript SHA-256 is recorded in SOURCE_CORRESPONDENCE.json.

Please assess the proof independently. The accompanying assistant
audit is not an independent referee report.

## Claim to assess

Let |X|=2^d, let T:X->X, let h:X->{0,1}, and let L>=d+1.
Assume the length-L itineraries separate all states.
All evaluation ranks are over Q.

Theorem 5.1 claims equivalence of:

A. Degree-(d-1) temporal evaluation rank is deficient.

B. The first d observations form a bijection to the d-cube and,
   in those coordinates, the terminal is constant or a literal.

C. The stabilized degree profile is the ordinary d-cube profile.

## Requested checks

1. Does the rational null vector define the required nonzero real
   hypercube function, using separation essentially?

2. Do Valyuzhenich's Theorems 1 and 2 apply with cube dimension L,
   lower spectral level d, and upper level L?

3. Does the equality statement give disjoint literal blocks,
   rather than merely an arbitrary affine support?

4. Does the no-pause argument force the first d observations to
   supply all parameters without assuming truncated shift closure?

5. Is the converse valid for arbitrary deterministic T, including
   transient and noninvertible cases?

6. Does recoverability of the prefix map prevent duplicate labelled
   transitions in the counting construction?

7. Are the d=1 boundary, L>=d+1 requirement, rational field,
   and labelled-count conventions handled correctly?

8. Is the temporal rank criterion known in prior register-realization,
   interpolation, null-design, or trade literature?

## Requested disposition

For each issue, please record one of:
SUPPORTED, GAP, MISMATCH, NOT_APPLICABLE.

For a GAP or MISMATCH, identify the exact line and either a missing
hypothesis, an invalid inference, or an explicit counterexample.

## Boundaries

No review, endorsement, acceptance, or author agreement is presumed.
No experiment replay is requested unless a specific implementation
question makes it necessary.
No message has been sent by preparation of this packet.
"""

(out / "REVIEW_REQUEST.md").write_text(request, encoding="utf-8")

prior_art = """# Closest-prior-art comparison: current limits

## Established components; not originality claims

Valyuzhenich, arXiv:2303.10995v1:
support bound and disjoint-block equality classification.

Moran-Rashtchian:
Hilbert-function and interpolation-degree framework.

Frankl-Pach 1983:
null-design support bound and trace argument.

Minimum-trade, register-realization, and output-equivalence
constructions have extensive earlier literature.

## Encoding count

Li, Zhu, Lu, arXiv:1911.01588v2, Remark 2:
the factor ((2^(d-1))!)^2 already appears.
Our total count must be described as a consequence of selecting
the constant/literal terminal families, not a new factorial principle.

## Temporal coordinate bijection

Xiong, Zhong, Lin:
Studying the isomorphism of NFSRs via a general framework of bijections.
Designs, Codes and Cryptography 93, 2823-2853, 2025.
DOI: 10.1007/s10623-025-01622-y.

The accessible publisher appendix explicitly uses
(b,b composed with F,...,b composed with F^(d-1)).
The complete main text was not available in the retrieved preview.
A complete theorem-level non-overlap assessment is NOT established.

## Candidate contribution to compare

The specific rational temporal rank-defect criterion forcing
the constant/literal register class.

No assertion that an identical theorem is absent from the literature
has been established.

## Version boundary

This packet reviews the pinned version 0.1.
A self-contained version 0.2 was proposed in the conversation,
but no successful preparation receipt has been supplied.
It is not silently substituted for the reviewed manuscript.
"""

(out / "PRIOR_ART_COMPARISON.md").write_text(
    prior_art, encoding="utf-8"
)

provenance = {
    "status": "PASS",
    "original_paper_directory": str(paper),
    "original_manifest_sha256": digest(manifest),
    "original_manuscript_sha256": EXPECTED,
    "original_files_verified_and_copied": len(entries),
    "manuscript_content_changed": False,
    "packet_role": "Independent review handoff, not a new manuscript",
    "reviewer_contacted": False,
    "submission_authorized": False,
    "stage_commit_fetch_push": "NONE",
}

(out / "PACKET_PROVENANCE.json").write_text(
    json.dumps(provenance, indent=2) + "\n",
    encoding="utf-8",
)

print("PINNED_MANUSCRIPT_HASH=PASS")
print("ORIGINAL_PAPER_MANIFEST=PASS")
print("UNCHANGED_PAPER_COPY=PASS")
print("SOURCE_CORRESPONDENCE_SAVED=PASS")
print("NUMBERED_REVIEW_TEXT_SAVED=PASS")
print("REVIEW_REQUEST_SAVED=PASS")
print("PRIOR_ART_LIMITATIONS_SAVED=PASS")
print("NEW_MANUSCRIPT_VERSION=NO")
print("EXPERIMENTS_RERUN=NO")
print("INDEPENDENT_REVIEW_COMPLETE=NO")
print("REVIEWER_CONTACTED=NO")
print("STAGED_COMMITTED_FETCHED_PUSHED=NO")
print("PACKET_PREPARATION=PASS")
