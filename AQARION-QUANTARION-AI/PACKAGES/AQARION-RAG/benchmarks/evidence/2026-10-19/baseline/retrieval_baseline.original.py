"""Development benchmark: reviewed supporting passages, not exhaustive qrels."""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import traceback
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE))
import retrieve

PINS = {
    "L": (
        "EVIDENCE-LEDGER.md",
        "b1642c3392bfee54d4d7854b3dc6d8b53f4f58b2",
    ),
    "Q": (
        "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG/corpus/quadratic-stability-witnesses.md",
        "e9322761a2525a2b5fb9a0c9d31888de092d7140",
    ),
}

# Each group is (source ID, alternative unique paragraph anchors).
# Multi-group cases require evidence for every group.
CASES = [
    ("L01", "single", "Is the evidence ledger a complete claim-level record?",
     [("L", ["Status: PARTIAL LEDGER"])]),
    ("L02", "single", "Were the original three checks independent implementations?",
     [("L", ['"Three independent checks" overstated independence'])]),
    ("L03", "single", "What did the actual production-source cross-check execute?",
     [("L", ["Execution: user ran the path-specific loader"])]),
    ("L04", "single", "Does the production cross-check establish general correctness?",
     [("L", ["Scope: finite-domain agreement"])]),
    ("L05", "single", "Was the equality replay byte-for-byte identical to the reported dependency?",
     [("L", ["**Dependency qualification:**"])]),
    ("L06", "single", "Was the closure-cost equality theorem Lean-formalized?",
     [("L", ["**Theorem status:**"])]),
    ("L07", "single", "Does zero forward defect imply commutation?",
     [("L", ["is forward stability, not commutation"])]),
    ("L08", "single", "Were the 18,737 non-bijective checks exhaustive?",
     [("L", ["18,737 random non-bijective"])]),
    ("L09", "single", "Where is the canonical oracle implementation of prof.py?",
     [("L", [
         "canonical oracle/census implementation",
         "The two unreferenced duplicates were removed.",
     ])]),
    ("L10", "single", "Does the ledger establish novelty or machine-checked proof for the closure-cost paper?",
     [("L", ["Paper proof is not machine-checked; novelty is not established."])]),
    ("Q01", "single", "How does this fixture define bounded_orbit?",
     [("Q", ["Definitions:"])]),
    ("Q02", "single", "How is c = 0.3 classified under the bounded-orbit reading?",
     [("Q", [
         "The quadratic map with c = 0.3 is unstable",
         "| 0.3 | false | false |",
     ])]),
    ("Q03", "single", "Does c = 0.25 have an attracting fixed point according to the fixture?",
     [("Q", ["| 0.25 | true | false |"])]),
    ("Q04", "single", "What constitutes a witness against universal bounded-orbit stability?",
     [("Q", ["Witness rule:"])]),
    ("Q05", "single", "Is c = -1.0 both bounded and attracting in the fixture?",
     [("Q", ["| -1.0 | true | false |"])]),
    ("Q06", "single", "What initial state is used for these quadratic computations?",
     [("Q", ["starting at x = 0."])]),
    ("M01", "multi", "What was wrong with the original provenance description, and what was actually checked afterward?",
     [
         ("L", ['"Three independent checks" overstated independence']),
         ("L", ["Execution: user ran the path-specific loader"]),
     ]),
    ("M02", "multi", "Does the feedback extension prove an equivalence, or only one implication?",
     [
         ("L", ["upper equality implies the nested-alphabet"]),
         ("L", ["It does not establish that nested alphabets"]),
     ]),
    ("M03", "multi", "Can the fixture classify an orbit as bounded without an attracting fixed point?",
     [
         ("Q", ["Definitions:"]),
         ("Q", ["| -2.0 | true | false |"]),
     ]),
    ("M04", "multi", "What was established by the equality replay, and what remains unverified?",
     [
         ("L", ["**Dependency qualification:**"]),
         ("L", ["**Theorem status:**"]),
     ]),
    ("N01", "unsupported", "What was the conclusion of GitHub Actions run 39346847689?", []),
    ("N02", "unsupported", "Which Lean axioms were reported by the closure-cost equality theorem's formal axiom audit?", []),
    ("N03", "unsupported", "What exact numerical value does the c = 0.5 orbit have at iteration 500?", []),
    ("N04", "lexical_no_match", "zzqxv_unindexed_7f3b91", []),
]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def passages(text):
    records = []
    offset = 0
    separator = chr(10) * 2
    for paragraph in text.split(separator):
        passage = paragraph.strip()
        start = offset + len(paragraph) - len(paragraph.lstrip())
        if passage:
            records.append({
                "char_start": start,
                "char_end": start + len(passage),
                "passage": passage,
            })
        offset += len(paragraph) + len(separator)
    return records

def key(record):
    return (
        record["path"], record["commit_sha"],
        record["char_start"], record["char_end"],
    )

def main(out, report):
    root = Path(subprocess.check_output(
        ["git", "-C", str(PACKAGE), "rev-parse", "--show-toplevel"],
        text=True,
    ).strip())

    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args])

    if out == root or root in out.parents:
        raise RuntimeError("Evidence directory must be outside the checkout")

    head = git("rev-parse", "HEAD").decode().strip()
    report.update({
        "benchmark_version": 1,
        "execution_context": "local_development_benchmark",
        "tested_commit": head,
        "python": sys.version,
        "platform": platform.platform(),
        "top_k": 3,
        "label_scope": "selected supporting passages; not exhaustive relevance judgments",
        "unsupported_scope": "corpus-local absence or unmet premise; not semantic abstention certification",
        "files": {},
        "sources": {},
        "cases": [],
    })

    if head != "a77f3dcc46eb89150e3e617f6648c6a49e147fae":
        raise RuntimeError("Unexpected implementation revision")

    for args in (
        ("diff", "--quiet", "--"),
        ("diff", "--cached", "--quiet", "--"),
    ):
        subprocess.check_call(["git", "-C", str(root), *args])

    tracked = [
        PACKAGE / "retrieve.py",
        PACKAGE / "corpus" / "MANIFEST.md",
        Path(__file__).resolve(),
    ]
    before = {str(p.relative_to(root)): digest(p.read_bytes()) for p in tracked}
    report["files"] = before

    manifest = retrieve.load_manifest()
    actual = [(row["path"], row["sha"]) for row in manifest]
    if len(actual) != len(PINS) or set(actual) != set(PINS.values()):
        raise RuntimeError("Manifest differs from the reviewed two-source corpus")

    texts = {}
    paragraphs = {}
    for source_id, (path, sha) in PINS.items():
        text = retrieve.load_at_sha(path, sha)
        texts[(path, sha)] = text
        paragraphs[source_id] = passages(text)
        raw = git("show", sha + ":" + path)
        report["sources"][source_id] = {
            "path": path,
            "commit_sha": sha,
            "git_blob_sha256": digest(raw),
            "decoded_text_utf8_sha256": digest(text.encode("utf-8")),
            "paragraph_count": len(paragraphs[source_id]),
        }

    ids = [case[0] for case in CASES]
    if len(CASES) != 24 or len(set(ids)) != len(ids):
        raise RuntimeError("Unexpected case count or duplicate IDs")

    resolved = []
    for case_id, kind, query, groups in CASES:
        accepted_groups = []
        for source_id, anchors in groups:
            path, sha = PINS[source_id]
            accepted = []
            for anchor in anchors:
                matches = [
                    p for p in paragraphs[source_id]
                    if anchor in p["passage"]
                ]
                if len(matches) != 1:
                    raise RuntimeError(
                        f"{case_id}: anchor must match exactly one paragraph: {anchor!r}; found {len(matches)}"
                    )
                accepted.append({
                    **matches[0],
                    "path": path,
                    "commit_sha": sha,
                    "anchor": anchor,
                })
            accepted_groups.append(accepted)
        resolved.append((case_id, kind, query, accepted_groups))

    citation_count = 0
    for case_id, kind, query, groups in resolved:
        results = retrieve.retrieve_cited(query, top_k=3)
        if len(results) > 3:
            raise RuntimeError("Retriever exceeded top_k")

        for rank, result in enumerate(results, 1):
            text = texts[(result["path"], result["commit_sha"])]
            start, end = result["char_start"], result["char_end"]
            if not (0 <= start <= end <= len(text)):
                raise RuntimeError(f"{case_id}: invalid citation bounds")
            if text[start:end] != result["passage"]:
                raise RuntimeError(f"{case_id}: citation reconstruction failed")
            if result["rank"] != rank:
                raise RuntimeError(f"{case_id}: invalid rank")
            citation_count += 1

        group_ranks = []
        for alternatives in groups:
            accepted_keys = {key(item) for item in alternatives}
            ranks = [
                result["rank"] for result in results
                if key(result) in accepted_keys
            ]
            group_ranks.append(min(ranks) if ranks else None)

        report["cases"].append({
            "id": case_id,
            "kind": kind,
            "query": query,
            "accepted_groups": groups,
            "first_rank_per_group": group_ranks,
            "results": results,
        })

    single = [c for c in report["cases"] if c["kind"] == "single"]
    multi = [c for c in report["cases"] if c["kind"] == "multi"]
    singles_hit = sum(c["first_rank_per_group"][0] is not None for c in single)
    complete_multi = sum(
        all(rank is not None for rank in c["first_rank_per_group"])
        for c in multi
    )
    covered = sum(
        rank is not None
        for c in multi for rank in c["first_rank_per_group"]
    )
    required = sum(len(c["first_rank_per_group"]) for c in multi)
    control = next(c for c in report["cases"] if c["id"] == "N04")

    report["metrics"] = {
        "single_passage_hits_at_3": singles_hit,
        "single_passage_cases": len(single),
        "supporting_passage_hit_at_3": singles_hit / len(single),
        "mrr_at_3": sum(
            1 / c["first_rank_per_group"][0]
            if c["first_rank_per_group"][0] is not None else 0
            for c in single
        ) / len(single),
        "multi_complete_at_3": complete_multi,
        "multi_cases": len(multi),
        "complete_support_rate_at_3": complete_multi / len(multi),
        "multi_groups_covered_at_3": covered,
        "multi_groups_required": required,
        "micro_evidence_group_coverage_at_3": covered / required,
        "citations_checked": citation_count,
        "citation_reconstruction_failures": 0,
        "lexical_no_match_control_empty": not control["results"],
    }

    after = {str(p.relative_to(root)): digest(p.read_bytes()) for p in tracked}
    if before != after:
        raise RuntimeError("Benchmark inputs changed during execution")
    if control["results"]:
        raise RuntimeError("Lexical no-match control returned passages")

    report["execution_status"] = "COMPLETED"
    report["quality_gate"] = "NOT_DEFINED_BASELINE_ONLY"

parser = argparse.ArgumentParser()
parser.add_argument("--output-dir", required=True)
args = parser.parse_args()
out = Path(args.output_dir).expanduser().resolve()
root = Path(subprocess.check_output(
    ["git", "-C", str(PACKAGE), "rev-parse", "--show-toplevel"],
    text=True,
).strip()).resolve()
if out == root or root in out.parents:
    raise SystemExit("STOP: output directory must be outside the checkout")
out.mkdir(parents=True, exist_ok=True)
if any(out.iterdir()):
    raise SystemExit("STOP: output directory must be empty")

report = {"execution_status": "ERROR"}
exit_code = 0
try:
    main(out, report)
except Exception:
    report["execution_status"] = "ERROR"
    report["error"] = traceback.format_exc()
    exit_code = 1
finally:
    payload = json.dumps(report, indent=2, ensure_ascii=False) + chr(10)
    (out / "report.json").write_text(payload, encoding="utf-8")
    summary = [
        "EXECUTION_STATUS=" + report["execution_status"],
        "QUALITY_GATE=" + report.get("quality_gate", "NOT_EVALUATED"),
    ]
    for name, value in report.get("metrics", {}).items():
        summary.append(f"{name}={value}")
    for case in report.get("cases", []):
        ranks = case["first_rank_per_group"]
        summary.append(
            f"{case['id']} kind={case['kind']} group_ranks={ranks} returned={len(case['results'])}"
        )
    if "error" in report:
        summary.append(report["error"])
    text = chr(10).join(summary) + chr(10)
    (out / "summary.txt").write_text(text, encoding="utf-8")
    checksums = [
        digest(p.read_bytes()) + "  " + p.name
        for p in sorted(out.iterdir())
        if p.is_file() and p.name != "SHA256SUMS"
    ]
    (out / "SHA256SUMS").write_text(
        chr(10).join(checksums) + chr(10), encoding="utf-8"
    )
    print(text, end="")

raise SystemExit(exit_code)
