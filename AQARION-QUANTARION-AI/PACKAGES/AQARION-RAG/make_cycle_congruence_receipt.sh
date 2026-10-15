#!/usr/bin/env bash
set -euo pipefail

SCRIPT="cycle_congruence.py"
OUTPUT="cycle_congruence.output.txt"
RECEIPT="cycle_congruence.receipt.txt"
HASH_RECEIPT="cycle_congruence.receipt.sha256"

STAMP="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
HOST="$(hostname)"
GIT_COMMIT="$(git rev-parse HEAD 2>/dev/null || echo 'not-a-git-repo')"

python3 "$SCRIPT" > "$OUTPUT"

SCRIPT_SHA="$(sha256sum "$SCRIPT" | awk '{print $1}')"
OUTPUT_SHA="$(sha256sum "$OUTPUT" | awk '{print $1}')"

{
  echo "AQARION-RAG VERIFICATION RECEIPT"
  echo "================================"
  echo "Suite:           cycle_congruence"
  echo "Status:          PASS"
  echo "Exit code:       0"
  echo "Generated (UTC): ${STAMP}"
  echo "Host:            ${HOST}"
  echo "Git commit:      ${GIT_COMMIT}"
  echo
  echo "Artifact integrity"
  echo "------------------"
  printf 'script  sha256  %s  %s
' "$SCRIPT_SHA" "$SCRIPT"
  printf 'output  sha256  %s  %s
' "$OUTPUT_SHA" "$OUTPUT"
} > "$RECEIPT"

sha256sum "$SCRIPT" "$OUTPUT" > "$HASH_RECEIPT"

cat "$RECEIPT"
echo
cat "$HASH_RECEIPT"
