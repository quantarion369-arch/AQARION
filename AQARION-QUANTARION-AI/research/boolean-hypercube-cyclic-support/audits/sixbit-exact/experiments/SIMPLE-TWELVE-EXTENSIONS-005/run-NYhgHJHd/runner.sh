#!/usr/bin/env bash
set -Eeuo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python -u "$HERE/classify_simple12.py" "$HERE" "$1"
