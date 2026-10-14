import re
from pathlib import Path
from retrieve import load_manifest, load_at_sha, WORD

MANIFEST = Path(__file__).parent / "corpus" / "MANIFEST.md"
STATUS = re.compile(r"Status:s*(.+)", re.IGNORECASE)
ARTIFACT = re.compile(r"[a-f0-9]{64}")

def parse_claims(sha=None):
    entries = load_manifest()
    if not entries:
        return []
    entry = entries[0]
    sha = sha or entry["sha"]
    text = load_at_sha(entry["path"], sha)
    claims = []
    cur = {"section": None, "status": None,
           "artifacts": [], "text": [], "sha": sha}
    for line in text.splitlines():
        if line.startswith("#"):
            if cur["text"] or cur["status"] or cur["artifacts"]:
                claims.append(cur)
            cur = {"section": line.lstrip("#").strip(),
                   "status": None, "artifacts": [],
                   "text": [], "sha": sha}
        elif STATUS.search(line):
            cur["status"] = STATUS.search(line).group(1).strip()
        elif ARTIFACT.search(line):
            cur["artifacts"].append(ARTIFACT.search(line).group(0))
        else:
            cur["text"].append(line)
    if cur["text"] or cur["status"] or cur["artifacts"]:
        claims.append(cur)
    for c in claims:
        c["text"] = " ".join(t.strip() for t in c["text"] if t.strip())
    return claims

def filter_claims(claims, status=None, has_artifact=False):
    out = claims
    if status:
        out = [c for c in out
               if c["status"] and status.lower() in c["status"].lower()]
    if has_artifact:
        out = [c for c in out if c["artifacts"]]
    return out

def retrieve_claims(query, status=None,
                    has_artifact=False, top_k=3):
    claims = filter_claims(parse_claims(), status, has_artifact)
    q = set(WORD.findall(query.lower()))
    scored = []
    for c in claims:
        blob = c["section"] + " " + c["text"]
        score = len(q & set(WORD.findall(blob.lower())))
        if score > 0:
            scored.append((score, c))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [c for _, c in scored[:top_k]]

if __name__ == "__main__":
    print("=== all claims ===")
    for c in parse_claims():
        n = len(c["artifacts"])
        print(f"[{c['section']}] status={c['status']} artifacts={n}")
    print()
    print("=== artifact-backed claims ===")
    for c in retrieve_claims("closure cost", has_artifact=True):
        h = c["artifacts"][0][:16]
        print(f"[{c['section']}] artifact={h}...")
