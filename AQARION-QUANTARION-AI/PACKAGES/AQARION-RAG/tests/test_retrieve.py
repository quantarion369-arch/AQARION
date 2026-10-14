from retrieve import load_manifest, retrieve

def test_manifest_loads():
    rows = load_manifest()
    assert len(rows) >= 1
    assert all(set(r) == {"doc", "path", "sha", "purpose"} for r in rows)

def test_retrieve_returns_cited_results():
    results = retrieve("evidence ledger")
    assert len(results) > 0
    for score, doc, sha, passage in results:
        assert sha, "every result must carry a pinned SHA"
        assert passage, "every result must carry a passage"
