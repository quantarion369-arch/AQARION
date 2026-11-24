import ast
import datetime
import functools
import hashlib
import itertools
import json
import os
import pathlib
import platform
import subprocess
import sys
import time

import sympy as sp

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

XS = sp.symbols(" ".join(NAMES))
ENV = dict(zip(NAMES,XS))

CASES = [
    (2,4),(2,5),(2,6),
    (3,6),(3,7),(3,8),(3,9),
    (4,8),(4,9),
]

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def log(message):
    print(message, flush=True)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (OUT/name).write_text(
        json.dumps(value, indent=2) + "\n"
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

def committed_package():
    actual_commit = git(
        "rev-parse",
        "--verify",
        COMMIT+"^{commit}",
    ).decode().strip()

    need(
        actual_commit == COMMIT,
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

    found = [
        path.decode()
        for path in changed.split(b"\0")
        if path
        and path.decode().startswith(PREFIX)
        and path.decode().endswith(
            "/ASSEMBLY_RECEIPT.json"
        )
    ]

    need(
        len(found) == 1,
        "Cannot uniquely resolve proof package at fixed commit",
    )

    package = found[0].rsplit("/",1)[0]

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
            "Unsafe committed manifest entry",
        )

        data = git(
            "cat-file",
            "blob",
            COMMIT+":"+package+"/"+name,
        )

        need(
            sha(data) == digest,
            "Committed package hash mismatch: "+name,
        )

        files[name] = data

    need(
        len(files) == 43,
        "Unexpected committed artifact count",
    )

    assembly = json.loads(
        files["ASSEMBLY_RECEIPT.json"]
    )

    need(
        assembly["status"]
        == "PROOF_PACKAGE_ASSEMBLED_AND_LINKS_VERIFIED",
        "Assembly scope mismatch",
    )

    need(
        sha(files["assemble.py"])
        == assembly["source_sha256"],
        "Assembler identity mismatch",
    )

    return package,manifest,files

@functools.lru_cache(None)
def terms(text):
    def decode(node):
        if (
            isinstance(node,ast.Constant)
            and type(node.value) is int
        ):
            return sp.Integer(node.value)

        if isinstance(node,ast.Name) and node.id in ENV:
            return ENV[node.id]

        if (
            isinstance(node,ast.UnaryOp)
            and isinstance(node.op,(ast.UAdd,ast.USub))
        ):
            value = decode(node.operand)
            if isinstance(node.op,ast.USub):
                return -value
            return value

        if isinstance(node,ast.BinOp):
            if isinstance(node.op,ast.Pow):
                need(
                    isinstance(node.right,ast.Constant)
                    and type(node.right.value) is int
                    and 0 <= node.right.value <= 32,
                    "Unsupported exponent",
                )
                return (
                    decode(node.left)
                    ** node.right.value
                )

            a,b = decode(node.left),decode(node.right)

            if isinstance(node.op,ast.Add):
                return a+b
            if isinstance(node.op,ast.Sub):
                return a-b
            if isinstance(node.op,ast.Mult):
                return a*b

        raise ValueError("Unsupported polynomial syntax")

    expression = decode(
        ast.parse(str(text),mode="eval").body
    )

    return tuple(
        (monomial,int(coefficient))
        for monomial,coefficient in sp.Poly(
            expression,*XS,domain=sp.ZZ
        ).terms()
        if coefficient
    )

@functools.lru_cache(None)
def compositions(total, parts):
    if total < 0:
        return ()

    if parts == 1:
        return ((total,),)

    result = []

    for bars in itertools.combinations(
        range(total+parts-1),
        parts-1,
    ):
        positions = (-1,)+bars+(total+parts-1,)

        result.append(tuple(
            positions[i+1]-positions[i]-1
            for i in range(parts)
        ))

    return tuple(result)

@functools.lru_cache(None)
def monomials(degree):
    if degree < 0:
        return ()

    result = []

    for twos in range(degree//2+1):
        for a in compositions(degree-2*twos,5):
            for b in compositions(twos,5):
                result.append(a+b)

    return tuple(sorted(result))

def component_columns(data, source, target, degree):
    row_ids = {}

    for i,shift in enumerate(target):
        for monomial in monomials(degree-shift):
            row_ids[i,monomial] = len(row_ids)

    parsed = [
        [terms(str(value)) for value in row]
        for row in data
    ]

    columns = {}
    count = 0

    for j,shift in enumerate(source):
        for multiplier in monomials(degree-shift):
            column = {}

            for i in range(len(target)):
                for monomial,coefficient in parsed[i][j]:
                    row = row_ids[
                        i,
                        tuple(
                            x+y
                            for x,y in zip(
                                monomial,multiplier
                            )
                        ),
                    ]

                    column[row] = (
                        column.get(row,0)+coefficient
                    )

            column = {
                row:value
                for row,value in column.items()
                if value
            }

            if column:
                columns[count] = column

            count += 1

    return columns,len(row_ids),count

def replay_columns(original, trace, nrows, ncols):
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
            "Invalid pivot range or value",
        )

        need(
            col in columns
            and columns[col].get(row) == unit,
            "Column-oriented pivot mismatch at step "
            + str(number),
        )

        pivot_column = columns.pop(col)

        for j,column in list(columns.items()):
            value = column.get(row,0)

            if not value:
                continue

            multiplier = value*unit

            for r,x in pivot_column.items():
                new = (
                    column.get(r,0)-multiplier*x
                )

                if new:
                    column[r] = new
                else:
                    column.pop(r,None)

            if not column:
                columns.pop(j)

    need(
        not columns,
        "Nonzero column residual after saved trace",
    )

    return len(trace)

NOTES = """SECOND-IMPLEMENTATION CHECK

This is a differently implemented certificate consumer, not independent
peer review.

It reads Git objects at a fixed commit and verifies every artifact in
the committed package manifest.

It imports none of the archived verifiers and executes no saved audit.

SymPy decodes polynomial coefficients over ZZ only.
No SymPy rank or Smith-normal-form routine is used.

Weighted monomials are generated by stars-and-bars for five weight-one
and five weight-two variables, then sorted lexicographically.

Original component traces were generated by row elimination.
This checker clears pivot rows using COLUMN operations and removes
the pivot column.

Both procedures leave the same Schur residual B-c*a/u for u=+1 or -1.
Every saved pivot must match the independently reconstructed matrix.

A zero residual gives exact rank and a unimodular rank minor.
No full Smith transformation matrices are claimed to be stored.

This run checks the nine component certificates only.
It does not recheck divisor homology or structural semigroup theorems.
No theorem status is changed and no Lean verification is claimed.
"""

def main():
    log(
        "PROJECT 2 — SECOND-IMPLEMENTATION "
        "COMPONENT CERTIFICATE CHECK"
    )

    package,manifest,files = committed_package()

    raw = files["evidence/qq/inputs/"+EXPORT]

    need(
        sha(raw) == FROZEN,
        "Frozen complex hash mismatch",
    )

    obj = json.loads(raw)

    need(
        obj["variables"] == NAMES
        and obj["weights"] == [1]*5+[2]*5,
        "Variables or weights differ",
    )

    need(
        [len(monomials(d)) for d in range(4)]
        == [1,5,20,60],
        "Independent monomial basis count",
    )

    inputs = OUT/"source_inputs"
    inputs.mkdir(exist_ok=False)

    (inputs/EXPORT).write_bytes(raw)
    (inputs/"COMMITTED_MANIFEST.reference.txt").write_bytes(
        manifest
    )

    results = []
    mutation_test_done = False

    for index,degree in CASES:
        name = "CASE_D%d_DEG%d.json" % (index,degree)

        case_raw = files["evidence/integral/"+name]
        case = json.loads(case_raw)

        (inputs/name).write_bytes(case_raw)

        need(
            case["map"] == "D"+str(index)
            and case["degree"] == degree,
            "Case identity mismatch",
        )

        data = obj["matrices"]["D"+str(index)]
        source = obj["module_scalar_shifts"][index]
        target = obj["module_scalar_shifts"][index-1]

        need(
            len(data) == len(target)
            and all(
                len(row) == len(source)
                for row in data
            ),
            "Matrix shape mismatch",
        )

        columns,nrows,ncols = component_columns(
            data,source,target,degree
        )

        need(
            (nrows,ncols)
            == (case["rows"],case["columns"]),
            "Independent basis dimensions differ",
        )

        actual_rank = replay_columns(
            columns,
            case["unit_pivot_trace"],
            nrows,
            ncols,
        )

        need(
            actual_rank == case["unit_pivots"]
            and case["residual_nonzero_entries"] == 0,
            "Rank metadata mismatch",
        )

        if not mutation_test_done:
            altered = [
                list(pivot)
                for pivot in case["unit_pivot_trace"]
            ]
            altered[0][2] *= -1

            rejected = False

            try:
                replay_columns(
                    columns,altered,nrows,ncols
                )
            except AssertionError:
                rejected = True

            need(
                rejected,
                "Mutated certificate was not rejected",
            )
            mutation_test_done = True

        results.append({
            "map": case["map"],
            "degree": degree,
            "rows": nrows,
            "columns": ncols,
            "recomputed_exact_rank": actual_rank,
            "certificate_sha256": sha(case_raw),
            "column_replay": "PASS",
        })

        log(
            "D%d degree %d: COLUMN_REPLAY=PASS rank=%d"
            % (index,degree,actual_rank)
        )

    (OUT/"METHOD_AND_LIMITS.txt").write_text(NOTES)

    save("RECEIPT.json", {
        "status": "PASS_SECOND_IMPLEMENTATION_COMPONENT_REPLAY",
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "sympy": sp.__version__,
        "platform": platform.platform(),
        "source_sha256": sha(
            pathlib.Path(__file__).read_bytes()
        ),
        "review_commit": COMMIT,
        "resolved_package": package,
        "committed_manifest_sha256": sha(manifest),
        "committed_artifacts_hash_checked": 43,
        "frozen_export_sha256": FROZEN,
        "cases": results,
        "negative_control_mutated_pivot_rejected":
            mutation_test_done,
        "elapsed_seconds": time.time()-START,
        "scope": {
            "archived_helpers_imported": False,
            "rank_or_smith_routine_used": False,
            "new_elimination_direction": "columns",
            "external_independent_researcher_execution": False,
            "formal_verification": False,
            "divisor_computation_rechecked": False,
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
    log("COLUMN_REPLAY_CASES=9/9")
    log("MUTATED_PIVOT_REJECTED=PASS")
    log("STATUS=PASS_SECOND_IMPLEMENTATION_COMPONENT_REPLAY")
    log("DIVISOR_RECHECK=NOT_PERFORMED_IN_THIS_RUN")
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
                "Diagnose a checker failure. Do not force a pass "
                "or automatically call it a theorem counterexample."
            ),
        })
        raise
