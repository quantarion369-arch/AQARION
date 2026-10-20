import copy
import math
import hashlib
import json
import subprocess
import sys
import traceback
from pathlib import Path

root = Path(sys.argv[1]).resolve()
review_path = Path(sys.argv[2]).resolve()
out = Path(__file__).resolve().parent
package = root / "AQARION-QUANTARION-AI/PACKAGES/AQARION-RAG"

STOP = frozenset(
    "a an the and or but as at by for from in into of on onto to with "
    "is am are was were be been being do does did "
    "how what which who whom whose when where why "
    "this that these those it its".split()
)

STOP = frozenset()

EXPECTED_REVIEW_HASH = (
    "431ceaef079b0f80e593e4ff3d34a6a6c7bf3f0c0c1654d68a9c77e5d02b4b71"
)
EXPECTED_COMMIT = "a77f3dcc46eb89150e3e617f6648c6a49e147fae"

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args])

def identity(item):
    return (
        item["path"], item["commit_sha"],
        item["char_start"], item["char_end"],
    )

def group_ranks(case, results):
    ranks = []
    for group in case["accepted_groups"]:
        accepted = {identity(item) for item in group}
        found = [
            item["rank"] for item in results
            if identity(item) in accepted
        ]
        ranks.append(min(found) if found else None)
    return ranks

def metrics(cases):
    singles = [c for c in cases if c["kind"] == "single"]
    multis = [c for c in cases if c["kind"] == "multi"]
    hits = sum(c["ranks"][0] is not None for c in singles)
    complete = sum(
        all(rank is not None for rank in c["ranks"])
        for c in multis
    )
    covered = sum(
        rank is not None for c in multis for rank in c["ranks"]
    )
    required = sum(len(c["ranks"]) for c in multis)
    return {
        "single_hits_at_3": hits,
        "single_cases": len(singles),
        "hit_at_3": hits / len(singles),
        "mrr_at_3": sum(
            1 / c["ranks"][0] if c["ranks"][0] is not None else 0
            for c in singles
        ) / len(singles),
        "multi_complete_at_3": complete,
        "multi_cases": len(multis),
        "multi_complete_rate": complete / len(multis),
        "multi_groups_covered": covered,
        "multi_groups_required": required,
        "multi_group_coverage": covered / required,
    }

report = {
    "execution_status": "ERROR",
    "experiment": "idf_weighted_overlap_v1",
    "stop_words": sorted(STOP),
    "quality_gate": "NOT_DEFINED_COMPARISON_ONLY",
    "cases": [],
}
exit_code = 0

try:
    raw = review_path.read_bytes()
    if sha(raw) != EXPECTED_REVIEW_HASH:
        raise RuntimeError("Reviewed-report checksum mismatch")
    reviewed = json.loads(raw)
    if reviewed.get("execution_status") != "COMPLETED":
        raise RuntimeError("Reviewed execution was not completed")
    if reviewed["tested_commit"] != EXPECTED_COMMIT:
        raise RuntimeError("Unexpected reviewed implementation revision")
    if git("rev-parse", "HEAD").decode().strip() != EXPECTED_COMMIT:
        raise RuntimeError("Checkout differs from reviewed revision")

    for args in (
        ("diff", "--quiet", "--"),
        ("diff", "--cached", "--quiet", "--"),
    ):
        subprocess.check_call(["git", "-C", str(root), *args])

    for relative, expected in reviewed["files"].items():
        if sha((root / relative).read_bytes()) != expected:
            raise RuntimeError("Reviewed input changed: " + relative)

    report["reviewed_report_sha256"] = sha(raw)
    report["tested_commit"] = EXPECTED_COMMIT
    report["experiment_script_sha256"] = sha(Path(__file__).read_bytes())
    report["input_hashes"] = dict(reviewed["files"])

    sys.path.insert(0, str(package))
    import retrieve

    manifest = retrieve.load_manifest()
    expected_sources = {
        (item["path"], item["commit_sha"]): item
        for item in reviewed["sources"].values()
    }
    actual_sources = [(item["path"], item["sha"]) for item in manifest]
    if (
        len(actual_sources) != len(expected_sources)
        or set(actual_sources) != set(expected_sources)
    ):
        raise RuntimeError("Manifest differs from reviewed corpus")

    texts = {}
    order = {}
    paragraph_limit = 0
    for index, entry in enumerate(manifest):
        source = (entry["path"], entry["sha"])
        text = retrieve.load_at_sha(*source)
        expected = expected_sources[source]
        if sha(text.encode("utf-8")) != expected["decoded_text_utf8_sha256"]:
            raise RuntimeError("Decoded source changed")
        if sha(git("show", source[1] + ":" + source[0])) != expected["git_blob_sha256"]:
            raise RuntimeError("Pinned source bytes changed")
        texts[source] = text
        order[source] = index
        paragraph_limit += len(text.split(retrieve.PARA_BREAK))

    frequencies = {}
    paragraph_count = 0
    for text in texts.values():
        for raw_paragraph in text.split(retrieve.PARA_BREAK):
            paragraph = raw_paragraph.strip()
            if not paragraph:
                continue
            paragraph_count += 1
            tokens = {
                retrieve.stem(word)
                for word in retrieve.WORD.findall(paragraph.lower())
            }
            for token in tokens:
                frequencies[token] = frequencies.get(token, 0) + 1

    weights = {
        token: math.log1p(
            (paragraph_count - count + 0.5) / (count + 0.5)
        )
        for token, count in frequencies.items()
    }
    report['idf_configuration'] = {
        'unit': 'nonempty original paragraph',
        'paragraph_count': paragraph_count,
        'formula': 'log(1 + (N - df + 0.5) / (df + 0.5))',
        'term_frequency_weighting': False,
        'length_normalization': False,
        'stopword_removal': False,
        'weights': weights,
        'document_frequencies': frequencies,
    }

    def filtered_tokens(text):
        return {
            retrieve.stem(word)
            for word in retrieve.WORD.findall(text.lower())
            if word not in STOP
        }

    baseline_cases = []
    candidate_cases = []
    candidate_citations = 0
    replayed = 0

    for case in reviewed["cases"]:
        pool = retrieve.retrieve_cited(
            case["query"], top_k=paragraph_limit
        )
        baseline_results = pool[:3]
        if baseline_results != case["results"]:
            raise RuntimeError("Baseline replay mismatch: " + case["id"])
        replayed += 1

        # Restore corpus order before applying the new stable score sort.
        # Otherwise old scores would become an unintended tie-breaker.
        pool.sort(key=lambda item: (
            order[(item["path"], item["commit_sha"])],
            item["char_start"],
        ))

        query_tokens = filtered_tokens(case["query"])
        candidate = []
        for original in pool:
            shared = query_tokens & filtered_tokens(original["passage"])
            score = math.fsum(
                weights[token] for token in sorted(shared)
            )
            if score:
                item = dict(original)
                item["score"] = score
                item.pop("rank", None)
                candidate.append(item)

        candidate.sort(key=lambda item: item["score"], reverse=True)
        candidate = candidate[:3]

        for rank, item in enumerate(candidate, 1):
            item["rank"] = rank
            text = texts[(item["path"], item["commit_sha"])]
            start, end = item["char_start"], item["char_end"]
            if not (0 <= start <= end <= len(text)):
                raise RuntimeError("Candidate citation bounds invalid")
            if text[start:end] != item["passage"]:
                raise RuntimeError("Candidate citation reconstruction failed")
            candidate_citations += 1

        before_ranks = group_ranks(case, baseline_results)
        after_ranks = group_ranks(case, candidate)
        if before_ranks != case["first_rank_per_group"]:
            raise RuntimeError("Reviewed-label scoring mismatch: " + case["id"])

        baseline_cases.append({
            "kind": case["kind"], "ranks": before_ranks,
        })
        candidate_cases.append({
            "kind": case["kind"], "ranks": after_ranks,
        })
        report["cases"].append({
            "id": case["id"],
            "kind": case["kind"],
            "query": case["query"],
            "accepted_groups": copy.deepcopy(case["accepted_groups"]),
            "baseline_group_ranks": before_ranks,
            "candidate_group_ranks": after_ranks,
            "filtered_query_tokens": sorted(query_tokens),
            "baseline_results": baseline_results,
            "candidate_results": candidate,
        })

    if replayed != 24:
        raise RuntimeError("Unexpected case count")

    control = next(c for c in report["cases"] if c["id"] == "N04")
    if control["candidate_results"]:
        raise RuntimeError("Lexical no-match control returned results")

    for relative, expected in reviewed["files"].items():
        if sha((root / relative).read_bytes()) != expected:
            raise RuntimeError("Input changed during execution: " + relative)

    for args in (
        ("diff", "--quiet", "--"),
        ("diff", "--cached", "--quiet", "--"),
    ):
        subprocess.check_call(["git", "-C", str(root), *args])

    report.update({
        "execution_status": "COMPLETED",
        "baseline_replay_cases_matched": replayed,
        "baseline_metrics": metrics(baseline_cases),
        "candidate_metrics": metrics(candidate_cases),
        "candidate_citations_checked": candidate_citations,
        "candidate_citation_failures": 0,
        "lexical_no_match_control_empty": True,
    })

except Exception:
    report["error"] = traceback.format_exc()
    exit_code = 1

finally:
    payload = json.dumps(report, indent=2, ensure_ascii=False) + chr(10)
    (out / "comparison.json").write_text(payload, encoding="utf-8")
    lines = [
        "EXECUTION_STATUS=" + report["execution_status"],
        "QUALITY_GATE=" + report["quality_gate"],
        "BASELINE_REPLAY_CASES_MATCHED=" + str(
            report.get("baseline_replay_cases_matched", 0)
        ),
    ]
    for name in ("baseline_metrics", "candidate_metrics"):
        lines.append(name.upper())
        for key, value in report.get(name, {}).items():
            lines.append(f"  {key}={value}")

    lines.append(
        "CANDIDATE_CITATIONS_CHECKED="
        + str(report.get("candidate_citations_checked", 0))
    )
    for case in report["cases"]:
        before = case["baseline_group_ranks"]
        after = case["candidate_group_ranks"]
        marker = "UNCHANGED" if before == after else "CHANGED"
        lines.append(
            f"{case['id']} {marker} ranks={before}->{after} "
            f"returned={len(case['baseline_results'])}"
            f"->{len(case['candidate_results'])}"
        )
    if "error" in report:
        lines.append(report["error"])

    summary = chr(10).join(lines) + chr(10)
    (out / "summary.txt").write_text(summary, encoding="utf-8")
    entries = [
        sha(path.read_bytes()) + "  " + path.name
        for path in sorted(out.iterdir())
        if path.is_file()
        and path.name in {"experiment.py", "comparison.json", "summary.txt"}
    ]
    (out / "SHA256SUMS").write_text(
        chr(10).join(entries) + chr(10), encoding="utf-8"
    )
    print(summary, end="")

raise SystemExit(exit_code)
