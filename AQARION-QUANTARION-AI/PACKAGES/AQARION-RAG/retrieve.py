"""Minimal citation-bound retrieval over the pinned corpus.

Reads corpus/MANIFEST.md, loads each document at its pinned SHA via git show,
and returns passages with the SHA attached. No embeddings, no LLM—exact
snapshot retrieval only.
"""
import re, subprocess
from pathlib import Path

MANIFEST = Path(__file__).parent / "corpus" / "MANIFEST.md"
WORD = re.compile(r"[A-Za-z0-9_]+")
PARA_BREAK = chr(10) * 2

def load_manifest():
    rows = []
    for line in MANIFEST.read_text().splitlines():
        if line.startswith("|") and not line.startswith("|--") and "Document" not in line:
            cols = [c.strip() for c in line.strip("|").split("|")]
            if len(cols) >= 4:
                rows.append({"doc": cols[0], "path": cols[1], "sha": cols[2], "purpose": cols[3]})
    return rows

def load_at_sha(path, sha):
    result = subprocess.run(
        ["git", "show", f"{sha}:{path}"],
        cwd=Path(__file__).resolve().parent,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout

def stem(w):
    for suf in "ization ational fulness ized ing ers ed s".split():
        if w.endswith(suf) and len(w) > len(suf) + 2:
            return w[:len(w) - len(suf)]
    return w

def retrieve(query, top_k=3):
    """Keyword-overlap retrieval against pinned snapshots."""
    q = set(stem(w) for w in WORD.findall(query.lower()))
    results = []
    for entry in load_manifest():
        text = load_at_sha(entry["path"], entry["sha"])
        for para in text.split(PARA_BREAK):
            words = set(stem(w) for w in WORD.findall(para.lower()))
            score = len(q & words)
            if score > 0:
                results.append((score, entry["doc"], entry["sha"], para.strip()))
    results.sort(reverse=True, key=lambda r: r[0])
    return results[:top_k]

if __name__ == "__main__":
    import sys
    for score, doc, sha, passage in retrieve(" ".join(sys.argv[1:])):
        print(f"[{score}] {doc} @ {sha[:8]}")
        print(passage)
        print()


def bm25_search(query, docs, k1=1.5, b=0.75):
    """Rank docs by BM25 relevance to query. Returns [(doc_id, score)] desc."""
    from collections import Counter
    import math

    stemmed_query = [stem(t) for t in query.lower().split()]
    doc_tokens = {did: [stem(t) for t in text.lower().split()]
                  for did, text in docs.items()}
    doc_lens = {did: len(toks) for did, toks in doc_tokens.items()}
    avgdl = sum(doc_lens.values()) / len(doc_lens) if doc_lens else 1
    n_docs = len(docs)

    scores = {}
    for did, toks in doc_tokens.items():
        tf = Counter(toks)
        score = 0.0
        for term in set(stemmed_query):
            f = tf.get(term, 0)
            if f == 0:
                continue
            df = sum(1 for t in doc_tokens.values() if term in t)
            idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)
            denom = f + k1 * (1 - b + b * doc_lens[did] / avgdl)
            score += idf * (f * (k1 + 1)) / denom
        scores[did] = score

    return sorted(scores.items(), key=lambda x: -x[1])
