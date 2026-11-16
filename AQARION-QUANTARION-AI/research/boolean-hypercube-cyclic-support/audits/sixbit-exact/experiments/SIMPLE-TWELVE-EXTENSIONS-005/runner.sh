#!/usr/bin/env bash
# Fresh-run launcher. Never executes inside a historical run directory.
set -Eeuo pipefail
umask 077

HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
DRIVER="$HERE/classify_simple12.py"

EXPECTED_SOURCE="be804ed6e839ed518852cd3ffa50743c046e567707037a49aac5e5269a9ee426"

usage() {
    echo "Usage:"
    echo "  bash runner.sh --no-run"
    echo "  bash runner.sh --run HISTORICAL_BASE_DIRECTORY"
    echo
    echo "No default execution. Historical outputs are never reused."
}

case "${1:-}" in
    --no-run)
        if [ "$#" -ne 1 ]; then
            usage
            exit 64
        fi
        ;;
    --run)
        if [ "$#" -ne 2 ]; then
            usage
            exit 64
        fi
        ;;
    *)
        usage
        exit 64
        ;;
esac

test -f "$DRIVER"

echo "=== VERIFY DRIVER IDENTITY ==="
printf '%s  %s\n' "$EXPECTED_SOURCE" "$DRIVER" |
    sha256sum -c -

echo "=== CHECK PYTHON SYNTAX WITHOUT EXECUTION ==="
python - "$DRIVER" <<'PY'
import ast
import sys
from pathlib import Path

source = Path(sys.argv[1])
ast.parse(source.read_text())
print("PASS: Python syntax; no import or experiment execution.")
PY

if [ "$1" = "--no-run" ]; then
    echo "PASS: launcher preflight only."
    echo "NO EXPERIMENT EXECUTED; NO OUTPUT DIRECTORY CREATED."
    exit 0
fi

HISTORICAL_BASE="$(CDPATH= cd -- "$2" && pwd -P)"
RUN="$(mktemp -d "$HERE/replay-XXXXXXXX")"

echo "=== CREATE FRESH EXECUTION PACKAGE ==="
cp -p -- "$DRIVER" "$RUN/classify_simple12.py"
cp -p -- "$HERE/runner.sh" "$RUN/launcher.sh"

printf '%s\n' "$HISTORICAL_BASE" > "$RUN/historical-base.txt"

echo "RETAINED: $RUN"
echo "HISTORICAL BASE: $HISTORICAL_BASE"

# Run only the copied driver, with the fresh directory as output.
set +e
python -u "$RUN/classify_simple12.py" \
    "$RUN" "$HISTORICAL_BASE" \
    > "$RUN/run.log" 2>&1
RC=$?
set -e

printf '%s\n' "$RC" > "$RUN/exit.txt"

set +e
cat "$RUN/run.log"
set -e

# Bind all top-level files emitted by this execution.
python - "$RUN" <<'PY'
import hashlib
import sys
from pathlib import Path

root = Path(sys.argv[1])
entries = []

for path in sorted(root.iterdir()):
    if path.is_file() and path.name != "SHA256SUMS":
        h = hashlib.sha256()
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                h.update(block)
        entries.append(h.hexdigest() + "  " + path.name)

(root / "SHA256SUMS").write_text(
    "\n".join(entries) + "\n"
)
PY

(
    cd "$RUN"
    sha256sum -c SHA256SUMS
)

echo "RETAINED: $RUN"
echo "EXPERIMENT EXIT: $RC"
echo "NO COMMIT OR PUSH PERFORMED."

exit "$RC"
