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
CAPS = (0, 500, 1000, 2000)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def identity(item):
    return (
        item["path"], item["commit_sha"],
        item["char_start"], item["char_end"],
    )

def coverage(groups, records):
    found = {identity(item) for item in records}
    return [
        any(identity(item) in found for item in group)
        for group in groups
    ]

def select(candidates, cap):
    accepted = []
    decisions = []
    used = 0
    for item in candidates:
        length = len(item["passage"])
        fits = length <= cap - used
        decisions.append({
            "citation": {
                key: item[key]
                for key in (
                    "path", "commit_sha", "char_start", "char_end"
                )
            },
            "characters": length,
            "remaining_before": cap - used,
            "accepted": fits,
        })
        if fits:
            accepted.append(item)
            used += length
    if used > cap:
        raise RuntimeError("Character cap exceeded")
    return accepted, decisions, used

def metrics(cases, method):
    singles = [case for case in cases if case["kind"] == "single"]
    multis = [case for case in cases if case["kind"] == "multi"]
    return {
        "single_supported": sum(case[method]["support"][0] for case in singles),
        "single_cases": len(singles),
        "multi_complete": sum(all(case[method]["support"]) for case in multis),
        "multi_cases": len(multis),
        "multi_groups_covered": sum(
            sum(case[method]["support"]) for case in multis
        ),
        "multi_groups_required": sum(
            len(case[method]["support"]) for case in multis
        ),
        "supplementary_passage_occurrences": sum(
            len(case[method]["accepted"]) for case in cases
        ),
        "supplementary_characters": sum(
            case[method]["characters"] for case in cases
        ),
        "unsupported_query_supplementary_characters": sum(
            case[method]["characters"]
            for case in cases if case["kind"] == "unsupported"
        ),
    }

report = {
    "execution_status": "ERROR",
    "experiment": "whole_passage_character_caps_v1",
    "caps": list(CAPS),
    "selection_rule": "accept whole passage if it fits; otherwise skip and continue",
    "seed_budget": "original top three retained separately, not charged to supplementary cap",
    "character_unit": "Python decoded-text length",
    "exact_consumption_matched": False,
    "quality_gate": "NOT_DEFINED_DEVELOPMENT_COMPARISON",
    "runs": [],
}
exit_code = 0

try:
    head = git("rev-parse", "HEAD").decode().strip()
    if head != "48fe8abc022ecfbfb0bfff6ed058fa7f59426eb6":
        raise RuntimeError("Unexpected implementation revision")

    adjacency_path = archive / "adjacency/comparison.json"
    review_path = archive / "label-review/reviewed-report.json"
    adjacency_raw = adjacency_path.read_bytes()
    review_raw = review_path.read_bytes()

    if sha(adjacency_raw) != "0c3379229f006d8f7a517ca6125784546f486cb30e59b751ac967199b699116e":
        raise RuntimeError("Saved adjacency checksum mismatch")
    if sha(review_raw) != "431ceaef079b0f80e593e4ff3d34a6a6c7bf3f0c0c1654d68a9c77e5d02b4b71":
        raise RuntimeError("Reviewed-label checksum mismatch")

    adjacency = json.loads(adjacency_raw)
    reviewed = json.loads(review_raw)
    if (
        adjacency["execution_status"] != "COMPLETED"
        or reviewed["execution_status"] != "COMPLETED"
    ):
        raise RuntimeError("Unexpected source receipt status")

    if sha((package / "context.py").read_bytes()) != (
        "7f3056a203acc9129c1718ecdefe1facefcefebe416f6cbb20c44b60770b1b46"
    ):
        raise RuntimeError("Context module differs from tested version")

    for name, expected in reviewed["files"].items():
        if name.endswith("/retrieve.py") or name.endswith("/corpus/MANIFEST.md"):
            if sha((root / name).read_bytes()) != expected:
                raise RuntimeError("Baseline retrieval input changed")

    inputs = [
        package / "context.py",
        package / "retrieve.py",
        package / "corpus/MANIFEST.md",
        adjacency_path,
        review_path,
        Path(__file__).resolve(),
    ]
    before = {str(path): sha(path.read_bytes()) for path in inputs}

    sys.path.insert(0, str(package))
    import context
    import retrieve

    expected_sources = {
        (item["path"], item["commit_sha"]): item
        for item in reviewed["sources"].values()
    }
    manifest = retrieve.load_manifest()
    actual = [(entry["path"], entry["sha"]) for entry in manifest]
    if len(actual) != len(expected_sources) or set(actual) != set(expected_sources):
        raise RuntimeError("Unexpected corpus")

    texts = {}
    paragraph_limit = 0
    for source, expected in expected_sources.items():
        text = retrieve.load_at_sha(*source)
        if sha(text.encode("utf-8")) != expected["decoded_text_utf8_sha256"]:
            raise RuntimeError("Decoded source checksum mismatch")
        if sha(git("show", source[1] + ":" + source[0])) != expected["git_blob_sha256"]:
            raise RuntimeError("Pinned source byte checksum mismatch")
        texts[source] = text
        paragraph_limit += len(text.split(retrieve.PARA_BREAK))

    def verify(records):
        if len({identity(item) for item in records}) != len(records):
            raise RuntimeError("Duplicate result citation")
        for item in records:
            text = texts[(item["path"], item["commit_sha"])]
            start, end = item["char_start"], item["char_end"]
            if not 0 <= start <= end <= len(text):
                raise RuntimeError("Invalid citation bounds")
            if text[start:end] != item["passage"]:
                raise RuntimeError("Citation reconstruction failed")

    references = {case["id"]: case for case in reviewed["cases"]}
    saved_cases = adjacency["cases"]
    if (
        len(references) != 24
        or len(saved_cases) != 24
        or {case["id"] for case in saved_cases} != set(references)
    ):
        raise RuntimeError("Unexpected case inventory")

    prepared = []
    for saved in saved_cases:
        reference = references[saved["id"]]
        if (
            saved["query"] != reference["query"]
            or saved["accepted_groups"] != reference["accepted_groups"]
        ):
            raise RuntimeError("Reviewed case mismatch")

        result = context.retrieve_with_context(saved["query"])
        seeds = result["seed_results"]
        neighbors = result["supplementary_context"]
        if (
            seeds != saved["seed_results"]
            or seeds != reference["results"]
            or neighbors != saved["supplementary_context"]
        ):
            raise RuntimeError("Maintained context replay mismatch")

        ranked = retrieve.retrieve_cited(
            saved["query"], top_k=paragraph_limit
        )
        if ranked[:len(seeds)] != seeds:
            raise RuntimeError("Ranked seed replay mismatch")

        seed_ids = {identity(item) for item in seeds}
        deeper = [
            item for item in ranked if identity(item) not in seed_ids
        ]
        verify(seeds)
        verify(neighbors)
        verify(deeper)

        prepared.append((saved, seeds, neighbors, deeper))

    for cap in CAPS:
        cases = []
        for saved, seeds, neighbors, deeper in prepared:
            case = {
                "id": saved["id"],
                "kind": saved["kind"],
                "query": saved["query"],
                "accepted_groups": saved["accepted_groups"],
                "seed_results": seeds,
                "seed_support": coverage(saved["accepted_groups"], seeds),
                "seed_characters": sum(len(item["passage"]) for item in seeds),
            }
            for method, pool in (
                ("adjacency", neighbors), ("deeper", deeper)
            ):
                accepted, decisions, used = select(pool, cap)
                verify(seeds + accepted)
                case[method] = {
                    "accepted": accepted,
                    "decisions": decisions,
                    "characters": used,
                    "unused_allowance": cap - used,
                    "support": coverage(
                        saved["accepted_groups"], seeds + accepted
                    ),
                }

            if cap == 0 and (
                case["adjacency"]["accepted"] or case["deeper"]["accepted"]
            ):
                raise RuntimeError("Zero-cap control added passages")
            cases.append(case)

        report["runs"].append({
            "cap_per_query": cap,
            "adjacency_metrics": metrics(cases, "adjacency"),
            "deeper_metrics": metrics(cases, "deeper"),
            "cases": cases,
        })

    if before != {str(path): sha(path.read_bytes()) for path in inputs}:
        raise RuntimeError("Input changed during execution")

    report.update({
        "execution_status": "COMPLETED",
        "tested_commit": head,
        "context_replay_cases_matched": len(prepared),
        "input_hashes": before,
        "citation_reconstruction_failures": 0,
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
        "CONTEXT_REPLAY_CASES_MATCHED=" + str(
            report.get("context_replay_cases_matched", 0)
        ),
        "EXACT_CONSUMPTION_MATCHED=False",
    ]
    for run in report["runs"]:
        lines.append("SUPPLEMENTARY_CAP=" + str(run["cap_per_query"]))
        for method in ("adjacency", "deeper"):
            lines.append(
                method.upper() + " "
                + json.dumps(run[method + "_metrics"], sort_keys=True)
            )
        for case in run["cases"]:
            if case["kind"] == "multi" or (
                case["kind"] == "single" and not all(case["seed_support"])
            ):
                lines.append(
                    f"{case['id']} seed={case['seed_support']} "
                    f"adj={case['adjacency']['support']} "
                    f"deep={case['deeper']['support']} "
                    f"extra_chars={case['adjacency']['characters']}"
                    f"/{case['deeper']['characters']}"
                )
    if "error" in report:
        lines.append(report["error"])

    summary = chr(10).join(lines) + chr(10)
    (out / "summary.txt").write_text(summary, encoding="utf-8")
    entries = [
        sha(path.read_bytes()) + "  " + path.name
        for path in sorted(out.iterdir())
        if path.name in {"experiment.py", "comparison.json", "summary.txt"}
    ]
    (out / "SHA256SUMS").write_text(
        chr(10).join(entries) + chr(10), encoding="utf-8"
    )
    print(summary, end="")

raise SystemExit(exit_code)
