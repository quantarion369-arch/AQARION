import ast
import datetime
import hashlib
import json
import os
import pathlib
import platform
import re
import signal
import subprocess
import sys
import threading
import time

OUT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

NAME = "AQARION-complete-complex-20261114T163933580791Z.json"

FROZEN = (
    "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"
)

NAMES = [
    "A","E0","E1","E2","E3",
    "B0","B1","B2","B3","C",
]

WALL_SECONDS = 180
ADDRESS_SPACE_KIB = 1572864

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

def m2_expression(text):
    def emit(node):
        if (
            isinstance(node,ast.Constant)
            and type(node.value) is int
        ):
            return str(node.value)

        if isinstance(node,ast.Name) and node.id in NAMES:
            return node.id

        if (
            isinstance(node,ast.UnaryOp)
            and isinstance(node.op,(ast.USub,ast.UAdd))
        ):
            prefix = "(-" if isinstance(node.op,ast.USub) else "(+"
            return prefix + emit(node.operand) + ")"

        if isinstance(node,ast.BinOp):
            if isinstance(node.op,ast.Pow):
                need(
                    isinstance(node.right,ast.Constant)
                    and type(node.right.value) is int
                    and 0 <= node.right.value <= 32,
                    "Unsupported exponent",
                )
                return (
                    "(" + emit(node.left)
                    + "^" + str(node.right.value) + ")"
                )

            operations = {
                ast.Add: "+",
                ast.Sub: "-",
                ast.Mult: "*",
            }

            for kind,symbol in operations.items():
                if isinstance(node.op,kind):
                    return (
                        "(" + emit(node.left)
                        + symbol + emit(node.right) + ")"
                    )

        raise ValueError("Unsupported polynomial syntax")

    return emit(ast.parse(str(text),mode="eval").body)

def make_m2(obj):
    need(
        obj["field"] == "QQ"
        and obj["variables"] == NAMES,
        "Field or variables differ",
    )
    need(
        obj["weights"] == [1]*5+[2]*5,
        "Weights differ",
    )

    shifts = obj["module_scalar_shifts"]

    need(
        [len(values) for values in shifts]
        == [1,14,35,35,14,1],
        "Module ranks differ",
    )

    lines = [
        "-- Generated from frozen JSON.",
        "-- No original audit script is executed.",
        "R = QQ["
        + ",".join(NAMES)
        + ", Degrees => {"
        + ",".join(map(str,obj["weights"]))
        + "}];",
    ]

    for i,degrees in enumerate(shifts):
        need(
            all(
                type(degree) is int and degree >= 0
                for degree in degrees
            ),
            "Invalid module shift",
        )

        lines.append(
            "F%d = R^{%s};"
            % (
                i,
                ",".join(str(-degree) for degree in degrees),
            )
        )

    for i in range(1,6):
        data = obj["matrices"]["D"+str(i)]

        need(
            len(data) == len(shifts[i-1])
            and all(
                len(row) == len(shifts[i])
                for row in data
            ),
            "Matrix shape",
        )

        body = ",\n".join(
            "{"
            + ",".join(m2_expression(value) for value in row)
            + "}"
            for row in data
        )

        lines.append(
            "D%d = map(F%d,F%d,matrix {\n%s\n});"
            % (i,i-1,i,body)
        )

    lines.append(
        'print("M2_QQ_MATRICES_CONSTRUCTED=PASS");'
    )

    for i in range(1,5):
        lines.append(
            "assert(D%d * D%d == 0);" % (i,i+1)
        )

    lines.append(
        'print("M2_QQ_COMPOSITIONS=PASS");'
    )

    lines += [
        "endpoint = coker D1;",
        'print("M2_QQ_ENDPOINT_DIMENSION=" | toString(dim endpoint));',
        "assert(dim endpoint == 5);",
    ]

    # Start at the tail so partial progress remains visible.
    for i in (5,4,3,2,1):
        expression = (
            "prune(ker D5)"
            if i == 5
            else "prune(homology(D%d,D%d))" % (i,i+1)
        )

        lines += [
            'print("START_HH_%d");' % i,
            "H%d = %s;" % (i,expression),
            'print("HH_%d_ZERO=" | toString(H%d == 0));' % (i,i),
            "assert(H%d == 0);" % i,
            'print("HH_%d_CHECK=PASS");' % i,
        ]

    lines += [
        'print("M2_QQ_POSITIVE_HOMOLOGY=PASS");',
        "exit 0;",
    ]

    return "\n".join(lines) + "\n"

def stop_group(process):
    if process.poll() is not None:
        return

    try:
        os.killpg(process.pid,signal.SIGTERM)
    except ProcessLookupError:
        return

    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid,signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()

NOTES = """BOUNDED INDEPENDENT-CAS EXPERIMENT

Object: the fixed archived complex over QQ.

Python translates JSON polynomial entries to Macaulay2 syntax.
No original verifier, homology_check.m2, or empty characteristic script
is executed.

Macaulay2 constructs the supplied maps and directly computes
ker(D_i)/image(D_(i+1)).
H5 is ker D5.

No res(coker D1) comparison resolution is constructed.

This is QQ only. It does not establish an all-characteristic theorem.
It does not independently reprove the toric/semigroup identification
of coker D1.

Limits:
180 seconds wall time for the container job.
1536 MiB virtual address space.

Timeout, allocation failure, or API error is incomplete or execution
error, not automatically a mathematical counterexample.

Existing research data and Git repositories are not modified.
"""

def main():
    log(
        "PROJECT 2 — BOUNDED MACAULAY2 "
        "DIRECT-HOMOLOGY EXPERIMENT"
    )

    source = (
        HOME
        / "aq_p2_json_native_CGdjVwxB"
        / "inputs"
        / NAME
    )

    raw = source.read_bytes()

    need(
        sha(raw) == FROZEN,
        "Frozen JSON hash mismatch",
    )

    obj = json.loads(raw)
    payload = make_m2(obj)

    (OUT/"inputs").mkdir(exist_ok=False)
    (OUT/"inputs"/NAME).write_bytes(raw)
    (OUT/"audit_QQ.m2").write_text(payload)
    (OUT/"METHOD_AND_LIMITS.txt").write_text(NOTES)

    log("Frozen input: PASS")
    log(
        "Wall cap: %d seconds; virtual-address cap: %d KiB"
        % (WALL_SECONDS,ADDRESS_SPACE_KIB)
    )

    shell = (
        "set -eu; "
        "ulimit -v " + str(ADDRESS_SPACE_KIB) + "; "
        "cd /work; "
        "export GC_NPROCS=1; "
        'printf "RUNTIME_ARCH="; uname -m; '
        'printf "RUNTIME_M2_VERSION="; /usr/bin/M2 --version; '
        "exec /usr/bin/M2 "
        "--stop --no-debug --silent -q "
        "--no-threads --no-readline audit_QQ.m2"
    )

    command = [
        "proot-distro",
        "login",
        "--bind", str(OUT)+":/work",
        "aqarion-m2",
        "--",
        "/bin/bash",
        "--noprofile",
        "--norc",
        "-c",
        shell,
    ]

    started = time.time()
    process = None
    timed_out = False
    interrupted = False

    with (OUT/"M2_QQ.log").open("wb") as output:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        def drain():
            for line in iter(process.stdout.readline,b""):
                output.write(line)
                output.flush()

                try:
                    sys.stdout.write(
                        line.decode("utf-8",errors="replace")
                    )
                    sys.stdout.flush()
                except BrokenPipeError:
                    pass

        thread = threading.Thread(
            target=drain,
            daemon=True,
        )
        thread.start()

        try:
            process.wait(timeout=WALL_SECONDS)

        except subprocess.TimeoutExpired:
            timed_out = True
            stop_group(process)

        except KeyboardInterrupt:
            interrupted = True
            stop_group(process)

        finally:
            if process.poll() is None:
                stop_group(process)
            thread.join(timeout=10)

    text = (OUT/"M2_QQ.log").read_text(
        errors="replace"
    )

    passed = [
        i for i in (5,4,3,2,1)
        if ("HH_%d_CHECK=PASS" % i) in text
    ]

    nonzero = [
        i for i in (5,4,3,2,1)
        if ("HH_%d_ZERO=false" % i) in text
    ]

    if interrupted:
        status = "INCOMPLETE_INTERRUPTED"
    elif timed_out:
        status = "INCOMPLETE_TIMEOUT"
    elif nonzero:
        status = "NONZERO_HOMOLOGY_REPORTED_REQUIRES_REVIEW"
    elif process.returncode != 0:
        status = "EXECUTION_ERROR_REQUIRES_DIAGNOSIS"
    elif (
        passed == [5,4,3,2,1]
        and "M2_QQ_COMPOSITIONS=PASS" in text
        and "M2_QQ_POSITIVE_HOMOLOGY=PASS" in text
    ):
        status = "PASS_M2_QQ_DIRECT_POSITIVE_HOMOLOGY"
    else:
        status = "INCOMPLETE_MISSING_MARKERS"

    version = re.search(
        r"^RUNTIME_M2_VERSION=(.*)$",
        text,
        re.MULTILINE,
    )

    receipt = {
        "status": status,
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "generator_sha256": sha(
            pathlib.Path(__file__).read_bytes()
        ),
        "frozen_input_sha256": FROZEN,
        "generated_m2_sha256": sha(payload.encode()),
        "coefficient_field": "QQ",
        "container": "aqarion-m2",
        "runtime_m2_version": (
            version.group(1).strip()
            if version else None
        ),
        "limits": {
            "wall_seconds": WALL_SECONDS,
            "virtual_address_space_KiB": ADDRESS_SPACE_KIB,
        },
        "elapsed_wall_seconds": time.time()-started,
        "returncode": process.returncode,
        "timeout": timed_out,
        "interrupted": interrupted,
        "positive_homology_checks_passed": passed,
        "nonzero_homology_reported": nonzero,
        "scope": {
            "archived_matrix_data_used": True,
            "old_audit_scripts_executed": False,
            "comparison_resolution_computed": False,
            "all_characteristic_claim": False,
            "integral_exactness_claim": False,
            "Lean_verification": False,
            "novelty_claim": False,
            "endpoint_semigroup_identification_reproved": False,
        },
    }

    save("RECEIPT.json",receipt)

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

    log("\nSTATUS="+status)
    log("COEFFICIENT_FIELD=QQ")
    log(
        "POSITIVE_HOMOLOGY_CHECKS_PASSED="
        + ",".join(map(str,passed))
    )
    log(
        "ALL_CHARACTERISTICS="
        "NOT_ESTABLISHED_BY_THIS_RUN"
    )
    log("RESULTS="+str(OUT))

    return (
        0
        if status == "PASS_M2_QQ_DIRECT_POSITIVE_HOMOLOGY"
        else 2
    )

if __name__ == "__main__":
    try:
        code = main()
    except BaseException as error:
        save("FAILURE.json", {
            "status": "EXPERIMENT_SETUP_OR_SUPERVISION_FAILED",
            "error_type": type(error).__name__,
            "message": str(error),
        })
        raise
    else:
        sys.exit(code)
