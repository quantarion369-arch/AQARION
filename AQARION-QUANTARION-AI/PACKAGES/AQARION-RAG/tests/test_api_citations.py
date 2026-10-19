"""HTTP compatibility and structured-citation contract tests."""

import json
import threading
from http.client import HTTPConnection
from http.server import HTTPServer
from urllib.parse import urlencode

import pytest

import api
import retrieve as retrieval


@pytest.fixture
def get_json(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    server = HTTPServer(("127.0.0.1", 0), api.Handler)
    thread = threading.Thread(
        target=lambda: server.serve_forever(poll_interval=0.01),
        daemon=True,
    )
    thread.start()

    def request(path):
        connection = HTTPConnection(
            "127.0.0.1", server.server_port, timeout=10
        )
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            status = response.status
            content_type = response.getheader("Content-Type")
            payload = json.loads(response.read())
            return status, content_type, payload
        finally:
            connection.close()

    try:
        yield request
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        assert not thread.is_alive(), "Test server failed to stop"


def test_legacy_search_response_is_unchanged(get_json):
    query = "evidence ledger"
    status, content_type, payload = get_json(
        "/api/search?" + urlencode({"q": query})
    )

    expected = [
        {"score": score, "doc": doc, "sha": sha, "passage": passage}
        for score, doc, sha, passage in retrieval.retrieve(query, top_k=3)
    ]

    assert status == 200
    assert content_type == "application/json"
    assert expected
    assert payload == {"query": query, "results": expected}


def test_cited_search_exposes_structured_records(get_json):
    query = "evidence ledger"
    status, content_type, payload = get_json(
        "/api/search/cited?" + urlencode({"q": query})
    )

    assert status == 200
    assert content_type == "application/json"

    expected = retrieval.retrieve_cited(query, top_k=3)
    assert expected
    assert payload == {"query": query, "results": expected}

    for item in payload["results"]:
        source = retrieval.load_at_sha(item["path"], item["commit_sha"])
        assert source[item["char_start"]:item["char_end"]] == item["passage"]


def test_cited_search_handles_missing_query(get_json):
    status, content_type, payload = get_json("/api/search/cited")

    assert status == 200
    assert content_type == "application/json"
    assert payload == {"query": "", "results": []}


def test_unknown_endpoint_remains_404(get_json):
    status, content_type, payload = get_json("/api/not-a-real-endpoint")

    assert status == 404
    assert content_type == "application/json"
    assert payload == {"error": "not found"}
