"""Integration checks for the pinned DEFECT preservation source."""
import json
import threading
from http.server import ThreadingHTTPServer
from unittest import mock
from urllib.parse import urlencode
from urllib.request import urlopen

import api
import context
import retrieve

PIN = "579ba9453b6ceb803492944f0228008e4b0989a4"
PATH = (
    "AQARION-QUANTARION-AI/research/"
    "AQARION_DEFECT_Lab/PRESERVATION_RECORD.md"
)
SID = PATH + "@" + PIN
LABEL = "AQARION DEFECT experiment preservation"


def test_defect_source_scope_and_original_citations():
    entry = retrieve.resolve_source_id(SID)
    assert entry["doc"] == LABEL
    assert entry["path"] == PATH
    assert entry["sha"] == PIN

    original = retrieve.load_at_sha(PATH, PIN)
    normalized = " ".join(original.split())
    assert "independent reproduction remain unestablished" in normalized
    assert "not production deployment" in normalized

    loader = retrieve.load_at_sha
    with mock.patch.object(retrieve, "load_at_sha", wraps=loader) as spy:
        bundle = context.retrieve_with_context(
            "reconstruction generalization",
            source_id=SID,
        )
        assert bundle["seed_results"]
        for item in (
            bundle["seed_results"] + bundle["supplementary_context"]
        ):
            assert item["path"] == PATH
            assert item["commit_sha"] == PIN
            assert item["doc"] == LABEL
            assert item["passage"] == original[
                item["char_start"]:item["char_end"]
            ]

        assert all(
            call.args == (PATH, PIN)
            for call in spy.call_args_list
        )

    seeds = "\n".join(
        item["passage"] for item in bundle["seed_results"]
    )
    assert "Reconstruction benefit is inconsistent." in seeds
    assert "Generalization" in seeds


def test_defect_source_real_http_listing_and_complete_view():
    server = ThreadingHTTPServer(("127.0.0.1", 0), api.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"

    try:
        with urlopen(base + "/api/sources", timeout=10) as response:
            listing = json.load(response)

        matches = [
            item for item in listing["sources"]
            if item["source_id"] == SID
        ]
        assert len(matches) == 1
        assert matches[0]["doc"] == LABEL

        url = base + "/api/sources/view?" + urlencode({"source_id": SID})
        with urlopen(url, timeout=10) as response:
            body = json.load(response)

        assert body["source"]["source_id"] == SID
        assert body["source"]["path"] == PATH
        assert body["source"]["sha"] == PIN
        assert body["text"] == retrieve.load_at_sha(PATH, PIN)
        assert "Remaining preservation gaps" in body["text"]

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
