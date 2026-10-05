#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
pip install -q -r requirements.txt
PYTHONPATH=. python -m pytest tests/test_join_stability_property.py -v
echo "Receipt: $SCRIPT_DIR/verification/receipts/H_AQ-001_n4_receipt.json"
ls -lh verification/receipts/
