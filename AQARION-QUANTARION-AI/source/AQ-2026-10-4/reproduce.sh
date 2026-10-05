#!/bin/bash
# Reproduce H_AQ-001 for n<=4
python -m pytest tests/test_join_stability_property.py -v
echo "Receipt: verification/receipts/H_AQ-001_n4_receipt.json"
