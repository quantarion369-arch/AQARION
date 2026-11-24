#!/bin/bash
set -euo pipefail

cd /work
sha256sum -c SOURCE_SHA256SUMS

export ELAN_HOME="$HOME/.elan-aqarion-p2"
export DEBIAN_FRONTEND=noninteractive

printf 'PRIVATE_ELAN_HOME=%s\n' "$ELAN_HOME"

if ! command -v curl >/dev/null 2>&1 \
   || ! command -v zstd >/dev/null 2>&1 \
   || [ ! -r /etc/ssl/certs/ca-certificates.crt ]
then
    apt-get update
    apt-get install -y curl ca-certificates zstd
fi

if [ ! -x "$ELAN_HOME/bin/elan" ]; then
    sh /work/elan-init.sh \
        -y \
        --no-modify-path \
        --default-toolchain none
fi

PIN="$(cat lean-toolchain)"

"$ELAN_HOME/bin/elan" --version | tee ELAN_VERSION.txt
"$ELAN_HOME/bin/elan" toolchain install "$PIN"

"$ELAN_HOME/bin/elan" run "$PIN" lean --version \
    | tee LEAN_CONTEXT.txt

EXPECTED="${PIN##*:v}"
grep -F "$EXPECTED" LEAN_CONTEXT.txt >/dev/null

COMPILER="$(
    ELAN_TOOLCHAIN="$PIN" \
    "$ELAN_HOME/bin/elan" which lean
)"

sha256sum "$COMPILER" | tee LEAN_BINARY_SHA256.txt

set +e
timeout -k 10s 120s \
    "$ELAN_HOME/bin/elan" run "$PIN" lean \
    -o ArithmeticKernel.olean \
    ArithmeticKernel.lean \
    2>&1 | tee LEAN_BUILD.log

BUILD_STATUS=${PIPESTATUS[0]}
set -e

printf '%s\n' "$BUILD_STATUS" > BUILD_EXIT_CODE.txt

if [ "$BUILD_STATUS" -ne 0 ]; then
    printf 'LEAN_CANDIDATE_COMPILATION=FAILED_OR_INCOMPLETE\n'
    exit "$BUILD_STATUS"
fi

if grep -q 'sorryAx' LEAN_BUILD.log; then
    printf 'SORRY_AXIOM_DETECTED\n'
    exit 3
fi

set +e
timeout -k 10s 120s \
    "$ELAN_HOME/bin/elan" run "$PIN" lean \
    -o NegativeControl.olean \
    NegativeControl.lean \
    2>&1 | tee NEGATIVE_CONTROL.log

NEGATIVE_STATUS=${PIPESTATUS[0]}
set -e

printf '%s\n' "$NEGATIVE_STATUS" > NEGATIVE_EXIT_CODE.txt

if [ "$NEGATIVE_STATUS" -ne 1 ]; then
    printf 'NEGATIVE_CONTROL=UNEXPECTED_EXIT\n'
    exit 4
fi

sha256sum -c SOURCE_SHA256SUMS

printf 'LEAN_CANDIDATE_COMPILATION=PASS\n'
printf 'FALSE_THEOREM_REJECTED=PASS\n'
