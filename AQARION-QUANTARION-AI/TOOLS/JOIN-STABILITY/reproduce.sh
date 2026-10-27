#!/usr/bin/env bash
set -uo pipefail
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)" || exit 90
exec python3 -B -I "$ROOT/reproduction.py" "$@"
