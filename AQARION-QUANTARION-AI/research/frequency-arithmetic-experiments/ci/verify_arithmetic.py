from pathlib import Path, PurePosixPath
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE.parents[2]
PREFIX = BASE.relative_to(ROOT).as_posix() + "/"

EXPECTED = {
    "ntt-boundary-inline-01":
        "NTT_INLINE_BOUNDARY_AUDIT=PASS",
    "montgomery-reduction-01-lrPAGMfw":
        "MONTGOMERY_REDUCTION_AUDIT=PASS",
    "barrett-crt-01-mww3hgfy":
        "BARRETT_CRT_AUDIT=PASS",
    "whole-pipeline-reference-01-ye6mjc21":
        "WHOLE_PIPELINE_REFERENCE_INTEGRATION=PASS",
}

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def verified_files(manifest):
    entries = manifest["files"]
    require(len(entries) == 27, "Unexpected manifest file count")
    seen = set()
    snapshot = {}

    for item in entries:
        name = item["path"]
        relative = PurePosixPath(name)
        require(
            not relative.is_absolute() and ".." not in relative.parts,
            "Unsafe manifest path",
        )
        require(name.startswith(PREFIX), "Out-of-scope manifest path")
        require(name not in seen, "Duplicate manifest entry")
        seen.add(name)

        within = name[len(PREFIX):]
        require(
            within == "README.md"
            or within.split("/")[0] in EXPECTED,
            "Unexpected evidence unit",
        )

        path = ROOT / name
        require(
            path.is_file() and not path.is_symlink(),
            "Missing file or disallowed symlink: " + name,
        )
        require(
            path.resolve().is_relative_to(BASE),
            "Evidence path escapes package",
        )

        data = path.read_bytes()
        require(len(data) == item["bytes"], "Size mismatch: " + name)
        require(
            hashlib.sha256(data).hexdigest() == item["sha256"],
            "Hash mismatch: " + name,
        )
        snapshot[name] = data

    return snapshot

def main():
    manifest_path = BASE / "EVIDENCE_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)

    require(
        manifest["schema_version"] == "AQARION-ARITHMETIC-EVIDENCE-1",
        "Unexpected manifest schema",
    )
    require(
        len(manifest["selection"]) == 4
        and set(manifest["selection"]) == set(EXPECTED),
        "Unexpected experiment selection",
    )

    snapshot = verified_files(manifest)
    records = manifest["execution_records"]

    require(len(records) == 4, "Unexpected execution record count")
    require(
        {record["unit"] for record in records} == set(EXPECTED),
        "Execution records do not match selection",
    )

    print("PYTHON:", sys.version, flush=True)
    print("PLATFORM:", platform.platform(), flush=True)
    print("ARCHIVED_MANIFEST_FILES_VERIFIED:", len(snapshot), flush=True)

    for record in records:
        unit = record["unit"]
        source = PREFIX + unit + "/experiment.py"
        output = PREFIX + unit + "/output.log"
        exit_path = PREFIX + unit + "/exit.txt"
        marker = EXPECTED[unit]

        require(record["source"] == source, "Unexpected source path")
        require(record["output"] == output, "Unexpected output path")
        require(record["success_marker"] == marker, "Marker mismatch")
        require(record["saved_exit"] == 0, "Saved nonzero exit")

        require(
            hashlib.sha256(snapshot[source]).hexdigest()
            == record["source_sha256"],
            "Execution source hash mismatch",
        )
        require(
            snapshot[exit_path].decode().strip() == "0",
            "Archived exit file is nonzero",
        )
        require(
            marker in snapshot[output].decode().splitlines(),
            "Archived success marker missing",
        )

        compile(snapshot[source], source, "exec")

        with tempfile.TemporaryDirectory(prefix="aqarion-ci-") as temporary:
            work = Path(temporary) / unit
            shutil.copytree(BASE / unit, work)

            print("=== REPLAY:", unit, "===", flush=True)
            try:
                result = subprocess.run(
                    [sys.executable, "-I", "-B", "experiment.py"],
                    cwd=work,
                    capture_output=True,
                    text=True,
                    timeout=300,
                )
            except subprocess.TimeoutExpired as error:
                print(error.stdout or "", flush=True)
                print(error.stderr or "", flush=True)
                raise RuntimeError("Replay timed out: " + unit) from error

            print(result.stdout, end="", flush=True)
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr, flush=True)

            require(result.returncode == 0, "Replay failed: " + unit)
            require(
                marker in result.stdout.splitlines(),
                "Fresh success marker missing: " + unit,
            )
            print("FRESH_REPLAY=PASS:" + unit, flush=True)

    require(
        manifest_path.read_bytes() == manifest_bytes,
        "Archived manifest changed during verification",
    )
    for name, original in snapshot.items():
        require(
            (ROOT / name).read_bytes() == original,
            "Archived evidence changed: " + name,
        )

    print("ARCHIVED_EVIDENCE_UNCHANGED=PASS")
    print("REPLAYED_EXPERIMENT_UNITS=4")
    print("OUTPUT_BYTE_EQUALITY_NOT_REQUIRED")
    print("SCOPE=MANIFEST_INTEGRITY_AND_DECLARED_PROGRAM_REPLAY")
    print("ARITHMETIC_CI=PASS")

if __name__ == "__main__":
    main()
