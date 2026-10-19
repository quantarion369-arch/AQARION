"""Contract tests for reconstructible, source-bound passage citations."""

import subprocess
from pathlib import Path

import retrieve as retrieval


def test_real_citations_reconstruct_from_pinned_sources():
    rows = retrieval.load_manifest()
    identities = {
        (row["doc"], row["path"], row["sha"])
        for row in rows
    }
    package = Path(retrieval.__file__).resolve().parent

    results = retrieval.retrieve_cited("evidence ledger")
    assert results

    required = {
        "score", "rank", "doc", "path", "commit_sha",
        "passage", "char_start", "char_end",
    }

    for result in results:
        assert required <= result.keys()
        identity = (result["doc"], result["path"], result["commit_sha"])
        assert identity in identities

        source = subprocess.check_output(
            [
                "git", "-C", str(package), "show",
                f"{result['commit_sha']}:{result['path']}",
            ],
            text=True,
        )

        start = result["char_start"]
        end = result["char_end"]

        assert type(start) is int
        assert type(end) is int
        assert 0 <= start < end <= len(source)
        assert source[start:end] == result["passage"]


def test_repeated_paragraphs_have_distinct_exact_locations(monkeypatch):
    separator = chr(10) * 2
    text = "  alpha proof  " + separator + "alpha proof"
    row = {
        "doc": "Repeated passage fixture",
        "path": "fixture.md",
        "sha": "a" * 40,
        "purpose": "citation span regression",
    }

    monkeypatch.setattr(retrieval, "load_manifest", lambda: [row])
    monkeypatch.setattr(
        retrieval, "load_at_sha", lambda path, sha: text
    )

    results = retrieval.retrieve_cited("alpha", top_k=10)

    assert len(results) == 2
    assert [item["passage"] for item in results] == [
        "alpha proof", "alpha proof"
    ]

    starts = [item["char_start"] for item in results]
    assert starts == [2, text.rindex("alpha proof")]
    assert starts[0] != starts[1]

    for item in results:
        assert item["path"] == row["path"]
        assert item["commit_sha"] == row["sha"]
        assert item["char_end"] == item["char_start"] + len(item["passage"])
        assert text[item["char_start"]:item["char_end"]] == item["passage"]


def test_legacy_ranking_ties_and_limits_are_preserved(monkeypatch):
    separator = chr(10) * 2
    sha_a = "a" * 40
    sha_b = "b" * 40
    rows = [
        {"doc": "A", "path": "a.md", "sha": sha_a, "purpose": "fixture"},
        {"doc": "B", "path": "b.md", "sha": sha_b, "purpose": "fixture"},
    ]
    texts = {
        ("a.md", sha_a): "alpha beta" + separator + "alpha",
        ("b.md", sha_b): "alpha beta",
    }

    monkeypatch.setattr(retrieval, "load_manifest", lambda: rows)
    monkeypatch.setattr(
        retrieval, "load_at_sha",
        lambda path, sha: texts[(path, sha)],
    )

    expected = [
        (2, "A", sha_a, "alpha beta"),
        (2, "B", sha_b, "alpha beta"),
        (1, "A", sha_a, "alpha"),
    ]

    for limit in (0, 1, 2, 3, 10):
        cited = retrieval.retrieve_cited("alpha beta", top_k=limit)
        projected = [
            (item["score"], item["doc"], item["commit_sha"], item["passage"])
            for item in cited
        ]

        assert [item["rank"] for item in cited] == list(range(1, len(cited) + 1))
        assert projected == expected[:limit]
        assert retrieval.retrieve("alpha beta", top_k=limit) == expected[:limit]
