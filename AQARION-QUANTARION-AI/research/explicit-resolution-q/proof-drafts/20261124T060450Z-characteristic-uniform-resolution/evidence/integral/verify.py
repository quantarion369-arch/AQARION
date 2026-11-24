import ast
import collections
import datetime
import functools
import hashlib
import itertools
import json
import math
import pathlib
import platform
import sys
import time

START = time.time()
OUT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

FROZEN = (
    "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"
)
NAME = "AQARION-complete-complex-20261114T163933580791Z.json"

NAMES = [
    "A","E0","E1","E2","E3",
    "B0","B1","B2","B3","C",
]
WEIGHTS = (1,1,1,1,1,2,2,2,2,2)
ZERO = (0,)*10

SHIFTS = [
    [0],
    [3]*8+[4]*6,
    [4]*3+[5]*24+[6]*8,
    [6]*8+[7]*24+[8]*3,
    [8]*6+[9]*8,
    [12],
]

CASES = [
    (2,4,3),
    (2,5,39),
    (2,6,180),
    (3,6,8),
    (3,7,64),
    (3,8,277),
    (3,9,937),
    (4,8,6),
    (4,9,38),
]

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def log(message):
    print(message, flush=True)

def save(name, value):
    (OUT/name).write_text(
        json.dumps(value, indent=2) + "\n"
    )

def add(a, b, factor=1):
    result = dict(a)
    for monomial, coefficient in b.items():
        result[monomial] = (
            result.get(monomial, 0)+factor*coefficient
        )
        if not result[monomial]:
            del result[monomial]
    return result

def mul(a, b):
    result = {}
    for x, c in a.items():
        for y, d in b.items():
            monomial = tuple(
                i+j for i,j in zip(x,y)
            )
            result[monomial] = (
                result.get(monomial, 0)+c*d
            )
            if not result[monomial]:
                del result[monomial]
    return result

@functools.lru_cache(None)
def parse(text):
    def visit(node):
        if (
            isinstance(node, ast.Constant)
            and type(node.value) is int
        ):
            return {ZERO: node.value} if node.value else {}

        if isinstance(node, ast.Name) and node.id in NAMES:
            index = NAMES.index(node.id)
            return {
                tuple(int(j == index) for j in range(10)): 1
            }

        if (
            isinstance(node, ast.UnaryOp)
            and isinstance(node.op, (ast.USub, ast.UAdd))
        ):
            value = visit(node.operand)
            if isinstance(node.op, ast.USub):
                return {
                    monomial: -coefficient
                    for monomial, coefficient in value.items()
                }
            return value

        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Pow):
                need(
                    isinstance(node.right, ast.Constant)
                    and type(node.right.value) is int
                    and 0 <= node.right.value <= 32,
                    "Invalid exponent",
                )
                base = visit(node.left)
                result = {ZERO: 1}
                for _ in range(node.right.value):
                    result = mul(result, base)
                return result

            a, b = visit(node.left), visit(node.right)

            if isinstance(node.op, ast.Add):
                return add(a,b)
            if isinstance(node.op, ast.Sub):
                return add(a,b,-1)
            if isinstance(node.op, ast.Mult):
                return mul(a,b)

        raise ValueError(
            "Only integral polynomial expressions are supported"
        )

    return visit(ast.parse(str(text), mode="eval").body)

@functools.lru_cache(None)
def monoms(degree, index=0):
    if degree < 0:
        return ()
    if index == 10:
        return ((),) if degree == 0 else ()

    return tuple(
        (exponent,)+tail
        for exponent in range(
            degree//WEIGHTS[index]+1
        )
        for tail in monoms(
            degree-exponent*WEIGHTS[index],
            index+1,
        )
    )

def component(M, source, target, degree):
    lookup = {}

    for row, shift in enumerate(target):
        for monomial in monoms(degree-shift):
            lookup[row,monomial] = len(lookup)

    rows = {}
    columns = 0

    for j, shift in enumerate(source):
        for multiplier in monoms(degree-shift):
            for i in range(len(target)):
                for monomial, coefficient in M[i][j].items():
                    row = lookup[
                        i,
                        tuple(
                            x+y
                            for x,y in zip(monomial,multiplier)
                        ),
                    ]
                    values = rows.setdefault(row,{})
                    values[columns] = (
                        values.get(columns,0)+coefficient
                    )
                    if not values[columns]:
                        del values[columns]

            columns += 1

    return (
        {i: row for i,row in rows.items() if row},
        len(lookup),
        columns,
    )

def reduce_units(original):
    rows = {
        i: dict(row)
        for i,row in original.items()
        if row
    }
    trace = []

    while rows:
        pivot = next(
            (
                (i,j,value)
                for i,row in rows.items()
                for j,value in row.items()
                if abs(value) == 1
            ),
            None,
        )

        if pivot is None:
            break

        i,j,unit = pivot
        pivot_row = rows.pop(i)
        trace.append([i,j,unit])

        for r,row in list(rows.items()):
            if j not in row:
                continue

            factor = row[j]*unit

            for column,x in pivot_row.items():
                value = row.get(column,0)-factor*x
                if value:
                    row[column] = value
                else:
                    row.pop(column,None)

            if not row:
                rows.pop(r)

    return trace,rows

def replay_units(original, trace):
    rows = {
        i: dict(row)
        for i,row in original.items()
        if row
    }

    for i,j,unit in trace:
        need(
            abs(unit) == 1
            and i in rows
            and rows[i].get(j) == unit,
            "Invalid pivot trace",
        )

        pivot_row = rows.pop(i)

        for r,row in list(rows.items()):
            coefficient = row.get(j,0)*unit
            if not coefficient:
                continue

            for column,x in pivot_row.items():
                value = row.get(column,0)-coefficient*x
                if value:
                    row[column] = value
                else:
                    row.pop(column,None)

            if not row:
                rows.pop(r)

    return rows

def check_manifest(root):
    raw = (root/"SHA256SUMS").read_bytes()
    count = 0

    for line in raw.decode().splitlines():
        if not line.strip():
            continue

        digest,name = line.split("  ",1)
        relative = pathlib.PurePosixPath(name)

        need(
            not relative.is_absolute()
            and ".." not in relative.parts,
            "Unsafe manifest path",
        )

        path = root.joinpath(*relative.parts)
        path.resolve().relative_to(root.resolve())

        need(
            hashlib.sha256(path.read_bytes()).hexdigest()
            == digest,
            "Prior bundle checksum mismatch: " + name,
        )
        count += 1

    return {
        "path": str(root),
        "manifest_sha256": hashlib.sha256(raw).hexdigest(),
        "files_verified": count,
    }

PROOF = """EXPERIMENT AND EVIDENCE BOUNDARY

This experiment constructs weighted component matrices directly over Z.

No imported research helper, CAS, finite-field arithmetic, or archived
source program is executed.

Unit-pivot elimination uses integer unimodular row/column operations.
A complete reduction to r unit pivots and a zero residual certifies
integral Smith form I_r plus zero.
A corresponding rank-r minor is unimodular.
The rank therefore equals r over every field.

Each stored trace is replayed against the original component matrix.

A unit-pivot stall is NOT a mathematical counterexample.
Some unimodular matrices require Euclidean operations before a unit
becomes visible.

Exactness of the archived resolution over every field is NOT
automatically asserted by this arithmetic status.
Its proof also requires:

1. The endpoint presentation agrees with the semigroup algebra over
   the fields in question.
   The pure-difference binomial presentation can be analyzed via its
   monoid congruence. Rational equality alone must be accompanied
   by that argument.

2. The structural and complete divisor-complex arguments give the
   intended field-independent Betti degrees.

3. Inductive kernel-generation arguments use the certified ranks
   in all necessary generator degrees.

4. The final-column primitive argument is valid over each field.
   A gcd computation over QQ alone is not its universal proof.

No Lean, novelty, or automatic theorem-status promotion is claimed.
"""

def main():
    log(
        "PROJECT 2 — INTEGRAL UNIT-PIVOT "
        "COMPONENT EXPERIMENT"
    )

    p2 = HOME/"aq_p2_json_native_CGdjVwxB"
    divisor = HOME/"aq_p2_divisor_b3X2omUU"

    prior = [
        check_manifest(p2),
        check_manifest(divisor),
    ]

    prior_p2 = json.loads(
        (p2/"RECEIPT.json").read_text()
    )
    prior_divisor = json.loads(
        (divisor/"RECEIPT.json").read_text()
    )

    need(
        prior_p2["status"]
        == "PASS_ARITHMETIC_WITH_EXPLICIT_THEOREM_DEPENDENCIES",
        "Unexpected prior QQ status",
    )
    need(
        prior_divisor["status"]
        == "PASS_COMPLETE_DIVISOR_HOMOLOGY_WITH_EXPLICIT_DEPENDENCIES",
        "Unexpected prior divisor status",
    )

    path = p2/"inputs"/NAME
    raw = path.read_bytes()

    need(
        hashlib.sha256(raw).hexdigest() == FROZEN,
        "Frozen export hash mismatch",
    )

    obj = json.loads(raw)

    need(
        obj["variables"] == NAMES
        and tuple(obj["weights"]) == WEIGHTS
        and obj["module_scalar_shifts"] == SHIFTS,
        "Variables, weights or shifts differ",
    )

    (OUT/"inputs").mkdir(exist_ok=False)
    (OUT/"inputs"/NAME).write_bytes(raw)
    (OUT/"PROOF_BOUNDARY.txt").write_text(PROOF)

    matrices = []

    for i in range(1,6):
        data = obj["matrices"]["D"+str(i)]

        need(
            len(data) == len(SHIFTS[i-1])
            and all(
                len(row) == len(SHIFTS[i])
                for row in data
            ),
            "Matrix shape",
        )

        M = [
            [parse(str(value)) for value in row]
            for row in data
        ]

        for r,row in enumerate(M):
            for c,polynomial in enumerate(row):
                for monomial in polynomial:
                    need(
                        sum(
                            x*y
                            for x,y in zip(monomial,WEIGHTS)
                        )
                        == SHIFTS[i][c]-SHIFTS[i-1][r],
                        "Weighted degree mismatch",
                    )

        matrices.append(M)

    for i in range(4):
        A,B = matrices[i],matrices[i+1]

        for r in range(len(A)):
            for c in range(len(B[0])):
                value = {}

                for k in range(len(B)):
                    if A[r][k] and B[k][c]:
                        value = add(
                            value,
                            mul(A[r][k],B[k][c]),
                        )

                need(
                    not value,
                    "Integral differential composition is nonzero",
                )

    need(
        all(
            len(polynomial) == 2
            and sorted(polynomial.values()) == [-1,1]
            for polynomial in matrices[0][0]
        ),
        "Endpoint is not the expected pure-difference presentation",
    )

    log("INPUT_BINDING=PASS")
    log("ALL_COMPOSITIONS_OVER_Z=PASS")

    cases = []

    for index,degree,expected in CASES:
        log(
            "Testing D%d degree %d ..."
            % (index,degree)
        )

        rows,number_rows,number_columns = component(
            matrices[index-1],
            SHIFTS[index],
            SHIFTS[index-1],
            degree,
        )

        trace,residual = reduce_units(rows)

        need(
            replay_units(rows,trace) == residual,
            "Trace replay mismatch",
        )

        unit_rank = len(trace)
        complete = not residual

        if complete and unit_rank == expected:
            status = "UNIMODULAR_RANK_CERTIFIED"
        elif residual:
            status = "UNIT_PIVOT_SEARCH_STALLED"
        else:
            status = "UNEXPECTED_RANK"

        item = {
            "map": "D"+str(index),
            "degree": degree,
            "rows": number_rows,
            "columns": number_columns,
            "expected_QQ_rank": expected,
            "unit_pivots": unit_rank,
            "status": status,
            "unit_pivot_trace": trace,
            "residual_nonzero_entries": sum(
                map(len,residual.values())
            ),
            "residual_entry_gcd": (
                math.gcd(*(
                    abs(value)
                    for row in residual.values()
                    for value in row.values()
                ))
                if residual else 0
            ),
        }

        if residual:
            item["residual_rows"] = {
                str(r): {
                    str(c): value
                    for c,value in row.items()
                }
                for r,row in residual.items()
            }

        cases.append(item)

        save(
            "CASE_D%d_DEG%d.json" % (index,degree),
            item,
        )

        log(
            "  %s: %d unit pivots; residual entries %d"
            % (
                status,
                unit_rank,
                item["residual_nonzero_entries"],
            )
        )

    all_ok = all(
        case["status"] == "UNIMODULAR_RANK_CERTIFIED"
        for case in cases
    )

    status = (
        "PASS_UNIMODULAR_COMPONENT_CERTIFICATES"
        if all_ok
        else "INCOMPLETE_UNIT_PIVOT_CERTIFICATION"
    )

    receipt = {
        "status": status,
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "elapsed_seconds": time.time()-START,
        "source_sha256": hashlib.sha256(
            pathlib.Path(__file__).read_bytes()
        ).hexdigest(),
        "frozen_export_sha256": FROZEN,
        "prior_bundles": prior,
        "cases_summary": [
            {
                key:value
                for key,value in case.items()
                if key not in (
                    "unit_pivot_trace",
                    "residual_rows",
                )
            }
            for case in cases
        ],
        "scope": {
            "integer_arithmetic_only": True,
            "sympy_used": False,
            "integral_compositions_verified": True,
            "archived_matrices_all_characteristic_exactness": (
                "NOT_AUTOMATICALLY_PROMOTED; "
                "see PROOF_BOUNDARY.txt"
            ),
            "formal_verification": False,
            "novelty_claimed": False,
        },
    }

    save("RECEIPT.json",receipt)

    checks = []

    for file in sorted(OUT.rglob("*")):
        if (
            file.is_file()
            and file.name not in ("console.log","SHA256SUMS")
            and "__pycache__" not in file.parts
        ):
            checks.append(
                hashlib.sha256(file.read_bytes()).hexdigest()
                + "  "
                + file.relative_to(OUT).as_posix()
            )

    (OUT/"SHA256SUMS").write_text(
        "\n".join(checks)+"\n"
    )

    log("\nSTATUS="+status)
    log(
        "UNIMODULAR_CASES=%d/9"
        % sum(
            case["status"] == "UNIMODULAR_RANK_CERTIFIED"
            for case in cases
        )
    )
    log(
        "ALL_CHARACTERISTIC_EXACTNESS="
        "REQUIRES_THEOREM_REVIEW"
    )
    log("RESULTS="+str(OUT))

    if not all_ok:
        log(
            "A stalled unit search is an incomplete method result, "
            "not a proof of a bad characteristic."
        )

if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        for name in ("RECEIPT.json","SHA256SUMS"):
            file = OUT/name
            if file.exists():
                file.unlink()

        save("FAILURE.json", {
            "status": "INCOMPLETE_OR_FAILED",
            "error_type": type(error).__name__,
            "message": str(error),
        })
        raise
