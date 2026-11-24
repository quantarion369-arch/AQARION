import datetime
import hashlib
import json
import pathlib
import platform
import sys

OUT = pathlib.Path(__file__).resolve().parent
returncode = int(sys.argv[1])

def text(name):
    path = OUT/name
    return (
        path.read_text(errors="replace")
        if path.is_file() else ""
    )

def sha(data):
    return hashlib.sha256(data).hexdigest()

names = json.loads(text("THEOREMS.json"))
pinning = json.loads(text("PINNING.json"))

build = text("LEAN_BUILD.log")
context = text("LEAN_CONTEXT.txt")
positive = text("BUILD_EXIT_CODE.txt").strip()
negative = text("NEGATIVE_EXIT_CODE.txt").strip()

source_ok = True

for line in text("SOURCE_SHA256SUMS").splitlines():
    digest,name = line.split("  ",1)
    if sha((OUT/name).read_bytes()) != digest:
        source_ok = False

all_names = all(name in build for name in names)
olean = OUT/"ArithmeticKernel.olean"

ok = (
    returncode == 0
    and positive == "0"
    and negative == "1"
    and source_ok
    and all_names
    and "sorryAx" not in build
    and olean.is_file()
    and olean.stat().st_size > 0
    and "4.35.0-rc4" in context
)

status = (
    "PASS_COMPILED_ARITHMETIC_KERNEL"
    if ok
    else "INCOMPLETE_OR_FAILED_LEAN_EXPERIMENT"
)

receipt = {
    "status": status,
    "utc": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
    "host_python": sys.version,
    "host_platform": platform.platform(),
    "supervisor_exit_code": returncode,
    "pinning": pinning,
    "source_manifest_unchanged": source_ok,
    "positive_compile_exit": positive,
    "negative_control_exit": negative,
    "all_twenty_axiom_reports_present": all_names,
    "sorryAx_in_positive_log": "sorryAx" in build,
    "lean_version_report": context.strip(),
    "elan_version_report":
        text("ELAN_VERSION.txt").strip(),
    "compiler_binary_sha256_record":
        text("LEAN_BINARY_SHA256.txt").strip(),
    "compiled_olean_sha256": (
        sha(olean.read_bytes())
        if olean.is_file() else None
    ),
    "formal_scope": {
        "candidate_named_theorems": len(names),
        "arithmetic_helpers_compiled": ok,
        "complete_semigroup_generation_theorem": False,
        "real_cone_interior_theorem": False,
        "whole_resolution_formalized": False,
        "mathlib_downloaded_by_script": False,
        "axiom_free_claim": False,
        "axioms": (
            "See LEAN_BUILD.log; this is not merely "
            "a source-token scan."
        ),
    },
}

(OUT/"RECEIPT.json").write_text(
    json.dumps(receipt,indent=2)+"\n"
)

checks = []

for path in sorted(OUT.rglob("*")):
    if (
        path.is_file()
        and path.name not in ("SHA256SUMS","console.log")
        and "__pycache__" not in path.parts
    ):
        checks.append(
            sha(path.read_bytes())
            +"  "
            +path.relative_to(OUT).as_posix()
        )

(OUT/"SHA256SUMS").write_text(
    "\n".join(checks)+"\n"
)

print("\nSTATUS="+status)
print("NAMED_ARITHMETIC_THEOREMS="+str(len(names)))
print("AXIOM_REPORTS_PRESENT="+str(all_names))
print("SOURCE_MANIFEST_UNCHANGED="+str(source_ok))
print("FULL_SEMIGROUP_THEOREM=NOT_YET_FORMALIZED")
print("WHOLE_RESOLUTION=NOT_FORMALIZED")
print("RESULTS="+str(OUT))

if not ok:
    print(
        "Keep the logs and isolated Elan installation. "
        "Do not force a pass or reinstall blindly."
    )
