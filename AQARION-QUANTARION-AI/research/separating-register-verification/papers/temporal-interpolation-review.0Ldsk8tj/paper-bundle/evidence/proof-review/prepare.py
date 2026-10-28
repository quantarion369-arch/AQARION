from pathlib import Path
import hashlib
import json
import math
import subprocess
import sys

repo = Path(sys.argv[1])
prior = Path(sys.argv[2])
out = Path(sys.argv[3])


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = prior / "SHA256SUMS"
require(manifest.is_file(), "Prior checksum manifest missing")

verified = {}

for line in manifest.read_text(encoding="utf-8").splitlines():
    expected, name = line.split("  ", 1)
    require(
        Path(name).name == name,
        "Unexpected path in prior checksum manifest",
    )
    path = prior / name
    require(path.is_file(), "Missing prior file: " + name)
    actual = sha256(path)
    require(actual == expected, "Prior checksum mismatch: " + name)
    verified[name] = actual

require(
    {"census.py", "results.json", "exit.txt", "stdout.txt"}
    <= set(verified),
    "Prior manifest lacks required execution artifacts",
)
require(
    (prior / "exit.txt").read_text().strip() == "0",
    "Prior execution did not exit zero",
)

result = json.loads(
    (prior / "results.json").read_text(encoding="utf-8")
)

require(result["execution_status"] == "PASS", "Prior status mismatch")
require(result["primitive_necklaces"] == 4080, "Necklace count mismatch")
require(result["full_rank_degree_3"] == 4080, "Full-rank count mismatch")
require(result["deficient_degree_3"] == 0, "Deficient count mismatch")
require(result["prefix_good_total"] == 16, "Prefix count mismatch")
require(result["full_rank_and_prefix_bad"] == 4064, "Prefix-bad mismatch")
require(result["exact_fallback_count"] == 0, "Fallback count mismatch")
require(result["bridge_test_nonvacuous"] is False, "Vacuity mismatch")
require(result["bridge_counterexamples"] == [], "Unexpected counterexamples")

cases = result["cases"]
require(len(cases) == 4080, "Recorded case count mismatch")

seen = set()
prefix_good = 0

for case in cases:
    text = case["word"]
    require(
        len(text) == 16 and set(text) <= {"0", "1"},
        "Malformed recorded word",
    )
    word = int(text, 2)
    rotations = [
        ((word << k) | (word >> (16 - k))) & 65535
        for k in range(16)
    ]

    require(len(set(rotations)) == 16, "Nonprimitive recorded case")
    require(min(rotations) == word, "Noncanonical recorded rotation")
    require(word not in seen, "Duplicate recorded representative")
    seen.add(word)

    separates = len({r >> 12 for r in rotations}) == 16
    require(
        case["four_prefix_separates"] == separates,
        "Recorded prefix flag mismatch",
    )
    require(case["modular_rank"] == 16, "Recorded modular rank mismatch")
    require(case["rational_rank"] == 16, "Recorded rational rank mismatch")
    require(
        case["rank_certificate_method"]
        == "modular_full_rank_certificate",
        "Unexpected recorded certificate method",
    )
    prefix_good += int(separates)

require(prefix_good == 16, "Independent prefix recount mismatch")

relative_sources = [
    "AQARION-QUANTARION-AI/research/separating-register-verification/"
    "cubic-exact-001/PROOF_AND_SCOPE.md",
    "AQARION-QUANTARION-AI/research/separating-register-verification/"
    "register-classification-001/verify_registers.py",
    "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/features/"
    "extremal_inspector/build-002/PROOF.md",
]

source_hashes = {}

for relative in relative_sources:
    path = repo / relative
    require(path.is_file(), "Expected local source missing: " + relative)
    source_hashes[relative] = sha256(path)

head = subprocess.run(
    ["git", "rev-parse", "HEAD"],
    cwd=repo,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()

proof = """# Spectral-to-register reduction: proof-review draft

## Status and dependency

This is a written mathematical derivation for independent review.
It is not a Lean proof, novelty clearance, or claim promotion.

External dependency:
Alexandr Valyuzhenich, Optimal functions with spectral constraints
in hypercubes, arXiv:2303.10995, Theorems 1 and 2.
The external theorem is not machine-proved by this package.

## Exact scope

Let d>=1, n=2^d, X a set of n states, T:X->X, and
h:X->{0,1}. Put a_t=h composed with T^t.

Assume length-n itineraries distinguish all states.
All polynomial ranks below are over Q.

Let H(n,j) be the rank of the evaluation matrix containing the
constant and every squarefree temporal monomial of degree <=j.

## Classification statement

H(n,d-1)<n if and only if the system, in its first-d-observation
coordinates, is a canonical shift register with a constant or
coordinate-literal/complement terminal.

In that case H(n,d-1)=n-1 and the stabilized degree-j dimension is
sum(binomial(d,k), k=0..min(j,d)).

## Forward proof

Rank deficiency gives a nonzero rational left annihilator.
Extend it by zero from the itinerary support Y to {0,1}^n.

Low-degree monomials and Walsh characters span the same filtered
space over Q and R. Thus the extension belongs to U_[d,n](n).

Theorem 1 gives support size >=2^d=n. Since |Y|=n, its support is Y.
Theorem 2 applies at equality.

Keep the full disjoint-block conclusion of that theorem:
there are d independent binary parameters b_1,...,b_d, and each
temporal coordinate is constant, b_i, or 1-b_i.
All d parameters occur. Hence dim span(1,a_0,...,a_(n-1))=d+1.

Define W_L=span_Q(1,a_0,...,a_(L-1)), with W_0=span_Q(1).

If W_(L+1)=W_L, then a_L lies in W_L. Composition K(g)=g composed
with T maps every generator of W_L into W_L, including K(1)=1.
Therefore W_L is K-invariant and all later observations lie in W_L.

The chain cannot pause and subsequently grow. It follows that
dim W_d=d+1. Otherwise an earlier pause would prevent W_n from
having dimension d+1.

Independence of 1,a_0,...,a_(d-1), together with their literal form,
forces the first d observations to use all d different parameters.
The prefix map is consequently bijective.

In those prefix coordinates the transition is
(u_1,...,u_d)->(u_2,...,u_d,f(u)).
Since d<n, the next observation a_d lies in the classified window,
so f is constant or a literal/complement.

This argument works on functions on X. It does not assume that
truncated itinerary supports are shift-closed.

## Converse

A constant/literal terminal produces only constants and literals
of the original prefix bits at all future times.
The first d observations already provide those original bits.

Thus degree-j temporal features span precisely the ordinary
degree-j polynomial functions on the full d-cube.
Their dimension is sum(binomial(d,k), k=0..min(j,d)).
At j=d-1 this is n-1.

## Single-cycle consequence

A bijective canonical constant/literal register must have terminal
u_1 or 1-u_1. The first fixes the all-zero state.
For the second, T^d is global complementation and T^(2d)=identity.

For d>=3, 2^d>2d, so neither transition is a single 2^d-cycle.
Therefore every separating observation on one 2^d-cycle has full
degree-(d-1) rational rank for d>=3.

This explains the cycle censuses. It does not make their
rank-defect implication nonvacuous.

## Labelled-map count for fixed balanced observation

Fix h with two fibers of size n/2.
A prefix coordinate bijection preserving h has ((n/2)!)^2 choices.
There are 2d+2 constant/literal terminals.

The prefix map is recovered uniquely from T and h, so distinct
encodings cannot represent the same observed transition.
The classification therefore gives
((n/2)!)^2 * (2d+2) represented extremal maps.

For d=3 this is (4!)^2*8=4608.

This is a mathematical completeness consequence under the external
dependency, not a new exhaustive eight-state computation.

## Evidence boundaries

The earlier Termux census is preserved, not rerun here.
Its manifest, recorded case structure, primitive representative
coverage, and prefix flags are checked by prepare.py.

That receipt review does not recompute its modular ranks and does
not authenticate its historical execution independently.
A checksum establishes current byte consistency, not proof validity.

The external equality theorem, this proof's correctness, and its
novelty require their own review. No application source changes,
claim enrollment, Git staging, commit, fetch, or push occur here.
"""

(out / "PROOF_AND_SCOPE.md").write_text(
    proof, encoding="utf-8"
)

review = {
    "status": "PASS",
    "repository_HEAD": head,
    "prior_run": str(prior),
    "prior_manifest_sha256": sha256(manifest),
    "verified_prior_files": verified,
    "recorded_primitive_cases": len(seen),
    "prefix_good_recount": prefix_good,
    "rank_census_rerun": False,
    "rank_claims": "Checked for receipt consistency; not recomputed",
    "local_source_hashes": source_hashes,
    "fixed_balanced_h_extremal_count_d3":
        math.factorial(4)**2 * 8,
    "proof_status": "Written derivation under external theorem; review draft",
    "machine_checked_general_proof": False,
    "application_sources_changed": False,
    "stage_commit_fetch_push": "NONE",
}

(out / "receipt_review.json").write_text(
    json.dumps(review, indent=2) + "\n",
    encoding="utf-8",
)

print("PRIOR_MANIFEST_VERIFIED=PASS")
print("RECORDED_PRIMITIVE_COVERAGE=4080")
print("PREFIX_FLAGS_RECOUNTED=PASS")
print("RANK_CENSUS_RERUN=NO")
print("LOCAL_SOURCE_HASHES_RECORDED=PASS")
print("FIXED_BALANCED_H_CLASSIFICATION_COUNT_D3=4608")
print("PROOF_STATUS=EXTERNAL_DEPENDENCY_REVIEW_DRAFT")
print("APPLICATION_SOURCES_CHANGED=NO")
print("STAGED_COMMITTED_FETCHED_PUSHED=NO")
print("PREPARATION_STATUS=PASS")
