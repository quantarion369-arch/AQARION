"""Minimal citation-bound retrieval over the pinned corpus.

Reads corpus/MANIFEST.md, loads each document at its pinned SHA via git show,
and returns passages with the SHA attached. No embeddings, no LLM—exact
snapshot retrieval only.
"""
import re, subprocess
from pathlib import Path

MANIFEST = Path(__file__).parent / "corpus" / "MANIFEST.md"

def load_manifest():
    rows = []
    for line in MANIFEST.read_text().splitlines():
        if line.startswith("|") and not line.startswith("|--") and "Document" not in line:
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 4:
                rows.append({"doc": cols[0], "path": cols[1], "sha": cols[2], "purpose": cols[3]})
    return rows

def load_at_sha(path, sha):
    result = subprocess.run(["git", "show", f"{sha}:{path}"], capture_output=True, text=True, check=True)
    return result.stdout

def retrieve(query, top_k=3):
    """Keyword-overlap retrieval against pinned snapshots. Returns list of (score, doc, sha, passage)."""
    q = set(re.findall(r"w+", query.lower()))
    results = []
    for entry in load_manifest():
        text = load_at_sha(entry["path"], entry["sha"])
        for para in text.split("

"):
            words = set(re.findall(r"w+", para.lower()))
            score = len(q & words)
            if score > 0:
                results.append((score, entry["doc"], entry["sha"], para.strip()))
    results.sort(reverse=True, key=lambda r: r[0])
    return results[:top_k]

if __name__ == "__main__":
    import sys
    for score, doc, sha, passage in retrieve(" ".join(sys.argv[1:])):
        print(f"[{score}] {doc} @ {sha[:8]}
{passage}
")
