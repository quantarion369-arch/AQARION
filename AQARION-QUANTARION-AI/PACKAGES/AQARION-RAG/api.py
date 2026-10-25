import json
import subprocess
import retrieve as retrieval_module
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, parse_qsl
from claims import parse_claims, retrieve_claims
from retrieve import retrieve, retrieve_cited
from pathlib import Path
import context
import relationships

class Handler(BaseHTTPRequestHandler):
    def _send(self, data, code=200):
        body = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        qs = parse_qs(url.query)
        source_scope = None
        selected_entry = None
        scoped_routes = {
            "/api/search", "/api/search/cited", "/api/search/context",
            "/api/search/evidence", "/api/sources/view",
        }
        if url.path in scoped_routes:
            values = [
                value for key, value in
                parse_qsl(url.query, keep_blank_values=True)
                if key == "source_id"
            ]
            if len(values) > 1 or (
                values and (
                    not values[0] or values[0] != values[0].strip()
                )
            ):
                self._send({"error": "invalid source_id parameter"}, 400)
                return
            if values:
                source_scope = values[0]
                try:
                    selected_entry = retrieval_module.resolve_source_id(
                        source_scope
                    )
                except KeyError:
                    self._send({"error": "unknown source_id"}, 404)
                    return
                except Exception:
                    self._send({"error": "manifest validation failed"}, 500)
                    return

        if url.path == "/api/sources":
            try:
                entries = retrieval_module.validate_manifest()
                self._send({"sources": [
                    {
                        "source_id": retrieval_module.source_id(entry),
                        "doc": entry["doc"],
                        "path": entry["path"],
                        "sha": entry["sha"],
                        "purpose": entry.get("purpose", ""),
                    }
                    for entry in entries
                ]})
            except Exception:
                self._send({"error": "manifest validation failed"}, 500)

        elif url.path == "/api/sources/view":
            if selected_entry is None:
                self._send({"error": "source_id is required"}, 400)
                return
            try:
                text = retrieval_module.load_at_sha(
                    selected_entry["path"], selected_entry["sha"]
                )
                self._send({
                    "source": {"source_id": source_scope, **selected_entry},
                    "text": text,
                })
            except subprocess.CalledProcessError:
                self._send({"error": "pinned Git object unavailable"}, 404)
            except Exception:
                self._send({"error": "pinned source loading failed"}, 500)

        elif url.path == "/":
            page = Path(__file__).resolve().parent / "static" / "index.html"
            body = page.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
        elif url.path == "/api/search/evidence":
            q = qs.get("q", [""])[0]
            if source_scope is None:
                retrieval_context = context.retrieve_with_context(q)
            else:
                retrieval_context = context.retrieve_with_context(
                    q, source_id=source_scope)
            passages = (
                retrieval_context["seed_results"]
                + retrieval_context["supplementary_context"]
            )
            enrichment = relationships.resolve_related(passages)
            self._send({
                "retrieval_context": retrieval_context,
                **enrichment,
            })
        elif url.path == "/api/search/context":
            q = qs.get("q", [""])[0]
            if source_scope is None:
                self._send(context.retrieve_with_context(q))
            else:
                self._send(context.retrieve_with_context(
                    q, source_id=source_scope))
        elif url.path == "/api/claims":
            claims = parse_claims()
            status = qs.get("status", [None])[0]
            if status:
                claims = [c for c in claims
                          if c["status"] and status.lower() in c["status"].lower()]
            self._send({"count": len(claims), "claims": claims})
        elif url.path == "/api/search":
            q = qs.get("q", [""])[0]
            if source_scope is None:
                results = retrieve(q, top_k=3)
            else:
                results = retrieve(
                    q, top_k=3, source_id=source_scope)
            self._send({"query": q, "results": [
                {"score": s, "doc": d, "sha": h, "passage": p}
                for s, d, h, p in results]})
        elif url.path == "/api/search/cited":
            q = qs.get("q", [""])[0]
            if source_scope is None:
                results = retrieve_cited(q, top_k=3)
            else:
                results = retrieve_cited(
                    q, top_k=3, source_id=source_scope)
            self._send({"query": q, "results": results})
        elif url.path == "/api/claims/search":
            q = qs.get("q", [""])[0]
            ha = qs.get("has_artifact", ["false"])[0] == "true"
            claims = retrieve_claims(q, has_artifact=ha)
            self._send({"query": q, "claims": claims})
        else:
            self._send({"error": "not found"}, 404)

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    with HTTPServer(("127.0.0.1", 8765), Handler) as server:
        print("AQARION-RAG API on http://localhost:8765")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("AQARION-RAG API stopped.")
