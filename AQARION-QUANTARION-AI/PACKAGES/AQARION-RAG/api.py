import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from claims import parse_claims, retrieve_claims
from retrieve import retrieve, retrieve_cited
from pathlib import Path
import context

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
        if url.path == "/":
            page = Path(__file__).resolve().parent / "static" / "index.html"
            body = page.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)
        elif url.path == "/api/search/context":
            q = qs.get("q", [""])[0]
            self._send(context.retrieve_with_context(q))
        elif url.path == "/api/claims":
            claims = parse_claims()
            status = qs.get("status", [None])[0]
            if status:
                claims = [c for c in claims
                          if c["status"] and status.lower() in c["status"].lower()]
            self._send({"count": len(claims), "claims": claims})
        elif url.path == "/api/search":
            q = qs.get("q", [""])[0]
            results = retrieve(q, top_k=3)
            self._send({"query": q, "results": [
                {"score": s, "doc": d, "sha": h, "passage": p}
                for s, d, h, p in results]})
        elif url.path == "/api/search/cited":
            q = qs.get("q", [""])[0]
            results = retrieve_cited(q, top_k=3)
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
