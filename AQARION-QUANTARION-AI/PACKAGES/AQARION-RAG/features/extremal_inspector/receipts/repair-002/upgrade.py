import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback
import xml.etree.ElementTree as ET

repo = Path(sys.argv[1]).resolve()
run = Path(sys.argv[2]).resolve()

package = (
    repo / "AQARION-QUANTARION-AI"
    / "PACKAGES" / "AQARION-RAG"
)
feature = package / "features" / "extremal_inspector"
build = feature / "build-002"
new_test = package / "tests" / "test_terminal_repair.py"

checkpoint = "813cfc47ca8aa109bc82483de0f76353f3a6219f"

def require(ok, message):
    if not ok:
        raise AssertionError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output([
        "git", "--no-optional-locks", "-C", str(repo), *args
    ])

def replace_once(text, old, new):
    require(text.count(old) == 1, "Patch anchor differs: " + old)
    return text.replace(old, new, 1)

report = {
    "status": "FAIL",
    "installation_started": False,
    "historical_build": "build-001",
    "new_build": "build-002",
    "rank_recomputation": "NONE",
    "git_stage_commit_push": "NONE",
}

process = None

def stop_test_process():
    if process is None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)

try:
    require(not build.exists(), "build-002 already exists.")
    require(not new_test.exists(), "Repair regression file already exists.")
    require(
        not git("diff", "--cached", "--name-only").strip(),
        "Index is not empty.",
    )

    paths = [
        feature / "recognizer.py",
        feature / "README.md",
        package / "api.py",
        package / "tests" / "test_extremal_inspector.py",
    ]

    originals = {}
    for path in paths:
        relative = path.relative_to(repo).as_posix()
        data = path.read_bytes()
        require(
            data == git("show", checkpoint + ":" + relative),
            "Local source differs from reviewed checkpoint: " + relative,
        )
        originals[path] = data

    old_build = feature / "build-001"
    sealed = {
        str(path.relative_to(repo)): digest(path)
        for path in old_build.rglob("*") if path.is_file()
    }

    text = originals[feature / "recognizer.py"].decode()
    helpers = (run / "repair_helpers.py").read_text()

    text = replace_once(
        text,
        "\ndef recognize_extremal(",
        "\n" + helpers + "\n\ndef recognize_extremal(",
    )

    marker = (
        '\n    result["scope"] = (\n'
        '        "The prefix separates all states, but the terminal is not "'
    )

    insertion = '''
    result["repair_certificate"] = terminal_repair_certificate(terminal)
    if result["repair_certificate"] is None:
        raise AssertionError("Nonliteral terminal lacks a repair certificate")
'''

    text = replace_once(text, marker, insertion + marker)
    compile(text, "candidate-recognizer.py", "exec")

    candidate_recognizer = run / "candidate-recognizer.py"
    candidate_recognizer.write_text(text)

    candidate_build = run / "build-002"

    subprocess.run([
        sys.executable, "-I", "-B",
        str(run / "enrich_cases.py"),
        str(feature),
        str(candidate_build),
        str(candidate_recognizer),
    ], check=True)

    shutil.copy2(
        run / "enrich_cases.py",
        candidate_build / "enrich_cases.py",
    )

    (candidate_build / "README.md").write_text(
        "# Constructive terminal repair extension\n\n"
        "Extends build-001 without recalculating its ranks or changing "
        "its historical recognition fields.\n\n"
        "Eight distinct nonliteral saved cases receive independently "
        "checked integer parity-moment certificates.\n\n"
        "A certificate supplies the missing top-monomial direction "
        "relative to the proper prefix monomials. Its detecting feature "
        "degree is not necessarily the degree where all functions "
        "become recoverable.\n\n"
        "Reproduction command, using a fresh output directory:\n\n"
        "python enrich_cases.py FEATURE_DIRECTORY OUTPUT_DIRECTORY "
        "[RECOGNIZER_FILE]\n"
    )

    (candidate_build / "PROOF.md").write_text(
        "# Elementary terminal-repair lemma\n\n"
        "Let the prefix range over the full d-cube. Proper prefix "
        "monomials span a codimension-one space W, missing only the "
        "full product.\n\n"
        "Expand a Boolean terminal f in its unique real/rational "
        "multilinear polynomial. If f is non-affine, choose a nonzero "
        "coefficient alpha_S of maximum degree >=2. The permitted "
        "temporal product f times all prefix coordinates outside S "
        "uses at most d-1 observables. Its top coefficient is alpha_S, "
        "since all strict supersets have zero coefficients.\n\n"
        "Its parity moment equals (-1)^d alpha_S and is nonzero. "
        "Together with W this yields full rank 2^d at degree d-1.\n\n"
        "An affine Boolean function over the reals is constant or a "
        "coordinate literal/complement. Such terminals do not introduce "
        "the missing direction.\n\n"
        "This lemma assumes a bijective full-cube prefix. It does not "
        "replace the external spectral reduction for arbitrary "
        "separating systems.\n"
    )

    lines = []
    for path in sorted(candidate_build.iterdir()):
        if path.is_file():
            lines.append(f"{digest(path)}  {path.name}\n")
    (candidate_build / "SHA256SUMS").write_text("".join(lines))

    api_path = package / "api.py"
    api_text = originals[api_path].decode()
    api_text = replace_once(
        api_text,
        '/ "build-001" / "inspector.html"',
        '/ "build-002" / "inspector.html"',
    )
    compile(api_text, str(api_path), "exec")

    old_test = package / "tests" / "test_extremal_inspector.py"
    test_text = originals[old_test].decode()

    test_text = replace_once(
        test_text,
        '(BUILD / "inspector.html").read_bytes()',
        '(FEATURE / "build-002" / "inspector.html").read_bytes()',
    )

    old_assertion = (
        '            self.assertEqual(result, case["recognition"])\n'
    )
    new_assertion = '''            self.assertEqual(
                {key: result[key] for key in case["recognition"]},
                case["recognition"],
            )
            if "repair_certificate" in result:
                self.assertTrue(module["verify_terminal_repair"](
                    result["terminal_truth_table"],
                    result["repair_certificate"],
                ))
'''

    test_text = replace_once(
        test_text, old_assertion, new_assertion
    )
    compile(test_text, str(old_test), "exec")
    compile(
        (run / "test_terminal_repair.py").read_text(),
        str(new_test), "exec",
    )

    backup = run / "before"
    for path, data in originals.items():
        target = backup / path.relative_to(package)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    report["installation_started"] = True

    shutil.copytree(candidate_build, build)
    (feature / "recognizer.py").write_text(text)
    api_path.write_text(api_text)
    old_test.write_text(test_text)
    new_test.write_bytes((run / "test_terminal_repair.py").read_bytes())

    with (feature / "README.md").open("a") as stream:
        stream.write(
            "\n## Constructive terminal repair\n\n"
            "The case route now serves build-002. Historical build-001 "
            "is unchanged. Nonliteral terminals include an integer "
            "Möbius/parity repair certificate, checked by direct "
            "subset sums and parity moments.\n"
        )

    installed = [
        *paths, new_test,
        *[path for path in build.rglob("*") if path.is_file()],
    ]
    installed_hashes = {
        str(path.relative_to(repo)): digest(path)
        for path in installed
    }

    environment = {
        **os.environ,
        "PYTHONPATH": str(package),
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
    }

    command = [
        sys.executable, "-u", "-B", "-m", "pytest",
        "-o", "addopts=", "-p", "no:cacheprovider",
        "-vv", "-s",
        "--junitxml=" + str(run / "tests.xml"),
        str(package / "tests"),
    ]

    print("RUNNING_RAG_SUITE_WITH_REPAIR_TESTS", flush=True)
    started = time.monotonic()

    with (run / "tests.log").open("wb") as writer:
        process = subprocess.Popen(
            command, cwd=run, env=environment,
            stdin=subprocess.DEVNULL,
            stdout=writer, stderr=subprocess.STDOUT,
            start_new_session=True,
        )

        with (run / "tests.log").open("rb") as reader:
            while process.poll() is None:
                chunk = reader.read()
                if chunk:
                    sys.stdout.buffer.write(chunk)
                    sys.stdout.buffer.flush()

                if time.monotonic() - started > 300:
                    stop_test_process()
                    raise TimeoutError("RAG suite exceeded 300 seconds")

                time.sleep(0.2)

            remainder = reader.read()
            if remainder:
                sys.stdout.buffer.write(remainder)
                sys.stdout.buffer.flush()

    require(process.returncode == 0, "RAG suite failed.")

    xml = ET.parse(run / "tests.xml").getroot()
    cases = list(xml.iter("testcase"))
    repair_cases = [
        node for node in cases
        if "TestTerminalRepair" in node.attrib.get("classname", "")
    ]

    require(len(repair_cases) == 9, "Expected nine repair tests.")
    require(
        all(
            not any(
                child.tag in {"failure", "error", "skipped"}
                for child in node
            )
            for node in repair_cases
        ),
        "A repair regression did not pass.",
    )

    for relative, expected in installed_hashes.items():
        require(
            digest(repo / relative) == expected,
            "Installed file changed during tests: " + relative,
        )

    for relative, expected in sealed.items():
        require(
            digest(repo / relative) == expected,
            "Historical build-001 changed: " + relative,
        )

    report.update({
        "status": "PASS",
        "repair_tests": 9,
        "full_suite_exit": process.returncode,
        "junit_cases_recorded": len(cases),
        "junit_skips": len(list(xml.iter("skipped"))),
        "build_001_unchanged": True,
        "installed_source_sha256": installed_hashes,
        "historical_build_sha256": sealed,
        "browser_rendering": "USER_CHECK_PENDING",
    })

    print("\nREPAIR_REGRESSION_TESTS=9/9")
    print("RAG_FULL_SUITE=PASS")
    print("NONLITERAL_SAVED_CASES_CERTIFIED=8")
    print("BUILD_001_UNCHANGED=YES")
    print("CASE_ROUTE_BUILD=build-002")
    print("RANK_RECOMPUTATION=NONE")
    print("GIT_STAGE_COMMIT_PUSH=NONE")
    print("OVERALL_UPGRADE_STATUS=PASS")

except BaseException:
    stop_test_process()
    report["error"] = traceback.format_exc()
    print(report["error"], file=sys.stderr)

finally:
    (run / "upgrade.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )

if report["status"] != "PASS":
    print("NO_AUTOMATIC_ROLLBACK_OR_COMMIT")
    print("BACKUPS_AND_REPORT=" + str(run))
    raise SystemExit(1)
