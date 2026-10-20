import json
import threading
from http.server import HTTPServer
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pytest

import api
import context
import relationships


@pytest.fixture
def evidence_get():
    server = HTTPServer(("127.0.0.1", 0), api.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = "http://127.0.0.1:" + str(server.server_port)

    def get(route):
        with urlopen(base + route, timeout=30) as response:
            return response.status, json.loads(response.read())

    try:
        yield get
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_enriched_endpoint_preserves_context_and_exposes_correction(evidence_get):
    query = "ALL VERIFIED — three independent checks, all clean."
    expected = context.retrieve_with_context(query)
    status, data = evidence_get(
        "/api/search/evidence?" + urlencode({"q": query})
    )
    assert status == 200
    assert data["retrieval_context"] == expected
    assert data["relationship_diagnostics"] == []
    assert len(data["related_evidence"]) == 1
    item = data["related_evidence"][0]
    assert item["review_status"] == "pending"
    assert item["locator_validation"] == "passed"
    assert item["subject"]["char_start"] == 2912
    assert item["subject"]["char_end"] == 3268
    for citation in (
        item["subject"], item["object"],
        item["supporting_evidence"][0]["citation"],
    ):
        assert relationships.validate_anchor(citation) == citation


def test_original_context_endpoint_has_no_enrichment_wrapper(evidence_get):
    query = "ALL VERIFIED — three independent checks, all clean."
    status, data = evidence_get(
        "/api/search/context?" + urlencode({"q": query})
    )
    assert status == 200
    assert data == context.retrieve_with_context(query)
    assert "related_evidence" not in data
    assert "retrieval_context" not in data


def test_invalid_relation_is_diagnostic_not_valid_evidence(evidence_get, monkeypatch):
    records = relationships.load_relationships()
    records[0]["subject"]["passage_sha256"] = "0" * 64
    monkeypatch.setattr(relationships, "load_relationships", lambda: records)
    status, data = evidence_get("/api/search/evidence?q=independent")
    assert status == 200
    assert "seed_results" in data["retrieval_context"]
    assert data["related_evidence"] == []
    assert len(data["relationship_diagnostics"]) == 1


def test_empty_enriched_query_preserves_existing_empty_context(evidence_get):
    status, data = evidence_get("/api/search/evidence")
    assert status == 200
    assert data["retrieval_context"] == context.retrieve_with_context("")
    assert data["related_evidence"] == []
    assert data["relationship_diagnostics"] == []


def test_enriched_page_uses_safe_text_and_explicit_review_labels():
    page = (
        Path(api.__file__).resolve().parent / "static" / "index.html"
    ).read_text(encoding="utf-8")
    for sink in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write"):
        assert sink not in page
    for text in (
        "/api/search/evidence",
        "Documented correction - review pending.",
        "Reported follow-up - not executed by this search",
        "No validated registry links matched",
        "This does not establish that no correction exists.",
    ):
        assert text in page
