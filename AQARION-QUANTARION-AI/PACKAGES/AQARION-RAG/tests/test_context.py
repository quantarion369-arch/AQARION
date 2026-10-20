import copy
import hashlib
import json
from pathlib import Path

import pytest
import context

SEP = chr(10) * 2
ABC = SEP.join(["A", "B", "C"])


@pytest.fixture
def install(monkeypatch):
    def configure(texts, specifications):
        entries = [
            {"doc": path, "path": path, "sha": sha}
            for path, sha in texts
        ]
        seeds = []
        for rank, (path, sha, start, end) in enumerate(specifications, 1):
            seeds.append({
                "score": 1,
                "doc": path,
                "path": path,
                "commit_sha": sha,
                "char_start": start,
                "char_end": end,
                "passage": texts[(path, sha)][start:end],
                "rank": rank,
            })

        def search(query, top_k):
            assert top_k == 3
            return seeds

        monkeypatch.setattr(context.retrieve, "retrieve_cited", search)
        monkeypatch.setattr(context.retrieve, "load_manifest", lambda: entries)
        monkeypatch.setattr(
            context.retrieve,
            "load_at_sha",
            lambda path, sha: texts[(path, sha)],
        )
        return seeds
    return configure


def test_empty_results(install):
    install({}, [])
    result = context.retrieve_with_context("")
    assert result["seed_results"] == []
    assert result["supplementary_context"] == []
    assert result["expansion_metadata"]["support_adjudicated"] is False


@pytest.mark.parametrize("start", [0, 6])
def test_document_edges_and_nonrecursive_expansion(install, start):
    install({("p", "a"): ABC}, [("p", "a", start, start + 1)])
    result = context.retrieve_with_context("query")
    assert [
        item["passage"] for item in result["supplementary_context"]
    ] == ["B"]


def test_shared_neighbor_has_two_seed_links(install):
    install(
        {("p", "a"): ABC},
        [("p", "a", 0, 1), ("p", "a", 6, 7)],
    )
    extra = context.retrieve_with_context("query")["supplementary_context"]
    assert len(extra) == 1
    assert extra[0]["passage"] == "B"
    assert [link["seed_rank"] for link in extra[0]["seed_links"]] == [1, 2]


def test_seed_results_are_not_duplicated_as_context(install):
    install(
        {("p", "a"): ABC},
        [("p", "a", 0, 1), ("p", "a", 3, 4)],
    )
    extra = context.retrieve_with_context("query")["supplementary_context"]
    assert [item["passage"] for item in extra] == ["C"]


def test_repeated_text_keeps_distinct_seed_locations(install):
    install(
        {("p", "a"): SEP.join(["same", "middle", "same"])},
        [("p", "a", 0, 4), ("p", "a", 14, 18)],
    )
    result = context.retrieve_with_context("query")
    assert [
        item["char_start"] for item in result["seed_results"]
    ] == [0, 14]
    extra = result["supplementary_context"]
    assert len(extra) == 1
    assert (extra[0]["char_start"], extra[0]["char_end"]) == (6, 12)
    assert len(extra[0]["seed_links"]) == 2


@pytest.mark.parametrize("other_source", [("q", "a"), ("p", "b")])
def test_document_and_revision_isolation(install, other_source):
    texts = {
        ("p", "a"): SEP.join(["A", "B"]),
        other_source: SEP.join(["X", "Y"]),
    }
    install(
        texts,
        [("p", "a", 0, 1), (*other_source, 3, 4)],
    )
    extra = context.retrieve_with_context("query")["supplementary_context"]
    assert {
        (item["path"], item["commit_sha"], item["passage"])
        for item in extra
    } == {("p", "a", "B"), (*other_source, "X")}


def test_seed_records_are_not_modified(install):
    seeds = install(
        {("p", "a"): SEP.join(["A", "B"])},
        [("p", "a", 0, 1)],
    )
    original = copy.deepcopy(seeds)
    result = context.retrieve_with_context("query")
    assert seeds == original
    assert result["seed_results"] == original
    assert result["supplementary_context"][0]["context_only"] is True


def test_invalid_seed_span_is_rejected(install):
    install(
        {("p", "a"): SEP.join(["A", "B"])},
        [("p", "a", 1, 2)],
    )
    with pytest.raises(ValueError, match="exact source paragraph"):
        context.retrieve_with_context("query")


def test_six_supplement_cap(install):
    text = SEP.join("ABCDEFGHI")
    install(
        {("p", "a"): text},
        [("p", "a", 3, 4), ("p", "a", 12, 13), ("p", "a", 21, 22)],
    )
    result = context.retrieve_with_context("query")
    assert len(result["supplementary_context"]) == 6
    assert result["expansion_metadata"]["supplementary_characters"] == 6


RECEIPT_PATH = (
    Path(__file__).resolve().parents[1]
    / "benchmarks/evidence/2026-10-19/adjacency/comparison.json"
)
RECEIPT_BYTES = RECEIPT_PATH.read_bytes()
if hashlib.sha256(RECEIPT_BYTES).hexdigest() != (
    "0c3379229f006d8f7a517ca6125784546f486cb30e59b751ac967199b699116e"
):
    raise RuntimeError("Saved adjacency receipt checksum mismatch")

SAVED_CASES = json.loads(RECEIPT_BYTES)["cases"]
if len(SAVED_CASES) != 24:
    raise RuntimeError("Expected 24 saved adjacency cases")


@pytest.mark.parametrize("case", SAVED_CASES, ids=lambda case: case["id"])
def test_exact_saved_adjacency_replay(case):
    result = context.retrieve_with_context(case["query"])
    assert result["seed_results"] == case["seed_results"]
    assert result["supplementary_context"] == case["supplementary_context"]
    metadata = result["expansion_metadata"]
    assert metadata["seed_characters"] == case["seed_characters"]
    assert metadata["supplementary_characters"] == case["supplementary_characters"]
    assert metadata["supplementary_count"] <= 6
    assert metadata["support_adjudicated"] is False
