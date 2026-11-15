import tarfile, hashlib, json
from pathlib import Path

p = Path.home() / "AQARION-resolution-evidence-20261114T171514834259Z.tar.gz"
def h(b):
    return hashlib.sha256(b).hexdigest()

with tarfile.open(p, "r:gz") as tf:
    manifest = json.load(tf.extractfile("MANIFEST.json"))

    for name in [
        "aq_complex_json_replay.py",
        "aq_d4_rank_witness.py",
        "aq_semigroup_certificate.py",
        "verify_bundle.py",
    ]:
        print("\n" + name)
        entry = manifest["files"][name]
        print("MANIFEST SHA:", entry["sha256"])
        print("MANIFEST BYTES:", entry["bytes"])

        member = tf.extractfile(name).read()
        print("ARCHIVE SHA:  ", h(member))
        print("ARCHIVE BYTES:", len(member))
        print("MANIFEST MATCH:", h(member) == entry["sha256"])

        local = Path.home() / name
        if local.exists():
            data = local.read_bytes()
            print("LOCAL SHA:    ", h(data))
            print("LOCAL BYTES:  ", len(data))
            print("LOCAL=ARCHIVE:", data == member)
        else:
            print("LOCAL FILE: absent")

print("\nREAD ONLY. No files modified.")
