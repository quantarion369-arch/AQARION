"""Detect explicit supersedes references in claim text."""
from claims import parse_claims

def find_supersedes(claims):
    pairs = []
    for c in claims:
        text = c["text"]
        idx = text.lower().find("supersedes")
        if idx == -1:
            continue
        rest = text[idx + len("supersedes"):]
        rest = rest.lstrip(": ").strip()
        end = rest.find(".")
        target = rest[:end] if end != -1 else rest
        pairs.append((c["section"], target.strip()))
    return pairs

if __name__ == "__main__":
    claims = parse_claims()
    pairs = find_supersedes(claims)
    print(str(len(pairs)) + " supersedes references found")
    for src, dst in pairs:
        print("  [" + src[:50] + "] -> " + dst[:60])
