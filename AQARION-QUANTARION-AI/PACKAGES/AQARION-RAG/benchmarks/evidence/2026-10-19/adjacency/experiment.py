import hashlib
import json
import subprocess
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
package = root / "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"
review_path = (
    package / "benchmarks/evidence/2026-10-19"
    / "label-review/reviewed-report.json"
)
expected_commit = "482af5384b280c647f976aa89602c0d99411d56d"
expected_review = "431ceaef079b0f80e593e4ff3d34a6a6c7bf3f0c0c1654d68a9c77e5d02b4b71"

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
        any(identity(item) in found for item in alternatives)
        for alternatives in groups
    ]

def metrics(cases, field):
    single = [case for case in cases if case["kind"] == "single"]
    multi = [case for case in cases if case["kind"] == "multi"]
    return {
        "single_supported": sum(case[field][0] for case in single),
        "single_cases": len(single),
        "multi_complete": sum(all(case[field]) for case in multi),
        "multi_cases": len(multi),
        "multi_groups_covered": sum(
            sum(case[field]) for case in multi
        ),
        "multi_groups_required": sum(
            len(case[field]) for case in multi
        ),
    }

report = {
    "execution_status": "ERROR",
    "experiment": "immediate_paragraph_neighbors_v1",
    "rule": {
        "seed_top_k": 3,
        "previous_nonempty_paragraphs": 1,
        "following_nonempty_paragraphs": 1,
        "recursive": False,
        "maximum_supplements_per_query": 6,
        "same_pinned_document_only": True,
    },
    "quality_gate": "NOT_DEFINED_DEVELOPMENT_EXPERIMENT",
    "cases": [],
}
exit_code = 0

try:
    if git("rev-parse", "HEAD").decode().strip() != expected_commit:
        raise RuntimeError("Unexpected repository revision")

    raw = review_path.read_bytes()
    if sha(raw) != expected_review:
        raise RuntimeError("Reviewed-report checksum mismatch")
    reviewed = json.loads(raw)
    if reviewed["execution_status"] != "COMPLETED":
        raise RuntimeError("Reviewed baseline did not complete")

    inputs = [
        package / "retrieve.py",
        package / "corpus/MANIFEST.md",
        package / "benchmarks/cases.json",
        review_path,
        Path(__file__).resolve(),
    ]
    before = {str(path): sha(path.read_bytes()) for path in inputs}

    for name, expected in reviewed["files"].items():
        if name.endswith("/retrieve.py") or name.endswith("/corpus/MANIFEST.md"):
            if sha((root / name).read_bytes()) != expected:
                raise RuntimeError("Baseline production input changed")

    labels = json.loads(
        (package / "benchmarks/cases.json").read_text(encoding="utf-8")
    )
    if labels["reviewed_report_sha256"] != expected_review:
        raise RuntimeError("Unexpected label provenance")

    sys.path.insert(0, str(package))
    import retrieve

    manifest = retrieve.load_manifest()
    expected_sources = {
        (item["path"], item["commit_sha"]): item
        for item in reviewed["sources"].values()
    }
    actual = [(item["path"], item["sha"]) for item in manifest]
    if len(actual) != len(expected_sources) or set(actual) != set(expected_sources):
        raise RuntimeError("Corpus differs from reviewed baseline")

    texts = {}
    paragraphs = {}
    positions = {}

    for entry in manifest:
        source = (entry["path"], entry["sha"])
        text = retrieve.load_at_sha(*source)
        reference = expected_sources[source]
        if sha(text.encode("utf-8")) != reference["decoded_text_utf8_sha256"]:
            raise RuntimeError("Decoded source checksum mismatch")
        if sha(git("show", source[1] + ":" + source[0])) != reference["git_blob_sha256"]:
            raise RuntimeError("Pinned source byte checksum mismatch")
        texts[source] = text
        records = []
        offset = 0

        for raw_paragraph in text.split(retrieve.PARA_BREAK):
            passage = raw_paragraph.strip()
            start = offset + len(raw_paragraph) - len(raw_paragraph.lstrip())
            if passage:
                record = {
                    "doc": entry["doc"],
                    "path": source[0],
                    "commit_sha": source[1],
                    "char_start": start,
                    "char_end": start + len(passage),
                    "passage": passage,
                }
                positions[identity(record)] = len(records)
                records.append(record)
            offset += len(raw_paragraph) + len(retrieve.PARA_BREAK)
        paragraphs[source] = records

    def check_citation(item):
        text = texts[(item["path"], item["commit_sha"])]
        start, end = item["char_start"], item["char_end"]
        if not (0 <= start <= end <= len(text)):
            raise RuntimeError("Invalid citation bounds")
        if text[start:end] != item["passage"]:
            raise RuntimeError("Citation reconstruction failed")

    replayed = 0
    seed_citations = 0
    supplement_citations = 0

    for case in reviewed["cases"]:
        seeds = retrieve.retrieve_cited(case["query"], top_k=3)
        if seeds != case["results"]:
            raise RuntimeError("Baseline replay mismatch: " + case["id"])
        replayed += 1

        seed_ids = {identity(item) for item in seeds}
        supplements = {}

        for seed in seeds:
            check_citation(seed)
            seed_citations += 1
            source = (seed["path"], seed["commit_sha"])
            records = paragraphs[source]
            index = positions[identity(seed)]

            for delta, direction in ((-1, "previous"), (1, "following")):
                neighbor_index = index + delta
                if not 0 <= neighbor_index < len(records):
                    continue
                neighbor = records[neighbor_index]
                key = identity(neighbor)
                if key in seed_ids:
                    continue
                if key not in supplements:
                    supplements[key] = {
                        **neighbor,
                        "context_only": True,
                        "seed_links": [],
                    }
                supplements[key]["seed_links"].append({
                    "seed_rank": seed["rank"],
                    "seed_char_start": seed["char_start"],
                    "seed_char_end": seed["char_end"],
                    "direction": direction,
                })

        extra = list(supplements.values())
        if len(extra) > 6:
            raise RuntimeError("Supplement budget exceeded")
        for item in extra:
            check_citation(item)
            supplement_citations += 1

        for group in case["accepted_groups"]:
            for item in group:
                check_citation(item)

        seed_support = coverage(case["accepted_groups"], seeds)
        expanded_support = coverage(case["accepted_groups"], seeds + extra)
        expected_support = [
            rank is not None for rank in case["first_rank_per_group"]
        ]
        if seed_support != expected_support:
            raise RuntimeError("Reviewed-label baseline mismatch")

        report["cases"].append({
            "id": case["id"],
            "kind": case["kind"],
            "query": case["query"],
            "accepted_groups": case["accepted_groups"],
            "seed_results": seeds,
            "supplementary_context": extra,
            "seed_support": seed_support,
            "expanded_support": expanded_support,
            "seed_characters": sum(len(item["passage"]) for item in seeds),
            "supplementary_characters": sum(
                len(item["passage"]) for item in extra
            ),
        })

    if replayed != 24:
        raise RuntimeError("Unexpected case count")
    control = next(case for case in report["cases"] if case["id"] == "N04")
    if control["seed_results"] or control["supplementary_context"]:
        raise RuntimeError("No-match control unexpectedly returned evidence")

    after = {str(path): sha(path.read_bytes()) for path in inputs}
    if before != after:
        raise RuntimeError("Experiment input changed during execution")

    report.update({
        "execution_status": "COMPLETED",
        "tested_commit": expected_commit,
        "reviewed_report_sha256": expected_review,
        "input_hashes": before,
        "baseline_replay_cases_matched": replayed,
        "seed_metrics": metrics(report["cases"], "seed_support"),
        "expanded_metrics": metrics(report["cases"], "expanded_support"),
        "seed_citations_checked": seed_citations,
        "supplement_citations_checked": supplement_citations,
        "citation_reconstruction_failures": 0,
        "budget": {
            "total_seed_passages": sum(
                len(case["seed_results"]) for case in report["cases"]
            ),
            "total_supplementary_passages": sum(
                len(case["supplementary_context"]) for case in report["cases"]
            ),
            "maximum_supplements_for_one_query": max(
                len(case["supplementary_context"]) for case in report["cases"]
            ),
            "total_seed_characters": sum(
                case["seed_characters"] for case in report["cases"]
            ),
            "total_supplementary_characters": sum(
                case["supplementary_characters"] for case in report["cases"]
            ),
        },
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
        "BASELINE_REPLAY_CASES_MATCHED=" + str(
            report.get("baseline_replay_cases_matched", 0)
        ),
    ]
    for section in ("seed_metrics", "expanded_metrics", "budget"):
        lines.append(section.upper())
        for key, value in report.get(section, {}).items():
            lines.append(f"  {key}={value}")

    for case in report["cases"]:
        lines.append(
            f"{case['id']} support={case['seed_support']}"
            f"->{case['expanded_support']} "
            f"seeds={len(case['seed_results'])} "
            f"extras={len(case['supplementary_context'])} "
            f"extra_chars={case['supplementary_characters']}"
        )
    lines.append(
        "CITATION_FAILURES="
        + str(report.get("citation_reconstruction_failures", "NOT_COMPLETED"))
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
