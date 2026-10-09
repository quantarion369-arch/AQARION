#!/usr/bin/env bash
set -uo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT" || exit 90

mkdir -p receipts || exit 91

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
LOG="receipts/reproduction-${STAMP}.log"
STATUS="receipts/reproduction-${STAMP}.status"

{
    echo "PACKAGE=JOIN-STABILITY"
    echo "UTC_START=${STAMP}"
    echo "PACKAGE_DIR=${ROOT}"
    echo "AQ_EXPECTED_TESTED_REVISION=${AQ_EXPECTED_TESTED_REVISION:-UNSET}"
    echo

    echo "=== Tested Git revision ==="
    if git rev-parse HEAD; then
        echo "GIT_REVISION_COMMAND=PASS"
    else
        echo "GIT_REVISION_COMMAND=FAIL"
        exit 10
    fi

    echo
    echo "=== Structural verifier ==="
    if python3 verify.py; then
        echo "VERIFY_EXIT=0"
    else
        rc=$?
        echo "VERIFY_EXIT=${rc}"
        exit 11
    fi

    echo
    echo "=== Independent finite audit ==="
    if python3 join_stability_independent_audit.py; then
        echo "AUDIT_EXIT=0"
    else
        rc=$?
        echo "AUDIT_EXIT=${rc}"
        exit 12
    fi

    echo
    echo "=== Negative-control self-tests ==="
    if python3 verify.py --self-test-negative-controls; then
        echo "NEGATIVE_CONTROLS_EXIT=0"
    else
        rc=$?
        echo "NEGATIVE_CONTROLS_EXIT=${rc}"
        exit 13
    fi

    echo
    echo "=== Lean status ==="
    echo "Lean is not compiled by this script."
    echo "LEAN_STATUS=OPEN"

    echo
    echo "RESULT=PACKAGE_AND_AUDIT_PASS"
    echo "RESULT_SCOPE=STRUCTURAL_AND_FINITE_COMPUTATIONAL_CHECKS_ONLY"
    exit 0
} 2>&1 | tee "$LOG"

RC=${PIPESTATUS[0]}

{
    echo "package=JOIN-STABILITY"
    echo "utc_start=${STAMP}"
    echo "exit_code=${RC}"
    echo "log=${LOG}"
    echo "tested_revision=${AQ_EXPECTED_TESTED_REVISION:-UNSET}"
    if [ "$RC" -eq 0 ]; then
        echo "result=PACKAGE_AND_AUDIT_PASS"
        echo "scope=STRUCTURAL_AND_FINITE_COMPUTATIONAL_CHECKS_ONLY"
    else
        echo "result=FAIL"
    fi
} > "$STATUS"

echo "REPRODUCTION_EXIT=${RC}"
echo "REPRODUCTION_LOG=${LOG}"
echo "REPRODUCTION_STATUS=${STATUS}"
exit "$RC"
