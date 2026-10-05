#!/bin/bash
set -e
echo "AQ-2026-10-4 — Corrected reproduction"
echo "H_AQ-001C = congruence join closure (E ⊆ T*E)"
echo "H_AQ-001_PB = PB-Join (T*E ⊆ E) — OPEN"
pip install -r requirements.txt -q
PYTHONPATH=. python -m pytest tests/test_join_stability_property.py -v
echo "Done — see README for distinction"
