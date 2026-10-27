
import http.client
import json
from pathlib import Path
import runpy
import threading
import unittest
from unittest import mock
from http.server import HTTPServer

import api

ROOT = Path(__file__).resolve().parents[1]
FEATURE = ROOT / "features" / "extremal_inspector"
BUILD = FEATURE / "build-001"


class TestExtremalInspector(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), api.Handler)
        cls.thread = threading.Thread(
            target=cls.server.serve_forever, daemon=True
        )
        cls.thread.start()
        cls.port = cls.server.server_address[1]

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def get(self, path):
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.port, timeout=10
        )
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return (
                response.status,
                dict(response.getheaders()),
                response.read(),
            )
        finally:
            connection.close()

    def test_fixed_case_page_and_headers(self):
        status, headers, body = self.get("/cases/extremal")
        self.assertEqual(status, 200)
        self.assertEqual(
            headers["Content-Type"], "text/html; charset=utf-8"
        )
        self.assertEqual(
            headers["X-Content-Type-Options"], "nosniff"
        )
        self.assertEqual(int(headers["Content-Length"]), len(body))
        self.assertEqual(body, (FEATURE / "build-002" / "inspector.html").read_bytes())
        self.assertNotIn(b"__CASE_DATA__", body)

    def test_homepage_links_to_case(self):
        status, _, body = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn(b'href="/cases/extremal"', body)

    def test_recorded_baseline_and_mutation(self):
        data = json.loads((BUILD / "cases.json").read_text())
        self.assertEqual(data["unique_maps"], 57)
        self.assertEqual(
            data["cases"]["7:6"]["rank_profile_computed_exactly"],
            [1, 4, 7, 8],
        )
        self.assertEqual(
            data["cases"]["7:7"]["rank_profile_computed_exactly"],
            [1, 5, 8, 8],
        )

    def test_reusable_recognizer_matches_saved_cases(self):
        module = runpy.run_path(str(FEATURE / "recognizer.py"))
        recognize = module["recognize_extremal"]
        data = json.loads((BUILD / "cases.json").read_text())
        seen = set()
        outcomes = set()

        for case in data["cases"].values():
            T = tuple(case["T"])
            if T in seen:
                continue
            seen.add(T)
            result = recognize(T, data["observation"])
            self.assertEqual(
                {key: result[key] for key in case["recognition"]},
                case["recognition"],
            )
            if "repair_certificate" in result:
                self.assertTrue(module["verify_terminal_repair"](
                    result["terminal_truth_table"],
                    result["repair_certificate"],
                ))
            outcomes.add(result["classification"])

        self.assertEqual(len(seen), 57)
        self.assertEqual(outcomes, {
            "EXTREMAL_REGISTER",
            "NONLITERAL_TERMINAL",
            "PREFIX_COLLISION",
        })

    def test_case_route_does_not_call_retrieval(self):
        with mock.patch.object(
            api, "retrieve",
            side_effect=AssertionError("unexpected retrieval"),
        ), mock.patch.object(
            api.retrieval_module, "validate_manifest",
            side_effect=AssertionError("unexpected source lookup"),
        ):
            status, _, _ = self.get("/cases/extremal")
        self.assertEqual(status, 200)

    def test_no_path_or_query_parameter_interface(self):
        status, _, _ = self.get(
            "/cases/extremal/../../api.py"
        )
        self.assertEqual(status, 404)

        status, _, _ = self.get(
            "/cases/extremal?path=api.py"
        )
        self.assertEqual(status, 400)
