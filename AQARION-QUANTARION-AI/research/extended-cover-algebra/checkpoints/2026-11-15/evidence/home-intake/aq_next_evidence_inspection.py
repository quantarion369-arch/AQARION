import tarfile, hashlib, json, os, sys
from pathlib import Path

archive = Path.home() / (
    "AQARION-resolution-evidence-20261114T171514834259Z.tar.gz"
)
expected = "b0231475bb60dd70eafca56752f1f14d36d2ed3ed9ff86dd79cd179257600e77"

if not archive.is_file():
    raise SystemExit(f"STOP: archive not found: {archive}")

actual = hashlib.sha256(archive.read_bytes()).hexdigest()
print("ARCHIVE SHA256:", actual)
if actual != expected:
    raise SystemExit("STOP: archive hash mismatch")
print("ARCHIVE HASH: PASS")

with tarfile.open(archive, "r:gz") as tf:
    members = [m for m in tf.getmembers() if m.isfile()]
    print("MEMBER COUNT:", len(members))
    for m in members:
        print(f"  {m.name}  ({m.size} bytes)")

    def read_match(tokens):
        matches = [
            m for m in members
            if all(t.lower() in m.name.lower() for t in tokens)
        ]
        if len(matches) != 1:
            print(f"\nMATCH ISSUE {tokens}: {len(matches)} candidates")
            for m in matches:
                print(" ", m.name)
            return None
        raw = tf.extractfile(matches[0]).read()
        return matches[0].name, raw

    for tokens in [
        ("semigroup-certificate",),
        ("rank13-witness",),
        ("proof-dependency",),
        ("manifest",),
    ]:
        result = read_match(tokens)
        if result is None:
            continue
        name, raw = result
        print("\n" + "=" * 78)
        print("ARTIFACT:", name)
        print("BYTES:", len(raw))
        print("SHA256:", hashlib.sha256(raw).hexdigest())
        print("-" * 78)

        if name.lower().endswith(".json"):
            try:
                obj = json.loads(raw)
                print(json.dumps(obj, indent=2, sort_keys=True))
            except Exception as e:
                print("JSON PARSE ERROR:", repr(e))
                print(raw.decode("utf-8", "replace"))
        else:
            print(raw.decode("utf-8", "replace"))

print("\nINSPECTION ONLY: no files written; no algebraic ranks recomputed.")
