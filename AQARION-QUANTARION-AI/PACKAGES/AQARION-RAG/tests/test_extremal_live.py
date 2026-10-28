import http.client
import json
from pathlib import Path
import threading
import unittest
from unittest import mock
from http.server import HTTPServer

import api
from features.extremal_inspector import live_analysis as live

BASE = [0,2,4,6,0,2,4,6]
MUTATION = [0,2,4,6,0,2,4,7]
CYCLE = [1,2,3,4,5,6,7,0]
H = [0,0,0,0,1,1,1,1]


class TestExtremalLive(unittest.TestCase):
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

    def request(self, payload=None, raw=None, headers=None,
                path="/api/cases/extremal/analyze", method="POST"):
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.port, timeout=10
        )
        body = raw if raw is not None else json.dumps(payload).encode()
        options = {"Content-Type": "application/json"}
        options.update(headers or {})
        try:
            connection.request(method, path, body=body, headers=options)
            response = connection.getresponse()
            data = response.read()
            return response.status, dict(response.getheaders()), data
        finally:
            connection.close()

    def result(self, T, h):
        code, headers, body = self.request({"T": T, "h": h})
        self.assertEqual(code, 200, body)
        self.assertEqual(headers["Cache-Control"], "no-store")
        return json.loads(body)

    def test_baseline(self):
        result = self.result(BASE, H)
        self.assertEqual(result["mode"], "LIVE_BOUNDED_EXACT")
        self.assertEqual(
            result["rank_profile_computed_exactly"], [1,4,7,8]
        )

    def test_mutation_certificate(self):
        result = self.result(MUTATION, H)
        self.assertEqual(
            result["rank_profile_computed_exactly"], [1,5,8,8]
        )
        self.assertTrue(result["repair_certificate_checked"])
        certificate = result["recognition"]["repair_certificate"]
        self.assertEqual(certificate["parity_moment"], -1)
        self.assertEqual(certificate["temporal_product_coordinates"], [3])

    def test_cycle_outside_saved_one_edge_family(self):
        result = self.result(CYCLE, H)
        self.assertEqual(
            result["rank_profile_computed_exactly"], [1,5,8,8]
        )
        self.assertTrue(result["observation_separates_states"])
        self.assertEqual(
            result["recognition"]["classification"], "PREFIX_COLLISION"
        )

    def test_two_and_four_states(self):
        for T, h in [
            ([1,0], [0,1]),
            ([0,2,0,2], [0,0,1,1]),
        ]:
            result = self.result(T, h)
            self.assertEqual(result["state_count"], len(T))

    def test_collapsed_itinerary_support(self):
        result = self.result([0,0], [0,0])
        self.assertEqual(result["distinct_itinerary_count"], 1)
        self.assertEqual(result["rank_profile_computed_exactly"], [1,1])
        self.assertEqual(
            result["minimum_full_degree_on_itinerary_support"], 0
        )
        self.assertFalse(result["observation_separates_states"])

    def test_shape_and_unknown_fields(self):
        for payload in (
            [], {}, {"T": BASE},
            {"T": BASE, "h": H, "command": "anything"},
        ):
            self.assertEqual(self.request(payload)[0], 400)

    def test_invalid_values(self):
        for T, h in (
            ([0,2], [0,1]),
            ([True,0], [0,1]),
            ([0,1], [0,False]),
            ([0,1], [0,2]),
            ("not an array", H),
        ):
            self.assertEqual(
                self.request({"T": T, "h": h})[0], 400
            )

    def test_state_budget(self):
        self.assertEqual(
            self.request({"T": list(range(16)), "h": [0]*16})[0],
            400,
        )

    def test_invalid_duplicate_and_nonfinite_json(self):
        for raw in (
            b"{",
            b'{"T":[0,1],"T":[1,0],"h":[0,1]}',
            b'{"T":[0,1],"h":[0,NaN]}',
        ):
            self.assertEqual(self.request(raw=raw)[0], 400)

    def test_content_type(self):
        self.assertEqual(
            self.request(
                {}, headers={"Content-Type": "text/plain"}
            )[0], 415
        )

    def test_body_budget(self):
        self.assertEqual(
            self.request(raw=b" " * 2049)[0], 413
        )

    def test_missing_length(self):
        connection = http.client.HTTPConnection(
            "127.0.0.1", self.port, timeout=10
        )
        try:
            connection.putrequest("POST", "/api/cases/extremal/analyze")
            connection.putheader("Content-Type", "application/json")
            connection.endheaders()
            response = connection.getresponse()
            self.assertEqual(response.status, 411)
            response.read()
        finally:
            connection.close()

    def test_invalid_length(self):
        self.assertEqual(
            self.request(
                {}, headers={"Content-Length": "-1"}
            )[0], 400
        )

    def test_foreign_origin(self):
        self.assertEqual(
            self.request(
                {}, headers={"Origin": "https://example.invalid"}
            )[0], 403
        )

    def test_foreign_host(self):
        self.assertEqual(
            self.request(
                {}, headers={"Host": "example.invalid"}
            )[0], 403
        )

    def test_transfer_encoding(self):
        self.assertEqual(
            self.request(
                {}, headers={"Transfer-Encoding": "chunked"}
            )[0], 400
        )

    def test_unknown_route_and_query(self):
        self.assertEqual(
            self.request({}, path="/api/not-a-live-route")[0], 404
        )
        self.assertEqual(
            self.request(
                {}, path="/api/cases/extremal/analyze?path=api.py"
            )[0], 400
        )

    def test_page_and_home_link(self):
        code, _, body = self.request(
            raw=b"", path="/cases/extremal/live", method="GET"
        )
        self.assertEqual(code, 200)
        self.assertIn(b"LIVE", body.upper())
        code, _, body = self.request(raw=b"", path="/", method="GET")
        self.assertEqual(code, 200)
        self.assertIn(b'href="/cases/extremal/live"', body)

    def test_no_retrieval_or_subprocess_execution(self):
        with mock.patch.object(
            api, "retrieve", side_effect=AssertionError("retrieval called")
        ), mock.patch.object(
            api.retrieval_module, "validate_manifest",
            side_effect=AssertionError("retrieval manifest called"),
        ), mock.patch.object(
            api.subprocess, "run",
            side_effect=AssertionError("subprocess called"),
        ):
            self.result(MUTATION, H)

    def test_fresh_execution_not_saved_response(self):
        with mock.patch.object(live, "analyze", wraps=live.analyze) as call:
            first = self.result(BASE, H)
            second = self.result(BASE, H)
        self.assertEqual(call.call_count, 2)
        self.assertNotEqual(first["analysis_id"], second["analysis_id"])
        self.assertEqual(first["input_sha256"], second["input_sha256"])

    def test_reference_unavailable_is_controlled(self):
        with mock.patch.object(
            live, "_reference",
            side_effect=live.ReferenceUnavailable("test"),
        ):
            self.assertEqual(
                self.request({"T": BASE, "h": H})[0], 503
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
