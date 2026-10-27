import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

repo = Path(sys.argv[1]).resolve()
run = Path(sys.argv[2]).resolve()

package = (
    repo / "AQARION-QUANTARION-AI"
    / "PACKAGES" / "AQARION-RAG"
)
feature = package / "features" / "extremal_inspector"
test = package / "tests" / "test_extremal_inspector.py"

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

require(feature.is_dir(), "Installed feature is missing.")
require(test.is_file(), "Integration test file is missing.")

tracked_inputs = [
    package / "api.py",
    package / "README.md",
    package / "static" / "index.html",
    test,
    *[p for p in feature.rglob("*") if p.is_file()],
]

before = {
    str(path.relative_to(repo)): digest(path)
    for path in tracked_inputs
}

environment = {
    **os.environ,
    "PYTHONPATH": str(package),
    "PYTHONDONTWRITEBYTECODE": "1",
    "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
}

report = {
    "status": "FAIL",
    "scope": "Verification of already-installed RAG case feature.",
    "application_files_reinstalled": False,
    "mathematical_cases_recomputed": False,
    "phases": [],
    "source_sha256_before": before,
    "git_stage_commit_push": "NONE",
}

def run_phase(name, target, seconds):
    log_path = run / (name + ".log")
    xml_path = run / (name + ".xml")

    command = [
        sys.executable, "-u", "-B", "-m", "pytest",
        "-o", "addopts=",
        "-p", "no:cacheprovider",
        "-vv", "-s",
        "--junitxml=" + str(xml_path),
        str(target),
    ]

    print(f"\n=== {name}: START ===", flush=True)
    print(f"TIMEOUT_SECONDS={seconds}", flush=True)

    started = time.monotonic()
    timed_out = False
    next_heartbeat = started + 10

    with log_path.open("wb") as writer:
        process = subprocess.Popen(
            command,
            cwd=run,
            env=environment,
            stdin=subprocess.DEVNULL,
            stdout=writer,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        with log_path.open("rb") as reader:
            while process.poll() is None:
                chunk = reader.read()
                if chunk:
                    sys.stdout.buffer.write(chunk)
                    sys.stdout.buffer.flush()

                now = time.monotonic()

                if now >= next_heartbeat:
                    print(
                        f"\nRUNNING_PHASE={name} "
                        f"ELAPSED_SECONDS={int(now-started)}",
                        flush=True,
                    )
                    next_heartbeat = now + 10

                if now - started >= seconds:
                    timed_out = True
                    print(
                        f"\nTIMEOUT_PHASE={name}; "
                        "stopping only this test process group",
                        flush=True,
                    )

                    try:
                        os.killpg(process.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass

                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        try:
                            os.killpg(process.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        process.wait(timeout=10)

                    break

                time.sleep(0.2)

            remainder = reader.read()
            if remainder:
                sys.stdout.buffer.write(remainder)
                sys.stdout.buffer.flush()

    phase = {
        "name": name,
        "command": command,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "elapsed_seconds": round(time.monotonic()-started, 3),
    }

    if xml_path.is_file():
        xml = ET.parse(xml_path).getroot()
        cases = list(xml.iter("testcase"))
        inspector_cases = [
            node for node in cases
            if "TestExtremalInspector"
            in node.attrib.get("classname", "")
        ]

        phase.update({
            "testcases_recorded": len(cases),
            "inspector_testcases_recorded": len(inspector_cases),
            "failures": len(list(xml.iter("failure"))),
            "errors": len(list(xml.iter("error"))),
            "skipped": len(list(xml.iter("skipped"))),
            "inspector_tests_all_passed": (
                len(inspector_cases) == 6
                and all(
                    not any(
                        child.tag in {"failure", "error", "skipped"}
                        for child in node
                    )
                    for node in inspector_cases
                )
            ),
        })

    report["phases"].append(phase)

    require(
        not timed_out,
        f"{name} timed out. Its live log identifies the last test.",
    )
    require(
        process.returncode == 0,
        f"{name} failed. See its preserved log.",
    )
    require(
        phase.get("inspector_tests_all_passed") is True,
        f"{name} did not record six passing inspector tests.",
    )

    print(f"\n=== {name}: PASS ===", flush=True)

try:
    # Diagnose the previously interrupted integration first.
    run_phase(
        "inspector-targeted",
        test,
        seconds=120,
    )

    # Check compatibility with the existing application.
    run_phase(
        "rag-full-suite",
        package / "tests",
        seconds=300,
    )

    after = {
        str(path.relative_to(repo)): digest(path)
        for path in tracked_inputs
    }

    require(
        after == before,
        "An installed application file changed during verification.",
    )

    report["source_sha256_after"] = after
    report["application_files_unchanged"] = True
    report["status"] = "PASS"

    print("\nINSPECTOR_TARGETED_TESTS=6/6")
    print("RAG_FULL_SUITE=PASS")
    print("INSTALLED_APPLICATION_FILES_UNCHANGED=YES")
    print("FEATURE_LOCATION=EXISTING_RAG_PACKAGE")
    print("MATHEMATICAL_RECOMPUTATION=NONE")
    print("GIT_STAGE_COMMIT_PUSH=NONE")
    print("OVERALL_VERIFICATION_STATUS=PASS")

except BaseException as error:
    report["error"] = f"{type(error).__name__}: {error}"
    print("\nVERIFICATION_STOPPED=" + report["error"], flush=True)
    raise

finally:
    (run / "verification.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
