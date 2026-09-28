#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$ROOT"

echo "AQARION JOIN-STABILITY"
echo "======================"
echo "Package: $ROOT"
echo

command -v python3 >/dev/null 2>&1 || {
    echo "ERROR: python3 is required" >&2
    exit 2
}

test -f manifest.json || {
    echo "ERROR: manifest.json is missing" >&2
    exit 2
}

test -f claims.jsonl || {
    echo "ERROR: claims.jsonl is missing" >&2
    exit 2
}

test -f evidence.jsonl || {
    echo "ERROR: evidence.jsonl is missing" >&2
    exit 2
}

test -f verify.py || {
    echo "ERROR: verify.py is missing" >&2
    exit 2
}

echo "Running independent verifier..."
echo

exec python3 verify.py
