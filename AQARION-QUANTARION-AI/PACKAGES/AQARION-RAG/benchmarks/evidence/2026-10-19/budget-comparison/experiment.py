import hashlib
import json
import subprocess
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
package = root / "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"
archive = package / "benchmarks/evidence/2026-10-19"
adjacency_path = archive / "adjacency/comparison.json"
review_path = archive / "label-review/reviewed-report.json"

EXPECTED_HEAD = "8a737b5658ad858275103e0c1f6b18d512a910a4"
EXPECTED_ADJACENCY = "0c3379229f006d8f7a517ca6125784546f486cb30e59b751ac967199b699116e"
EXPECTED_REVIEW = "431ceaef079b0f80e593e4ff3d34a6a6c7bf3f0c0c1654d68a9c77e5d02b4b71"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def identity(item):
    return (
        item["path"], item["commit_sha"],
        item["char_start"], item["char_end"],
    )

def support(groups, records):
    found = {identity(item) for item in records}
    return [
        any(identity(item) in found for item in group)
        for group in groups
    ]

def metrics(cases, method):
    singles = [case for case in cases if case["kind"] == "single"]
    multis = [case for case in cases if case["kind"] == "multi"]
    return {
        "single_supported": sum(case[method][0] for case in singles),
        "single_cases": len(singles),
        "multi_complete": sum(all(case[method]) for case in multis),
        "multi_cases": len(multis),
        "multi_groups_covered": sum(sum(case[method]) for case in multis),
        "multi_groups_required": sum(len(case[method]) for case in multis),
    }

report = {
    "execution_status": "ERROR",
    "experiment": "adjacency_vs_deeper_retrieval_v1",
    "budget_policy": "Per-query passage allowance equals saved seeds plus supplements.",
    "character_budget_matched": False,
    "quality_gate": "NOT_DEFINED_DEVELOPMENT_COMPARISON",
    "cases": [],
}
exit_code = 0

try:
    head = git("rev-parse", "HEAD").decode().strip()
    if head != EXPECTED_HEAD:
        raise RuntimeError("Unexpected checkout revision")

    adjacency_raw = adjacency_path.read_bytes()
    review_raw = review_path.read_bytes()
    if sha(adjacency_raw) != EXPECTED_ADJACENCY:
        raise RuntimeError("Published adjacency-report checksum mismatch")
    if sha(review_raw) != EXPECTED_REVIEW:
        raise RuntimeError("Reviewed-report checksum mismatch")

    adjacency = json.loads(adjacency_raw)
    reviewed = json.loads(review_raw)
    if (
        adjacency["execution_status"] != "COMPLETED"
        or adjacency["baseline_replay_cases_matched"] != 24
        or reviewed["execution_status"] != "COMPLETED"
    ):
        raise RuntimeError("Unexpected source execution status")

    inputs = [
        package / "retrieve.py",
        package / "corpus/MANIFEST.md",
        adjacency_path,
        review_path,
        Path(__file__).resolve(),
    ]
    before = {str(path): sha(path.read_bytes()) for path in inputs}

    for name, expected in reviewed["files"].items():
        if name.endswith("/retrieve.py") or name.endswith("/corpus/MANIFEST.md"):
            if sha((root / name).read_bytes()) != expected:
                raise RuntimeError("Baseline production input changed")

    sys.path.insert(0, str(package))
    import retrieve

    expected_sources = {
        (item["path"], item["commit_sha"]): item
        for item in reviewed["sources"].values()
    }
    manifest = retrieve.load_manifest()
    actual = [(entry["path"], entry["sha"]) for entry in manifest]
    if len(actual) != len(expected_sources) or set(actual) != set(expected_sources):
        raise RuntimeError("Corpus differs from the reviewed corpus")

    texts = {}
    for source, expected in expected_sources.items():
        text = retrieve.load_at_sha(*source)
        if sha(text.encode("utf-8")) != expected["decoded_text_utf8_sha256"]:
            raise RuntimeError("Decoded source checksum mismatch")
        if sha(git("show", source[1] + ":" + source[0])) != expected["git_blob_sha256"]:
            raise RuntimeError("Pinned source byte checksum mismatch")
        texts[source] = text

    def verify(records):
        ids = [identity(item) for item in records]
        if len(ids) != len(set(ids)):
            raise RuntimeError("Duplicate citation in a result collection")
        for item in records:
            text = texts[(item["path"], item["commit_sha"])]
            start, end = item["char_start"], item["char_end"]
            if not (0 <= start <= end <= len(text)):
                raise RuntimeError("Invalid citation bounds")
            if text[start:end] != item["passage"]:
                raise RuntimeError("Citation reconstruction failed")

    reference_cases = {case["id"]: case for case in reviewed["cases"]}
    cases = adjacency["cases"]
    if (
        len(cases) != 24
        or len(reference_cases) != 24
        or len({case["id"] for case in cases}) != 24
        or {case["id"] for case in cases} != set(reference_cases)
    ):
        raise RuntimeError("Unexpected case inventory")

    for saved in cases:
        reference = reference_cases[saved["id"]]
        if (
            saved["query"] != reference["query"]
            or saved["kind"] != reference["kind"]
            or saved["accepted_groups"] != reference["accepted_groups"]
        ):
            raise RuntimeError("Case or label mismatch")

        seeds = saved["seed_results"]
        expanded = seeds + saved["supplementary_context"]
        allowance = len(expanded)

        deeper = retrieve.retrieve_cited(
            saved["query"], top_k=allowance
        )
        if deeper[:len(seeds)] != seeds or seeds != reference["results"]:
            raise RuntimeError("Original seed replay mismatch: " + saved["id"])
        if len(deeper) > allowance:
            raise RuntimeError("Deeper retrieval exceeded allowance")

        verify(seeds)
        verify(expanded)
        verify(deeper)

        for rank, item in enumerate(deeper, 1):
            if item["rank"] != rank:
                raise RuntimeError("Invalid deeper-retrieval rank")

        groups = saved["accepted_groups"]
        seed_support = support(groups, seeds)
        adjacency_support = support(groups, expanded)
        deeper_support = support(groups, deeper)

        if (
            seed_support != saved["seed_support"]
            or adjacency_support != saved["expanded_support"]
        ):
            raise RuntimeError("Saved support receipt does not reproduce")

        report["cases"].append({
            "id": saved["id"],
            "kind": saved["kind"],
            "query": saved["query"],
            "accepted_groups": groups,
            "seed_support": seed_support,
            "adjacency_support": adjacency_support,
            "deeper_support": deeper_support,
            "passage_allowance": allowance,
            "deeper_shortfall": allowance - len(deeper),
            "seed_count": len(seeds),
            "adjacency_count": len(expanded),
            "deeper_count": len(deeper),
            "seed_characters": sum(len(item["passage"]) for item in seeds),
            "adjacency_characters": sum(len(item["passage"]) for item in expanded),
            "deeper_characters": sum(len(item["passage"]) for item in deeper),
            "deeper_results": deeper,
        })

    after = {str(path): sha(path.read_bytes()) for path in inputs}
    if before != after:
        raise RuntimeError("Experiment input changed during execution")

    report.update({
        "execution_status": "COMPLETED",
        "tested_commit": head,
        "seed_replay_cases_matched": len(report["cases"]),
        "input_hashes": before,
        "citation_reconstruction_failures": 0,
        "seed_metrics": metrics(report["cases"], "seed_support"),
        "adjacency_metrics": metrics(report["cases"], "adjacency_support"),
        "deeper_metrics": metrics(report["cases"], "deeper_support"),
        "budgets": {
            method: {
                "total_passage_occurrences": sum(
                    case[method + "_count"] for case in report["cases"]
                ),
                "total_characters": sum(
                    case[method + "_characters"] for case in report["cases"]
                ),
            }
            for method in ("seed", "adjacency", "deeper")
        },
        "queries_with_deeper_shortfall": sum(
            case["deeper_shortfall"] > 0 for case in report["cases"]
        ),
    })

except Exception:
    report["error"] = traceback.format_exc()
    exit_code = 1

finally:
    (out / "comparison.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + chr(10),
        encoding="utf-8",
    )
    lines = [
        "EXECUTION_STATUS=" + report["execution_status"],
        "QUALITY_GATE=" + report["quality_gate"],
        "SEED_REPLAY_CASES_MATCHED=" + str(
            report.get("seed_replay_cases_matched", 0)
        ),
        "CHARACTER_BUDGET_MATCHED=False",
    ]
    for name in ("seed_metrics", "adjacency_metrics", "deeper_metrics", "budgets"):
        lines.append(name.upper())
        lines.append(json.dumps(report.get(name, {}), sort_keys=True))
    lines.append(
        "QUERIES_WITH_DEEPER_SHORTFALL="
        + str(report.get("queries_with_deeper_shortfall", "NOT_COMPLETED"))
    )
    for case in report["cases"]:
        lines.append(
            f"{case['id']} seed={case['seed_support']} "
            f"adjacent={case['adjacency_support']} "
            f"deeper={case['deeper_support']} "
            f"allowance={case['passage_allowance']} "
            f"shortfall={case['deeper_shortfall']} "
            f"chars(adj/deep)={case['adjacency_characters']}"
            f"/{case['deeper_characters']}"
        )
    if "error" in report:
        lines.append(report["error"])

    summary = chr(10).join(lines) + chr(10)
    (out / "summary.txt").write_text(summary, encoding="utf-8")
    checksums = [
        sha(path.read_bytes()) + "  " + path.name
        for path in sorted(out.iterdir())
        if path.name in {"experiment.py", "comparison.json", "summary.txt"}
    ]
    (out / "SHA256SUMS").write_text(
        chr(10).join(checksums) + chr(10), encoding="utf-8"
    )
    print(summary, end="")

raise SystemExit(exit_code)
