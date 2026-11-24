#!/bin/bash
set -u
cd /work
LEAN=/root/.elan-aqarion-p2/toolchains/leanprover--lean4---v4.35.0-rc4/bin/lean
test -x "$LEAN" || { echo "COMPILER_NOT_FOUND_IN_CONTAINER"; exit 0; }
"$LEAN" --version | tee LEAN_VERSION.txt
sha256sum "$LEAN" | tee LEAN_BINARY_SHA256.txt

timeout -k 10s 240s "$LEAN" -o GenKernel.olean GenKernel.lean > GEN_BUILD.log 2>&1
echo $? > GEN_EXIT.txt
cat GEN_BUILD.log

timeout -k 10s 120s "$LEAN" -o NegativeControl2.olean NegativeControl2.lean > NEG2.log 2>&1
echo $? > NEG2_EXIT.txt

AX=$(grep -c "depends on axioms" GEN_BUILD.log || true)
SORRY=$(grep -c "sorryAx" GEN_BUILD.log || true)
echo
echo "GEN_EXIT=$(cat GEN_EXIT.txt)"
echo "NEGATIVE_EXIT=$(cat NEG2_EXIT.txt)"
echo "AXIOM_REPORT_LINES=$AX"
echo "SORRYAX_LINES=$SORRY"
if [ "$(cat GEN_EXIT.txt)" = "0" ] && [ "$(cat NEG2_EXIT.txt)" = "1" ] \
   && [ "$AX" = "4" ] && [ "$SORRY" = "0" ]; then
  echo "STATUS=PASS_COMPILED_GENERATED_SUBMONOID_THEOREM"
else
  echo "STATUS=INCOMPLETE_OR_FAILED"
fi
