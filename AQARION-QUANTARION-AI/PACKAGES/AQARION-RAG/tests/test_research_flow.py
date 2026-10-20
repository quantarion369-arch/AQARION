import json
import threading
import unittest
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

import api
import context
import retrieve


class ResearchFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), api.Handler)
        cls.thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.thread.start()
        cls.base = "http://127.0.0.1:" + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, route):
        try:
            response = urlopen(self.base + route, timeout=30)
        except HTTPError as error:
            response = error
        with response:
            return response.status, response.headers, response.read()

    def test_root_serves_exact_page(self):
        status, headers, body = self.get("/")
        page = Path(api.__file__).resolve().parent / "static" / "index.html"
        self.assertEqual(status, 200)
        self.assertEqual(body, page.read_bytes())
        self.assertIn("text/html", headers["Content-Type"])
        self.assertEqual(int(headers["Content-Length"]), len(body))
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")

    def test_context_delegates_decoded_query_without_wrapper(self):
        query = "theorem & qualification + evidence"
        expected = {
            "seed_results": [{"passage": "<img src=x onerror=alert(1)>"}],
            "supplementary_context": [],
            "expansion_metadata": {"support_adjudicated": False},
        }
        with patch.object(
            api.context, "retrieve_with_context", return_value=expected
        ) as call:
            status, headers, body = self.get(
                "/api/search/context?" + urlencode({"q": query})
            )
        self.assertEqual(status, 200)
        self.assertIn("application/json", headers["Content-Type"])
        self.assertEqual(json.loads(body), expected)
        call.assert_called_once_with(query)

    def test_missing_and_empty_queries_match_existing_function(self):
        expected = context.retrieve_with_context("")
        for route in ("/api/search/context", "/api/search/context?q="):
            with self.subTest(route=route):
                status, _, body = self.get(route)
                self.assertEqual(status, 200)
                self.assertEqual(json.loads(body), expected)

    def test_unknown_endpoint_remains_json_404(self):
        status, headers, body = self.get("/api/not-a-route")
        self.assertEqual(status, 404)
        self.assertIn("application/json", headers["Content-Type"])
        self.assertEqual(json.loads(body), {"error": "not found"})

    def test_legacy_search_shape_and_top_k(self):
        with patch.object(
            api, "retrieve", return_value=[(2, "doc", "sha", "text")]
        ) as call:
            status, _, body = self.get("/api/search?q=theorem")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {
            "query": "theorem",
            "results": [
                {"score": 2, "doc": "doc", "sha": "sha", "passage": "text"}
            ],
        })
        call.assert_called_once_with("theorem", top_k=3)

    def test_legacy_cited_shape_and_top_k(self):
        results = [{"rank": 1, "passage": "text"}]
        with patch.object(
            api, "retrieve_cited", return_value=results
        ) as call:
            status, _, body = self.get("/api/search/cited?q=theorem")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {
            "query": "theorem", "results": results
        })
        call.assert_called_once_with("theorem", top_k=3)

    def test_claim_search_preserves_artifact_filter(self):
        claims = [{"section": "Test", "text": "Claim", "artifacts": []}]
        with patch.object(
            api, "retrieve_claims", return_value=claims
        ) as call:
            status, _, body = self.get(
                "/api/claims/search?q=theorem&has_artifact=true"
            )
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {
            "query": "theorem", "claims": claims
        })
        call.assert_called_once_with("theorem", has_artifact=True)

    def test_claim_list_preserves_status_filter(self):
        claims = [{"status": "verified"}, {"status": "pending"}]
        with patch.object(api, "parse_claims", return_value=claims):
            status, _, body = self.get("/api/claims?status=verified")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {
            "count": 1, "claims": [claims[0]]
        })

    def test_real_context_http_and_pinned_citation_reconstruction(self):
        expected = context.retrieve_with_context("theorem")
        status, _, body = self.get("/api/search/context?q=theorem")
        self.assertEqual(status, 200)
        result = json.loads(body)
        self.assertEqual(result, expected)
        self.assertTrue(result["seed_results"])
        seeds = result["seed_results"]
        extras = result["supplementary_context"]
        self.assertLessEqual(len(seeds), 3)
        self.assertLessEqual(len(extras), 6)

        def identity(item):
            return (
                item["path"], item["commit_sha"],
                item["char_start"], item["char_end"]
            )

        seed_ids = {identity(item) for item in seeds}
        extra_ids = [identity(item) for item in extras]
        self.assertEqual(len(extra_ids), len(set(extra_ids)))
        self.assertTrue(seed_ids.isdisjoint(extra_ids))

        for item in seeds + extras:
            with self.subTest(citation=identity(item)):
                source = retrieve.load_at_sha(
                    item["path"], item["commit_sha"]
                )
                self.assertEqual(
                    source[item["char_start"]:item["char_end"]],
                    item["passage"],
                )

        by_rank = {seed["rank"]: seed for seed in seeds}
        for item in extras:
            self.assertTrue(item["context_only"])
            self.assertTrue(item["seed_links"])
            for link in item["seed_links"]:
                seed = by_rank[link["seed_rank"]]
                self.assertEqual(item["path"], seed["path"])
                self.assertEqual(item["commit_sha"], seed["commit_sha"])
                self.assertEqual(
                    link["seed_char_start"], seed["char_start"]
                )
                self.assertEqual(
                    link["seed_char_end"], seed["char_end"]
                )
                self.assertIn(link["direction"], ("previous", "following"))

        self.assertFalse(
            result["expansion_metadata"]["support_adjudicated"]
        )

    def test_real_claim_search_matches_existing_function(self):
        expected = api.retrieve_claims("theorem", has_artifact=False)
        status, _, body = self.get("/api/claims/search?q=theorem")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {
            "query": "theorem", "claims": expected
        })

    def test_page_static_safe_rendering_and_request_guards(self):
        page = (
            Path(api.__file__).resolve().parent / "static" / "index.html"
        ).read_text(encoding="utf-8")
        for sink in (
            "innerHTML", "outerHTML",
            "insertAdjacentHTML", "document.write"
        ):
            self.assertNotIn(sink, page)
        for expected in (
            "element.textContent = String(text)",
            "id !== requestId",
            "controller.abort()",
            "Context only - support not adjudicated.",
            "/api/search/context",
            "/api/claims/search",
            "encodeURIComponent",
        ):
            self.assertIn(expected, page)


if __name__ == "__main__":
    unittest.main()
