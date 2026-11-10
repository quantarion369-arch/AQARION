#!/usr/bin/env python3
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument(
    "stage", choices=("odd12-stage1", "odd12-stage2", "odd8-base1", "odd8-bases2to6")
)
parser.add_argument("--release", required=True, type=Path)
parser.add_argument("--frozen", required=True, type=Path)
parser.add_argument("--outroot", required=True, type=Path)
parser.add_argument("--previous", type=Path)
args = parser.parse_args()

release = args.release.resolve()
frozen = args.frozen.resolve()
outroot = args.outroot.resolve()

audit = release / (
    "AQARION-QUANTARION-AI/research/"
    "boolean-hypercube-cyclic-support/audits/sixbit-exact"
)
validation = audit / "validation-runs"
specs = {
    "odd12-stage1": (
        "independent-odd12-stage1-T6tbrkW2", "reconstruct.py"
    ),
    "odd12-stage2": (
        "independent-odd12-stage2-7muy2t5i",
        "lift_all_hyperplanes.py"
    ),
    "odd8-base1": ("direct-odd8-base1-UsreglHb", "check.py"),
    "odd8-bases2to6": (
        "direct-odd8-bases2to6-b0hP586v", "check.py"
    ),
}

directory, filename = specs[args.stage]
archived = validation / directory
raw = (archived / filename).read_bytes()
report = json.loads((archived / "REPORT.json").read_text())

manifest = {}
for line in (archived / "SHA256SUMS").read_text().splitlines():
    digest, name = line.split("  ", 1)
    manifest[name] = digest

if manifest.get(filename) != sha(raw):
    raise SystemExit("STOP: archived source/manifest mismatch")
if report.get("source_sha256") != sha(raw):
    raise SystemExit("STOP: archived source/report mismatch")

expected = "5093e2af9db66567cba85caaff34220f1f8a0b35"
head = subprocess.run(
    ["git", "-C", str(frozen), "rev-parse", "HEAD"],
    check=True, capture_output=True, text=True
).stdout.strip()
if head != expected:
    raise SystemExit("STOP: wrong frozen checkout")

if not outroot.is_dir():
    raise SystemExit("STOP: outroot must already exist")

needs_previous = args.stage in ("odd12-stage2", "odd8-bases2to6")
if needs_previous and args.previous is None:
    raise SystemExit("STOP: this stage requires --previous")

import os
env = os.environ.copy()
env["PYTHONDONTWRITEBYTECODE"] = "1"

if args.stage.startswith("odd8-"):
    input_home = audit / (
        "synthesis/2026-11-09/direct-reconstruction-successor/"
        "portable-reproduction/input-home"
    )
    if not input_home.is_dir():
        raise SystemExit("STOP: portable input-home missing")
    env["HOME"] = str(input_home)

out = Path(tempfile.mkdtemp(
    prefix=args.stage + "-replay-", dir=str(outroot)
))
copied = out / filename
copied.write_bytes(raw)

if args.stage == "odd12-stage1":
    arguments = [str(out)]
elif args.stage == "odd8-base1":
    arguments = [str(frozen), str(out)]
else:
    arguments = [
        str(frozen), str(args.previous.resolve()), str(out)
    ]

print("FRESH OUTPUT:", out, flush=True)
print("COPIED SOURCE SHA256:", sha(raw), flush=True)
print("ARCHIVED SOURCE UNCHANGED", flush=True)

process = subprocess.Popen(
    [sys.executable, "-B", "-u", str(copied), *arguments],
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
with (out / "replay.log").open("w") as log:
    for line in process.stdout:
        print(line, end="", flush=True)
        log.write(line)
        log.flush()
code = process.wait()

print("PROCESS EXIT:", code)
result_path = out / "REPORT.json"
if result_path.is_file():
    result = json.loads(result_path.read_text())
    print("REPORT STATUS:", result.get("status"))
    print("REPORT SHA256:", sha(result_path.read_bytes()))

# Separate wrapper receipt: do not rewrite the checker's manifest.
receipt = {
    "stage": args.stage,
    "exit_code": code,
    "archived_source_sha256": sha(raw),
    "copied_source_sha256": sha(copied.read_bytes()),
    "output": str(out),
    "note": "replay.log and this receipt are wrapper additions "
            "outside the checker's original output manifest",
}
(out / "WRAPPER-RECEIPT.json").write_text(
    json.dumps(receipt, indent=2) + "\n"
)

print("NO STAGING, COMMIT, PUSH, OR PR")
sys.exit(code)
