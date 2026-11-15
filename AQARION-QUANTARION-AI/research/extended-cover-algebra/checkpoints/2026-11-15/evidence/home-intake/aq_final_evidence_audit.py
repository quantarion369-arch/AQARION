#!/usr/bin/env python3
import tarfile
import json
import hashlib
import sys
from pathlib import Path
from fractions import Fraction

ARCHIVE = Path.home() / (
    "AQARION-resolution-evidence-20261114T171514834259Z.tar.gz"
)
EXPECTED_ARCHIVE_SHA = (
    "b0231475bb60dd70eafca56752f1f14d36d2ed3ed9ff86dd79cd179257600e77"
)

EXPECTED_FILES = {
    "AQARION-D4-rank13-witness-20261114T165438532744Z.json":
        ("6604", "4a25bf580162f71d27d2a7dcc58ed4d6caa7a7c1792a425864997a6653e8e5f7"),
    "AQARION-algebra-replay-20261114T164651806439Z.json":
        ("2978", "5581387035a1f5448f514adacc04fc47c1357c3f0cbb48496fae2b901c64d07d"),
    "AQARION-complete-complex-20261114T163933580791Z.json":
        ("63260", "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"),
    "AQARION-semigroup-certificate-20261114T164416695765Z.json":
        ("7712", "291b40ac0b15a131b733ba96ae98752f5054ebf0a387c960efca39fb46c07f5b"),
    "PROOF-DEPENDENCIES.md":
        ("5245", "258e98de69c1035356356a9c7e6566956df498e24d9e5f50c4e13268088f4a99"),
    "aq_complex_json_replay.py":
        ("10794", "3bcd30a8ec4985287dc26028810a9a794c9085ccf4ad7eaf72ce11615393785"),
    "aq_d4_rank_witness.py":
        ("3280", "fd45b5e5a49ae0646371893d3431c69921740180fdab9ffcda6ddcade3e23014"),
    "aq_semigroup_certificate.py":
        ("7217", "4338a6b3a7e4d7a4ce96e4526c876bb1be63965530c5a308b50e320ed39c0804"),
    "verify_bundle.py":
        ("958", "cfc26e61b244198697322239edd28d0742d8e3cf90cfdf9a7fbfcfe58c8e69f3"),
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def fail(message):
    print("\nFAIL:", message)
    sys.exit(1)

def exact_rank(matrix):
    """Fraction-free Gaussian elimination over Q."""
    a = [[Fraction(x) for x in row] for row in matrix]
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    rank = 0
    pivot_row = 0

    for col in range(cols):
        pivot = next(
            (r for r in range(pivot_row, rows) if a[r][col] != 0),
            None
        )
        if pivot is None:
            continue

        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        p = a[pivot_row][col]
        a[pivot_row] = [x / p for x in a[pivot_row]]

        for r in range(rows):
            if r == pivot_row:
                continue
            factor = a[r][col]
            if factor:
                a[r] = [
                    a[r][j] - factor * a[pivot_row][j]
                    for j in range(cols)
                ]

        rank += 1
        pivot_row += 1
        if pivot_row == rows:
            break

    return rank

print("=" * 72)
print("AQARION FINAL EVIDENCE AUDIT")
print("=" * 72)

if not ARCHIVE.is_file():
    fail("Evidence archive not found: " + str(ARCHIVE))

archive_bytes = ARCHIVE.read_bytes()
archive_hash = sha(archive_bytes)
print("Archive:", ARCHIVE)
print("Archive SHA256:", archive_hash)

if archive_hash != EXPECTED_ARCHIVE_SHA:
    fail("Archive SHA256 does not match the recorded checkpoint.")
print("PASS: archive SHA256")

try:
    tf = tarfile.open(ARCHIVE, "r:gz")
except Exception as e:
    fail("Cannot open archive: " + repr(e))

with tf:
    files = {}
    for member in tf.getmembers():
        if not member.isfile():
            continue
        if member.name in files:
            fail("Duplicate archive member: " + member.name)
        stream = tf.extractfile(member)
        if stream is None:
            fail("Cannot read archive member: " + member.name)
        files[member.name] = stream.read()

    print("Archive regular-file count:", len(files))
    if len(files) != 10:
        fail("Expected exactly 10 regular files.")

    for name, (size_text, digest) in EXPECTED_FILES.items():
        if name not in files:
            fail("Missing expected member: " + name)
        data = files[name]
        if len(data) != int(size_text):
            fail("Size mismatch: " + name)
        if sha(data) != digest:
            fail("SHA256 mismatch: " + name)
        print("PASS:", name)

    if "MANIFEST.json" not in files:
        fail("MANIFEST.json missing")

    manifest = json.loads(files["MANIFEST.json"])
    for name, (_, digest) in EXPECTED_FILES.items():
        entry = manifest.get("files", {}).get(name)
        if not isinstance(entry, dict):
            fail("Manifest entry missing: " + name)
        if entry.get("sha256") != digest:
            fail("Manifest hash mismatch: " + name)
        if entry.get("bytes") != len(files[name]):
            fail("Manifest byte count mismatch: " + name)

    print("PASS: manifest entries agree with independently checked bytes")

    # D4 exact specialization replay
    witness_name = (
        "AQARION-D4-rank13-witness-20261114T165438532744Z.json"
    )
    witness = json.loads(files[witness_name])

    D4 = witness["D4_value"]
    D5 = witness["D5_value"]

    if len(D4) != 35 or any(len(row) != 14 for row in D4):
        fail("D4 specialization is not 35 x 14")
    if len(D5) != 14:
        fail("D5 specialization does not have 14 entries")

    D4q = [[Fraction(x) for x in row] for row in D4]
    D5q = [Fraction(x) for x in D5]

    # Compute D4 * D5 exactly over Q.
    product = []
    for row in D4q:
        total = sum(
            (row[j] * D5q[j] for j in range(14)),
            Fraction(0)
        )
        product.append(total)

    product_zero = all(x == 0 for x in product)
    d5_nonzero = any(x != 0 for x in D5q)
    rank = exact_rank(D4q)

    print("\n--- D4 SPECIALIZATION ---")
    print("Point:", json.dumps(witness["point"], sort_keys=True))
    print("Matrix shape:", len(D4q), "x", len(D4q[0]))
    print("Exact rank over Q:", rank)
    print("Exact D4 * D5 = 0:", product_zero)
    print("Specialized D5 nonzero:", d5_nonzero)
    print("Witness recorded rank:", witness.get("rank"))
    print("Complex SHA binding:", witness.get("complex_sha256"))

    if rank != 13:
        fail("Independent exact rank is not 13")
    if not product_zero:
        fail("Specialized D4*D5 is not zero")
    if not d5_nonzero:
        fail("Specialized D5 is zero")
    if witness.get("rank") != 13:
        fail("Witness rank field disagrees")
    if witness.get("complex_sha256") != (
        "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"
    ):
        fail("Witness is not bound to expected complex export")

    print("PASS: independent exact D4 rank-13 specialization")
    print("PASS: specialized differential product")
    print("PASS: nonzero specialized D5 vector")

    # Semigroup proof metadata consistency checks.
    sem_name = (
        "AQARION-semigroup-certificate-20261114T164416695765Z.json"
    )
    sem = json.loads(files[sem_name])

    generators = sem["generators"]
    if len(generators) != 10 or any(len(g) != 5 for g in generators):
        fail("Unexpected semigroup generator dimensions")

    kappa = sem["kappa"]
    if kappa != [1, 1, 1, 1, 1]:
        fail("Unexpected kappa")

    facets = sem["primitive_facets"]
    if len(facets) != 10:
        fail("Expected ten listed primitive facets")

    # Verify all listed facet normals are nonnegative on all generators.
    for i, facet in enumerate(facets):
        normal = facet["normal"]
        values = [
            sum(normal[j] * g[j] for j in range(5))
            for g in generators
        ]
        if values != facet["values_on_generators"]:
            fail("Facet values mismatch at facet " + str(i))
        if any(v < 0 for v in values):
            fail("Generator lies outside listed cone at facet " + str(i))
        if sum(normal[j] * kappa[j] for j in range(5)) != 1:
            fail("Facet does not take value one on kappa")

    proof = sem.get("semigroup_generation_proof", [])
    if len(proof) < 7:
        fail("Semigroup induction proof text missing or incomplete")

    print("\n--- SEMIGROUP STRUCTURE ---")
    print("Generators:", len(generators))
    print("Primitive facets:", len(facets))
    print("Unimodular basis determinant:",
          sem.get("lattice_basis_determinant"))
    print("Induction proof steps:", len(proof))
    print("PASS: recorded facet values and kappa checks")
    print("NOTE: proof validity is mathematical, not established merely by JSON parsing.")

    # Print complete proof dependency note.
    print("\n" + "=" * 72)
    print("COMPLETE PROOF DEPENDENCY NOTE")
    print("=" * 72)
    print(files["PROOF-DEPENDENCIES.md"].decode("utf-8"))

print("\n" + "=" * 72)
print("FINAL AUDIT RESULT")
print("=" * 72)
print("PASS: archive and all expected artifact hashes")
print("PASS: manifest byte/hash consistency")
print("PASS: independent exact rational D4 rank = 13")
print("PASS: specialized D4*D5 = 0")
print("PASS: specialized D5 != 0")
print("PASS: semigroup facet metadata consistency")
print("No project files written or modified.")
print("No repository changes, uploads, commits, or publication.")
print("Global exactness still requires the proof-dependency review.")
