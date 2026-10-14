"""Revision chains for evolving claims."""
from claims import parse_claims

def build_chains(claims):
    chains = {}
    for c in claims:
        cid = c["section"]
        chains.setdefault(cid, []).append(c)
    return chains

def latest(chains, cid):
    revs = chains.get(cid, [])
    return revs[-1] if revs else None

def history(chains, cid):
    return chains.get(cid, [])

def supersedes_chain(chains, cid):
    return list(reversed(history(chains, cid)))

if __name__ == "__main__":
    claims = parse_claims()
    chains = build_chains(claims)
    n_chains = len(chains)
    n_rev = len(claims)
    print(str(n_chains) + " chains, " + str(n_rev) + " revisions")
    for cid in list(chains)[:3]:
        print("")
        print("[" + cid + "]")
        for r in supersedes_chain(chains, cid):
            line = "  status=" + str(r["status"])
            line += " artifacts=" + str(len(r["artifacts"]))
            print(line)
