"""Traversal over the claim/artifact evidence graph."""
from claims import parse_claims
from supersedes import find_supersedes

def build_index(claims):
    by_section = {}
    for c in claims:
        by_section[c["section"]] = c
    return by_section

def evidence_chain(claims, section):
    """Return the claim plus its artifacts, following supersedes links."""
    idx = build_index(claims)
    chain = []
    seen = set()
    cur = section
    while cur and cur in idx and cur not in seen:
        seen.add(cur)
        c = idx[cur]
        chain.append(c)
        nxt = None
        for src, dst in find_supersedes(claims):
            if src == cur:
                nxt = dst
                break
        cur = nxt
    return chain

def dependents_of(claims, artifact_hash):
    """Return claims whose artifacts include this hash."""
    out = []
    for c in claims:
        if artifact_hash in c["artifacts"]:
            out.append(c["section"])
    return out

if __name__ == "__main__":
    claims = parse_claims()
    h = "e97325fedd0ee6a5d9223003b857358ce5ba303c483603b36215eb233f115db1"
    print("dependents of artifact " + h[:16] + ":")
    for s in dependents_of(claims, h):
        print("  " + s)
    print("")
    print("evidence chain from 'Provenance correction':")
    for c in evidence_chain(claims,
        "Provenance correction and actual-source check (2026-10-14)"):
        print("  [" + c["section"][:50] + "]")
