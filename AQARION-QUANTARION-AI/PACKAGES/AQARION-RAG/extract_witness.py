#!/usr/bin/env python3
import json, re, sys
from retrieve import retrieve
from assess import READINGS, make_claim, assess

B = chr(92)
C = re.compile(B + "bc" + B + "s*=" + B + "s*(-?" + B + "d+(?:" + B + "." + B + "d+)?)" + B + "b")
FAM = re.compile(B + "bquadratic" + B + "b", re.I)
LAB = re.compile(B + "b(stable|unstable)" + B + "b", re.I)

def extract(text):
    m = C.search(text)
    if not m or not FAM.search(text):
        return None
    labels = {x.lower() for x in LAB.findall(text)}
    if len(labels) != 1:
        return None
    return {"family": "quadratic", "c": float(m.group(1)), "label": labels.pop()}

def run(query, top_k=3):
    out, skipped = [], []
    for score, doc, sha, passage in retrieve(query, top_k=top_k):
        w = extract(passage)
        if w is None:
            skipped.append({"doc": doc, "sha": sha})
        else:
            w.update(id=doc + ":" + sha[:12], provenance={"doc": doc, "sha": sha, "passage": passage})
            out.append(w)
    return out, skipped

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        assert extract("quadratic c = 0.5 unstable") == {"family": "quadratic", "c": 0.5, "label": "unstable"}
        assert extract("quadratic c = 0.2 stable unstable") is None
        assert extract("quadratic unstable") is None
        print("SELF_TEST=PASS")
        sys.exit(0)
    ws, skipped = run(" ".join(sys.argv[1:]))
    print(json.dumps({"status": "OK", "witness_count": len(ws), "witnesses": ws, "skipped": skipped}, indent=2))
