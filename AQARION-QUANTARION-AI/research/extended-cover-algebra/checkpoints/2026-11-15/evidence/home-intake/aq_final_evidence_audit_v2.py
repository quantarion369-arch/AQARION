#!/usr/bin/env python3
import tarfile, json, hashlib, sys
from pathlib import Path
from fractions import Fraction

ARCHIVE = Path.home() / (
    "AQARION-resolution-evidence-20261114T171514834259Z.tar.gz"
)
EXPECTED_ARCHIVE = (
    "b0231475bb60dd70eafca56752f1f14d36d2ed3ed9ff86dd79cd179257600e77"
)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def stop(msg):
    print("\nBLOCKED:", msg)
    sys.exit(1)

def exact_rank(M):
    a = [[Fraction(x) for x in row] for row in M]
    nr, nc = len(a), len(a[0])
    r = 0
    for c in range(nc):
        p = next((i for i in range(r, nr) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        q = a[r][c]
        a[r] = [x/q for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                q = a[i][c]
                a[i] = [a[i][j]-q*a[r][j] for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r

print("=" * 72)
print("AQARION FINAL EVIDENCE AUDIT V2")
print("=" * 72)

if not ARCHIVE.is_file():
    stop("Archive not found: " + str(ARCHIVE))

archive_hash = sha(ARCHIVE.read_bytes())
print("Archive SHA256:", archive_hash)
if archive_hash != EXPECTED_ARCHIVE:
    stop("Archive hash differs from preserved checkpoint.")
print("PASS: archive checkpoint hash")

with tarfile.open(ARCHIVE, "r:gz") as tf:
    members = {}
    for m in tf.getmembers():
        if not m.isfile():
            continue
        if m.name in members:
            stop("Duplicate archive member: " + m.name)
        f = tf.extractfile(m)
        if f is None:
            stop("Cannot read: " + m.name)
        members[m.name] = f.read()

    print("Regular files:", len(members))
    if len(members) != 10:
        stop("Expected 10 regular files.")

    if "MANIFEST.json" not in members:
        stop("MANIFEST.json missing.")

    manifest = json.loads(members["MANIFEST.json"])
    entries = manifest.get("files")
    if not isinstance(entries, dict):
        stop("Manifest files object missing.")

    if set(entries) != set(members) - {"MANIFEST.json"}:
        stop("Manifest/member inventory mismatch.")

    # Verify every archive member against the manifest itself.
    for name, entry in sorted(entries.items()):
        data = members[name]
        got_hash = sha(data)
        got_size = len(data)
        if got_hash != entry.get("sha256"):
            stop("Manifest SHA mismatch: " + name)
        if got_size != entry.get("bytes"):
            stop("Manifest size mismatch: " + name)
        print("PASS:", name, got_size, got_hash)

    print("\nPASS: all nine payload members match MANIFEST.json")

    # Verify the four reference artifact bindings.
    refs = manifest.get("reference_artifacts", {})
    for name, digest in refs.items():
        if name not in members or sha(members[name]) != digest:
            stop("Reference artifact binding failed: " + name)
    if len(refs) != 4:
        stop("Expected four reference artifact bindings.")
    print("PASS: four reference JSON bindings")

    # D4 witness replay.
    wn = "AQARION-D4-rank13-witness-20261114T165438532744Z.json"
    w = json.loads(members[wn])
    D4 = w["D4_value"]
    D5 = w["D5_value"]

    if len(D4) != 35 or any(len(row) != 14 for row in D4):
        stop("D4 dimensions are not 35 x 14.")
    if len(D5) != 14:
        stop("D5 vector length is not 14.")

    Q4 = [[Fraction(x) for x in row] for row in D4]
    Q5 = [Fraction(x) for x in D5]

    product = [
        sum((Q4[i][j] * Q5[j] for j in range(14)), Fraction(0))
        for i in range(35)
    ]
    rank = exact_rank(Q4)
    product_zero = all(x == 0 for x in product)
    vector_nonzero = any(x != 0 for x in Q5)

    print("\n--- INDEPENDENT D4 REPLAY ---")
    print("Specialization:", json.dumps(w["point"], sort_keys=True))
    print("D4 dimensions:", len(Q4), "x", len(Q4[0]))
    print("Exact rational rank:", rank)
    print("Exact specialized D4*D5 zero:", product_zero)
    print("Specialized D5 nonzero:", vector_nonzero)
    print("Witness complex SHA:", w.get("complex_sha256"))

    if rank != 13:
        stop("Independent D4 rank is not 13.")
    if not product_zero:
        stop("Specialized D4*D5 is nonzero.")
    if not vector_nonzero:
        stop("Specialized D5 is zero.")
    if w.get("rank") != 13 or w.get("specialized_rank") != 13:
        stop("Witness recorded rank fields disagree.")

    complex_hash = refs.get(
        "AQARION-complete-complex-20261114T163933580791Z.json"
    )
    if w.get("complex_sha256") != complex_hash:
        stop("D4 witness is not bound to complex export.")

    print("PASS: independent exact rank-13 witness")
    print("PASS: specialized differential product")
    print("PASS: nonzero specialized D5")

    # Structural certificate consistency.
    sn = "AQARION-semigroup-certificate-20261114T164416695765Z.json"
    s = json.loads(members[sn])
    gens = s["generators"]
    facets = s["primitive_facets"]
    kappa = s["kappa"]

    if len(gens) != 10 or any(len(g) != 5 for g in gens):
        stop("Semigroup generator dimensions invalid.")
    if len(facets) != 10 or kappa != [1,1,1,1,1]:
        stop("Facet count or kappa mismatch.")

    for i, f in enumerate(facets):
        n = f["normal"]
        vals = [sum(n[j]*g[j] for j in range(5)) for g in gens]
        if vals != f["values_on_generators"]:
            stop("Facet value mismatch at facet " + str(i))
        if min(vals) < 0:
            stop("A generator violates a facet inequality.")
        if sum(n[j]*kappa[j] for j in range(5)) != 1:
            stop("Facet value on kappa is not one.")

    if s.get("lattice_basis_determinant") not in (1, -1):
        stop("Lattice basis is not recorded as unimodular.")
    if len(s.get("semigroup_generation_proof", [])) < 7:
        stop("Semigroup generation proof text missing.")

    print("\nPASS: semigroup certificate structural consistency")
    print("Facets:", len(facets))
    print("Generators:", len(gens))
    print("Lattice basis determinant:", s["lattice_basis_determinant"])

    print("\n" + "=" * 72)
    print("PROOF DEPENDENCIES")
    print("=" * 72)
    print(members["PROOF-DEPENDENCIES.md"].decode("utf-8"))

print("\n" + "=" * 72)
print("AUDIT SUMMARY")
print("=" * 72)
print("PASS: archive integrity")
print("PASS: manifest and all payload hashes")
print("PASS: four reference artifact bindings")
print("PASS: independent exact D4 rank 13")
print("PASS: specialized D4*D5 = 0")
print("PASS: specialized D5 != 0")
print("PASS: semigroup certificate metadata checks")
print("No files written by this audit.")
print("No repository modifications, uploads, commits, or publication.")
print("Global exactness remains subject to the dependency proof review.")
