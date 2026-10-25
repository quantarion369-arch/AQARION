#!/data/data/com.termux/files/usr/bin/bash
set -u
cd "$(dirname "$0")" || exit 2

echo "=== AQARION Test Suite v0.1 ==="
echo "timestamp=$(date -Iseconds 2>/dev/null || date)"
echo "python=$(python --version 2>&1)"
echo "AQARION_RAG_PATH=${AQARION_RAG_PATH:-<not set>}"
echo

echo "=== Runtime inventory ==="
python - <<'PY'
import platform, shutil, sys, importlib.util
print("python_version:", sys.version.replace("\n", " "))
print("implementation:", platform.python_implementation())
print("platform:", platform.platform())
print("machine:", platform.machine())
for x in ("git", "clang", "cmake", "make", "llama-server"):
    print(x + ":", shutil.which(x) or "NOT_FOUND")
for x in ("flint", "pytest", "requests"):
    print("module_" + x + ":", bool(importlib.util.find_spec(x)))
PY

echo
echo "=== Unit tests ==="
python -m unittest discover -s tests -v
rc=$?
echo
echo "UNITTEST_EXIT=$rc"
exit "$rc"
