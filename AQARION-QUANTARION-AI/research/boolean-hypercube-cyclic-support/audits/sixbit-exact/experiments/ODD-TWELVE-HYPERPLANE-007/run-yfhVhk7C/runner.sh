#!/usr/bin/env bash
set -Eeuo pipefail
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python -u "$HERE/audit_odd12.py" "$HERE"
