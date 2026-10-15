#!/bin/sh
# Usage: sh make_receipt.sh cycle_congruence.py ["RESULT: ALL PASS"]
S="$1"; M="${2:-RESULT: ALL PASS}"
O="${S%.py}.output.txt"; R="${S%.py}.receipt.txt"

python3 -I "$S" > "$O" 2>&1; EC=$?
N=$(grep -cxF "$M" "$O" 2>/dev/null || echo 0)
SZ=$(wc -c < "$O")

if [ "$EC" -eq 0 ] && [ "$SZ" -gt 0 ] && [ "$N" -eq 1 ]; then ST=PASS; else ST=FAIL; fi

if git ls-files --error-unmatch "$S" >/dev/null 2>&1 \
   && [ -z "$(git status --porcelain -- "$S" 2>/dev/null)" ]; then
    GS="tracked+clean"
else
    GS="UNTRACKED-OR-DIRTY"
fi

{
echo "Status: $ST"
echo "Exit code: $EC"
echo "Output bytes: $SZ"
echo "Marker lines: $N"
echo "Python: $(python3 -V 2>&1)"
echo "Git HEAD: $(git rev-parse HEAD 2>/dev/null || echo none)"
echo "Script git state: $GS"
echo "Script sha256: $(sha256sum "$S" | cut -d' ' -f1)"
echo "Output sha256: $(sha256sum "$O" | cut -d' ' -f1)"
} > "$R"

cat "$R"
[ "$ST" = PASS ]
