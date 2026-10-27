#!/usr/bin/env python3
"""JOIN-STABILITY-specific reproduction and checked receipt writer."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def utc():
    return datetime.now(timezone.utc).isoformat()

def git(package, *args):
    return subprocess.check_output(
        ["git", "--no-optional-locks", "-C", str(package), *args],
        stderr=subprocess.PIPE,
    )

def snapshot(package, repo):
    prefix = package.relative_to(repo).as_posix()
    names = git(repo, "ls-files", "-z", "--", prefix).split(b"\0")
    result = {}
    for raw in names:
        if not raw:
            continue
        name = raw.decode("utf-8")
        path = repo / name
        if path.is_symlink() or not path.is_file():
            raise RuntimeError("Nonregular tracked input: " + name)
        result[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

def write_checked(handle, data):
    if handle.write(data) != len(data):
        raise OSError("Short output write")
    handle.flush()

def atomic_receipt(path, report):
    temporary = path.with_suffix(".json.tmp")
    try:
        with temporary.open("xb") as handle:
            write_checked(
                handle,
                (json.dumps(report, indent=2) + "\n").encode(),
            )
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass
        raise

def command(package, output, label, argv, environment, console):
    record = {
        "name": label,
        "argv": argv,
        "result": "FAIL",
        "exit_code": None,
        "logging_exit": None,
        "started_at_utc": utc(),
        "stdout": label + ".stdout",
        "stderr": label + ".stderr",
    }
    process = None
    selector = selectors.DefaultSelector()
    try:
        with (output / record["stdout"]).open("xb") as out, \
             (output / record["stderr"]).open("xb") as err, \
             (output / "reproduction.log").open("ab") as combined:
            process = subprocess.Popen(
                argv,
                cwd=package,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            selector.register(
                process.stdout, selectors.EVENT_READ, out
            )
            selector.register(
                process.stderr, selectors.EVENT_READ, err
            )
            while selector.get_map():
                for key, _ in selector.select():
                    data = key.fileobj.read1(8192)
                    if data:
                        write_checked(key.data, data)
                        write_checked(combined, data)
                        write_checked(console, data)
                    else:
                        selector.unregister(key.fileobj)
                        key.fileobj.close()
            record["exit_code"] = process.wait()
            record["logging_exit"] = 0
            record["result"] = (
                "PASS" if process.returncode == 0 else "FAIL"
            )
    except (Exception, KeyboardInterrupt) as exc:
        record["interrupted"] = isinstance(exc, KeyboardInterrupt)
        record["result"] = "FAIL"
        record["error"] = type(exc).__name__ + ": " + str(exc)
        record["logging_exit"] = 90
    finally:
        selector.close()
        if process is not None:
            if process.poll() is None:
                process.kill()
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    stream.close()
            record["exit_code"] = process.wait()
        record["finished_at_utc"] = utc()
    return record

def run(package, parent, expected, console=None):
    package = Path(package).resolve()
    parent = Path(parent).resolve()
    console = sys.stdout.buffer if console is None else console
    repo = Path(
        git(package, "rev-parse", "--show-toplevel")
        .decode().strip()
    ).resolve()
    if parent == repo or repo in parent.parents:
        raise RuntimeError(
            "Receipt parent must be outside the repository"
        )

    output = Path(tempfile.mkdtemp(
        prefix="AQARION-join-stability-", dir=parent
    ))
    receipt = output / "receipt.json"
    stages = [
        ("verify", [
            sys.executable, "-B", "-I", "verify.py"
        ]),
        ("audit", [
            sys.executable, "-B", "-I",
            "join_stability_independent_audit.py"
        ]),
        ("negative-controls", [
            sys.executable, "-B", "-I", "verify.py",
            "--self-test-negative-controls"
        ]),
    ]
    report = {
        "package_id": "JOIN-STABILITY",
        "package_version": None,
        "started_at_utc": utc(),
        "expected_tested_revision": expected,
        "wrapper_command": list(sys.argv),
        "python_version": sys.version,
        "source_baseline": None,
        "tested_revision": None,
        "repository_url": None,
        "preflight": "BLOCKED",
        "commands": [
            {
                "name": name,
                "argv": argv,
                "result": "NOT_RUN",
                "exit_code": None,
            }
            for name, argv in stages
        ],
        "result": "BLOCKED",
        "scope": "STRUCTURAL_AND_FINITE_COMPUTATIONAL_CHECKS_ONLY",
        "lean": {
            "result": "NOT_RUN",
            "status": "OPEN",
            "version": None,
            "mathlib_revision": None,
        },
        "promotion_changed": False,
    }
    before = None
    rc = 2
    try:
        if not re.fullmatch(r"[0-9a-f]{40}", expected or ""):
            raise RuntimeError(
                "Supply a full AQ_EXPECTED_TESTED_REVISION"
            )
        revision = git(repo, "rev-parse", "HEAD").decode().strip()
        report["tested_revision"] = revision
        if revision != expected:
            raise RuntimeError(
                "Expected revision does not match HEAD"
            )
        if git(
            repo, "status", "--porcelain", "--untracked-files=no"
        ):
            raise RuntimeError(
                "Tracked working tree or index is dirty"
            )

        before = snapshot(package, repo)
        report["source_sha256_before"] = before
        manifest = json.loads(
            (package / "manifest.json").read_text(encoding="utf-8")
        )
        if manifest.get("package_id") != "JOIN-STABILITY":
            raise RuntimeError("Unexpected package ID")
        report["package_version"] = manifest["package_version"]
        report["source_baseline"] = manifest["source_revision"]

        needed = {
            "manifest.json",
            "reproduce.sh",
            "reproduction.py",
            "verify.py",
            "join_stability_independent_audit.py",
            manifest["claim_registry"],
            manifest["evidence_registry"],
            *manifest["required_artifacts"],
        }
        for relative in needed:
            path = (package / relative).resolve()
            if path == package or package not in path.parents:
                raise RuntimeError(
                    "Input escapes package: " + relative
                )
            if path.relative_to(repo).as_posix() not in before:
                raise RuntimeError(
                    "Required input is not tracked: " + relative
                )

        subprocess.run(
            ["git", "-C", str(repo), "merge-base",
             "--is-ancestor", manifest["source_revision"], revision],
            check=True,
            capture_output=True,
        )
        report["repository_url"] = git(
            repo, "remote", "get-url", "origin"
        ).decode().strip()
        report["preflight"] = "PASS"
        environment = dict(
            os.environ,
            AQ_EXPECTED_TESTED_REVISION=expected,
            PYTHONDONTWRITEBYTECODE="1",
        )
        rc = 0
        for i, (name, argv) in enumerate(stages):
            record = command(
                package, output, name, argv, environment, console
            )
            report["commands"][i] = record
            if record["result"] != "PASS":
                rc = (
                    130 if record.get("interrupted")
                    else (90 if record["logging_exit"] else 1)
                )
                break
            if (
                snapshot(package, repo) != before
                or git(repo, "rev-parse", "HEAD")
                .decode().strip() != revision
                or git(
                    repo, "status", "--porcelain",
                    "--untracked-files=no"
                )
            ):
                rc = 94
                break
        report["result"] = "PASS" if rc == 0 else "FAIL"
    except (Exception, KeyboardInterrupt) as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        rc = (
            130 if isinstance(exc, KeyboardInterrupt)
            else (1 if report["preflight"] == "PASS" else 2)
        )
        if report["preflight"] == "PASS":
            report["result"] = "FAIL"
    finally:
        if before is not None:
            try:
                after = snapshot(package, repo)
                report["source_sha256_after"] = after
                unchanged = (
                    after == before
                    and git(repo, "rev-parse", "HEAD")
                    .decode().strip() == report["tested_revision"]
                    and not git(
                        repo, "status", "--porcelain",
                        "--untracked-files=no"
                    )
                )
                report[
                    "tracked_sources_and_revision_unchanged"
                ] = unchanged
                if not unchanged:
                    report["result"] = "FAIL"
                    rc = 94
            except Exception as exc:
                report["postflight_error"] = str(exc)
                report["result"] = "FAIL"
                rc = 94

        report["finished_at_utc"] = utc()
        try:
            report["output_sha256"] = {
                path.name: hashlib.sha256(
                    path.read_bytes()
                ).hexdigest()
                for path in sorted(output.iterdir())
                if path.is_file()
            }
            report["overall_exit"] = rc
            report["receipt_write_exit"] = 0
            atomic_receipt(receipt, report)
        except Exception as exc:
            print(
                "RECEIPT_WRITE_ERROR=" + str(exc),
                file=sys.stderr,
            )
            return 93, output
    return rc, output

def main():
    try:
        rc, output = run(
            ROOT,
            Path.home(),
            os.environ.get("AQ_EXPECTED_TESTED_REVISION", ""),
        )
        print("REPRODUCTION_EXIT=" + str(rc))
        print("REPRODUCTION_DIRECTORY=" + str(output))
        print("REPRODUCTION_RECEIPT=" + str(output / "receipt.json"))
        print("REPRODUCTION_STATUS=" + str(output / "receipt.json"))
        print("REPRODUCTION_LOG=" + str(output / "reproduction.log"))
        print("LEAN_STATUS=OPEN")
        return rc
    except Exception as exc:
        print(
            "REPRODUCTION_ERROR=" + str(exc), file=sys.stderr
        )
        return 95

if __name__ == "__main__":
    raise SystemExit(main())
