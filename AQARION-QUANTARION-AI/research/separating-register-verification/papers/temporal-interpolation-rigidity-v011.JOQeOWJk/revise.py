from pathlib import Path
import hashlib
import json
import shutil
import sys

old, census, out = map(Path, sys.argv[1:])

EXPECTED_MANUSCRIPT = (
    "6c068e7944ffee836903415d198fdee2"
    "2d17aea79edcf14b5883679e161dc906"
)
EXPECTED_DEFECT_LIST = (
    "12a3ef626871915fa3c9a69a00a6701ff"
    "14c88e792e5f3f54db78c7ad1fb72af"
)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(folder):
    path = folder / "SHA256SUMS"
    require(path.is_file(), "Manifest missing: " + str(folder))
    entries = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        expected, name = line.split("  ", 1)
        relative = Path(name)

        require(
            not relative.is_absolute()
            and ".." not in relative.parts,
            "Unsafe manifest path",
        )

        source = folder / relative
        require(source.is_file(), "Missing file: " + str(source))
        require(
            digest(source) == expected,
            "Checksum mismatch: " + str(source),
        )
        entries[name] = expected

    return entries


def copy_verified(folder, entries, destination):
    destination.mkdir(parents=True)

    for name, expected in entries.items():
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(folder / name, target)
        require(
            digest(target) == expected,
            "Copied evidence mismatch: " + name,
        )

    shutil.copy2(
        folder / "SHA256SUMS",
        destination / "SHA256SUMS",
    )


def replace_once(text, before, after):
    require(
        text.count(before) == 1,
        "Missing or ambiguous revision anchor: " + before[:80],
    )
    return text.replace(before, after, 1)


old_entries = verify_manifest(old)
census_entries = verify_manifest(census)

require(
    old_entries.get("MANUSCRIPT.md") == EXPECTED_MANUSCRIPT,
    "Wrong parent manuscript",
)

require(
    {"results.json", "rational_defect_codes.txt", "verify_all.py"}
    <= set(census_entries),
    "Required census artifacts are not manifested",
)

require(
    digest(census / "rational_defect_codes.txt")
    == EXPECTED_DEFECT_LIST,
    "Defect-list fingerprint mismatch",
)

data = json.loads(
    (census / "results.json").read_text(encoding="utf-8")
)
require(data["status"] == "PASS", "Census audit did not pass")

counts = data["census"]

require(counts["maps"] == 16777216, "Map count mismatch")
require(counts["separating"] == 1612800, "Separating count mismatch")
require(counts["F2_deficient"] == 9216, "F2 count mismatch")
require(counts["Q_rank7"] == 4608, "Rational defect count mismatch")
require(
    counts["Q_rank8_separating"] == 1608192,
    "Rational full-rank count mismatch",
)
require(counts["sha256"] == EXPECTED_DEFECT_LIST, "Recorded hash mismatch")
require(
    counts["generated_set_equals_census"] is True,
    "Generated-set equality missing",
)

text = (old / "MANUSCRIPT.md").read_text(encoding="utf-8")

text = replace_once(
    text,
    "Version 0.1 — 27 October 2026",
    "Version 0.1.1 — 27 October 2026",
)

text = replace_once(
    text,
    "Let X be a finite state set, T:X->X a deterministic transition, and\n"
    "h:X->{0,1} a binary observation. Put",
    "Let X be a nonempty finite state set, T:X->X a deterministic\n"
    "transition, and h:X->{0,1} a binary observation. Observation lengths\n"
    "L and degree cutoffs j are nonnegative integers. Put",
)

text = replace_once(
    text,
    "    W_L = span_Q(1,a_0,...,a_(L-1)),  W_0=span_Q(1).\n",
    "    W_L = span_Q(1,a_0,...,a_(L-1)),  W_0=span_Q(1).\n\n"
    "Write W_infinity=span_Q({1} union {a_t:t>=0}).\n",
)

text = replace_once(
    text,
    "Low-degree monomials and low-weight Walsh characters span the same\n"
    "filtered polynomial space over Q and R. The extension v therefore\n"
    "belongs to U_[d,L](L).",
    "For A subset {0,...,L-1}, the Walsh character is\n\n"
    "    chi_A(y)=product(1-2*y_t : t in A).\n\n"
    "Conversely, a monomial y_S equals\n"
    "2^(-|S|)*product(1-chi_{t}(y):t in S).\n"
    "Thus low-degree monomials and low-weight Walsh characters span the\n"
    "same filtered polynomial space over Q and R. The extension v\n"
    "therefore belongs to U_[d,L](L).",
)

text = replace_once(
    text,
    "transition with prefix map exactly q.\n",
    "transition with prefix map exactly q:\n\n"
    "    Phi_d(x)=q(x).\n",
)

text = replace_once(
    text,
    "The register proof above additionally identifies the noncyclic\n"
    "extremal systems.",
    "For the alternative argument, a single full cycle makes the affine\n"
    "map's order exactly 2^d. Its homogeneous matrix M satisfies\n"
    "(M-I)^(2^d)=0 in characteristic two. Thus M-I is nilpotent of\n"
    "index at most d+1, which gives the stated power-of-two order bound.\n\n"
    "The register proof above additionally identifies the noncyclic\n"
    "extremal systems.",
)

related = """The older null-design literature must also be distinguished from
our temporal conclusion. Frankl-Pach [FP] proves the weighted support
bound and supplies the trace mechanism. Disjoint-block trade geometry
appears in Krotov [K] and Ghorbani et al. [GKKK].

The output-preserving encoding factor ((2^(d-1))!)^2 appears explicitly
in Li-Zhu-Lu [LZL, Remark 2]. Xiong-Zhong-Lin [XZL, Appendix B] explicitly
uses a temporal-coordinate bijection. We do not claim those ingredients
as new. The specific criterion requiring priority comparison is the
rational temporal rank defect forcing the constant/literal terminal class.

The accessible preview of [XZL] does not expose its complete main text.
No complete theorem-level non-overlap assessment is claimed.

"""

text = replace_once(
    text,
    "This manuscript supplies a proof for review.",
    related + "This manuscript supplies a proof for review.",
)

addition = """### 8.1 Unrestricted eight-state finite check

A subsequent completed Termux audit enumerated all 8^8=16,777,216
transition arrays with fixed observation h=00001111. It found:

    separating transition maps:                    1612800
    F2 degree-two deficient candidates:                9216
    Q degree-two rank-seven maps:                      4608
    Q degree-two rank-eight maps among candidates:     4608
    Q degree-two full-rank separating maps overall:  1608192

Every F2-full-rank matrix is full rank over Q by the integer-minor
argument. Every F2-deficient candidate received exact rational rank
using integer elimination with gcd reduction.

All 9,216 candidates had a bijective three-prefix and induced one
of the sixteen affine Boolean feedback functions. Each feedback
occurred 576 times. The eight constant/literal functions gave rational
rank seven; the other eight affine functions gave rational rank eight.

The rational-defect set agreed exactly with the independently generated
observation-preserving relabelings of the eight constant/literal
registers. All 4,608 parity obstructions and cubic witnesses passed.
The sixteen canonical representatives were also checked using separate
Fraction Gaussian elimination.

For increasing transition code
m=sum(T[i]*8^i, i=0..7), encoded as one ASCII decimal integer plus LF
per record, the 4,608 rational-defect codes have SHA-256:

    12a3ef626871915fa3c9a69a00a6701ff14c88e792e5f3f54db78c7ad1fb72af

This is a finite check for one fixed balanced observation, not a proof
of Theorem 5.1 for arbitrary d. The attached audit also contains
partition-ratio and trade-matrix checks; those are separate research
lanes and are not dependencies of this manuscript.

"""

text = replace_once(
    text,
    "## 9. Field and scope limitations",
    addition + "## 9. Field and scope limitations",
)

text = replace_once(
    text,
    "The numerical evidence is complete for the sixteen-cycle census.\n"
    "A larger cycle census is not required for the theorem.",
    "The numerical evidence is complete for the sixteen-cycle census\n"
    "and the fixed-observation unrestricted eight-state census.\n"
    "Neither finite check replaces the general proof.\n"
    "A larger cycle census is not required for the theorem.",
)

extra_references = """
[FP] Peter Frankl and Janos Pach.
On the Number of Sets in a Null t-Design.
European Journal of Combinatorics 4(1), 21-23, 1983.
DOI: 10.1016/S0195-6698(83)80004-3.

[K] Denis S. Krotov.
On the gaps of the spectrum of volumes of trades.
Journal of Combinatorial Designs 26(3), 119-126, 2018.
DOI: 10.1002/jcd.21592.

[GKKK] E. Ghorbani, S. Kamali, G. B. Khosrovshahi, D. S. Krotov.
On the volumes and affine types of trades.
Electronic Journal of Combinatorics 27(1), P1.29, 2020.
DOI: 10.37236/8367.

[LZL] Bowen Li, Shiyong Zhu, Jianquan Lu.
Improved transformation between Fibonacci FSRs and Galois FSRs
based on semi-tensor product.
Consulted preprint: arXiv:1911.01588v2, 26 June 2020.
Remark 2 is the encoding-count comparison.

[XZL] Jingtao Xiong, Jianghua Zhong, Dongdai Lin.
Studying the isomorphism of NFSRs via a general framework of bijections.
Designs, Codes and Cryptography 93, 2823-2853, 2025.
DOI: 10.1007/s10623-025-01622-y.
Publisher abstract and accessible appendices inspected.
Complete main-text comparison remains pending.
"""

text = text.rstrip() + "\n" + extra_references

(out / "MANUSCRIPT.md").write_text(text, encoding="utf-8")

copy_verified(
    old, old_entries,
    out / "evidence" / "parent-v01",
)
copy_verified(
    census, census_entries,
    out / "evidence" / "eight-state-audit",
)

changelog = """# Changes from pinned v0.1

- Explicit nonempty state set and integer horizon/degree conventions.
- Explicit definition of W_infinity.
- Displayed Walsh/monomial conversion.
- Displayed recoverable-prefix identity Phi_d=q.
- Expanded justification of the alternative affine order bound.
- Added the completed unrestricted eight-state finite check.
- Expanded attribution and recorded the closest-source access limit.

The spectral proof is retained. No self-contained v0.2 branch is
silently adopted. The central classification and counting conclusions
are unchanged.

The source-correspondence review of v0.1 remains bound to v0.1.
This revision needs delta review and independent assessment.
No independent referee approval or originality clearance is claimed.
"""

(out / "CHANGELOG.md").write_text(changelog, encoding="utf-8")

report = {
    "status": "PASS",
    "version": "0.1.1",
    "parent_manuscript_sha256": EXPECTED_MANUSCRIPT,
    "parent_manifest_sha256": digest(old / "SHA256SUMS"),
    "manuscript_sha256": digest(out / "MANUSCRIPT.md"),
    "eight_state_audit_origin": str(census),
    "eight_state_audit_manifest_sha256": digest(census / "SHA256SUMS"),
    "rational_defect_list_sha256": EXPECTED_DEFECT_LIST,
    "proof_route": "External spectral equality theorem retained",
    "central_theorem_changed": False,
    "assistant_review_basis": "Pinned v0.1 full text",
    "revision_delta_review_pending": True,
    "independent_referee_review_complete": False,
    "novelty_cleared": False,
    "author_list_confirmed": False,
    "experiments_rerun": False,
    "original_bundles_changed": False,
    "application_sources_changed": False,
    "stage_commit_fetch_push": "NONE",
    "submission_authorized": False,
}

(out / "REVISION_REPORT.json").write_text(
    json.dumps(report, indent=2) + "\n",
    encoding="utf-8",
)

print("PARENT_V01_HASH=PASS")
print("PARENT_PAPER_MANIFEST=PASS")
print("EIGHT_STATE_AUDIT_MANIFEST=PASS")
print("DEFECT_LIST_FINGERPRINT=PASS")
print("EVIDENCE_COPIES_VERIFIED=PASS")
print("MANUSCRIPT_VERSION=0.1.1")
print("CENTRAL_THEOREM_CHANGED=NO")
print("MANUSCRIPT_SHA256=" + report["manuscript_sha256"])
print("EXPERIMENTS_RERUN=NO")
print("ORIGINAL_BUNDLES_CHANGED=NO")
print("APPLICATION_SOURCES_CHANGED=NO")
print("STAGED_COMMITTED_FETCHED_PUSHED=NO")
print("REVISION_PREPARATION=PASS")
