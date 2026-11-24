import collections
import csv
import datetime
import hashlib
import io
import itertools
import json
import os
import pathlib
import platform
import subprocess
import sys
import time

START = time.time()
OUT = pathlib.Path(__file__).resolve().parent

REPO = (
    pathlib.Path.home()
    / "aqarion_git_publish_O7dQgVBV"
    / "AQARION"
)

COMMIT = "4ebd01fdb849555c2967cd7975a3ba3fdc03c128"

PREFIX = (
    "AQARION-QUANTARION-AI/research/"
    "explicit-resolution-q/proof-drafts/"
)

EXPORT = "AQARION-complete-complex-20261114T163933580791Z.json"

FROZEN = (
    "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"
)

NAMES = [
    "A","E0","E1","E2","E3",
    "B0","B1","B2","B3","C",
]

PAIRS = list(itertools.combinations(range(4),2))

GENERATORS = [(0,0,0,0,-1)]

GENERATORS += [
    tuple(int(i == j) for i in range(4))+(0,)
    for j in range(4)
]

GENERATORS += [
    tuple(int(i != j) for i in range(4))+(1,)
    for j in range(4)
]

GENERATORS += [(1,1,1,1,2)]
TOP = (4,4,4,4,4)

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def log(message):
    print(message, flush=True)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (OUT/name).write_text(
        json.dumps(value, indent=2)+"\n"
    )

def git(*args):
    env = dict(
        os.environ,
        GIT_OPTIONAL_LOCKS="0",
        GIT_NO_LAZY_FETCH="1",
    )

    result = subprocess.run(
        ["git","-C",str(REPO),*args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )

    if result.returncode:
        raise RuntimeError(
            result.stderr.decode(errors="replace")
        )

    return result.stdout

def load_fixed_package():
    need(
        git(
            "rev-parse",
            "--verify",
            COMMIT+"^{commit}",
        ).decode().strip() == COMMIT,
        "Review commit unavailable",
    )

    changed = git(
        "diff-tree",
        "--no-commit-id",
        "-r",
        "--name-only",
        "-z",
        COMMIT,
    )

    paths = [
        path.decode()
        for path in changed.split(b"\0")
        if path
        and path.decode().startswith(PREFIX)
        and path.decode().endswith(
            "/ASSEMBLY_RECEIPT.json"
        )
    ]

    need(
        len(paths) == 1,
        "Cannot uniquely locate fixed proof package",
    )

    package = paths[0].rsplit("/",1)[0]

    manifest = git(
        "cat-file",
        "blob",
        COMMIT+":"+package+"/SHA256SUMS",
    )

    files = {}

    for line in manifest.decode().splitlines():
        if not line.strip():
            continue

        digest,name = line.split("  ",1)
        relative = pathlib.PurePosixPath(name)

        need(
            relative.parts
            and not relative.is_absolute()
            and ".." not in relative.parts
            and name not in files,
            "Unsafe manifest entry",
        )

        raw = git(
            "cat-file",
            "blob",
            COMMIT+":"+package+"/"+name,
        )

        need(
            sha(raw) == digest,
            "Committed artifact hash mismatch: "+name,
        )
        files[name] = raw

    need(
        len(files) == 43,
        "Unexpected package artifact count",
    )

    assembly = json.loads(
        files["ASSEMBLY_RECEIPT.json"]
    )

    need(
        assembly["status"]
        == "PROOF_PACKAGE_ASSEMBLED_AND_LINKS_VERIFIED",
        "Assembly status",
    )
    need(
        assembly["source_sha256"]
        == sha(files["assemble.py"]),
        "Assembler identity",
    )

    return package,manifest,files

def signature(v):
    a = v[:4]
    k = v[4]
    return tuple(a)+tuple(
        a[i]+a[j]-k
        for i,j in PAIRS
    )

def nonnegative(values):
    return all(value >= 0 for value in values)

def scalar(b):
    return sum(b[:4])-b[4]

def subset_signatures():
    generator_signatures = [
        signature(g) for g in GENERATORS
    ]
    result = {}

    # Enumerate subsets by cardinality rather than a bit recurrence.
    for size in range(11):
        for vertices in itertools.combinations(
            range(10),size
        ):
            mask = sum(1 << vertex for vertex in vertices)

            result[mask] = tuple(
                sum(
                    generator_signatures[vertex][j]
                    for vertex in vertices
                )
                for j in range(10)
            )

    need(len(result) == 1024, "Subset coverage")
    return result

def reconstruct_faces(b, subsets):
    values = signature(b)

    return sorted(
        mask
        for mask,total in subsets.items()
        if all(
            x <= y
            for x,y in zip(total,values)
        )
    )

def check_faces(b, recorded, subsets):
    actual = reconstruct_faces(b,subsets)
    need(recorded == actual, "Divisor face-set mismatch")
    return actual

def boundary_columns(faces, dimension):
    target = {
        mask:i
        for i,mask in enumerate(
            faces.get(dimension-1,[])
        )
    }

    columns = {}

    for column,mask in enumerate(
        faces.get(dimension,[])
    ):
        values = {}

        for vertex in range(10):
            if mask & (1 << vertex):
                face = mask ^ (1 << vertex)

                need(
                    face in target,
                    "Boundary face missing",
                )

                position = (
                    mask & ((1 << vertex)-1)
                ).bit_count()

                values[target[face]] = (-1)**position

        if values:
            columns[column] = values

    return (
        columns,
        len(target),
        len(faces.get(dimension,[])),
    )

def column_replay(original, trace, nrows, ncols):
    columns = {
        j:dict(column)
        for j,column in original.items()
        if column
    }

    for number,pivot in enumerate(trace):
        need(
            isinstance(pivot,list)
            and len(pivot) == 3
            and all(type(value) is int for value in pivot),
            "Invalid pivot encoding",
        )

        row,col,unit = pivot

        need(
            0 <= row < nrows
            and 0 <= col < ncols
            and abs(unit) == 1,
            "Invalid pivot bounds or unit",
        )

        need(
            col in columns
            and columns[col].get(row) == unit,
            "Column pivot mismatch at step "+str(number),
        )

        pivot_column = columns.pop(col)

        for j,column in list(columns.items()):
            multiplier = column.get(row,0)*unit

            if not multiplier:
                continue

            for r,value in pivot_column.items():
                new = (
                    column.get(r,0)-multiplier*value
                )

                if new:
                    column[r] = new
                else:
                    column.pop(r,None)

            if not column:
                columns.pop(j)

    need(not columns, "Nonzero column residual")
    return len(trace)

def audit_divisors(raw, expected_shifts, recorded_results):
    candidates = set()

    # Independent rectangular-box enumeration.
    for a in itertools.product(range(5),repeat=4):
        for k in range(-4,9):
            b = a+(k,)
            dual = tuple(
                x-y for x,y in zip(TOP,b)
            )

            if (
                nonnegative(signature(b))
                and nonnegative(signature(dual))
            ):
                candidates.add(b)

    need(
        len(candidates) == 835,
        "Independent degree enumeration",
    )

    subsets = subset_signatures()
    seen = set()
    betti = collections.Counter()
    boundary_count = 0
    chain_checks = 0

    bad_face_rejected = False
    bad_pivot_rejected = False

    with (OUT/"DEGREE_REPLAY.jsonl").open(
        "w",buffering=1
    ) as report:
        for number,line in enumerate(
            io.StringIO(raw.decode("utf-8")),1
        ):
            need(
                line.strip(),
                "Unexpected blank certificate line",
            )

            record = json.loads(line)
            b = tuple(record["degree"])

            need(
                len(b) == 5
                and all(type(value) is int for value in b)
                and b in candidates
                and b not in seen,
                "Unexpected or duplicate degree",
            )

            seen.add(b)

            masks = check_faces(
                b,record["face_masks"],subsets
            )

            if not bad_face_rejected:
                missing = next(
                    mask for mask in range(1024)
                    if mask not in masks
                )

                try:
                    check_faces(
                        b,
                        sorted(masks+[missing]),
                        subsets,
                    )
                except AssertionError:
                    bad_face_rejected = True

                need(
                    bad_face_rejected,
                    "Corrupted face set was accepted",
                )

            faces = collections.defaultdict(list)

            for mask in masks:
                faces[mask.bit_count()-1].append(mask)

            need(
                faces[-1] == [0],
                "Augmentation convention",
            )

            top = max(faces)

            by_dimension = {
                entry["dimension"]:entry
                for entry in record["boundaries"]
            }

            need(
                len(by_dimension)
                == len(record["boundaries"])
                and set(by_dimension)
                == set(range(top+1)),
                "Boundary dimension coverage",
            )

            ranks = {}
            previous = None
            boundary_summary = []

            for dimension in range(top+1):
                columns,nrows,ncols = boundary_columns(
                    faces,dimension
                )

                if previous is not None:
                    for column in columns.values():
                        product = collections.Counter()

                        for middle,coefficient in column.items():
                            for row,value in previous.get(
                                middle,{}
                            ).items():
                                product[row] += coefficient*value

                        need(
                            all(
                                value == 0
                                for value in product.values()
                            ),
                            "Reconstructed boundary squared is nonzero",
                        )

                    chain_checks += 1

                previous = columns
                certificate = by_dimension[dimension]

                need(
                    (nrows,ncols)
                    == (
                        certificate["rows"],
                        certificate["columns"],
                    ),
                    "Boundary shape mismatch",
                )

                rank = column_replay(
                    columns,
                    certificate["integer_unit_pivot_trace"],
                    nrows,
                    ncols,
                )

                need(
                    rank == certificate["rank"],
                    "Recorded boundary rank mismatch",
                )

                if not bad_pivot_rejected and rank:
                    changed = [
                        list(pivot)
                        for pivot in certificate[
                            "integer_unit_pivot_trace"
                        ]
                    ]
                    changed[0][2] *= -1

                    try:
                        column_replay(
                            columns,changed,nrows,ncols
                        )
                    except AssertionError:
                        bad_pivot_rejected = True

                    need(
                        bad_pivot_rejected,
                        "Corrupted boundary pivot accepted",
                    )

                ranks[dimension] = rank
                boundary_count += 1

                boundary_summary.append([
                    dimension,nrows,ncols,rank
                ])

            actual_homology = []

            for dimension in range(-1,top+1):
                free_rank = (
                    len(faces[dimension])
                    - ranks.get(dimension,0)
                    - ranks.get(dimension+1,0)
                )

                need(
                    free_rank >= 0,
                    "Negative homology dimension",
                )

                # Complete unit reductions certify torsion-free cokernels.
                actual_homology.append({
                    "dimension": dimension,
                    "free_rank": free_rank,
                    "torsion_invariant_factors": [],
                })

                if free_rank:
                    betti[dimension+1,b] += free_rank

            need(
                actual_homology
                == record["reduced_integral_homology"],
                "Original homology record mismatch",
            )

            report.write(json.dumps({
                "degree": b,
                "face_count": len(masks),
                "column_replayed_boundaries": boundary_summary,
                "reduced_integral_homology": actual_homology,
            },separators=(",",":"))+"\n")

            if number % 50 == 0 or number == 835:
                log(
                    "  Degrees checked: %d / 835"
                    % number
                )

    need(
        seen == candidates,
        "Incomplete degree coverage",
    )
    need(
        boundary_count == 2956
        and chain_checks == 2122,
        "Boundary coverage mismatch",
    )
    need(
        recorded_results["degrees"] == len(seen)
        and recorded_results["boundary_smith_forms"]
        == boundary_count
        and recorded_results["boundary_composition_checks"]
        == chain_checks,
        "Original receipt coverage mismatch",
    )

    expected = collections.Counter(
        (i,tuple(b))
        for i,shifts in enumerate(expected_shifts)
        for b in shifts
    )

    need(
        betti == expected and len(betti) == 54,
        "Multigraded Betti mismatch",
    )

    totals = collections.Counter()
    weighted = collections.Counter()

    for (i,b),multiplicity in betti.items():
        totals[i] += multiplicity
        weighted[i,scalar(b)] += multiplicity

    need(
        [totals[i] for i in range(6)]
        == [1,14,35,35,14,1],
        "Betti totals mismatch",
    )

    with (OUT/"REPLAY_BETTI_MULTIGRADED.csv").open(
        "w",newline=""
    ) as handle:
        writer = csv.writer(handle)

        writer.writerow([
            "homological_degree",
            "a0","a1","a2","a3","k",
            "scalar_degree","multiplicity",
        ])

        for (i,b),multiplicity in sorted(betti.items()):
            writer.writerow([
                i,*b,scalar(b),multiplicity
            ])

    save(
        "REPLAY_BETTI_WEIGHTED.json",
        [
            {
                "homological_degree": i,
                "scalar_degree": degree,
                "multiplicity": multiplicity,
            }
            for (i,degree),multiplicity
            in sorted(weighted.items())
        ],
    )

    return {
        "degrees": len(seen),
        "column_replayed_boundaries": boundary_count,
        "boundary_composition_checks": chain_checks,
        "torsion_cases": 0,
        "nonzero_multigraded_positions": len(betti),
        "betti_totals": [
            totals[i] for i in range(6)
        ],
        "corrupted_face_rejected": bad_face_rejected,
        "corrupted_pivot_rejected": bad_pivot_rejected,
    }

NOTES = """SECOND-IMPLEMENTATION DIVISOR CHECK

Differently implemented finite-certificate consumer, not external peer review.

The source package is pinned by a full Git commit and its manifest.
No archived verifier is imported or executed.
No SymPy, rank routine, or Smith routine is used.

Candidate degrees are enumerated by a rectangular-box test of both cone
memberships, rather than the original k-interval constructor.

Faces are rebuilt using facet signatures of generator subsets, enumerated
by combinations rather than the original bit-sum recurrence.

Boundary signs use the number of set bits below the removed vertex.

Original row-elimination traces are checked using COLUMN elimination.
Stored Smith diagonals are not used to obtain ranks or torsion conclusions.

Complete unit reductions certify integral equivalence to I_r plus zero,
hence torsion-free cokernels.
The split quotient onto the free previous-boundary image identifies
homology torsion with next-boundary cokernel torsion.

Homology ranks and Betti data are recomputed from the reconstructed faces
and validated boundary ranks.

The theoretical degree cutoff and divisor/Koszul interpretation remain
explicit mathematical dependencies, not formal-verification claims.

A unit-pivot rank certificate does NOT assert total unimodularity of
every submatrix.

No theorem-status promotion, novelty claim, or Git write is performed.
"""

def main():
    log(
        "PROJECT 2 — SECOND-IMPLEMENTATION "
        "DIVISOR CERTIFICATE CHECK"
    )

    package,manifest,files = load_fixed_package()

    raw_export = files["evidence/qq/inputs/"+EXPORT]

    need(
        sha(raw_export) == FROZEN,
        "Frozen export identity",
    )

    export = json.loads(raw_export)

    need(
        export["variables"] == NAMES
        and export["variable_semigroup_degrees"]
        == [list(g) for g in GENERATORS],
        "Semigroup model mismatch",
    )

    raw = files[
        "evidence/divisor/DIVISOR_CERTIFICATES.jsonl"
    ]

    original_receipt = json.loads(
        files["evidence/divisor/RECEIPT.json"]
    )

    need(
        original_receipt["status"]
        == "PASS_COMPLETE_DIVISOR_HOMOLOGY_WITH_EXPLICIT_DEPENDENCIES",
        "Original divisor receipt status",
    )

    inputs = OUT/"source_inputs"
    inputs.mkdir(exist_ok=False)

    (inputs/EXPORT).write_bytes(raw_export)
    (inputs/"DIVISOR_CERTIFICATES.jsonl").write_bytes(raw)
    (inputs/"COMMITTED_MANIFEST.reference.txt").write_bytes(
        manifest
    )

    result = audit_divisors(
        raw,
        export["module_semigroup_shifts"],
        original_receipt["results"],
    )

    (OUT/"METHOD_AND_LIMITS.txt").write_text(NOTES)

    save("RECEIPT.json", {
        "status": "PASS_SECOND_IMPLEMENTATION_DIVISOR_REPLAY",
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "elapsed_seconds": time.time()-START,
        "source_sha256": sha(
            pathlib.Path(__file__).read_bytes()
        ),
        "review_commit": COMMIT,
        "resolved_package": package,
        "committed_manifest_sha256": sha(manifest),
        "committed_artifacts_hash_checked": 43,
        "frozen_export_sha256": FROZEN,
        "original_divisor_certificate_sha256": sha(raw),
        "results": result,
        "scope": {
            "archived_verifiers_imported": False,
            "sympy_used": False,
            "rank_or_smith_routine_used": False,
            "independent_face_construction": True,
            "elimination_direction": "columns",
            "external_independent_researcher_execution": False,
            "formal_verification": False,
            "theorem_status_changed": False,
        },
    })

    checks = []

    for path in sorted(OUT.rglob("*")):
        if (
            path.is_file()
            and path.name not in ("SHA256SUMS","console.log")
            and "__pycache__" not in path.parts
        ):
            checks.append(
                sha(path.read_bytes())
                + "  "
                + path.relative_to(OUT).as_posix()
            )

    (OUT/"SHA256SUMS").write_text(
        "\n".join(checks)+"\n"
    )

    log("\nCOMMITTED_ARTIFACT_HASHES=43/43")
    log("DEGREES_RECONSTRUCTED=835")
    log("COLUMN_REPLAYED_BOUNDARIES=2956")
    log("BOUNDARY_COMPOSITIONS_CHECKED=2122")
    log("TORSION_CASES=0")
    log("MULTIGRADED_BETTI_MATCH=PASS")
    log("NEGATIVE_CONTROLS=PASS")
    log("STATUS=PASS_SECOND_IMPLEMENTATION_DIVISOR_REPLAY")
    log("THEOREM_STATUS=UNCHANGED_DRAFT")
    log("RESULTS="+str(OUT))

if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        for name in ("RECEIPT.json","SHA256SUMS"):
            path = OUT/name
            if path.exists():
                path.unlink()

        save("FAILURE.json", {
            "status": "CHECKER_FAILED_OR_INCOMPLETE",
            "error_type": type(error).__name__,
            "message": str(error),
            "note": (
                "Do not force a pass or equate an implementation "
                "failure with a theorem counterexample."
            ),
        })
        raise
