#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SCRIPT="cycle_congruence.py"
OUTPUT="cycle_congruence.output.txt"
RECEIPT="cycle_congruence.receipt.txt"
HASH_RECEIPT="cycle_congruence.receipt.sha256"
BUNDLE_HASHES="cycle_congruence.bundle.sha256"

for file in "$SCRIPT" "make_receipt.sh"; do
  [[ -f "$file" ]] || { echo "MISSING_REQUIRED_FILE: $file" >&2; exit 2; }
done

set +e
bash ./make_receipt.sh "$SCRIPT" "RESULT: ALL PASS"
status=$?
set -e

[[ -f "$RECEIPT" ]] || { echo "RECEIPT_NOT_CREATED" >&2; exit 5; }

sha256sum "$SCRIPT" "$OUTPUT" > "$HASH_RECEIPT"
sha256sum "$SCRIPT" "$OUTPUT" "$RECEIPT" > "$BUNDLE_HASHES"

sha256sum -c "$HASH_RECEIPT" || { echo "SOURCE_OUTPUT_HASH_CHECK_FAILED" >&2; exit 3; }
sha256sum -c "$BUNDLE_HASHES" || { echo "BUNDLE_HASH_CHECK_FAILED" >&2; exit 4; }

if (( status != 0 )); then
  echo "CYCLE_CONGRUENCE_VALIDATION_FAILED" >&2
  exit "$status"
fi

echo "CYCLE_CONGRUENCE_VALIDATION=PASS"
echo "RECEIPT=$RECEIPT"
echo "SOURCE_OUTPUT_HASHES=$HASH_RECEIPT"
echo "BUNDLE_HASHES=$BUNDLE_HASHES"
